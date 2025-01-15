from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.entities import Appointment, Doctor, Patient
from datetime import datetime
from controllers.schemas import AppointmentCreate, AppointmentUpdate


class AppointmentController:
    def __init__(self, session: Session):
        self.session = session

    def create_appointment(self, appointment_data: AppointmentCreate):
        # Validation du format de la date
        try:
            appointment_date = datetime.strptime(appointment_data.appointment_date, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=400, detail="Le format de la date doit être DD-MM-YYYY HH:MM:SS")

        # Vérification si le médecin et le patient existent
        doctor = self.session.query(Doctor).filter(Doctor.id == appointment_data.doctor_id).first()
        patient = self.session.query(Patient).filter(Patient.id == appointment_data.patient_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Médecin non trouvé")

        if not patient:
            raise HTTPException(status_code=404, detail="Patient non trouvé")

        # Création du rendez-vous
        appointment = Appointment(
            description=appointment_data.description,
            appointment_date=appointment_date,
            doctor_id=appointment_data.doctor_id,
            patient_id=appointment_data.patient_id
        )

        self.session.add(appointment)
        self.session.commit()
        return {"message": "Rendez-vous créé avec succès", "appointment_id": appointment.appointment_id}

    def update_appointment(self, appointment_id: int, appointment_data: AppointmentUpdate):
        # Recherche du rendez-vous
        appointment = self.session.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()

        if not appointment:
            raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")

        # Mise à jour des champs si nécessaire
        if appointment_data.description:
            appointment.description = appointment_data.description

        if appointment_data.appointment_date:
            try:
                appointment.appointment_date = datetime.strptime(appointment_data.appointment_date, "%d-%m-%Y %H:%M:%S")
            except ValueError:
                raise HTTPException(status_code=400, detail="Le format de la date doit être DD-MM-YYYY HH:MM:SS")

        if appointment_data.doctor_id:
            # Vérification si le médecin existe
            doctor = self.session.query(Doctor).filter(Doctor.id == appointment_data.doctor_id).first()
            if not doctor:
                raise HTTPException(status_code=404, detail="Médecin non trouvé")
            appointment.doctor_id = appointment_data.doctor_id

        if appointment_data.patient_id:
            # Vérification si le patient existe
            patient = self.session.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient non trouvé")
            appointment.patient_id = appointment_data.patient_id

        self.session.commit()
        return {"message": "Rendez-vous mis à jour avec succès"}

    def get_appointment(self, appointment_id: int):
        # Recherche du rendez-vous
        appointment = self.session.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()

        if not appointment:
            raise HTTPException(status_code=404, detail="Rendez-vous non trouvé")

        return {
            "appointment_id": appointment.appointment_id,
            "description": appointment.description,
            "appointment_date": appointment.appointment_date.strftime("%d-%m-%Y %H:%M:%S"),
            "doctor_id": appointment.doctor_id,
            "patient_id": appointment.patient_id
        }

    def get_all_appointments(self):
        appointments = self.session.query(Appointment).all()
        return [
            {
                "appointment_id": appointment.appointment_id,
                "description": appointment.description,
                "appointment_date": appointment.appointment_date.strftime("%d-%m-%Y %H:%M:%S"),
                "doctor_id": appointment.doctor_id,
                "patient_id": appointment.patient_id
            }
            for appointment in appointments
        ]

    def delete_appointment(self, appointment_id: int) -> dict:
        """
        Delete a appointement by their ID.
        """
        appointment = self.session.query(Appointment).filter_by(id=appointment_id).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointement not found")

        self.session.delete(appointment)
        self.session.commit()
        return {"message": "Appointement deleted successfully"}
