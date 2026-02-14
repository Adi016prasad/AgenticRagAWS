from pydantic import Field, BaseModel

class CreateSession(BaseModel):
    userId: str