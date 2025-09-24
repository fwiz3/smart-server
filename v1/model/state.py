from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional


class DeviceState(BaseModel):
    currentState: str = Field(
        description="Current state of the device (e.g., 'on', 'off')", default="off"
    )
    updatedAt: str = Field(
        description="Last update at",
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    power:str = Field(description="Power state", default="off")
    controlWith: str = Field(description="Control with Suntime/Scheduled time", default=None)
    scheduledAt: Optional[time] = Field(description="Last scheduled at", examples=["14:00"],title="Scheduled time",default=None)
    offset: str = Field(description="Offset of the device", default=None)
