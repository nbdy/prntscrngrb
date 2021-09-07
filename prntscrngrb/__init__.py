import datetime
import uuid

from loguru import logger as log
from hashlib import sha1
from pony import orm


db = orm.Database()


def hash_str(data: str):
    return sha1(data.encode('utf-8')).hexdigest()


'''
@dataclass
class Screenshot:
    uuid: str
    created: datetime.datetime
    file_path: str
    url: str
    name: str
    nsfw_detected: bool = False
    nsfw_scanned: bool = False
    text_detected: bool = False
    text_scanned: bool = False
    text_result: str = ""
'''


class Screenshot(db.Entity):
    uuid = orm.PrimaryKey(str)
    created = orm.Required(datetime.datetime)
    file_path = orm.Required(str)
    url = orm.Required(str)
    name = orm.Required(str)
    nsfw_detected = orm.Optional(bool)
    nsfw_scanned = orm.Optional(bool)
    text_detected = orm.Optional(bool)
    text_scanned = orm.Optional(bool)
    text_result = orm.Optional(str)


@orm.db_session
def insert_screenshot(name: str, file_path: str, url: str):
    Screenshot(
        uuid=str(uuid.uuid4()),
        created=datetime.datetime.now(),
        file_path=file_path,
        url=url,
        name=name,
        nsfw_detected=False,
        nsfw_scanned=False,
        text_detected=False,
        text_scanned=False,
        text_result=""
    )


@orm.db_session
def db_has_screenshot_with_name(name: str) -> bool:
    return orm.count(s for s in Screenshot if s.name == name) > 0


__all__ = ['log', 'Screenshot', 'db', 'db_has_screenshot_with_name', 'insert_screenshot']
