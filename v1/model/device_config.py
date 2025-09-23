import uuid
from pydantic import BaseModel, Field
from v1.model.state import DeviceState
class Device(BaseModel):
    name:str = Field(...,description="Name of the device",examples=['Bedroom Light'],title="Name of the device")
    id: str = Field(description="Unique identifier for the added device",default_factory=lambda: str(uuid.uuid4()),title="Unique identifier of the added device")
    ip: str = Field(..., description="IP address of the added device",title="IP address of the added device")
    port: int = Field(description="Port number of the added device", default=None)
    currentMode: str = Field(description="Current mode of the added device",default='manual',title="Current mode of the added device")
    state: DeviceState = Field(description="Current state of the device (e.g., 'on', 'off')",default_factory=DeviceState)