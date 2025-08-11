from abc import ABC, abstractmethod
from dataclasses import dataclass
from models import Job


@dataclass
class BaseScraper(ABC):
    URL: str
    COMPANY: str

    @abstractmethod
    def scrape_jobs(self) -> dict[str, Job]:
        pass
