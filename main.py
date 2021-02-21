from argparse import ArgumentParser
from datetime import datetime
from os.path import abspath, join, dirname, isfile
from os import listdir
from tqdm import tqdm

from prntscrngrb import ImageFetcher, NSFWDetector, TextDetector, log, db, ScreenShot
# todo if tor gets blocked by prnt.sc / cloudflare
# todo use torpy for multithreading


def index_directory(nsfw: NSFWDetector, text: TextDetector, directory: str):
    log.info("Indexing {}", directory)
    for fp in tqdm(listdir(directory)):
        p = join(directory, fp)
        if isfile(p) and fp.endswith(".png"):
            n = fp.split(".")[0]
            log.info("Checking if {} exists in the database", n)
            if not db.contains({"name": n}):
                log.info("{} does not exist", n)
                ss = ScreenShot(p, "", n)
                nsfw.detect(ss)
                text.detect(ss)
            else:
                log.info("{} exists")
    log.info("Indexing finished")


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("-l", "--languages", nargs='+', default=['en', 'de'], help="TextDetector languages")
    ap.add_argument("-d", "--directory", default="crawled", help="Where to put them images")
    ap.add_argument("-sl", "--suffix_length", default=6, help="URL suffix length")
    ap.add_argument("-nmp", "--nsfw-model-path", help="Where is the nsfw model",
                    default=join(abspath(dirname(__file__)), 'prntscrngrb', 'nsfw_nn', 'saved_model.h5'))
    ap.add_argument("-id", "--index-directory", help="Index before actually running.", action="store_true")
    ap.add_argument("-co", "--crawl-only", help="Only download images", action="store_true")
    a = ap.parse_args()

    img_fetcher = ImageFetcher(a.suffix_length, a.directory)
    if not a.crawl_only:
        text_detect = TextDetector()
        nsfw_detect = NSFWDetector(a.nsfw_model_path)

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
