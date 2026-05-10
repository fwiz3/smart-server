from datetime import datetime

from fastapi import HTTPException, Path
from v1.model.device_config import Device
from tinydb import Query
from data.db import devices_table, configs_table
from v1.model.update_device_model import DeviceUpdate


# ...........................................................................................................
#ADD DEVICES TO THE SYSTEM

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

#..................................................................................................................
# RELOAD A DEVICE ONLY
# or GET A PARTICULAR DEVICE

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

#.................................................................................................................
# GET ALL THE DEVICES ALL AT ONCE

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

#..................................................................................................................
# REMOVE ALL THE DEVICES REGISTERED

def remove_all_devices():
    if len(devices_table) == 0:
        raise HTTPException(
            status_code=404,
            detail="No devices to remove"
        )
    print(devices_table.name)
    devices_table.truncate()
    return {"message": "All devices removed successfully"}

#..................................................................................................................
# REMOVE A PARTICULAR DEVICE

def remove_device_with_id(deviceid: str = Path(..., description="Device ID (e.g. lala1)")):
    device_query = Query()
    removed = devices_table.remove(device_query.id == deviceid)
    if not removed:
        raise HTTPException(
            status_code=404,
            detail=f"No device found with id '{deviceid}'"
        )
    return {"message": f"Device '{deviceid}' removed successfully"}

#..................................................................................................................
# UPDATE A PARTICULAR DEVICE DETAIL TO DATABASE

def update_dev_method(device_id: str, payload: DeviceUpdate):
    device = devices_table.get(Query().id == device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Update name
    if payload.name:
        device["name"] = payload.name

    # Update mode
    if payload.currentMode:
        device["currentMode"] = payload.currentMode

    # Update state
    if payload.state:
        if payload.state.currentState:
            device["state"]["currentState"] = payload.state.currentState
        if payload.state.controlWith:
            device["state"]["controlWith"] = payload.state.controlWith
        if payload.state.power:
            device["state"]["power"] = payload.state.power
        device["state"]["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Contact IoT device (only if state change)
        # requests.post(
        #     f"http://{device['ip']}/relay",
        #     headers={"X-Auth-Token": "your_secret"},
        #     json={"state": payload.state.currentState}
        # )

    devices_table.update(device, Query().id == device_id)
    device_copy = {k: v for k, v in device.items() if k != "device_type"}

    # find config by matching type
    config = next(
        (cfg for cfg in configs_table.all() if cfg["device_type"] == device["device_type"]),
        {}
    )
    return {**device_copy, "config": config}
