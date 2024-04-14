from .adapter import Adapter
from .repository import Repository


def connect(db_name: str):
    return Adapter.connect(db_name)
