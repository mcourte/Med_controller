from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from controllers.doctor_controller import DoctorController
from controllers.schemas import (
    DoctorCreate,
    DoctorUpdate,
)

router = APIRouter()


# Doctors Routes
@router.post("/doctors", status_code=status.HTTP_201_CREATED)
def create_doctor(doctor_data: DoctorCreate, db: Session = Depends(get_db)):
    return DoctorController(db).create_doctor(doctor_data)


@router.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return DoctorController(db).get_doctor_by_id(doctor_id)


@router.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor_data: DoctorUpdate, db: Session = Depends(get_db)):
    return DoctorController(db).update_doctor(doctor_id, doctor_data)


@router.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return DoctorController(db).delete_doctor(doctor_id)


@router.get("/doctors")
def get_all_doctors(db: Session = Depends(get_db)):
    return DoctorController(db).get_all_doctors()
