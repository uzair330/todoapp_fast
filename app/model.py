from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "title": "First Post",
                "content": "This is the first post",
            }
        }


# User Schema
class UserSchema(BaseModel):
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john@example.com",
                "password": "XXXXXX",
            }
        }


# login schema
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "XXXXXX",
            }
        }
