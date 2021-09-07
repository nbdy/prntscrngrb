from time import sleep
from runnable import Runnable
from nude import is_nude
from pony.orm import db_session, select

from prntscrngrb import log, Screenshot


class NSFWDetector(Runnable):
    def on_start(self):
        log.info("Starting NSFW detector")

    def on_stop(self):
        log.info("Stopping NSFW detector")

    @staticmethod
    def detect(item: Screenshot):
        try:
            item.nsfw_detected = is_nude(item.file_path)
            if item.nsfw_detected:
                log.info("Detected nudity: '{}'", item.file_path)
        except Exception as e:
            item.nsfw_detected = False
            log.warning(e)
        item.nsfw_scanned = True

    @db_session
    def work(self):
        screenshots = select(s for s in Screenshot if not s.nsfw_scanned)
        for s in screenshots:
            self.detect(s)
        sleep(0.1)
