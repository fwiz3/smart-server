from fastapi import APIRouter, Path

from services.devices_service import remove_all_devices
from services.devices_service import remove_device_with_id

router = APIRouter()


@router.get(
    path="/removeAll",
    description="api to clean device list"
)
async def remove_all():
    return remove_all_devices()


@router.post(
    path="/{deviceid}/remove",
    description="to remove particular device from the device list"
)
async def remove_device(deviceid: str = Path(..., description="Device ID (e.g. lala1)")):
    return remove_device_with_id(deviceid)
