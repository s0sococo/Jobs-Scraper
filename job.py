import hashlib
import json


class Job:
    def __init__(self, company_name, job_name, url, reqs_str):
        self.company_name = company_name
        self.job_name = job_name
        self.url = url
        self.reqs_str = reqs_str

    def to_dict(self):
        return {
            'company_name': self.company_name,
            'job_name': self.job_name,
            'url': self.url,
            'reqs_str': self.reqs_str
        }

    def hash(self):
        job_dict = self.to_dict()
        job_str = json.dumps(job_dict, sort_keys=True)
        return hashlib.sha256(job_str.encode("utf-8")).hexdigest()
