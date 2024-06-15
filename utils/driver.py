from selenium import webdriver
from selenium.webdriver import ChromeService, ChromeOptions
from dotenv import load_dotenv, find_dotenv

from utils.logger import get_logger


logger = get_logger('driver.log')

envfile = find_dotenv()
load_dotenv(envfile)


def create_driver() -> webdriver.chrome.webdriver.WebDriver:
    driver_options = ChromeOptions()
    # driver_options.add_argument("--headless=new")
    driver_options.add_extension("D:\projects\wiffy\chromedriver\extensions\AdBlocker-Ultimate.crx")
    driver_service = ChromeService()
    driver = webdriver.Chrome(options=driver_options, service=driver_service)
    driver.maximize_window() # в релизной версии будет заменено на driver.minimize_window()
    return driver
