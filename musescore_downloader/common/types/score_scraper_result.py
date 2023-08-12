from dataclasses import dataclass

@dataclass
class ScoreScraperResult:
    title: str
    urls: list[str]
    num_of_pages: int
    