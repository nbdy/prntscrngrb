from argparse import ArgumentParser
from os.path import join, isfile
from os import listdir
from tqdm import tqdm

from prntscrngrb import log, Screenshot, db
from prntscrngrb.ImageFetcher import ImageFetcher
from prntscrngrb.TextDetector import TextDetector
from prntscrngrb.NSFWDetector import NSFWDetector

# todo if tor gets blocked by prnt.sc / cloudflare
# todo use torpy for multithreading


def index_directory(nsfw: NSFWDetector, text: TextDetector, directory: str):
    log.info("Indexing {}", directory)
    for fp in tqdm(listdir(directory)):
        p = join(directory, fp)
        if isfile(p) and fp.endswith(".png"):
            n = fp.split(".")[0]
            log.info("Checking if {} exists in the database", n)
            if not Screenshot.select().count().where(Screenshot.name == n) > 0:
                log.info("{} does not exist", n)
                ss = Screenshot(p, "", n)
                nsfw.detect(ss)
                text.detect(ss)
            else:
                log.info("{} exists")
    log.info("Indexing finished")


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("-l", "--languages", nargs='+', default=['en', 'de'], help="TextDetector languages")
    ap.add_argument("-d", "--directory", default="crawled", help="Where to put them images")
    ap.add_argument("-sl", "--suffix_length", default=10, help="URL suffix length")
    ap.add_argument("-id", "--index-directory", help="Index before actually running.", action="store_true")
    ap.add_argument("-co", "--crawl-only", help="Only download images", action="store_true")
    ap.add_argument("-db", "--database", help="Database name", default="prntscrn.db")
    a = ap.parse_args()

    db.bind(provider="sqlite", filename=a.database, create_db=True)
    db.generate_mapping(create_tables=True)

    text_detect = TextDetector()
    nsfw_detect = NSFWDetector()

    img_fetcher = ImageFetcher(a.suffix_length, a.directory)
    if not a.crawl_only:
        if a.index_directory:
            index_directory(nsfw_detect, text_detect, a.directory)
            exit()

    try:
        log.info("Starting all threads")
        img_fetcher.start()
        if not a.crawl_only:
            text_detect.start()
            nsfw_detect.start()
    except KeyboardInterrupt:
        log.info("Stopping all threads")
        img_fetcher.stop()
        if not a.crawl_only:
            text_detect.stop()
            nsfw_detect.stop()
