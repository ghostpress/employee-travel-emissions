# -*- coding: utf-8 -*-

# Import libraries
import os
import sys
import string
import copy
import datetime
import time
import requests
import numpy as np
import pandas as pd
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Scraper(object):

    def __init__(self):
        self.init()

    def init(self):
        self.updatePaths()

#---------- Methods for file input - output

    def write_txt(self, text, filePath):
        with open(filePath, 'w') as f:
            f.write(text)

    def read_dict(self, filePath):
        return np.load(filePath).item()

    def write_dict(self, dictionary, filePath):
        np.save(filePath, dictionary)

    def convertListToPandasDf(self, table, header=True):
        if (header == False):
            df = pd.DataFrame(table)
        else:
            df = pd.DataFrame(table, columns=header)
        return df

    def savePandasDfAsCsv(self, df, filePath, header=True):
        if (header == False):
            df.to_csv(filePath, index=False, header=False)
        else:
            df.to_csv(filePath, index=False)

#---------- Methods for keeping time

    def startTimer(self):
        self.startTime = time.time()

    def elapsedTime(self):
        currentTime = time.time()
        return (currentTime - self.startTime)

    def wait(self, seconds=2, random=False):
        if (random):
            time.sleep(randint(seconds-1, seconds))
        else:
            time.sleep(seconds)

#---------- Methods for dynamically creating file paths and folders

    def updatePaths(self):
        self.getDate()

    def getDate(self):
        # YYYY-MM-DD
        now       = datetime.datetime.now()
        self.now  = now
        yearStr = str(now.year)
        monthStr = str(now.month)
        if (len(monthStr) < 2):
            monthStr = '0' + monthStr
        dayStr = str(now.day)
        self.date = yearStr + '-' + monthStr + '-' + dayStr

    def dirMissing(self, directory):
        if (not os.path.exists(directory)):
            return True
        return False

    def createFolder(self, directory):
        print('Creating Folder: ' + directory)
        os.makedirs(directory)

#---------- Methods for starting webdriver (aka browser) and opening / closing

    def restartBrowser(self):
        print('\tRestarting browser')
        self.quitBrowser()
        self.openBrowser()

    def openBrowser(self, runHeadless=False, loadImages=False):
        options = webdriver.ChromeOptions()
        if (runHeadless):
            options.add_argument('--headless')
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
        # Set the window size
        options.add_argument('--window-size=800,600')
        if (loadImages == False):
            prefs = {'profile.managed_default_content_settings.images':2}
            options.add_experimental_option('prefs', prefs)
        # Set the location
        options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        chromedriverPath ='/Users/jhelvy/Documents/chromedriver'
        self.browser = webdriver.Chrome(executable_path=chromedriverPath,
                                        options=options)

    def openNewBrowserTab(self):
        self.browser.execute_script('''window.open("about:blank","_blank");''')

    def switchToBrowserTab(self, tabIndex):
        tabs = self.browser.window_handles
        self.browser.switch_to.window(tabs[tabIndex])

    def closeBrowserTab(self, tabIndex=None):
        if (tabIndex == None):
            self.browser.close()
        else:
            self.switchToBrowserTab(tabIndex)
            self.browser.close()

    def quitBrowser(self):
        self.browser.quit()

#---------- Methods for browser navigation

    def browserToUrl(self):
        url = self.buildUrl()
        self.browser.get(url)
        pageLoaded = False
        self.startTimer()
        while (pageLoaded == False):
            self.wait()
            pageLoaded = self.hasPageLoaded()
            if (self.elapsedTime() > 30):
                self.restartBrowser()

    def buildUrl(self):
        return 'http://www.google.com'

    def hasPageLoaded(self):
        return True

#---------- Methods for getting data from the browser

    def getHtmlFromBrowser(self):
        return self.browser.page_source

    def getHtmlFromUrl(self, url):
        page = requests.get(url)
        return page.text

    def getSoup(self, html):
        return BeautifulSoup(html, 'lxml')

    def screenshot(self):
        self.browser.save_screenshot('./screenshots/temp.png')

    def getPageData(self):
        return 42











