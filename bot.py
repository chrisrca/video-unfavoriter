from selenium.webdriver.common.by import By

from tiktok_uploader.browsers import get_browser
from tiktok_uploader.auth import AuthBackend
from tiktok_uploader import config, logger
from tiktok_uploader.utils import bold, green, red
from tiktok_uploader.proxy_auth_extension.proxy_auth_extension import proxy_is_working

def open(auth: AuthBackend = None, proxy: dict = None, browser='chrome', browser_agent=None, on_complete=None, headless=False, num_retires : int = 1, *args, **kwargs):
    if not browser_agent: 
        logger.debug('Create a %s browser instance %s', browser,
                    'in headless mode' if headless else '')
        driver = get_browser(name=browser, headless=headless, proxy=proxy, *args, **kwargs)
    else:
        logger.debug('Using user-defined browser agent')
        driver = browser_agent
    if proxy:
        if proxy_is_working(driver, proxy['host']):
            logger.debug(green('Proxy is working'))
        else:
            logger.error('Proxy is not working')
            driver.quit()
            raise Exception('Proxy is not working')
    driver = auth.authenticate_agent(driver)

    def run():
        try:
            button = driver.find_element('css selector', 'div[aria-label="Open settings menu"]')
            button.click()

            button = driver.find_element(By.XPATH, '//span[text()="View profile"]')
            button.click()

            button = driver.find_element(By.XPATH, '//span[text()="Favorites"]')
            button.click()

            button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Watch in full screen"]')
            button.click()

        except:
            pass

        while(True):
            try:
                button = driver.find_element(By.CSS_SELECTOR, 'span[data-e2e="undefined-icon"]')
                button.click()

                next_video_button = driver.find_element('css selector', 'button[aria-label="Go to next video"]')
                next_video_button.click()
            except:
                pass    

    driver.get(config['paths']['main'])
    run()

auth = AuthBackend(cookies='cookies.txt')
while(True):    
    open(auth=auth)