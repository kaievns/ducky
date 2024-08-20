from .adapter import Adapter


class Migration:
    inst = None
    cache = {}

    @staticmethod
    def reset():
        Migration.inst = None
        Migration.cache = {}

    @staticmethod
    def run(script: str):
        if Migration.inst == None:
            Migration.inst = Migration()

        if script not in Migration.cache:
            Migration.cache[script] = True
            Migration.inst.check(script)

    def __init__(self) -> None:
        self.adapter = Adapter()
        self.adapter.write("""
            CREATE TABLE IF NOT EXISTS _migrations (
                script VARCHAR NOT NULL
            );
        """, None)

    def check(self, script: str):
        recs = self.adapter.read(
            "SELECT * FROM _migrations WHERE script = ? LIMIT 1", [script])

        if len(recs) == 0:
            self.adapter.write(script, [])
            self.adapter.write("INSERT INTO _migrations VALUES (?)", [script])
