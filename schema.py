from pydantic import BaseModel


class PredictionRequest(BaseModel):
    nitrogen: int
    phosphorus: int
    potassium: int
    temperature: float
    humidity: float
    ph_level: float
    rainfall: float
