import requests, json
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from job import Job


class SamsungRDScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            URL='https://samsungrd.pl/en/?internship=1',
            COMPANY='Samsung R&D Institute Poland'
        )

    def scrape_jobs(self):
        url = 'https://samsungrd.pl/Samsungrd/offers/ajax-search-offer'
        payload = {
            'employment[]': 1,  # internships
            'where[]': 'Warszawa',
            'offset': 0
        }

        new_jobs = {}
        page = 1
        while payload['offset'] < page:
            res = requests.post(url, data=payload)
            filtered = json.loads(res.text)

            for job_dict in filtered['items']:
                res = requests.get(job_dict['url'])
                uls = BeautifulSoup(res.text, 'html.parser').find_all('ul')
                reqs = []
                if len(uls) >= 3: # works only for Internships
                    for li in uls[2].find_all('li'):
                        reqs.append(f'- {li.get_text(strip=True)}')

                job = Job(self.COMPANY, job_dict['title'], job_dict['url'], '\n'.join(reqs))
                new_jobs[job.hash()] = job

            payload['offset'] += 1
            page = filtered['page']

        return new_jobs
