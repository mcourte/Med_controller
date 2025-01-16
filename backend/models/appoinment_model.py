from sqlalchemy import (
    Column, Integer, String, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Définir la base pour les modèles
Base = declarative_base()


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    description = Column(String(500), nullable=False)
    appointment_date = Column(TIMESTAMP, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=False)

    # Relations
    folder = relationship("Folder", back_populates="appointments")
    reports = relationship("Report", back_populates="appointment", cascade="all, delete-orphan")
    doctor = relationship('Doctor', back_populates='appointments', foreign_keys=[doctor_id])
    patient = relationship('Patient', back_populates='appointments', foreign_keys=[patient_id])
