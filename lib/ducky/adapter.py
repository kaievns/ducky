import duckdb
from contextlib import closing


class Adapter:
    connection: duckdb.DuckDBPyConnection

    @classmethod
    def connect(cls, db_name: str):
        cls.connection = duckdb.connect(db_name)

        return cls.connection

    def read(self, query: str, params: list | tuple | dict) -> list[any]:
        with closing(self.connection.cursor()) as db:
            result = db.execute(query, params).fetchall()

        return result

    def write(self, query: str, data: list | tuple | dict):
        with closing(self.connection.cursor()) as db:
            db.execute(query, data)
            db.commit()

    def dump(self, query: str, data: list[dict]):
        with closing(self.connection.cursor()) as db:
            db.executemany(query, data)
            db.commit()
