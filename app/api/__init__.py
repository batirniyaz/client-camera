from fastapi import APIRouter
from .employees import router as employees_router
from .attendance import router as attendance_router
from .filial import router as filial_router

router = APIRouter()
router.include_router(employees_router, prefix="/employees", tags=["Employees"])
router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
router.include_router(filial_router, prefix="/filial", tags=["Filials"])