import requests, re, json, urllib.parse, html
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from models import Job


class Point72Scraper(BaseScraper):
    def __init__(self):
        super().__init__(
            URL='https://careers.point72.com',
            COMPANY='Point72'
        )

    def scrape_jobs(self):
        res = requests.get(self.URL)

        match = re.search(r"CSSearchModule\.init\('(.+?)',", html.unescape(res.text))
        if not match:
            return {}

        json_str = (
            match.group(1)
            .encode('utf-8').decode('unicode_escape')
            .encode('latin1').decode('utf-8')
        )

        jobs_filtered = list(filter(lambda x: x['job']['Experience__c'] == 'Internships'
                                    and 'Technology & Engineering' in x['job']['Area__c']
                                    and x['job']['Posted_Location__c'] == 'Warsaw, PL'
                                    , json.loads(json_str)))

        new_jobs = {}
        for job_dict in jobs_filtered:
            job_url = self.URL + '/CSJobDetail?' + \
                      'jobName=' + job_dict['friendlyJobName'] + '&' + \
                      'jobCode=' + job_dict['job']['Job_Code__c'] + '&' + \
                      'location=' + urllib.parse.quote(job_dict['job']['Posted_Location__c'], safe=',') + '&' + \
                      'locale=English&retURL=/CSCareerSearch'

            soup = BeautifulSoup(job_dict['job']['Job_Description_External__c'], "html.parser")
            reqs_section = soup.find('ul')
            reqs = []
            if reqs_section:
                for li in reqs_section.find_all('li'):
                    reqs.append(f'- {li.get_text(strip=True)}')

            job = Job(self.COMPANY, job_dict['job']['Name'], job_url, '\n'.join(reqs))
            new_jobs[job.hash()] = job

        return new_jobs
