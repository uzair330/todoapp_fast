# This file is responsible for signing, encoding, decoding, and returning JWTs.
import time
import jwt
from decouple import config


JWT_SECRET = config("SECRET_TOKEN")
JWT_ALGORITHM = config("ALGORITHM")


# Function return generated token jwt
def token_response(token: str):
    return {"access_token": token}


# Function for signing the JWT string
def signJWT(user_id: str):
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


# decode JWT function
def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
