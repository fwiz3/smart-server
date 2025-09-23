from fastapi import HTTPException
from v1.model.device_config import Device
from tinydb import Query
from data.db import devices_table, configs_table


def add_device(device: Device, device_type: str):
    DeviceQuery = Query()

    # Debug: Print what we're looking for
    print(f"🔍 Looking for device_type: '{device_type}'")

    # Debug: Print all configs to see what's in the table
    all_configs = configs_table.all()
    print("📋 All configs in table:")
    for config in all_configs:
        print(f"  - {config}")

    # ✅ Query with correct field name
    device_config = configs_table.get(DeviceQuery.device_type == device_type)

    print(f"✅ Found config: {device_config}")

    if not device_config:
        raise HTTPException(
            status_code=404,
            detail=f"No config found for device_type '{device_type}'",
        )

    new_device = {
        **device.model_dump(mode='json'),
        "device_type": device_type,
    }
    devices_table.insert(new_device)
    print("✅ Device added successfully")
    return {**device.model_dump(mode='json'), }