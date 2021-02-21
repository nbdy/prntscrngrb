from runnable import Runnable
from nsfw_detector import predict

from prntscrngrb import log, db, ScreenShot
from time import sleep


class NSFWDetector(Runnable):
    def __init__(self, model_path: str):
        Runnable.__init__(self)
        self.model = predict.load_model(model_path)

    def on_start(self):
        log.info("Starting NSFW detector")

    def on_stop(self):
        log.info("Stopping NSFW detector")

    def detect(self, item: ScreenShot):
        try:
            r = predict.classify(self.model, item.file_path)
            setattr(item, "nsfw_result", r)
            item.nsfw_detected = True
            db.update(item)
        except Exception as e:
            log.warning(e)

    def work(self):
        for item in db.find({"nsfw_detected": False}):
            self.detect(item)
        sleep(0.1)
