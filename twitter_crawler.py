import requests
import re
import time
import json
import logging
import pathlib as pl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from fnmatch import fnmatch

# Set the outputs of log and terminal
fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler("./twitter_crawler.log", encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)

# Set the base url
base_url = 'https://twitter.com/'

class TwitterCrawler():
    def __init__(self):
        """
        Initialize the crawler settings

        :return:
        """
        # Initialize the settings from json file
        with open("twitter_settings.json", "r", encoding="utf8") as f:
            self.settings = json.load(f)    # Load settings
        logger.info("Json settings loaded")
        
        # Initialize the settings of chrome driver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--proxy-server=" + self.settings["proxy_server"])
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
        logger.info("Chrome driver initialized")

        # All settings loaded
        logger.info("All Settings ready for work")

    def login(self):
        """
        Login to twitter

        :return:
        """
        # Get the login url
        d = self.driver
        login_url = base_url + "i/flow/login"
        d.get(login_url)

        # Get the username form
        wdw(d, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
        usrn_form = d.find_element(By.TAG_NAME, 'input')
        usrn_form.send_keys(self.settings["login_info"]["username"])
        btn = d.find_elements(By.XPATH, "//div[@role='button']")[-2]
        btn.click()

        # Get the password form
        wdw(d, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
        pswd_form = d.find_elements(By.TAG_NAME, 'input')[-1]
        pswd_form.send_keys(self.settings["login_info"]["password"])
        btn = d.find_elements(By.XPATH, "//div[@role='button']")[-1]
        btn.click()

        # Wait for the login success
        wdw(d, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'header')))
        logger.info("Successfully login")

    def sleep(self, sleep_key: str, delta=0):
        """
        Execute sleeping for a time configured in the settings

        :param sleep_key: the sleep time label
        :param delta: added to the sleep time
        :return:
        """
        _t = self.settings["config"][sleep_key] + delta
        logger.info(f"Sleep {_t} second(s)")
        time.sleep(_t)

    # Get all the image downloading links of the user
    def get_users_images(self, username: str) -> list:
        """
        Get all the image downloading links of the user
        
        :param username: username of the user
        :return:
        """
        start_url = base_url + username + '/media'
        logger.info(f"Driver get url: {start_url}")
        self.driver.get(start_url)

        # Collect the image links
        img_list = []
        filtered_img_list = []

        # Scroll down to the bottom of the page
        count_scroll = 0
        for _ in range(self.settings["user_media_info"][username]):
            # Get the image links
            img_list += [img.get_attribute('src') for img in self.driver.find_elements(By.XPATH, '//img')]
            logger.info(f"[@{username}] Get images at scroll {count_scroll + 1}")

            # scroll down
            js = f"window.scrollTo(0, document.body.clientHeight * {count_scroll + 1}, behavior='smooth')"
            self.driver.execute_script(js)
            count_scroll += 1
            self.sleep("interval_between_scroll")

        # Forecast the arrival to the bottom
        logger.info(f"[@{username}] Reach the bottom of the page")

        # Filter the image links
        img_list = list(set(img_list))
        def is_img_needed(img_url: str) -> bool:
            return fnmatch(img_url, "*format=jpg&name=*")
        for img_url in img_list[:]:
            if is_img_needed(img_url):
                # Replace the image url with the real url
                img_url = img_url.replace("format=jpg", "format=png")
                img_url = re.sub(r"(name=\d+x\d+)|(name=\w+)", "name=4096x4096", img_url)
                filtered_img_list.append(img_url)
        return filtered_img_list

    def download(self, url: str, dirpath: str):
        """
        Download the image by url

        :param url: url of the image
        :return:
        """
        resp = requests.get(url, headers=self.settings["headers"], proxies=self.settings["proxies"])

        with open(f"{dirpath}", "wb") as f:
            f.write(resp.content)
        logger.info(f"Successfully download {url.split('/')[-1]}")

    def download_users_all_images(self, username: str):
        """
        Download all works by username

        :param username: username
        :return:
        """
        # Save all download links of images of the user
        links = self.get_users_images(username)
        logger.info(f"[@{username}] Get {len(links)} images")

        # Make directory
        dir = pl.Path() / f"twitter_images/{username}"
        if not dir.exists():
            dir.mkdir(parents=True)
            logger.info(f"Make directory {dir}")
        else:
            logger.info(f"Directory {dir} already exists")

        # Download all works by the links
        for idx, link in enumerate(links):
            try:
                self.download(link, f"{dir}/{idx + 1}.png")
                logger.info(f"[@{username}] Download {idx + 1}/{len(links)}")
            except Exception as e:
                logger.error(f"Error: {e}")
                continue

if __name__ == '__main__':
    t = TwitterCrawler()
    begin_time = time.time()    # Start time
    t.login()
    for username in t.settings["user_media_info"].keys():
        t.download_users_all_images(username)
        logger.info(f"Username: {username} finish downloading")
        t.sleep("interval_between_user")
    t.driver.close()
    end_time = time.time()      # End time
    logger.info("Finish downloading all users")

    # Print the time spent
    minutes = int((end_time - begin_time) / 60)
    seconds = int((end_time - begin_time) % 60)
    logger.info(f"Time spent: {minutes} (m) {seconds} (s)")
