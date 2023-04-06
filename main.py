from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
import random
from time import sleep
import pandas as pd


def random_sleep(a=1, b=2):
    sleep(random.randint(a, b))

indeed = {
    'job_input': '//input[@placeholder="Job title, keywords, or company"]',
    'location_input': '//input[@placeholder="city or region"]',
    'find_jobs': "//button[contains(text(),'Find jobs')]",
    'jobs':'//div[@class="css-1m4cuuf e37uo190"]',
    'salary': '//div[@id="salaryInfoAndJobType"]/span',
    'title':'//div[contains(@class, "jobsearch-JobInfoHeader-title-container")]/*/*',
    'apply_link':'//div[@id="applyButtonLinkContainer"]/*/*/*',
    'job_description':'//div[@id="jobDescriptionText"]',
    'company': '//div[@data-company-name="true"]/a',
    'next_page': '//a[@data-testid="pagination-page-next"]'
}

JOB = 'data scientist'
LOCATION = 'casablanca'
MAX_JOBS = 5


options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")

services = Service(executable_path=CM().install())

driver = webdriver.Chrome(service=services, options=options)
driver.maximize_window()
driver.implicitly_wait(10)

indeed_link = 'https://www.indeed.com/'

driver.get(indeed_link)

job_input = driver.find_element(by='xpath' , value=indeed['job_input'])
location_input = driver.find_element(by='xpath' , value=indeed['location_input'])
find_jobs = driver.find_element(by='xpath' , value=indeed['find_jobs'])

job_input.send_keys(JOB)
location_input.send_keys(LOCATION)
find_jobs.click()

random_sleep()

data = {
    'title': [],
    'salary': [],
    'company': [],
    'company_profile': [],
    'job_description': [],
    'apply_link': []
}

while len(data['title']) < MAX_JOBS:
    
    jobs = driver.find_elements(by='xpath', value=indeed['jobs'])
    print(len(jobs))
    
    try:
        driver.find_element(by='xpath', value='//button[@class="icl-CloseButton icl-Modal-close"]').click()
    except:
        pass
    
    for job in jobs:

        if len(data['title']) > MAX_JOBS:
            break
        job.location_once_scrolled_into_view
        random_sleep()
        job.click()
        
        for key in ['title', 'job_description', 'company', 'salary']:
            try:
                info = driver.find_element(by='xpath', value=indeed[key]).text
                print(info[:20])
                data[key].append(info)
                
            except:
                data[key].append('NaN')
        
        try:
            apply_link = driver.find_element(by='xpath', value=indeed['apply_link']).get_attribute('href')
            data['apply_link'].append(apply_link)
        except:
            data['apply_link'].append(driver.current_url)
        
        try:
            company_profile = driver.find_element(by='xpath', value=indeed['company']).get_attribute('href')
            data['company_profile'].append(company_profile)
        except:
            data['company_profile'].append('NaN')
            
            
        random_sleep()
        
    try:
        driver.find_element(by='xpath', value=indeed['next_page']).click()
    except:
        print('max page')
        break
    
    random_sleep()
driver.quit()

df = pd.DataFrame(data=data)
df.to_csv('output.csv', index=False)
