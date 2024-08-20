import pytest
from .. import connect


@pytest.fixture
def db():
    db = connect(":memory:")

    yield db

    db.close()
