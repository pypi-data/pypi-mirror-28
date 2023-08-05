import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class MetadataValue:
    """
    Represents a single piece of metadata about a piece of Confluence content.
    """
    def __init__(self, metadata_id: int, key: str, title: str, content: str) -> None:
        self.metadata_id = metadata_id
        self.key = key
        self.title = title
        self.content = content
