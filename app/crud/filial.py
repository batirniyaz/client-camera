from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.filial import Filial
from ..schemas.filial import FilialCreate, FilialResponse, FilialResponseModel, FilialUpdate


def create_filial(db: Session, filial: FilialCreate):
    try:
        db_filial = Filial(
            name=filial.name,
            address=filial.address,
            employees=filial.employees,
            device_id=filial.device_id,
            created_at=filial.created_at
        )
        db.add(db_filial)
        db.commit()
        db.refresh(db_filial)

        response_data = FilialResponse(
            id=db_filial.id,
            name=db_filial.name,
            address=db_filial.address,
            employees=db_filial.employees,
            device_id=db_filial.device_id,
            created_at=db_filial.created_at
        )
        return FilialResponseModel(
            status="success",
            message="Filial created successfully",
            data=response_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_filials(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Filial).offset(skip).limit(limit).all()


def get_filial(db: Session, filial_id: int):
    filial = db.query(Filial).filter(Filial.id == filial_id).first()
    if not filial:
        raise HTTPException(status_code=404, detail="Filial not found")
    return filial


def update_filial(db: Session, filial_id: int, filial: FilialUpdate):
    db_filial = db.query(Filial).filter(Filial.id == filial_id).first()
    if not db_filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    db_filial.name = filial.name
    db_filial.address = filial.address
    db_filial.employees = filial.employees
    db_filial.device_id = filial.device_id
    db_filial.created_at = filial.created_at

    db.commit()
    db.refresh(db_filial)

    response_data = FilialResponse(
        id=db_filial.id,
        name=db_filial.name,
        address=db_filial.address,
        employees=db_filial.employees,
        device_id=db_filial.device_id,
        created_at=db_filial.created_at
    )
    return FilialResponseModel(
        status="success",
        message="Filial updated successfully",
        data=response_data
    )


def delete_filial(db: Session, filial_id: int):
    db_filial = db.query(Filial).filter(Filial.id == filial_id).first()
    if not db_filial:
        raise HTTPException(status_code=404, detail="Filial not found")

    db.delete(db_filial)
    db.commit()

    return {"status": "success", "message": "Filial deleted successfully"}
