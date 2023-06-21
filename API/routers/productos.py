from fastapi import APIRouter

router = APIRouter(prefix="/productos", responses={404: {"message": "No encontrado"}}, tags=["products"])

@router.get("/")
async def productos():
    return ["Productos"]