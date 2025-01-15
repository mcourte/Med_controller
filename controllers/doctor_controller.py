from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.entities import Doctor, Patient
from pydantic import BaseModel
from typing import List


# Pydantic models pour la validation des données
class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    specialty: str
    phone: str
    address: str
    is_active: bool


class DoctorUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    specialty: str = None
    phone: str = None
    address: str = None
    is_active: bool = None


class DoctorController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_doctors(self) -> List[Doctor]:
        """
        Get a list of all doctors in the database.
        """
        doctors = self.session.query(Doctor).all()
        return doctors

    def get_doctor_by_id(self, doctor_id: int) -> Doctor:
        """
        Get a specific doctor by their ID.
        """
        doctor = self.session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor

    def create_doctor(self, doctor: DoctorCreate) -> dict:
        """
        Add a new doctor to the database.
        """
        new_doctor = Doctor(
            first_name=doctor.first_name,
            last_name=doctor.last_name,
            email=doctor.email,
            specialty=doctor.specialty,
            phone=doctor.phone,
            address=doctor.address,
            is_active=doctor.is_active
        )
        self.session.add(new_doctor)
        self.session.commit()
        return {"message": "Doctor added successfully"}

    def update_doctor(self, doctor_id: int, doctor_data: DoctorUpdate) -> dict:
        """
        Update an existing doctor's information.
        """
        doctor = self.session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        doctor.first_name = doctor_data.first_name or doctor.first_name
        doctor.last_name = doctor_data.last_name or doctor.last_name
        doctor.email = doctor_data.email or doctor.email
        doctor.specialty = doctor_data.specialty or doctor.specialty
        doctor.phone = doctor_data.phone or doctor.phone
        doctor.address = doctor_data.address or doctor.address
        doctor.is_active = doctor_data.is_active if doctor_data.is_active is not None else doctor.is_active

        self.session.commit()
        return {"message": "Doctor updated successfully"}

    def delete_doctor(self, doctor_id: int) -> dict:
        """
        Delete a doctor by their ID.
        """
        doctor = self.session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # On peut aussi supprimer les patients associés ou gérer autrement les dépendances
        # par exemple en désactivant les relations dans les patients avant la suppression
        self.session.delete(doctor)
        self.session.commit()
        return {"message": "Doctor deleted successfully"}

    def get_patients_for_doctor(self, doctor_id: int) -> List[Patient]:
        """
        Get all patients associated with a specific doctor.
        """
        doctor = self.session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Récupérer tous les patients associés à ce médecin
        patients = doctor.patients
        return patients
