from tinydb import TinyDB
from pathlib import Path
from tinydb.storages import JSONStorage
import json


class PrettyJSONStorage(JSONStorage):
    def write(self, data):
        self._handle.seek(0)
        # just make it human-readable
        serialized = json.dumps(data, indent=4, ensure_ascii=False)
        self._handle.write(serialized)
        self._handle.truncate()


DB_PATH = Path(__file__).parent / "main_database.json"


db = TinyDB(DB_PATH, storage=PrettyJSONStorage)

configs_table = db.table("configs")
devices_table = db.table("devices")

# config_table = db.table("configs")
# device_table = db.table("device")
