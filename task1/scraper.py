#!/usr/bin/env python
# coding: utf-8

# In[23]:


from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
import requests
import time
import pandas as pd
# In[24]:
driver = webdriver.Chrome("chromedriver.exe")
def  login():
 
 email = 'mostaf7583@gmail.com'
 passwors = ''
 url = "https://linkedin.com"
 time.sleep(5)
 driver.get(url)
 login = driver.find_element_by_id("session_key")
 login.send_keys(email)
 login = driver.find_element_by_id("session_password")
 print(login)
 login.send_keys(passwors)
 go = driver.find_element_by_class_name("sign-in-form__submit-button")
 go.click()

         
login()


# In[25]:


#Extrating links of jobs using selinum
i=0
links=[]
while(i<=700):
    url2 = "https://www.linkedin.com/jobs/search/?geoId=106155005&keywords=egypt&start="+str(i)
    driver.get(url2)
    time.sleep(5)
    list_of_all_links=driver.find_elements_by_xpath('.//a')
    with open('jobs_links.txt', 'w') as f:
        for a in list_of_all_links:
         links.append(a.get_attribute('href'))
         
    i=i+25


# In[6]:



# def readFile(fileName):
#         fileObj = open(fileName, "r") #opens the file in read mode
#         words = fileObj.read().splitlines() #puts the file into an array
#         fileObj.close()
#         return words
    
# links=readFile('jobs_links.txt')
links=[s for s in links if s.startswith('https://www.linkedin.com/jobs/view/')]


# In[7]:


def get_job_title():
    job_title = soup.find_all('h1',class_='t-24 t-bold')
    if(not len(job_title)==0):
      return job_title[0].text
    else:
      return "null"


# In[8]:


def get_location():
    location = soup.find_all('span',class_='topcard__flavordef  topcard__flavor--bullet')
    if(not len(location)==0):
        return location[0].text
    else:
        return "null"


# In[9]:


def get_descrption():
    description=soup.find_all('div',id='job-details')
    description= description
    if(not len(description)==0):
        return description[0].text
    else:
        return "null"


# In[10]:


def get_number_of_applicants():
    nmofapplicants=soup.find_all('span',class_='jobs-unified-top-card__applicant-count jobs-unified-top-card__applicant-count--low t-bold')
    if(not len(nmofapplicants)==0):
        return nmofapplicants[0].text
    else:
        return "null"


# In[11]:


def get_type_of_job():
    type= soup.find_all('li',class_='jobs-unified-top-card__job-insight')
  
    if(not len(type)==0):
        type=type[0].find_all('span')
        return type
    else:
        return "null"


# In[12]:


def get_number_of_employees():
    numEmp = soup.find_all('li',class_='jobs-unified-top-card__job-insight')
    

    if(not len(numEmp)==0):
        numEmp=numEmp[0].find_all('span')
        return numEmp[0].text
    else:
        return "null"
  


# In[13]:


def get_date():
    date=soup.find_all('span',class_='jobs-unified-top-card__posted-date')
    if(not len(date)==0):
        return date[0].text
    else:
        return "null"


# In[14]:


def get_number_of_applicants():
    nmofapplicants=soup.find_all('span',class_='jobs-unified-top-card__applicant-count jobs-unified-top-card__applicant-count--low t-bold')
    if(not len(nmofapplicants)==0):
        return nmofapplicants[0].text
    else:
        return "null"


# In[26]:


i=0
number_of_applications=[]
job_title=[]
location =[]
date     =[]
job_type =[]
nma=[]
nme=[]
descrption=[]
while(i<len(links)):
   
    source = driver.get(links[i])
    source=driver.page_source
    soup = BeautifulSoup(source,'lxml')
    job_title.append(str(get_job_title()))
    location .append(str(get_location()))
    date     .append(str(get_date()))
    job_type .append(str(get_type_of_job()))
    nma      .append(str(get_number_of_applicants()))
    nme      .append(str(get_number_of_employees()))
    descrption.append(str(get_descrption()))
    i=i+1

    



data={
"number_of_employee":nme,
"job_title":job_title,
"location":location,
"date":date,
"job_type":job_type,
"description":descrption,
"number_of_applications":nma,
"links":links
}
df=pd.DataFrame(data)



df.to_csv('linkfinal')

