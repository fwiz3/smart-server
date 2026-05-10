from fastapi import APIRouter

from v1.model.update_device_model import DeviceUpdate
from services.devices_service import update_dev_method

router = APIRouter()

@router.patch("/devices/{device_id}")
async def update_device(device_id: str, payload: DeviceUpdate):
    res=update_dev_method(device_id, payload)
    return res
