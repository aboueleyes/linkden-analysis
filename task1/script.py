#!/usr/bin/env python3
import csv
import time
import requests
from bs4 import BeautifulSoup
import browser_cookie3
import re
import json

cookiejar = browser_cookie3.chrome()
url_jobsearch = "https://www.linkedin.com/jobs/search/?start="

r = requests.get(url_jobsearch, cookies=cookiejar)

def get_jobs_data(chunk: int) -> dict:
    r = requests.get(f"https://www.linkedin.com/jobs/search/?start={chunk}", cookies=cookiejar)
    soup = BeautifulSoup(r.text, "lxml")
    raw = soup.find_all("code", {"id" : re.compile('bpr-guid-*')})
    json_data = json.loads(raw[-2].text)
    return json_data

def get_job_info(link: str) -> list:
    r = requests.get(link, cookies=cookiejar)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.find_all("h1", {"class" : "t-24"})
    writeout(r.text)
    print(title)

def writeout(data):
    with open("out", "r+") as f:
        f.write(data)




def parse_job_data(data: dict) -> dict:
    try:
        job_title = data["title"]
        job_location = data["formattedLocation"]
        job_id = data["jobPostingId"]
        job_remote = data["workRemoteAllowed"]
        job_listing_date_epoch = int(str(data["listedAt"])[:10])
        job_listing_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(job_listing_date_epoch))
        job_company_id = data["companyDetails"]["company"].split("company:")[1]
        cleaned_data = {
            "Title" : job_title,
            "Location" : job_location,
            "ID" : job_id,
            "Remote" : job_remote,
            "Listing Date" : job_listing_time,
            "Company ID" : job_company_id
        }
        return cleaned_data
    except:
        pass

jobs = []
def scrape_page(chunk: int) -> None:
    for job_data in get_jobs_data(chunk)["included"]:
        jobs.append(parse_job_data(job_data))

def write_csv(data: dict) -> None:
    try:
        with open("out.csv", "w", newline="") as f:
            title = "Title,Location,ID,Remote,Listing Date,Company ID".split(",")
            cw = csv.DictWriter(f, fieldnames=title)
            cw.writeheader()
            cw.writerows(data)
    except:
        pass

scrape_page(0)
write_csv(jobs)
