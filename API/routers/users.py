from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(responses={404: {"message": "No encontrado"}}, tags=["users"])

# Entidad user


class User(BaseModel):
    id: int
    name: str
    username: str
    url: str
    age: int


users_list = [User(id=1, name="Zeke1", username="Zeke161", url="http://zeke161.com", age=21),
              User(id=2, name="Zeke2", username="Zeke162",
                   url="http://zeke162.com", age=22),
              User(id=3, name="Zeke3", username="Zeke163",
                   url="http://zeke163.com", age=23),
              User(id=4, name="Zeke4", username="Zeke164", url="http://zeke164.com", age=24)]


@router.get("/usersjson")
async def usersjson():
    return {"Users:": "Hola usuarios"}


@router.get("/users")
async def users():
    return list(users_list)

# Con path
@router.get("/user/{id}")
async def user(id: int):
    return search_user_by_id(id)

# Con query
@router.get("/user")
async def user(id: int):
    return search_user_by_id(id)


def search_user_by_id(id):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": f"Usuario con id {id} no existe"}


@router.post("/user")
async def user(user: User):
    if type(search_user_by_id(user.id)) == User:
        return {"error": "El usuario ya existe!"}
    else:
        users_list.routerend(user)


@router.put("/user")
async def user(user: User):
    Found = False

    for index, users in enumerate(users_list):
        if users.id == user.id:
            users_list[index] = user
            Found = True
    if not Found:
        return {"Error": "Usuario no encontrado"}
    return user

@router.delete("/user/{id}")
async def user(id: int):
    Found = False
    for index, users in enumerate(users_list):
        if users.id == id:
            del users_list[index]
            Found = True
    if not Found:
        return {"Error": "Usuario no encontrado"}
    return {"response": "Eliminado"}