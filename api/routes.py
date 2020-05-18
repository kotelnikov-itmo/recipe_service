from fastapi import APIRouter

router = APIRouter()

@router.get("/test/")
async def test(q: str):
    return {"echo": q}