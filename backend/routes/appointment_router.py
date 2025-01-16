from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.controllers.appointment_controller import AppointmentController
from backend.controllers.schemas import (
    AppointmentCreate,
    AppointmentUpdate,
)

router = APIRouter()


# Appointments Routes
@router.post("/appointments", status_code=status.HTTP_201_CREATED)
def create_appointment(appointment_data: AppointmentCreate, db: Session = Depends(get_db)):
    return AppointmentController(db).create_appointment(appointment_data)


@router.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return AppointmentController(db).get_appointment(appointment_id)


@router.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, appointment_data: AppointmentUpdate, db: Session = Depends(get_db)):
    return AppointmentController(db).update_appointment(appointment_id, appointment_data)


@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return AppointmentController(db).delete_appointment(appointment_id)


@router.get("/appointments")
def get_all_appointments(db: Session = Depends(get_db)):
    return AppointmentController(db).get_all_appointments()
