from requests import get, exceptions
from bs4 import BeautifulSoup
from random import choices, randint
from string import ascii_lowercase, digits
from os.path import isdir, join
from os import makedirs
from shutil import copyfileobj
from runnable import Runnable
from time import sleep
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from prntscrngrb import log, db_has_screenshot_with_name, insert_screenshot


class ImageFetcher(Runnable):
    base_url = "https://prnt.sc/"
    suffix_charset = ascii_lowercase + digits

    def __init__(self, suffix_length: int, save_directory: str):
        Runnable.__init__(self)
        self.suffix_length = suffix_length
        self.save_directory = save_directory

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

        self.user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                            limit=100)

    def on_start(self):
        log.info("Starting image fetcher")

    def on_stop(self):
        log.info("Stopping image fetcher")

    def generate_suffix(self):
        return ''.join(choices(self.suffix_charset, k=self.suffix_length))

    def is_screenshot(self, url):
        log.debug("Checking: {}", url)
        try:
            rsp = get(url, headers={
                'User-Agent': self.user_agent_rotator.get_random_user_agent()
            })
            soup = BeautifulSoup(rsp.content, "lxml")
            img = soup.find("img", {"id": "screenshot-image"})
            if img and img.has_attr("src"):
                return img["src"]
        except exceptions.ConnectionError as e:
            log.warning(e)
            pass
        return None

    def save_img(self, url, name, directory):
        if not isdir(directory):
            makedirs(directory)
        try:
            rsp = get(url, stream=True, headers={
                'User-Agent': self.user_agent_rotator.get_random_user_agent()
            })
            file_path = join(directory, name + '.png')
            with open(file_path, 'wb') as o:
                copyfileobj(rsp.raw, o)
            del rsp
            insert_screenshot(name, file_path, url)
            log.info("Saved image {}", file_path)
        except exceptions.ConnectionError as e:
            log.warning(e)
        except exceptions.InvalidURL as e:
            log.warning(e)

    def work(self):
        n = self.generate_suffix()
        if db_has_screenshot_with_name(n):
            return
        img_url = self.is_screenshot(self.base_url + n)
        if img_url:
            if not img_url.startswith("https") or not img_url.startswith("http"):
                img_url = "https:" + img_url
            self.save_img(img_url, n, self.save_directory)
        sleep(randint(1, 4))
