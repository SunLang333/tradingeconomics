# filepath: backend/app/models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GDPData(BaseModel):
    date: datetime
    value: float
    growth_rate: Optional[float] = None

class GDPResponse(BaseModel):
    country: str
    data: List[GDPData]
    mean_gdp: float
    growth_rate: float
    volatility: float
    regression_slope: float
    r_squared: float
    p_value: float
    predicted_values: List[float]