from fastapi import HTTPException, Path
from tinydb import Query

from data.db import devices_table


def remove_device_with_id(deviceid: str = Path(..., description="Device ID (e.g. lala1)")):
    device_query = Query()
    removed = devices_table.remove(device_query.id == deviceid)
    if not removed:
        raise HTTPException(
            status_code=404,
            detail=f"No device found with id '{deviceid}'"
        )
    return {"message": f"Device '{deviceid}' removed successfully"}
