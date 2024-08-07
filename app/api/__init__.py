from fastapi import APIRouter
from .employees import router as employees_router
from .attendance import router as attendance_router
from .filial import router as filial_router
from .employee_image import router as employee_image_router
from .position import router as position_router
from .working_graphic import router as working_graphic_router

router = APIRouter()
router.include_router(employees_router, prefix="/employees", tags=["Employees"])
router.include_router(employee_image_router, prefix="/employee_images", tags=["Employee Images"])
router.include_router(filial_router, prefix="/filials", tags=["Filials"])
router.include_router(position_router, prefix="/positions", tags=["Positions"])
router.include_router(working_graphic_router, prefix="/working_graphics", tags=["Working Graphics"])
router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
