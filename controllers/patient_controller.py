from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.entities import Patient, Doctor
from pydantic import BaseModel
from typing import List


# Pydantic models pour la validation des données
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    doctor_id: int


class PatientUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    doctor_id: int = None


class PatientController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_patients(self) -> List[Patient]:
        """
        Get a list of all patients in the database.
        """
        patients = self.session.query(Patient).all()
        return patients

    def get_patient_by_id(self, patient_id: int) -> Patient:
        """
        Get a specific patient by their ID.
        """
        patient = self.session.query(Patient).filter_by(id=patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    def create_patient(self, patient: PatientCreate) -> dict:
        """
        Add a new patient to the database.
        """
        new_patient = Patient(
            first_name=patient.first_name,
            last_name=patient.last_name,
            email=patient.email,
            doctor_id=patient.doctor_id
        )
        self.session.add(new_patient)
        self.session.commit()
        return {"message": "Patient added successfully"}

    def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> dict:
        """
        Update an existing patient's information.
        """
        patient = self.session.query(Patient).filter_by(id=patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        patient.first_name = patient_data.first_name or patient.first_name
        patient.last_name = patient_data.last_name or patient.last_name
        patient.email = patient_data.email or patient.email
        patient.doctor_id = patient_data.doctor_id if patient_data.doctor_id is not None else patient.doctor_id

        self.session.commit()
        return {"message": "Patient updated successfully"}

    def delete_patient(self, patient_id: int) -> dict:
        """
        Delete a patient by their ID.
        """
        patient = self.session.query(Patient).filter_by(id=patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        self.session.delete(patient)
        self.session.commit()
        return {"message": "Patient deleted successfully"}

    def get_doctor_for_patient(self, patient_id: int) -> Doctor:
        """
        Get the doctor assigned to a specific patient.
        """
        patient = self.session.query(Patient).filter_by(id=patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        doctor = patient.doctor
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        return doctor
