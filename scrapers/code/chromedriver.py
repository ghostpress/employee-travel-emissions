# Import libraries
from selenium import webdriver

def chrome_driver(url: str):
    chrome_driver_path = '/home/lucia/Documents/chromedriver'  # change according to system

    # Preliminary chromedriver settings:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")       # maximize the Chrome window
    options.add_argument("disable-infobars")      # disable infobars
    options.add_argument("--disable-extensions")  # disable extensions

    # Declare the driver using the path and options specified above

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)  # TODO: read docs & fix
    driver.get(url)  # navigates Chrome to the given url

    return driver

