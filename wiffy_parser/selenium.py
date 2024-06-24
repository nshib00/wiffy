from os import getenv
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import Keys, Chrome, ChromeService, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger
from utils.user_data import get_pwd
from wiffy_parser.html import save_html_in_file


load_dotenv()

logger = get_logger(__file__)


def create_driver() -> WebDriver:
    driver_options = ChromeOptions()
    # driver_options.add_argument("--headless=new")
    driver_options.add_extension("D:\projects\wiffy\chromedriver\extensions\AdBlocker-Ultimate.crx")
    driver_service = ChromeService()
    driver = Chrome(options=driver_options, service=driver_service)
    driver.maximize_window() # в релизной версии будет заменено на driver.minimize_window()
    return driver


def get_source_page(driver: WebDriver) -> None:
    pages_html = []
    page_num = 1
    next_page_btn_xpath = "/html/body/div[6]/div/div[3]/div[3]/p[2]/button[2]"
    wait = WebDriverWait(driver, timeout=30)
    while True:
        try:
            next_page_btn = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, next_page_btn_xpath)
                )
            )
            print(f'{page_num=}: {next_page_btn.get_attribute("disabled")=}')
            try:
                next_page_btn.click()
            except WebDriverException:
                logger.info(f'Button is not clickable on page {page_num}.')
                break
            pages_html.append(driver.page_source)
            page_num += 1
        except TimeoutException:
            popup = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, 'shareModal')
                )
            )
            close_btn = popup.find_element(By.CLASS_NAME, 'close')
            close_btn.click()
            continue
        except Exception as e:
            logger.error(f'Exception occured: {e.__class__.__name__}: {e}')
            break
        finally:
            print(f'{page_num=}: {len(driver.page_source)=}')
            save_html_in_file(pages_html)


def kissvk_auth(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, timeout=10)
    auth_btn = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success.btn-lg"))
    )
    auth_btn.click()
    login_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'login'))
    )
    login_input.clear()
    login_input.send_keys(getenv("VK_LOGIN"))
    login_input.send_keys(Keys.ENTER)
    pwd_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    pwd_input.clear()
    pwd_input.send_keys(str(get_pwd()))
    pwd_input.send_keys(Keys.ENTER)


def close_popup_window(driver: WebDriver) -> None:
    ''' Закрывает окно браузера (обозначено popup_window), открывающееся расширением. '''
    main_window = driver.current_window_handle # основное окно (в котором открыт kissvk)
    main_window_index = driver.window_handles.index(main_window) # индекс может иметь значения 0 или 1 (т.к. selenium открывает только 2 окна: с kissvk и с расширением)
    popup_window = driver.window_handles[not main_window_index] # если одно окно из двух - с kissvk, то другое - с расширением
    driver.switch_to.window(popup_window)
    driver.close()
    driver.switch_to.window(main_window)
    