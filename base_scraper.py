from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
from job import Job


@dataclass
class BaseScraper(ABC):
    URL: str
    COMPANY: str

    @abstractmethod
    def scrape_jobs(self) -> dict[str, Job]:
        pass

    def fetch_url(self, url: str = None):
        target_url = url if url is not None else self.URL
        try:
            resp = requests.get(target_url)
            resp.raise_for_status()
            return resp
        except Exception:
            raise ScraperError(f"Failed to fetch jobs from {target_url}.") from None

class ScraperError(Exception):
    pass