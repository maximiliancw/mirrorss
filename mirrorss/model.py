from datetime import datetime
from time import mktime
from typing import List

from feedparser import FeedParserDict, parse

from mirrorss.helpers import is_valid_url

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
        for source in sources:
            if not is_valid_url(source):
                raise ValueError(f"Invalid URL found in param 'sources': {source}")
        
        self.sources: List[FeedParserDict] = [parse(source) for source in sources]
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