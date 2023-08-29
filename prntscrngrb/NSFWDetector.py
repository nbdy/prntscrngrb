from time import sleep
from runnable import Runnable
from nudenetupdated import NudeDetector
from json import dumps
from pony.orm import db_session, select

from prntscrngrb import log, Screenshot


class NSFWDetector(Runnable):
    detector = NudeDetector()

    def on_start(self):
        log.info("Starting NSFW detector")

    def on_stop(self):
        log.info("Stopping NSFW detector")

    @db_session
    def detect(self, item: Screenshot):
        try:
            r = self.detector.detect(item.file_path, mode='fast')
            item.nsfw_detected = len(r) > 0
            if item.nsfw_detected:
                log.info("Detected human features: '{}'", item.file_path)
                item.nsfw_result = dumps(r)
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
