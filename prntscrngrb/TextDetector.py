from keras_ocr import tools
from keras_ocr.pipeline import Pipeline
from runnable import Runnable
from prntscrngrb import log, db, ScreenShot
from time import sleep


class TextDetector(Runnable):
    def __init__(self):
        Runnable.__init__(self)
        self.pipeline = Pipeline()

    def on_start(self):
        log.info("Starting TextDetector")

    def on_stop(self):
        log.info("Stopping TextDetector")

    def detect(self, item: ScreenShot):
        try:
            r = self.pipeline.recognize([tools.read(item.file_path)])
            setattr(item, "text_result", r)
            item.text_detected = True
            db.update(item)
        except Exception as e:
            log.warning(e)

    def work(self):
        for item in db.find({"text_detected": False}):
            self.detect(item)
        sleep(0.1)
