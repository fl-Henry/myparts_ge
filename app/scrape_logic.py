from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


from selenium_handler import SeleniumHandler
from log_handler import LogHandler


def script_process(sh: SeleniumHandler, lh: LogHandler):
    sb = sh.browser
    logs = lh.logger
    sb.set_window_size(1200, 720)
    # open url https://www.myparts.ge/en/
    for counter in range(3):
        url = 'https://www.myparts.ge/en/'
        try:
            logs.info(f"Loading URL:{url}")
            print(f"Loading URL:{url}")
            sb.get(url)
            sleep(10)
            logs.debug(f"URL is loaded:{url}")
            break
        except WebDriverException as _ex:
            sleep(2)
            print(f"Try: {counter} | Exception: {repr(_ex)}")
            sh.reinitialize()
            sb = sh.browser

    # close modal container
    # print(sb.find_element(By.CSS_SELECTOR, ".custom-modal-container"))
    if sb.find_element(By.CSS_SELECTOR, ".custom-modal-container").is_displayed():
        logs.info(f"Closing modal container")
        print(f"Closing modal container")
        close_button = sb.find_element(By.CSS_SELECTOR, "button.close-popup")
        close_button.click()
        # sb.refresh()
        logs.debug(f"Modal container is closed")
        sleep(2)

    # click on Manufacturer
    logs.info(f"Click on Manufacturer")
    print(f"Click on Manufacturer")
    xpath = '//div[text()="Manufacturer"]/parent::*/input'

    for counter in range(3):
        try:
            WebDriverWait(sb, poll_frequency=1, timeout=10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            manufacturer_input = sb.find_element(By.XPATH, xpath)
            ActionChains(sb).move_to_element(manufacturer_input).click().perform()
            logs.debug(f"Click on Manufacturer is done")
            break
        except TimeoutException as _ex:
            print(f"Try: {counter} | Exception: {repr(_ex)}")
            sb.refresh()

    # get list of Manufacturer
    # //div[contains(@class, "cursor-pointer")]/parent::div[contains(@class, "custom-scroll-bar")]
    logs.info(f"Getting list of Manufacturer")
    print(f"Getting list of Manufacturer")
    for counter in range(3):
        try:
            xpath = '//div[contains(@class, "cursor-pointer")]/parent::div[contains(@class, "custom-scroll-bar")]'
            WebDriverWait(sb, poll_frequency=1, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            manufacturer_list = sb.find_element(By.XPATH, xpath)
            print(manufacturer_list.text)
            sleep(1)
            break
        except TimeoutException as _ex:
            print(f"Try: {counter} | Exception: {repr(_ex)}")
            sb.refresh()

    # search_prompt = sh.browser.find_element(By.CLASS_NAME, 'search-global-typeahead__input')
    # search_prompt.send_keys('CEO')
    # sleep(2)
    # search_prompt.send_keys(Keys.ENTER)
    # # see_all_button = sh.browser.find_element(By.CLASS_NAME, 'search-global-typehead__hit-text t-16 t-black')
    # # see_all_button = sh.browser.find_element(By.XPATH, '//span[contains(text(), "all results")]')
    # # see_all_button.click()
    # sleep(3)
    #
    # # people_button = sh.browser.find_element(By.XPATH, '//*[contains(@class, "search-navigation-panel__button")]')
    # # people_button = sh.browser.find_element(By.XPATH, '//button[contains(text(), "People")]')
    # people_button = sh.browser.find_element(By.XPATH, '//a[contains(text(), "See all people results")]')
    # people_button.click()
    # sleep(5)
    #
    # # https://www.linkedin.com/groups/3732032/
    # sh.browser.get('https://www.linkedin.com/groups/3732032/')
    # sleep(7)
    # join_button = sh.browser.find_element(By.XPATH, '//span[contains(text(), "Join")]/ancestor::button')
    # join_button.click()
    # sleep(2)
    #
    # # Continue to group
    # sh.browser.get('https://www.linkedin.com/groups/3732032/')
    # sleep(5)
    #
    # # Close Messaging
    # join_button = sh.browser.find_element(By.XPATH, '//span[text()="Messaging"]/ancestor::button')
    # join_button.click()
    # sleep(2)
    #
    # # Show all members
    # all_members_button = sh.browser.find_element(By.XPATH, '//a[contains(@aria-label, "Show all members")]')
    # all_members_button.click()
    # sleep(10)