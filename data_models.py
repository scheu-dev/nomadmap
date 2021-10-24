from pydantic import BaseModel
from datetime import datetime
from typing import Tuple

class Step(BaseModel):
    title: str = None
    long: float
    lat: float
    date_time: datetime
    description: str = None




