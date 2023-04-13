import os
import time
import configparser
import sys
from selenium.webdriver.common.by import By
from selenium import webdriver
from logging import Logger


class SeleniumHandler:

    def __init__(self, config_file, logger: Logger = None):
        print("Initializing Browser Instance!")
        if logger is not None:
            self.logger = logger
            self.logger.info("Initializing Browser Instance!")

        if os.path.exists(config_file):
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
        else:
            print("[Warning]: Config_file doesn't exist")
            sys.exit(1)

        # browser_path = config.get('DEFAULT', 'browser_path')
        # if self.logger is not None:
        #     self.logger.debug("browser_path: %s", browser_path)
        driver_path = self.config.get('DEFAULT', 'driver_path')
        if self.logger is not None:
            self.logger.debug("driver_path: %s", driver_path)

        option = webdriver.ChromeOptions()
        # option.binary_location = browser_path
        if self.config.get('OPTIONS', 'headless') == 'YES':
            option.add_argument("--headless")
            if self.logger is not None:
                self.logger.debug("--headless mode enabled")

        if self.config.get('OPTIONS', 'incognito') == 'YES':
            option.add_argument("--incognito")
            if self.logger is not None:
                self.logger.debug("--incognito mode enabled")

        # Create new Instance of Browser
        self.browser = webdriver.Chrome(options=option)
        print("Browser has been initialized!")
        if self.logger is not None:
            self.logger.info("Browser has been initialized!")

    def quit_browser(self):
        print("Quitting Browser Instance!")
        if self.logger is not None:
            self.logger.info("Quitting Browser Instance! - Finished")

        self.browser.quit()

    def exit(self, x):
        self.quit_browser()
        sys.exit(x)

    def login(self):
        # open login url in browser
        self.browser.get(self.config.get('LOGIN', 'url'))

        username = self.browser.find_element(By.ID, 'username')
        username.send_keys(self.config.get('LOGIN', 'username'))

        password = self.browser.find_element(By.ID, 'password')
        password.send_keys(self.config.get('LOGIN', 'password'))

        log_in_button = self.browser.find_element(By.XPATH, '//*[@type="submit"]')
        log_in_button.click()

        # wait time
        time.sleep(self.config.getint('LOGIN', 'wait_time'))

        # validate success url
        if self.logger is not None:
            self.logger.debug("current_url: %s", self.browser.current_url)
            self.logger.debug("success_url: %s", self.config.get('LOGIN', 'success'))

        if self.browser.current_url == self.config.get('LOGIN', 'success'):
            print("Login Successful!")
            if self.logger is not None:
                self.logger.info("Login Successful!")
        else:
            print("Login Failed!")
            print("Current URL:", self.browser.current_url)
            if self.logger is not None:
                self.logger.info("Login Failed!")
                self.logger.info(f"Current URL: {self.browser.current_url}")
            # exit(1)


if __name__ == '__main__':
    sh = SeleniumHandler('main.cfg')
