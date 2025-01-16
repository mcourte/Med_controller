from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.controllers.doctor_controller import DoctorController
from backend.controllers.schemas import (
    DoctorCreate,
    DoctorUpdate,
)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def render_doctors_page():
    with open("backend/templates/doctors.html") as f:
        return HTMLResponse(content=f.read())


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


@router.put("/doctors/{doctor_id}/patient")
def get_patient_by_doctor_id(doctor_id: int, db: Session = Depends(get_db)):
    return DoctorController(db).get_patient_by_doctor_id(doctor_id)


@router.get("/doctors")
def get_all_doctors(db: Session = Depends(get_db)):
    return DoctorController(db).get_all_doctors()
