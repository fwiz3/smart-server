from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from v1.routes.getDevices.services.get_all_devices_method import get_all_devices
router = APIRouter()

@router.get(path='/get-all',description="show all the devices in the added list")
async def show_all():
    all_devices:list = get_all_devices()
    if all_devices:
        return JSONResponse(content=all_devices,status_code=200)
    else:
        raise HTTPException(
            status_code=404,
            detail="No data found"
        )