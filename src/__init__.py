from .adapter import Adapter
from .migration import Migration
from .repository import Repository


def connect(db_name: str):
    Migration.reset()
    return Adapter.connect(db_name)
