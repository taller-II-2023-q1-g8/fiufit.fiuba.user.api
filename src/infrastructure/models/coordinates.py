from pydantic import BaseModel, validator

class Coordinates(BaseModel):
    longitude: float
    latitude: float

    @validator("longitude")
    def longitude_between_range(cls, longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError("longitude must be between -180 and 180")
        return float(longitude)

    @validator("latitude")
    def latitude_between_range(cls, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude must be between -90 and 90")
        return float(latitude)

