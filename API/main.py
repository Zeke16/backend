from fastapi import FastAPI
from routers import productos, users, basic_auth_user, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(productos.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_user.router)
app.include_router(users_db.router)
app.mount("/static",StaticFiles(directory="static"), name="static")
@app.get("/")
async def Home():
    return {"message": "Hola FastApi!"}