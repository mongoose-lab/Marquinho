# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:05:47 2021

@author: b3dd37

Script to generate a list of linkedin URLs for matching profiles, 
then send them a scripted message
"""



"""
 from selenium.webdriver.remote.webdriver.WebDriver import execute_script
 
 from selenium.webdriver.common.by import By
 
 from selenium.webdriver.support.ui import WebDriverWait
 
 from selenium.webdriver.support import expected_conditions as EC
 
 from selenium.webdriver.common.alert import Alert
 
 import urllib
 
 import pandas as pd
 
 import time
 
 from selenium.webdriver.chrome.options import Options
 
 import ssl
 
 import http
 
 import requests

"""


import time

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException

#from selenium.webdriver.remote import execute_script

from selenium.webdriver.support.ui import Select

import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains

import re

from os import chdir, getcwd


wd=getcwd()
chdir('C:/Users/b3dd37/OneDrive - Linde Group/Projects/Personal/LinkedIn Automation')

"""

Pre-work. Setting up the searches.

"""

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
browser.get('https://www.linkedin.com/feed/')

time.sleep(2)
browser.find_element_by_xpath('/html/body/div[2]/main/p[1]/a').click() # enter log-in page

# enter log in details and log in
# this stage requires 2-stage authentication via text message
browser.find_element_by_xpath('//*[@id="username"]').send_keys('beatriz@7liveshr.com')
time.sleep(5)
browser.find_element_by_xpath('//*[@id="password"]').send_keys('y5pdVOcJ')
time.sleep(5)
browser.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()

# manually enter site and enter code sent to phone

time.sleep(2)

"""
Set up a manual recruiter search. Copy the url of the results page into page_1_advanced below
"""

"""
Script Part 1. Automated profile scraping.
"""

browser.switch_to.window(browser.window_handles[0]) #force first tab active

page_1_advanced='https://www.linkedin.com/talent/search?searchContextId=ca72fe7f-41af-4da6-a47a-776d410ca91f&searchHistoryId=4967218146&searchKeyword=%22backend%20developer%22%20OR%20%22software%20engineer%22&searchRequestId=b5281bd8-7bff-4832-9207-b976c1c6062a&start=0&uiOrigin=ADVANCED_SEARCH'

#browser.switch_to.window(browser.window_handles[0]) #switch tab

browser.get(f'{page_1_advanced}') # enter the first results 
time.sleep(10)
browser.get(f'{page_1_advanced}') # re-enter incase web browser is frozen after inactivity
time.sleep(10) 
try:
    browser.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/div/div[1]').click() # close pop-up window                           
except NoSuchElementException:
    print("Pop up already closed.")

for k in range(1,19) :
    browser.execute_script(f"window.scrollTo(0, {k*500})")
    time.sleep(2)
    print(f'Scroll number {k}, page 1')

browser.execute_script("window.scrollTo(0, 0)")
candidate_list = []
name_list = []
failed_to_grab_profile_list = []
for i in range(1,26):
        try:
            browser.find_element_by_xpath(f'/html/body/div[3]/div[5]/div/div[2]/div[1]/div[1]/div/div/div[2]/section/span/div/form/ol/li[{i}]/div/article/div/article/article/div/div[1]/div[1]/section/div/div[2]/span/span[1]/div/a').click() # click on candidate link                             
            time.sleep(4)
            url=browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[2]/span/div/div/div[2]/div/section[4]/ul/li/div/a/span[1]').text
            name=browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[2]/span/div/div/header/section/div[1]/div[1]/section/div/div[2]/span/span[1]/div').text
#            print(url)
#            print(name)
            candidate_list.append(url)
            name_list.append(name)             
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/div/a').click() # click out of pop-up   
            except NoSuchElementException:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/a').click() # click out of pop-up 
            
            print(f'Profile {i} on page 1 successfull.')
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"{i}th profile on page 1 failed.")
            failed_to_grab_profile_list.append(f' Page 1. Profile {i}') # record which profiles we didn't catch
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/div/a').click() # click out of pop-up   
            except NoSuchElementException:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/a').click() # click out of pop-up    
        continue
   
# after page 1



"""
get the link for subsequent pages
"""

time.sleep(10)
browser.get(f'{page_1_advanced}') # enter the first results
time.sleep(10)
browser.execute_script('window.scrollTo(0, 20000)') # skip to bottom of page
time.sleep(10)
browser.find_element_by_xpath('/html/body/div[3]/div[5]/div/div[2]/div[1]/div[1]/div/div/div[2]/section/span/div/form/nav/ol/li[2]/a').click() #enter second page
time.sleep(10)
page_2_advanced=browser.current_url

for j in range(1,5):
    page_start_number=f'{j*25}'
    page_start=page_2_advanced.replace('start=25',f'start={page_start_number}')
    print(page_start)
    browser.get(f'{page_start}')
    time.sleep(10)
    for k in range(1,19) :
        browser.execute_script(f"window.scrollTo(0, {k*500})")
        time.sleep(2)
        print(f'Scroll number {k}, page {j + 1}')
    browser.execute_script('window.scrollTo(0, 0)') # return to top of page
    time.sleep(10)
    for i in range(1,26):
        try:
            browser.find_element_by_xpath(f'/html/body/div[3]/div[5]/div/div[2]/div[1]/div[1]/div/div/div[2]/section/span/div/form/ol/li[{i}]/div/article/div/article/article/div/div[1]/div[1]/section/div/div[2]/span/span[1]/div/a').click() # open profile screen
            time.sleep(7)
            url=browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[2]/span/div/div/div[2]/div/section[4]/ul/li/div/a/span[1]').text                                             
            name=browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[2]/span/div/div/header/section/div[1]/div[1]/section/div/div[2]/span/span[1]/div').text
            candidate_list.append(url)
            name_list.append(name) 
            time.sleep(2)
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/div/a').click() # click out of pop-up   
            except NoSuchElementException:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/a').click() # click out of pop-up    
            print(f'Profile {i} on page {j + 1} successfull.')
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"Profile {i} on page {j + 1} failed.")
            failed_to_grab_profile_list.append(f' Page {j + 1}. Profile {i}') # record which profiles we didn't catch
            time.sleep(10)
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/div/a').click() # click out of pop-up   
            except NoSuchElementException:
                browser.find_element_by_xpath('/html/body/div[3]/div[6]/base-slidein-container/div/div/div/div/div[1]/a').click() # click out of pop-up    
        continue

failure_ratio=len(failed_to_grab_profile_list)/(len(failed_to_grab_profile_list)+len(candidate_list))
print(f"{(1-failure_ratio)*100}% of profiles scraped.")


#remove any duplicates results
d={'name':name_list,'url':candidate_list}
dftest=pd.DataFrame(d)

dftest_n = dftest.drop_duplicates(subset=['url'])

len(dftest)
len(dftest_n)
candidate_list=dftest_n['url']
name_list=dftest_n['name']

#dftest.to_csv('dftest.csv')


# remove any blank or empty spaces in the lists

candidate_list = list(filter(None, candidate_list))
name_list = list(filter(None, name_list))
failed_to_grab_profile_list = list(filter(None,set(failed_to_grab_profile_list)))

# check if the names and candidate list have successfully loaded with the same length

if len(candidate_list) == len(name_list):
    print("Profile and name list successfully extracted.")
else:
    print("Profile and name list lengths do not match! Stop process now!")


# extract only first name from each name


# name_list=[re.sub('[^a-zA-Z0 ]+', '', x) for x in name_list] #remove special characters / icons

# name_list=[x.title() for x in name_list]

def first_word(input_list):          
    output_list = [x.split()[0] for x in input_list]
    return output_list

first_name=first_word(name_list)

len_first_name=len((first_name))

print(f"{len_first_name} candidates to message")

candidate_list
first_name

"""
End script
"""

# automated message sending

"""
Script Part 2. Automated message sending.
"""

# section for candidates without a connection

job_profile_link = 'https://www.7liveshr.com/python-backend-developer'
profiles_failed_to_send=[f'{job_profile_link}']
profile_sent_successfully = []

for i in range(0,len(candidate_list)): # start range at 0 to go from start 
    try:
        message = f"""Hello {first_name[i]},
    
7 Lives might be looking for a person like you!
    
{job_profile_link}
    
If IT skills you can show
I would love to have a chat
Please do let me know
If you would be up for that.
"""
        browser.switch_to.window(browser.window_handles[0])
        browser.get(f'{candidate_list[i]}') # go to candidate url page
        time.sleep(7)
#        print(1.0) 
        try:
            browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]').click() # connect
        except (NoSuchElementException):
             try:
                 browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]').click() # connect
             except (NoSuchElementException):
                 browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button[1]').click() # connect                                            
#        print(2.0)                                       
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]').click() # add message
#        print(3.0)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/textarea').send_keys(message) # send message to text area
#        print(4.0)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click() # send connection invite
        print(f'Candidate {i} successfully contacted')
        profile_sent_successfully.append(candidate_list[i])
    except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException) as e:
        try:
            print('First method failed, try second method.')
    #        browser.find_element_by_xpath('/html/body/div[7]/aside/div[2]/header/section[2]/button[2]').click() # close pop-up window
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, 200)") # scroll down
#            print(1.1)
            try:
                browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[3]/button').click() # connect
                                               
            except (NoSuchElementException):
                 try:
                     browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[3]/button').click() # connect                                                    
                 except (NoSuchElementException):
                     browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[3]/button').click() # connect                                            
            time.sleep(2)
#            print(2.1)
            time.sleep(2)
#            print(3.1)
            try:                
#                browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/div/div/ul/li[4]/div/span[1]').click() #old link - appears to be broken
                browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div/div/div/ul/li[5]/div').click() # enter connect page              
            except (NoSuchElementException):
                browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/div/div/ul/li[4]/div/span[1]').click() # enter connect page
            time.sleep(2)
#            print(4.1)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]').click() # connect
            time.sleep(2)
#            print(5.1)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]').click() # add message
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/textarea').send_keys(message) # send message to text area
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click() # send connection invite
            print(f'Candidate {i} successfully contacted.')
            profile_sent_successfully.append(candidate_list[i])
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException) as e:
            print(f'Candidate {i} failed to send.')
            profiles_failed_to_send.append(candidate_list[i])
            continue



# print out which profiles failed and create a .csv output
# cross out any profiles which fall into the successfully contacted list
coldf=[]
for i in range(1,len(profiles_failed_to_send)+1):
    if i == 1:
        coldf.append('Job Profile Link')
    else:
        coldf.append('Candidate Profile Link')

profile_sent_successfully
profiles_failed_to_send


successfully_sent_number=len(profile_sent_successfully)
success_send_ratio=len(profile_sent_successfully)/(len(profile_sent_successfully)+(len(profiles_failed_to_send)-1))
print(f"{successfully_sent_number} ({(success_send_ratio)*100}%) profiles successfully messaged.")






"""

Script Part 3. Retry the failed profiles.

"""



dftest_n # the original df of urls and candidate full names

dftest_n_1=dftest_n[dftest_n.url.isin(profiles_failed_to_send)] # the urls and candidate names which did not send successfully


candidate_list=dftest_n_1['url']
name_list=dftest_n_1['name']

#dftest.to_csv('dftest.csv')


# remove any blank or empty spaces in the lists

candidate_list = list(filter(None, candidate_list))
name_list = list(filter(None, name_list))

# check if the names and candidate list have successfully loaded with the same length

if len(candidate_list) == len(name_list):
    print("Profile and name list successfully extracted.")
else:
    print("Profile and name list lengths do not match! Stop process now!")
    
first_name=first_word(name_list)

len((first_name))


# rerun message sending

profiles_failed_to_send=[f'{job_profile_link}']
for i in range(0,len(candidate_list)): # start range at 0 to go from start
    try:
        message = f"""Hello {first_name[i]},
    
7 Lives might be looking for a person like you!
    
{job_profile_link}
    
If IT skills you can show
I would love to have a chat
Please do let me know
If you would be up for that.

In case you would like to work with Vue.js here is another opportunity that might be interesting for you: https://www.7liveshr.com/principal-front-end-vuejs
"""
        browser.switch_to.window(browser.window_handles[0])
        browser.get(f'{candidate_list[i]}') # go to candidate url page
        time.sleep(7)
        browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/button[1]/span').click() # connect   
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]').click() # add message
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/textarea').send_keys(message) # send message to text area
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click() # send connection invite
        print(f'Candidate {i} successfully contacted')
        profile_sent_successfully.append(candidate_list[i])
    except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException) as e:
        try:
    #        print('First method failed, try second method.')
    #        browser.find_element_by_xpath('/html/body/div[7]/aside/div[2]/header/section[2]/button[2]').click() # close pop-up window
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/button').click() # show more options
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, 200)") # scroll down
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/div/div/div/ul/li[4]/div/span[1]').click() # enter connect page
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]').click() # connect
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]').click() # add message
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/textarea').send_keys(message) # send message to text area
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click() # send connection invite
            print(f'Candidate {i} successfully contacted.')
            profile_sent_successfully.append(candidate_list[i])
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException) as e:
            print(f'Candidate {i} failed to send.')
            profiles_failed_to_send.append(candidate_list[i])
            continue
        
len(profile_sent_successfully)
df_length=len(profiles_failed_to_send)
print(f'{df_length} profliles failed to send.' )
#df.to_csv('missed_profiles.csv')





candidate_list_df=pd.DataFrame(candidate_list)
name_list_df = pd.DataFrame(name_list)

candidate_list=pd.read_csv('candidate_list.csv')

candidate_list_1=candidate_list.iloc[0:,1:2]

candidate_list=candidate_list_1.values.tolist()

test=strin

name_list=pd.read_csv('name_list.csv')

name_list_1=name_list.iloc[0:,1:2]

name_list=name_list_1.values.tolist()



type(candidate_list_1)

candidate_list_df.to_csv('candidate_list.csv')
name_list_df.to_csv('name_list.csv')

# candidate list needs to be a list of the urls

##########################


missed_profiles_index = [7,11,18]

missed_profiles=[]
for i in missed_profiles_index:
    missed_profiles.append(candidate_list[i])

df=pd.DataFrame(missed_profiles)
df.to_csv('missed_profiles.csv')



