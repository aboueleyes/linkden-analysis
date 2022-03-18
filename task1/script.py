#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import browser_cookie3
import re
import json

cookiejar = browser_cookie3.chrome()
url_jobsearch = "https://www.linkedin.com/jobs/search/?start="

r = requests.get(url_jobsearch, cookies=cookiejar)
def get_jobs_links(chunk) -> list:
    r = requests.get(f"https://www.linkedin.com/jobs/search/?start={chunk}", cookies=cookiejar)
    regex = "fs_normalized_jobPosting:[0-9]{10}"
    job_ids_raw = re.findall(regex, r.text)
    job_ids = [f"https://www.linkedin.com/jobs/view/{item.split(':')[1]}" for item in set(job_ids_raw)]
    return job_ids

def get_jobs_links_new(chunk) -> list:
    r = requests.get(f"https://www.linkedin.com/jobs/search/?start={chunk}", cookies=cookiejar)
    soup = BeautifulSoup(r.text, "lxml")
    raw = soup.find_all("code", {"id" : re.compile('bpr-guid-*')})
    json_data = json.loads(raw[-2].text)
    print(type(json_data))

def get_job_info(link: str) -> list:
    r = requests.get(link, cookies=cookiejar)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.find_all("h1", {"class" : "t-24"})
    writeout(r.text)
    print(title)

def writeout(data):
    with open("out", "r+") as f:
        f.write(data)



#get_job_info("https://www.linkedin.com/jobs/view/2947388512")

get_jobs_links_new(100)
