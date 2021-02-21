from loguru import logger as log
from podb import DB, DBEntry
from hashlib import sha1

db = DB("prntscrn")


def hash_str(data: str):
    return sha1(data.encode('utf-8')).hexdigest()


class ScreenShot(DBEntry):
    file_path: str
    url: str
    nsfw_detected: bool
    text_detected: bool

    def __init__(self, file_path: str, url: str, name: str):
        DBEntry.__init__(self, **{
            "uuid": hash_str(name),
            "file_path": file_path,
            "url": url,
            "name": name,
            "nsfw_detected": False,
            "text_detected": False
        })


from prntscrngrb.ImageFetcher import ImageFetcher
from prntscrngrb.NSFWDetector import NSFWDetector
from prntscrngrb.TextDetector import TextDetector


__all__ = ['ImageFetcher', 'log', 'db', 'NSFWDetector', 'TextDetector', 'ScreenShot']
