from data.db import devices_table, configs_table

def get_all_devices():
    config_map = {c["device_type"]: dict(c) for c in configs_table.all()}

    # Fetch devices and inline their config by device_type
    expanded = []
    for doc in devices_table.all():
        d = dict(doc)  # cast TinyDB Document -> plain dict
        dt = d.get("device_type")
        config = config_map.get(dt)
        if not config:
            # If a device points to a missing config, decide your policy:
            # Here we keep the device and set config=None (or raise if you prefer)
            config = None
        d.pop("device_type",None)
        expanded.append({**d, "config": config})
    return expanded


    