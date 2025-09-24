from datetime import datetime

from fastapi import HTTPException
from tinydb import Query

from data.db import devices_table
from v1.model.update_device_model import DeviceUpdate


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
        device["state"]["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Contact IoT device (only if state change)
        # requests.post(
        #     f"http://{device['ip']}/relay",
        #     headers={"X-Auth-Token": "your_secret"},
        #     json={"state": payload.state.currentState}
        # )

    devices_table.update(device, Query().id == device_id)
    return {"message": "Device updated successfully"}
