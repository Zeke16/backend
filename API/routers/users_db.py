from fastapi import APIRouter, HTTPException, status
from  db.models.user import User
from db.connection import db_connection
from db.schemas.user import userSchema, usersSchema
from bson import ObjectId

router = APIRouter(prefix="/userdb", tags=["userdb"], responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []

@router.get("/", response_model=list[User])
async def users():
    return usersSchema(db_connection.users.find())

# Con path
@router.get("/user/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Con query
@router.get("/user")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="el usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_connection.users.insert_one(user_dict).inserted_id

    new_user = userSchema(db_connection.users.find_one({"_id": id}))

    return User(**new_user)

@router.put("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_connection.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"Error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_connection.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"Error": "No se ha eliminado el usuario"}

def search_user(field: str, key):
    try:
        user = userSchema(db_connection.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": f"Usuario con {field} {key} no existe"}
