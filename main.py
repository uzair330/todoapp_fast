from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JWTBearer

posts = [
    {"id": 1, "title": "First Post", "content": "This is my first post"},
    {"id": 2, "title": "Second Post", "content": "This is my second post"},
    {"id": 3, "title": "Third Post", "content": "This is my third post"},
]

users = []
app = FastAPI()


# 1 Get post for testing
@app.get("/", tags=["test"])
def test():
    return {"message": "Hello World"}


# 2 Get posts
@app.get("/post", tags=["posts"])
def getPost():
    return {"data": posts}


# 3 Get post by id
@app.get("/post/{id}", tags=["posts"])
def getPostById(id: int):
    if id > len(posts):
        return {"message": f"Post with id={id} not found"}
    else:
        return {"data": "Invalid Id"}
    for post in posts:
        if post["id"] == id:
            return {"data": post}


# 4 Post a blog post (handler for creating a post)
@app.post("/post", dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post_added: PostSchema):
    post_added.id = len(posts) + 1
    posts.append(post_added.dict())
    return {"info": "post added"}


# 5 User Sign (Creating a new user)
@app.post("/user/signup", tags=["user"])
def sign_user(user_added: UserSchema = Body(default=None)):
    users.append(user_added.dict())
    return signJWT(user_added.email)


# function check the user if exits
def check_user(data: UserLoginSchema):
    for user in users:
        if user["email"] == data.email and user["password"] == data.password:
            return True
    return False


# 6 User Login (Login user)
@app.post("/user/login", tags=["user"])
def login_user(user_login: UserLoginSchema = Body(default=None)):
    if check_user(user_login):
        return signJWT(user_login.email)
    else:
        return {"error": "Invalid User"}
