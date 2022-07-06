import time
import dateparser
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
driver.find_element(By.ID, 'username').send_keys('EMAIL')
driver.find_element(By.ID, 'password').send_keys('PASSWORD')
driver.find_element(By.ID, 'password').send_keys(Keys.ENTER)

result = []

while(result.__len__() < 1000):
    driver.get('https://www.linkedin.com/jobs/search/?location=Egypt&start=' + str(result.__len__()))
    time.sleep(5)
    jobs = driver.find_elements(By.XPATH, "//ul[@class='jobs-search-results__list list-style-none']/li")
    for job in jobs:
        try:
            job.click()

            # Read all data of the job
            jobTitle = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/a/h2"))).text
            companyName = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/span/span[@class='jobs-unified-top-card__company-name']"))).text
            location = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/span/span[@class='jobs-unified-top-card__bullet']"))).text
            dateAndTime = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/span[@class='jobs-unified-top-card__subtitle-secondary-grouping t-black--light']/span[1]"))).text
            jobType = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/ul/li[@class='jobs-unified-top-card__job-insight'][1]/span"))).text
            seniorityLevel = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/ul/li[@class='jobs-unified-top-card__job-insight'][1]/span"))).text
            industry = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/ul/li[@class='jobs-unified-top-card__job-insight'][2]/span"))).text
            noOfApplicants = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='jobs-unified-top-card__content--two-pane']/div/span[@class='jobs-unified-top-card__subtitle-secondary-grouping t-black--light']/span[2]"))).text
            jobDesc = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='job-details']"))).text

            # Clean the data
            jobTitle = jobTitle.strip()
            companyName = companyName.strip()
            location = location.strip()
            dateAndTime = dateparser.parse(dateAndTime)
            try:
                jobType = jobType.split('·')[0].strip()
            except:
                jobType = ''
            
            try:
                seniorityLevel = seniorityLevel.split('·')[1].strip()
            except:
                seniorityLevel = ''
            
            try:
                industry = industry.split('·')[1].strip()
            except:
                industry = ''
            
            try:
                noOfApplicants = int(noOfApplicants.split(' ')[0].strip())
            except:
                noOfApplicants = float("nan")
            jobDesc = jobDesc.strip()

            result.append([jobTitle, companyName, location, dateAndTime, jobType, seniorityLevel, industry, noOfApplicants, jobDesc])
            print('Processed ' + jobTitle + ' at ' + companyName)
        except:
            print('error skipping')
    print("Processed so far: " + str(result.__len__()))

print('Got all data... writing CSV!')
csv = pd.DataFrame(result, columns=['Job Title', 'Company Name', 'Location', 'Date', 'Job Type', 'Seniority Level', 'Industry', 'No. of Applicants', 'Job Description'])
csv.to_csv('sample-data.csv', index=False)
print('Done!')
print('Total jobs: ' + str(result.__len__()))

driver.quit()