from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from v1.routes.device.services.reload import reload
from v1.model.device_config import Device

router = APIRouter()
@router.post(path='/{deviceid}/reload-device',description="show all the devices in the added list")
async def reload_device(deviceid: str):
    device:Device =  reload(deviceid)
    if device:
        return JSONResponse(status_code=200, content=device)
    else:
        raise HTTPException(
            status_code=404,
            detail="No data found"
        )