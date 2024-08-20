# Ducky

A super simple data-mapper/repository for [duck.db](https://duckdb.org/). It has
DB <-> DAO mapping both ways, a simple query engine. And a simple migrations
util. And it also supports batching for large data dumps

```py
from dataclasses import dataclass, asdict
from ducky import Repository


@dataclass
class User:
    id: int
    name: str
    age: int


class UserRepo(Repository[User]):
    table_query = """
        CREATE SEQUENCE seq_userid START 1;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_userid'),
            name VARCHAR NOT NULL,
            age INTEGER
        );

        CREATE UNIQUE INDEX users_name ON users(name);
    """

    insert_query = """
        INSERT INTO users (name, age) VALUES (?, ?)
    """

    def row_to_record(self, row: tuple) -> User:
        (id, name, age) = row
        return User(id, name, age)

    def record_to_row(self, record: User) -> tuple:
        return (record.name, record.age)

repo = UserRepo()

repo.save(User(None, "hi", 123))

users = repo.query("users").fetch()

assert users == [
    User(1, "hi", 123)
]
```

## Copyright & License

All code in this repository is released under the terms of the MIT license

Copyright (C) 2024 Kai Evans
