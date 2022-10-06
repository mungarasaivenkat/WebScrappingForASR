from selenium import webdriver
import wget
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import shutil
import glob
import datetime
import time
# URL for scraping the Transcript data
url = 'http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx'
# Set chrome profile
ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":"Z:\Python\Transcript"})
driver = webdriver.Chrome(executable_path='Z:/Python/chromedriver_win32/chromedriver.exe',chrome_options=ChromeOptions)
driver.implicitly_wait(30)
# SET variables for the website:
NSD_TYPE = 'Regional'
NSD_Region = 'Itanagar'
NSD_Language = 'Hindi'
NSD_Bulletin = '1645'
Dates = []
# Functions for doing various stuff.
def PageInitialization():
    driver.get(url)
    driver.implicitly_wait(10)
    MianBroadcast_Button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_program_type_cbl_1")
    MianBroadcast_Button.click()
    driver.implicitly_wait(10)
    Type = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwtype'))
    Type.select_by_visible_text(NSD_TYPE)
    Region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsdname'))
    Region.select_by_visible_text(NSD_Region)
    Language = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwlanguages'))
    Language.select_by_visible_text(NSD_Language)
    Bulletin = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsd_bname'))
    Bulletin.select_by_visible_text(NSD_Bulletin)
    # Press the find button to get the text  files.
    find_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1')
    find_button.click()

def ExtractTranscript():
    print('[INFO] The website has been loaded, now searching links.')
    driver.implicitly_wait(10)
    # FInd  all the  Download Link :
    download = driver.find_elements_by_link_text('Download')
    print('[INFO] Downloading all transcripts.')
    driver.implicitly_wait(10)
    for link in download:
        link.click()
        driver.implicitly_wait(10)
        time.sleep(5)
    driver.implicitly_wait(10
    return len(download)
def ExtractDate(num):
    Date =[]
    print('The total number of files,',num)
    driver.implicitly_wait(10)
    row = ["%.2d" % i for i in range(2,num+2)]
    stringOne ='ctl00_ContentPlaceHolder1_GridView1_ctl'
    stringTwo = '_Label3'
    for num in row:
        id = stringOne + str(num) + stringTwo
        if driver.find_element_by_id(id) is not None:
            Dates.append(driver.find_element_by_id(id).text)
        else:
            print('It\'s else')
            break
    driver.implicitly_wait(10)
def LoopForPages():
    num = 2
    page = True
    while(page):
        NoOfFiles = ExtractTranscript()
        ExtractDate(NoOfFiles)
        filenames = glob.glob(directory+'*.pdf')
        print('[INFO] File is being Sorted.\n')
        filenames.sort(key=os.path.getmtime)
        for i in range (0,len(Dates)):
            new_name = new_directory + Dates[i]+'.pdf'
            shutil.move(filenames[i],new_name ) 
        try:
            next = driver.find_element_by_link_text(str(num))
            next.click()
            print('Next Page is found.')
            num = num + 1
        except:
           try:
                next = driver.find_element_by_link_text('...')
                next.click()
                print('Page Incrementation. The num is',num)
                driver.implicitly_wait(3)
                time.sleep(3)
                num = num + 1
           except:
                continue
           try :
                next = driver.find_element_by_link_text(str(num))
           except:
                print('Pages are over.')
                page = False

''' ---------------------------Perform the looping task----------------------------------------'''
directory = 'Z:/Python/Transcript/'
new_directory = 'Z:/Python/Transcript/Renamed/'
PageInitialization()
LoopForPages()