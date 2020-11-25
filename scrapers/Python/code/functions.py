# -*- coding: utf-8 -*-

# Import libraries
import os
import sys
import string
import copy
import datetime
import numpy as np
import pandas as pd
import time
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from Scraper import*

#------------------------------------------------------------------------------
# Functions for continuously saving all the listings

def scrape():
    scraper = Scraper()
    print('Done!')

