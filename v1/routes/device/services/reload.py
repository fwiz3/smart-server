from data.db import devices_table, configs_table
from tinydb import Query

def reload(dev_id: str):
    """Get device by key, attach its matching config, remove duplicate device_type."""
    print(dev_id)
    device_query = Query()
    device = devices_table.get(device_query.id == dev_id)
    if not device:
        return None

    # copy without device_type
    device_copy = {k: v for k, v in device.items() if k != "device_type"}

    # find config by matching type
    config = next(
        (cfg for cfg in configs_table.all() if cfg["device_type"] == device["device_type"]),
        {}
    )

    return {**device_copy, "config": config}
