from fastapi import APIRouter
from .employees import router as employees_router

router = APIRouter()
router.include_router(employees_router, prefix="/employees", tags=["employees"])