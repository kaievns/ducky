import duckdb
from contextlib import closing


def batch(iterable, size=1):
    l = len(iterable)
    for ndx in range(0, l, size):
        yield iterable[ndx:min(ndx + size, l)]


class Adapter:
    connection: duckdb.DuckDBPyConnection

    @staticmethod
    def connect(db_name: str):
        Adapter.connection = duckdb.connect(db_name)

        return Adapter.connection

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
            for chunk in batch(data, 100):
                db.executemany(query, chunk)
                db.commit()
