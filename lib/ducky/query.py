from typing import Generic, TypeVar
from .adapter import Adapter

T = TypeVar("T")


class Query(Generic[T]):
    adapter: Adapter
    fields = "*"
    source = "none"
    conditions: list[(str, tuple[any])]
    sort = None
    size = None

    def __init__(self, adapter: Adapter, converter: callable) -> None:
        self.adapter = adapter
        self.converter = converter
        self.conditions = []

    def select(self, fields: str):
        return self.clone(fields=fields)

    def table(self, name: str):
        return self.clone(source=name)

    def where(self, token: str, *args):
        conditions = self.conditions.copy()
        conditions.append((token, args))
        return self.clone(conditions=conditions)

    def limit(self, size: int):
        return self.clone(size=size)

    def order(self, name: str):
        return self.clone(sort=name)

    def fetch(self) -> list[T]:
        return [self.converter(r) for r in self.result()]

    def result(self) -> list[tuple]:
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
            query += f" LIMIT {self.size}"

        return self.adapter.read(query, params)

    def clone(self, **kwargs):
        query = Query(self.adapter, self.converter)
        query.fields = self.fields
        query.source = self.source
        query.conditions = self.conditions
        query.sort = self.sort
        query.size = self.size

        for key in kwargs:
            setattr(query, key, kwargs[key])

        return query
