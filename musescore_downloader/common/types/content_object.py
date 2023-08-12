from dataclasses import dataclass

@dataclass
class ContentObject:
    content: bytes
    content_type: str
    page_num: int
    title: str
