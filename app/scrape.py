from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_handler import SeleniumHandler


def script_process(sh: SeleniumHandler):
    search_prompt = sh.browser.find_element(By.CLASS_NAME, 'search-global-typeahead__input')
    search_prompt.send_keys('CEO')
    sleep(2)
    search_prompt.send_keys(Keys.ENTER)
    # see_all_button = sh.browser.find_element(By.CLASS_NAME, 'search-global-typehead__hit-text t-16 t-black')
    # see_all_button = sh.browser.find_element(By.XPATH, '//span[contains(text(), "all results")]')
    # see_all_button.click()
    sleep(3)

    # people_button = sh.browser.find_element(By.XPATH, '//*[contains(@class, "search-navigation-panel__button")]')
    # people_button = sh.browser.find_element(By.XPATH, '//button[contains(text(), "People")]')
    people_button = sh.browser.find_element(By.XPATH, '//a[contains(text(), "See all people results")]')
    people_button.click()
    sleep(5)

    # https://www.linkedin.com/groups/3732032/
    sh.browser.get('https://www.linkedin.com/groups/3732032/')
    sleep(7)
    join_button = sh.browser.find_element(By.XPATH, '//span[contains(text(), "Join")]/ancestor::button')
    join_button.click()
    sleep(2)

    # Continue to group
    sh.browser.get('https://www.linkedin.com/groups/3732032/')
    sleep(5)

    # Close Messaging
    join_button = sh.browser.find_element(By.XPATH, '//span[text()="Messaging"]/ancestor::button')
    join_button.click()
    sleep(2)

    # Show all members
    all_members_button = sh.browser.find_element(By.XPATH, '//a[contains(@aria-label, "Show all members")]')
    all_members_button.click()
    sleep(10)