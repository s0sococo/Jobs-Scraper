import re, json, urllib.parse, html, codecs
from bs4 import BeautifulSoup
from base_scraper import BaseScraper, ScraperError
from job import Job


class Point72Scraper(BaseScraper):
    def __init__(self):
        super().__init__(
            URL='https://careers.point72.com',
            COMPANY='Point72'
        )

    def scrape_jobs(self):
        resp = self.fetch_url()

        match = re.search(r"CSSearchModule\.init\('(.+?)',", html.unescape(resp.text))
        if not match:
            raise ScraperError(f"Failed to parse response from {self.URL}")

        json_str = match.group(1)
        json_str = re.sub(r'(?<!\\)"', r'/"', json_str) # escapes unescaped " inside
        json_str = codecs.escape_decode(bytes(json_str, "utf-8"))[0].decode("utf-8")
        json_str = re.sub(r'/"', r'\"', json_str)

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
            uls = soup.find_all('ul')
            if len(uls) >= 3: # assumes requirements are in the 3rd unordered list
                reqs = []
                for li in uls[2].find_all('li'):
                    reqs.append(f'- {li.get_text(strip=True)}')

            job = Job(self.COMPANY, job_dict['job']['Name'], job_url, '\n'.join(reqs))
            new_jobs[job.hash()] = job

        return new_jobs
