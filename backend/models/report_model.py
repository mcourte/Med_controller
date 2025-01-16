from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from enum import Enum as PyEnum
from backend.database import Base


class ReportState(PyEnum):
    DOCTORS = "D"
    BOTH = "B"


#  Classe Report
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)  # Clé étrangère
    analyse_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    content = Column(Text, nullable=False)
    date_created = Column(DateTime, nullable=False)
    state = Column(SQLEnum(ReportState), nullable=False, default=ReportState.DOCTORS)  # Etat du rapport

    # Relations
    folder = relationship("Folder", back_populates="reports")
    appointment = relationship("Appointment", back_populates="reports")  # Relation avec Appointment
    analyse = relationship("Analyse", back_populates="reports")
