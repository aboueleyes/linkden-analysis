import csv
from dataclasses import Field
import time
from typing import Container
import dateparser
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import zip_longest

jobTitles=[]
companyNames=[]
locations=[]
remote=[]
links=[]
date=[]
applicants=[]
jobTimes=[]
seniority=[]
sector=[]
jobDescription=[]

PATH='/home/omar/chromedriver_linux64/chromedriver' #change it to where chromedriver(or any other browser driver) exist on your computer
driver=webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

username = driver.find_element_by_id("username")
username.send_keys("yourEmail")  # Enter Your Email Address instead of (yourEmail)
  
password = driver.find_element_by_id("password")
password.send_keys("yourPassword")        # Enter Your Password instead of (yourPassword)
driver.find_element_by_xpath("//button[@type='submit']").click()
pageNum=0

while(pageNum<=25*40):
    driver.get(f"https://www.linkedin.com/jobs/search/?start={pageNum}")
    time.sleep(2)
    src = driver.page_source
    soup=BeautifulSoup(src,'lxml')
    container=soup.find_all("div",{"class":"flex-grow-1 artdeco-entity-lockup__content ember-view"})
    
    for i in range (len(container)):
        #scraping the outlines of all jobs
        jobTitle=container[i].find("a",{"class":"disabled ember-view job-card-container__link job-card-list__title"})
        jobTitles.append(jobTitle.text.strip().replace("\n",""))
        links.append("https://www.linkedin.com"+jobTitle.get('href'))
        
        if(container[i].find(["div","a"],{"class":["job-card-container__company-name","job-card-container__link job-card-container__company-name ember-view"]})==None):
            companyNames.append("Null")
        else:
            companyName=container[i].find(["div","a"],{"class":["job-card-container__company-name","job-card-container__link job-card-container__company-name ember-view"]})
            companyNames.append(companyName.text.strip().replace("\n",""))
        
        location=container[i].find("li",{"class":"job-card-container__metadata-item"})
        locations.append(location.text.strip().replace("\n",""))
        
        if container[i].find("li",{"class":"job-card-container__metadata-item job-card-container__metadata-item--workplace-type"})==None:
            remote.append("Null")
        else:
            isRemote=container[i].find("li",{"class":"job-card-container__metadata-item job-card-container__metadata-item--workplace-type"})
            remote.append(isRemote.text.strip().replace("\n",""))
    pageNum=pageNum+25


for link in links:
    #scraping every individual job details
    driver.get(link)
    time.sleep(2)
    src=driver.page_source
    soup=BeautifulSoup(src,"lxml")
    notCoolDate=soup.find("span",{"class":"jobs-unified-top-card__posted-date"})
    applying=soup.find("span",{"class":"jobs-unified-top-card__applicant-count"})
    jobDetails=soup.find_all("li",{"class":"jobs-unified-top-card__job-insight"})
    jobDesc=soup.find("div",{"id": "job-details"})
    
    if(jobDesc==None):
        jobDescription.append("Null")
    else:
        description=jobDesc.find("span").text
        jobDescription.append(description)


    if jobDetails ==None or len(jobDetails)==0:
         jobTimes.append("Null")
         seniority.append("Null")       
    elif "·" in jobDetails[0].text:
        jobTimes.append((jobDetails[0].text.split("·"))[0].strip().replace("\n",""))
        seniority.append((jobDetails[0].text.split("·"))[1].strip().replace("\n",""))
    else:
        jobTimes.append(jobDetails[0].text.strip().replace("\n",""))
        seniority.append("Null")
    
    if len(jobDetails)>1:  
        if "·" in jobDetails[1].text:
            sector.append((jobDetails[1].text.split("·"))[1].strip().replace("\n",""))
        else:
            sector.append("Null")
    else:
        sector.append("Null")
    

    if notCoolDate == None:
        date.append("Null")
    else:
        date.append(dateparser.parse(notCoolDate.text.strip().replace("\n","")).strftime("%Y-%m-%d"))
 
    
    if applying == None:
        if(jobDesc==None and (jobDetails==None or len(jobDetails)==0)): #sometimes the link is no longer available(the job is removed) and if this condition is true then we know that this is the case
            applicants.append("Null")
        else:
            applicants.append("Over 200 applicants")
    else:
        applicants.append(applying.text.strip().replace("\n",""))
    
    

allLists=[jobTitles,companyNames,locations,remote,date,applicants,jobTimes,sector,seniority,jobDescription,links]
export= zip_longest(*allLists)
with open("/home/omar/DataAnalysis/linkedinScrap.csv", "w") as myfile:
   write=csv.writer(myfile)
   write.writerow(["Job title", "Company name","Location","Remote/on site","Date","Applicants","Full/Part time","Sector","Seniority level","JobDescription","Links"])
   write.writerows(export)

