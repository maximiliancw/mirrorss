from datetime import datetime
import json
from time import mktime
from typing import List
from diskcache import Index, Cache

from feedparser import FeedParserDict, parse

from mirrorss.helpers import is_valid_url, less_than_1h_ago

class Mirror(object):

    def __init__(
        self,
        sources: List[str],
        title: str,
        description: str = "",
        link: str = "",
        image: str = "",
        keywords: List[str] = [],
        limit: int = 10,
        order: str = "desc"
    ):          
        sources = list(map(lambda s: s.strip(), sources))
        self.sources: List[FeedParserDict] = self.load(sources)
        self.title = title
        self.description = description

        if link and not is_valid_url(link):
            raise ValueError(f"Invalid URL found in param 'link': {link}")
        self.link = link

        if image and not is_valid_url(image):
            raise ValueError(f"Invalid URL found in param 'image': {image}")
        self.image = image

        self.keywords = keywords
        self.limit = limit
        self.reversed = order == "desc"
        self.published = datetime.now()
        
    @property
    def items(self):
        # Note: Entries without <pubDate> will be ignored!
        entries = [entry for source in self.sources for entry in source.entries if entry.published_parsed]
        sorted_items = sorted(entries, key=lambda entry: mktime(entry.published_parsed), reverse=self.reversed)
        filtered_items = []
        for item in sorted_items:
            s = json.dumps({k: v for k, v in item.items()})
            if any([k.lower().strip() in s.lower() for k in self.keywords]):
                filtered_items.append(item)

        return filtered_items[:self.limit]
    
    def load(self, sources: List[str]) -> List[FeedParserDict]:
        cache = Cache("cache")
        expiry = 365*24*60*60
        try:
            for url in sources:
                if not is_valid_url(url):
                    raise ValueError(f"Invalid URL found in param 'sources': {url}")
                
                if url in cache:
                    saved, expire = cache.get(url, expire_time=True)
                    if less_than_1h_ago(expire - expiry):
                        yield saved
                        continue

                    update = parse(url, etag=saved.etag, modified=saved.modified)
                    if update.status == 304:
                        yield saved
                        continue
                    
                    cache.set(url, update, expire=expiry)
                    yield update
                else:          
                    src = parse(url)
                    cache.set(url, src, expire=expiry)
                    yield src
        except Exception as e:
            raise e
        finally:
            cache.close()