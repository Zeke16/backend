from fastapi import APIRouter, HTTPException, status
from  db.models.user import User
from db.connection import db_connection
from db.schemas.user import userSchema, usersSchema

router = APIRouter(prefix="/userdb", tags=["userdb"], responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []

@router.get("/", response_model=list( User))
async def users():
    return usersSchema(db_connection.local.users.find())

# Con path
@router.get("/{id}")
async def user(id: int):
    return search_user_by_id(id)

# Con query
@router.get("/")
async def user(id: int):
    return search_user_by_id(id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_connection.local.users.insert_one(user_dict).inserted_id

    new_user = userSchema(db_connection.local.users.find_one({"_id": id}))

    return User(**new_user)

@router.put("/")
async def user(user: User):
    Found = False

    for index, users in enumerate(users_list):
        if users.id == user.id:
            users_list[index] = user
            Found = True
    if not Found:
        return {"Error": "Usuario no encontrado"}
    return user

@router.delete("/{id}")
async def user(id: int):
    Found = False
    for index, users in enumerate(users_list):
        if users.id == id:
            del users_list[index]
            Found = True
    if not Found:
        return {"Error": "Usuario no encontrado"}
    return {"response": "Eliminado"}

def search_user(field: str, key: str):
    try:
        user = userSchema(db_connection.local.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": f"Usuario con {field} {key} no existe"}
