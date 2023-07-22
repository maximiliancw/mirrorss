from datetime import datetime
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
        entries = [entry for source in self.sources for entry in source.entries]
        sorted_entries = sorted(entries, key=lambda entry: mktime(entry.published_parsed), reverse=self.reversed)
        return sorted_entries[:self.limit]
    
    def load(self, sources: List[str]) -> List[FeedParserDict]:
        cache = Cache("cache")

        for url in sources:
            if not is_valid_url(url):
                raise ValueError(f"Invalid URL found in param 'sources': {url}")
            
            if url in cache:
                saved, timestamp = cache.get(url, expire_time=True)
                if less_than_1h_ago(timestamp):
                    yield saved
                    continue

                update = parse(url, etag=saved.etag, modified=saved.modified)
                if update.status == 304:
                    yield saved
                else:
                    cache.set(url, update, expire=24*60*60)
                    yield update
            else:          
                src = parse(url)
                cache.set(url, src, expire=24*60*60)
                yield src