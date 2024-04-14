from typing import Generic, TypeVar
from .adapter import Adapter

T = TypeVar("T")


class Query(Generic[T]):
    adapter: Adapter
    fields = "*"
    source = "none"
    conditions: list[(str, tuple[any])] = []
    sort = None
    size = None

    def __init__(self, adapter: Adapter, converter: callable) -> None:
        self.adapter = adapter
        self.converter = converter

    def select(self, fields: str):
        self.fields = fields
        return self

    def table(self, name: str):
        self.source = name
        return self

    def where(self, token: str, *args):
        self.conditions.append((token, args))
        return self

    def limit(self, size: int):
        self.size = size
        return self

    def order(self, name: str):
        self.sort = name
        return self

    def fetch(self) -> list[T]:
        query = f"SELECT {self.fields} FROM {self.source}"

        params = []
        wheres = []
        for (where, args) in self.conditions:
            wheres.append(where)
            params += args

        if len(wheres) > 0:
            query += " WHERE " + " AND ".join(wheres)

        if self.sort != None:
            query += f" ORDER BY {self.sort}"

        if self.size != None:
            query += f" LIMIT {self.limit}"

        result = self.adapter.read(query, params)

        return [self.converter(r) for r in result]
