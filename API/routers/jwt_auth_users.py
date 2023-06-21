from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITH = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "b6ff653a5cae2907c21b20d263d35208517e8cdd231b7b690f9b3d9a99c69109"
router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "Zeke16": {
        "username": "Zeke16",
        "full_name": "Ezequiel Ramirez",
        "email": "kr2000.16@gmail.com",
        "disabled": False,
        "password": "$2a$12$PYAq/mNC2jyM5KoxOZoBPec50S5LteV.RRQHQSzmTJkOt/i.riZsS"
    },
    "Zeke162": {
        "username": "Zeke162",
        "full_name": "Ezequiel Ramirez 2",
        "email": "kr2000.162@gmail.com",
        "disabled": True,
        "password": "$2a$12$.aUQ3LbGZYCAnR0uIOlpcuoFyw8qgTQiFWSn2OaWEBxgw/jD.8uXW"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticacion invalidas",
                            headers={"WWW-Authenticate": "jwt"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITH]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no existe")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub": user.username, "exp": expire}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITH, ), "token_type": "jwt"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
