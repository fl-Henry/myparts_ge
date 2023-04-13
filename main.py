from time import sleep

from log_handler import LogHandler
from selenium_handler import SeleniumHandler
from scrape import script_process

if __name__ == '__main__':
    try:
        lh = LogHandler(name='log_handler_01', config_file='main.cfg')
        sh = SeleniumHandler('main.cfg', lh.logger)
        sh.login()
        script_process(sh)
        sleep(10)
    finally:
        sh.quit_browser()
