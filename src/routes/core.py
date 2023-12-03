from fastapi import APIRouter

from ..controllers import core as controller
from ..models.inputs import Query

router = APIRouter()


@router.post("/chat")
async def chat(body: Query):
    return await controller.chat(body)
