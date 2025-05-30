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
class ReviewForm(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
