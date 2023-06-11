from pydantic import BaseModel

class UserDeviceTokenDTO(BaseModel):
    """User Data Transfer Object for Sign Up """
    device_token: str