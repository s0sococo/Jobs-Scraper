import requests
import json
from base_scraper import BaseScraper
from scrapers import *


def send_job(job):
    bot_token = ''
    chat_id = ''

    text = f'{job.company_name}\n' \
           f'<a href="{job.url}">{job.job_name}</a>\n' \
           f'{job.reqs_str}'

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }

    response = requests.post(url, data=payload)
    print(response.json())


def scrape_jobs(scraper: BaseScraper, jobs_hashes_by_company):
    old_hashes = set(jobs_hashes_by_company.get(scraper.COMPANY, []))
    new_jobs = scraper.scrape_jobs()
    new_hashes = set(new_jobs)

    for jh in new_hashes - old_hashes:
        send_job(new_jobs[jh])

    jobs_hashes_by_company[scraper.COMPANY] = list(new_jobs.keys())


if __name__ == "__main__":
    # scr = SamsungRDScraper()
    #
    # jobs = scr.scrape_jobs()
    try:
        with open('jobs_hashes_by_company.json', 'r', encoding='utf-8') as f:
            jobs_hashes_by_company = json.load(f)
    except Exception:
        jobs_hashes_by_company = {}

    scrapers = [
        VentionScraper(),
        Point72Scraper(),
        SamsungRDScraper()
    ]

    for scr in scrapers:
        scrape_jobs(scr, jobs_hashes_by_company)

    with open('jobs_hashes_by_company.json', 'w', encoding='utf-8') as f:
        json.dump(jobs_hashes_by_company, f)





