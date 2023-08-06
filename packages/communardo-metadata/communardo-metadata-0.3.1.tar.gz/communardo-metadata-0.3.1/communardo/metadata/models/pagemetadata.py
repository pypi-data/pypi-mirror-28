from communardo.metadata.models.metadatavalue import MetadataValue
import logging
from typing import List

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PageMetadata:
    """
    Represents the set of communardo metadata about a page.
    """
    def __init__(self, page_id: int, page_title: str, page_url: str, page_content_type: str,
                 page_metadata: List[MetadataValue]) -> None:
        self.page_id = page_id
        self.page_title = page_title
        self.page_url = page_url
        self.page_content_type = page_content_type
        self.page_metadata = page_metadata

    def __str__(self):
        return f'{self.page_id} | {self.page_title}'
