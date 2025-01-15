from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from controllers.patient_controller import PatientController
from controllers.schemas import (
    PatientCreate,
    PatientUpdate,
)

router = APIRouter()


# Patients Routes
@router.post("/patients", status_code=status.HTTP_201_CREATED)
def create_patient(patient_data: PatientCreate, db: Session = Depends(get_db)):
    return PatientController(db).create_patient(patient_data)


@router.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return PatientController(db).get_patient_by_id(patient_id)


@router.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient_data: PatientUpdate, db: Session = Depends(get_db)):
    return PatientController(db).update_patient(patient_id, patient_data)


@router.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    return PatientController(db).delete_patient(patient_id)


@router.get("/patients")
def get_all_patients(db: Session = Depends(get_db)):
    return PatientController(db).get_all_patients()
