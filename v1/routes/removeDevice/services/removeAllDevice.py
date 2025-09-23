from fastapi import HTTPException

from data.db import devices_table


def remove_all_devices():
    if len(devices_table) == 0:
        raise HTTPException(
            status_code=404,
            detail="No devices to remove"
        )
    print(devices_table.name)
    devices_table.truncate()
    return {"message": "All devices removed successfully"}
