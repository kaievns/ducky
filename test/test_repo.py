from dataclasses import dataclass, asdict
from .. import Repository
from . import *


@dataclass
class User:
    id: int
    name: str
    password: str


class UserRepo(Repository[User]):
    table_query = """
        CREATE SEQUENCE seq_userid START 1;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_userid'),
            name VARCHAR NOT NULL,
            password VARCHAR NOT NULL
        );

        CREATE UNIQUE INDEX users_name ON users(name);
    """

    insert_query = """
        INSERT INTO users (name, password) VALUES (?, ?)
    """

    def row_to_record(self, row: tuple) -> User:
        (id, name, password) = row
        return User(id, name, password)

    def record_to_row(self, record: User) -> tuple:
        return (record.name, record.password)


def test_repository(db):
    repo = UserRepo()

    repo.save(User(None, "hi", "there"))

    users = repo.query("users").fetch()

    print(users)

    assert users == [
        User(1, "hi", "there")
    ]
