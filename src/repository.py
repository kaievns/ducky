from typing import Generic, TypeVar
from .migration import Migration
from .adapter import Adapter
from .query import Query


T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self) -> None:
        Migration.run(self.table_query)
        self.adapter = Adapter()

    table_query: str
    insert_query: str

    def row_to_record(self, row: tuple[any]) -> T:
        pass

    def record_to_row(self, record: T) -> tuple[any]:
        pass

    def save(self, record: T):
        self.adapter.write(self.insert_query, self.record_to_row(record))

    def dump(self, records: list[T]):
        data = [self.record_to_row(r) for r in records]
        self.adapter.dump(self.insert_query, data)

    def query(self, table: str) -> Query[T]:
        return Query[T](self.adapter, self.row_to_record).table(table)
