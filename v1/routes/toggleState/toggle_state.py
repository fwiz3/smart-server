from fastapi import APIRouter,Header
from fastapi.responses import JSONResponse
from aiomqtt import Client
from data.db import devices_table
from tinydb import  Query
from datetime import datetime

router = APIRouter()

MQTT_BROKER = "0.0.0.0"  # or your broker IP
MQTT_PORT = 1883
MQTT_TOPIC = "home/light/relay1/set"
MQTT_STATE_TOPIC = "home/light/relay1/state"

async def publish_mqtt(state: str):
    async with Client(MQTT_BROKER, MQTT_PORT) as client:
        await client.publish(MQTT_TOPIC, state.encode())


@router.post(
    "/device/{device_id}/state", description="Set device state to 'on' or 'off'"
)
async def set_device_state(device_id: str, cmd: str=Header(..., description="Command to set the device state ('on' or 'off')", examples=['on','off'])):
    try:
        if cmd not in ["on", "off"]:
            return JSONResponse(content={"error": "Invalid command"}, status_code=400)

        device_query = Query()
        device = devices_table.get(device_query.id == device_id)
        if not device:
            return JSONResponse(content={"error": "Device not found"}, status_code=404)

        # Publish the state change to MQTT
        try:
            await publish_mqtt(cmd)
        except Exception as e:
            return JSONResponse(content={"error": f"MQTT publish failed: {str(e)}"}, status_code=500)

        # Update the device state in the database
        devices_table.update(
            {"state": {"currentState": cmd, "updatedAt":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}},
            device_query.id == device_id,
        )

        return JSONResponse(
            content={"message": f"Device '{device_id}' state set to '{cmd}'"},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
