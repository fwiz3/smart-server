from fastapi import APIRouter

from v1.model.update_device_model import DeviceUpdate
from v1.routes.update.services.update_device_method import update_dev_method

router = APIRouter()

@router.patch("/devices/{device_id}")
async def update_device(device_id: str, payload: DeviceUpdate):
    res=update_dev_method(device_id, payload)
    return res
