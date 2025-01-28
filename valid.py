from pydantic import BaseModel, Field

class NewCat(BaseModel):
    nickname: str = Field(max_length=20)
    color: str = Field(max_length=20)
    age: int = Field(gt=0, le=20)

class UserLoginSchema(BaseModel):
    username: str
    password: str