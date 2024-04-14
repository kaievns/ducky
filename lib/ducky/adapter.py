import duckdb
from threading import Thread


class Adapter:
    connection: duckdb.DuckDBPyConnection

    @staticmethod
    def connect(db_name: str):
        Adapter.connection = duckdb.connect(db_name)

        return Adapter.connection

    def read(self, query: str, params: list | tuple | dict) -> list[any]:
        db = self.connection.cursor()
        result = db.execute(query, params).fetchall()
        db.close()

        return result

    def write(self, query: str, data: list | tuple | dict):
        db = self.connection.cursor()
        db.execute(query, data)
        db.close()

    def dump(self, query: str, data: list[dict]):
        db = self.connection.cursor()
        db.executemany(query, data)
        db.close()
