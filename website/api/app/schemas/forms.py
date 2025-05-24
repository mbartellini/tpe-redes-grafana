from pydantic import BaseModel, Field

# "..." means "not null" 


## USERS ##
class CreateUserForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=20)

    
class LoginForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=20)

## REVIEWS ##
#ge=0 means  greater than or equal to 0
class ReviewForm(BaseModel):
    userId: int = Field(..., ge=0)
    mediaId: int = Field(..., ge=0)
    content: str = Field(..., min_length=1, max_length=500)
