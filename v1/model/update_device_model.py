from pydantic import BaseModel
from typing import Optional

class StateUpdate(BaseModel):
    power: Optional[str]=None
    currentState: Optional[str] = None
    controlWith: Optional[str] = None
    scheduledAt: Optional[str] = None
    offset: Optional[int] = None

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    currentMode: Optional[str] = None
    state: Optional[StateUpdate] = None