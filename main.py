from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import joinedload
from app.model import (
    Todo_Table,
    UserSchema,
    UserLoginSchema,
    Users,
    TodoSchema,
    Creating_table,
)
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JWTBearer
from app.database import Session

app = FastAPI()
Creating_table()


# 1 Get post for testing
@app.get("/", tags=["test"])
def test():
    return {"message": "Hello World"}


# 2 Get posts
@app.get("/post", tags=["posts"])
async def read_todos():
    with Session() as session:
        todos = session.query(Todo_Table).all()
    return todos


# 4 Post a blog post (handler for creating a post)
@app.post("/post", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(todo: TodoSchema):
    with Session() as session:
        todo = Todo_Table(task=todo.task, status=todo.status)
        session.add(todo)
        session.commit()

    return {"message": "Todo added to dataabse"}


# users = []


# 5 User Signup (Creating a new user)
# @app.post("/user/signup", tags=["user"])
# def user_signup(user: UserSchema):
#     with Session() as session:
#         user = Users(fullname=user.fullname, email=user.email, password=user.password)

#         session.add(user)
#         session.commit()

#     return signJWT(user.email)


@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema):
    with Session() as session:
        existing_user = session.query(Users).filter(Users.email == user.email).first()

        # If a user with the given email does not exist, create a new one
        if existing_user is None:
            new_user = Users(
                fullname=user.fullname, email=user.email, password=user.password
            )
            session.add(new_user)
            session.commit()
            return signJWT(new_user.email)
        else:
            return {"error": "A user with this email already exists."}


# def sign_user(user_added: UserSchema = Body(default=None)):
#     users.append(user_added.dict())
#     return signJWT(user_added.email)


# function check the user if exits
def check_user(data: UserLoginSchema):
    with Session() as session:
        user = (
            session.query(Users)
            .filter(Users.email == data.email, Users.password == data.password)
            .first()
        )
        if user:
            return True
    return False


# 6 User Login (Login user)
@app.post("/user/login", tags=["user"])
def login_user(user_login: UserLoginSchema = Body(default=None)):
    if check_user(user_login):
        return signJWT(user_login.email)
    else:
        return {"error": "Invalid User"}
