from dataclasses import dataclass

@dataclass
class SaveCompleteObject:
    path: str
    page_num: int
    filetype: str