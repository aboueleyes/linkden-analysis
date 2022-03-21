from os import EX_CANTCREAT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas
import time

driver = webdriver.Chrome()


def logIn():
    driver.get("https://linkedIn.com")

    signIn_page = driver.find_element(by = By.CLASS_NAME, value ="nav__button-secondary")
    signIn_page.click()

    driver.implicitly_wait(5)
    user_name = driver.find_element(by = By.ID, value= "username")
    user_name.send_keys(input('Enter your username: '))

    password = driver.find_element(by = By.ID, value = "password")
    password.send_keys(input('Enter your password: '))

    try:
        getButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login__form_action_container"))
        )

        signIn = getButton.find_element(by = By.TAG_NAME, value = "button")
        signIn.click()
    except:
        driver.quit()
 

jobTitle = []
companyName =[]
Location = []
FullTimeOrPartTime = []
SectorOfIndustry = []
NumberOfApplicants = []
jobDescription = []

def getJobsFromTable():

    j=0
    while(j<=975):
        driver.implicitly_wait(5)
        if(j==0):
            driver.get("https://www.linkedin.com/jobs/search/?geoId=106155005&keywords=egypt&location=Egypt")
        else:
            driver.get("https://www.linkedin.com/jobs/search/?geoId=106155005&keywords=egypt&location=Egypt&start="+str(j))


        page_source = driver.page_source
        lxml_soup = bs(page_source, 'lxml')

        jobLink=[]

        # searching for all job containers
        job_container = lxml_soup.find('ul', class_='jobs-search-results__list list-style-none')

        for link in job_container.find_all('a', class_='disabled ember-view job-card-container__link job-card-list__title'):
            jobLink.append(link['href'])
        
        print(len(jobLink))
        for i in range(len(jobLink)):
            
            driver.get('https://linkedin.com'+jobLink[i])

            jobTitle.append(driver.find_element(by = By.TAG_NAME, value = "h1").text)
        


            try:
                getName = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__company-name"))
                )
                tag = getName.find_element(by = By.TAG_NAME, value ="a")
                companyName.append(tag.text)
            except:
                companyName.append('null')

            try:
                getLocation = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__bullet"))
                )
                Location.append(getLocation.text)
            except:
                Location.append('null')

            try:
                getSector = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/ul/li[2]/span"))
                )
                SectorOfIndustry.append(getSector.text.split[1])
            except:
                SectorOfIndustry.append('null')


            try:
                getNum = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__applicant-count                    "))
                )
                NumberOfApplicants.append(getNum.text)
            except:
                NumberOfApplicants.append('Over 200 applicants')

            try:
                getDes = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='job-details']"))
                )
                
                jobDescription.append(getDes.text)
            except:
                jobDescription.append('null')

            try:
                li = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__job-insight"))
                )
                getPorF = li.find_element(by = By.TAG_NAME, value = "span")

                FullTimeOrPartTime.append(getPorF.text.strip())
            except:
                FullTimeOrPartTime.append('null')
            df = pandas.DataFrame({'Job Title':jobTitle,'Company Name':companyName, 'Location':Location,'Full-time / Part-time':FullTimeOrPartTime,'Sector or Industry':SectorOfIndustry,'Number of Applicants':NumberOfApplicants,'Job Description':jobDescription})
            df.to_csv('sample-data.csv', index = False, encoding = 'utf-8')
        j += 25
    
logIn()
getJobsFromTable()

