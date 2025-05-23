from pydantic import BaseModel

## USERS ##
class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True