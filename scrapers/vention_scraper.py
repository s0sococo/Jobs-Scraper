import re, json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from base_scraper import BaseScraper, ScraperError
from job import Job


class VentionScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            URL='https://join.ventionteams.com/job-openings',
            COMPANY='Vention'
        )

    def scrape_jobs(self):
        cur_url = self.URL
        new_jobs = {}
        while cur_url:
            resp = self.fetch_url(cur_url)
            soup = BeautifulSoup(resp.text, 'html.parser')

            next_link = soup.find('a', rel='next')
            if next_link and next_link.has_attr('href'):
                cur_url = urljoin(self.URL, next_link.get('href'))
            else:
                cur_url = None

            script = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script:
                raise ScraperError(f"Script tag missing from {cur_url}.")
            match = re.search(r'"initialVacancies":{.*?"items":(\[.+?])', script.string)
            if not match:
                raise ScraperError(f"Failed to parse response from {cur_url}")

            json_str = match.group(1)

            jobs_filtered = list(filter(lambda x: x['city']['name'] == 'Warsaw'
                                        and x['technology']['category']['name'] in ('Development', 'DevOps')
                                        and x['level']['name'] == 'Internship'
                                        , json.loads(json_str)))

            for job_dict in jobs_filtered:
                resp = self.fetch_url(job_dict['meta']['html_url'])
                uls = BeautifulSoup(resp.text, 'html.parser').find_all('ul')
                reqs = []
                if len(uls) >= 2:
                    for li in uls[1].find_all('li'):
                        reqs.append(f'- {li.get_text(strip=True)}')

                job = Job(self.COMPANY, job_dict['title'], job_dict['meta']['html_url'], '\n'.join(reqs))
                new_jobs[job.hash()] = job

        return new_jobs
