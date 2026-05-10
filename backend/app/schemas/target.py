from pydantic import BaseModel, field_validator
import re

class TargetCreate(BaseModel):
    domain: str

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, v):
        pattern = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid domain format")
        return v.lower()


class TargetUpdate(BaseModel):
    domain: str