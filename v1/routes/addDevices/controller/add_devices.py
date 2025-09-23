from fastapi import APIRouter, HTTPException, Path, Body
from tinydb import Query

from data.db import devices_table
from v1.routes.addDevices.services.add_device_method import add_device
from utility.services.isIp import is_ip
from v1.model.device_config import Device

router = APIRouter()


# Get table references
@router.post(
    path="/{device_type}",
    description="Add a new device",
)
async def setup_devices(
        metadata: Device = Body(..., description="Metadata of the device to be added",
                                examples=["{\"name\": \"Bedroom Light\", \n \"ip\": \"192.168.1.18\"}"]),
        device_type: str = Path(..., description="Type of the device", examples=['light_auto', 'light_manual']),
):
    if metadata.ip is None or metadata.id is None or not is_ip(metadata.ip):
        raise HTTPException(
            status_code=400,
            detail="IP address and ID must be provided with valid IP format",
        )

    try:
        DeviceQuery = Query()

        # Check if device already exists
        existing_device = devices_table.get(
            (DeviceQuery.id == metadata.id) | (DeviceQuery.ip == metadata.ip)
        )

        if existing_device:
            raise HTTPException(
                status_code=400,
                detail="Device with this ID or IP already exists",
            )

        # Add the device (validation happens inside add_device)
        result = add_device(metadata, device_type)
        return {'detail': 'Device added', 'device': result}

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other exceptions
        print(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
