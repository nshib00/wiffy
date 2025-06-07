from os import getenv

from dotenv import load_dotenv
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import Chrome, ChromeOptions, ChromeService, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from chrome_extension_python import Extension

from exceptions import ExtensionNotFoundError
from utils.logger import get_parser_logger
from utils.user_data import get_pwd
from wiffy_parser.html import save_html_in_file

load_dotenv()

logger = get_parser_logger()


def create_driver() -> WebDriver:
    driver_options = ChromeOptions()
    try:
        adblock_url = r"https://chromewebstore.google.com/detail/adblocker-ultimate/ohahllgiabjaoigichmmfljhkcfikeof"
        adblock_extension = Extension(adblock_url).load() 
        driver_options.add_argument(adblock_extension)
    except OSError as e:
        logger.error(f"Error in driver creation: {e.__class__.__name__}: {e}")
        raise ExtensionNotFoundError
    driver_service = ChromeService()
    driver = Chrome(options=driver_options, service=driver_service)

    if getenv("APP_MODE") == "DEBUG":
        driver.maximize_window()
    else:
        driver_options.add_argument("--headless=new")
        driver_options.add_argument("--no-sandbox")
        driver.minimize_window()

    return driver


def get_source_page(driver: WebDriver) -> None:
    pages_html = []
    page_num = 0
    next_page_btn_xpath = "/html/body/div[6]/div/div[3]/div[3]/p[2]/button[2]"
    wait = WebDriverWait(driver, timeout=30, poll_frequency=0.2)
    while True:
        try:
            next_page_btn = wait.until(EC.visibility_of_element_located((By.XPATH, next_page_btn_xpath)))
            pages_html.append(driver.page_source)
            next_page_btn.click()
            page_num += 1
        except TimeoutException:
            popup = wait.until(EC.visibility_of_element_located((By.ID, "shareModal")))
            close_btn = popup.find_element(By.CLASS_NAME, "close")
            close_btn.click()
            continue
        except ElementClickInterceptedException as e:
            logger.warning(f"{e.__class__.__name__}: Button is not clickable on page {page_num}.")
            break
        except Exception as e:
            logger.error(f"Exception occured: {e.__class__.__name__}: {e}")
            break
        finally:
            if len(driver.page_source) > 50000:
                logger.info(f"{page_num=}: {len(driver.page_source)=}")
            else:
                logger.warning(f"{page_num=}: {len(driver.page_source)=}")
            save_html_in_file(pages_html)


def kissvk_auth(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, timeout=10)
    auth_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success.btn-lg")))
    auth_btn.click()
    login_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    login_input.clear()
    login_input.send_keys(getenv("VK_LOGIN")[2:])
    login_input.send_keys(Keys.ENTER)
    pwd_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    pwd_input.clear()
    pwd_input.send_keys(str(get_pwd()))
    pwd_input.send_keys(Keys.ENTER)


def close_popup_window(driver: WebDriver) -> None:
    main_window = driver.current_window_handle

    for handle in driver.window_handles:
        if handle != main_window:
            popup_window = handle
            break

    driver.switch_to.window(popup_window)
    driver.close()
    driver.switch_to.window(main_window)
