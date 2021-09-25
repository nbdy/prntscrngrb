from keras_ocr import tools
from keras_ocr.pipeline import Pipeline
from runnable import Runnable
from prntscrngrb import log, Screenshot
from pony.orm import select, db_session
from time import sleep


class TextDetector(Runnable):
    def __init__(self):
        Runnable.__init__(self)
        self.pipeline = Pipeline()

    def on_start(self):
        log.info("Starting TextDetector")

    def on_stop(self):
        log.info("Stopping TextDetector")

    @db_session
    def detect(self, item: Screenshot):
        try:
            text = ""
            recognized_text = self.pipeline.recognize([tools.read(item.file_path)])
            for text_items in recognized_text:
                for text_item in text_items:
                    text += text_item[0] + " "
            log.info("Extracted text: '{}'", text)
            item.text_result = text
            item.text_detected = True
        except Exception as e:
            item.text_detected = False
            log.warning(e)

        item.text_scanned = True

    @db_session
    def work(self):
        for s in select(s for s in Screenshot if not s.text_scanned):
            self.detect(s)
        sleep(0.1)
