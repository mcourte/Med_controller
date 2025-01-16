from sqlalchemy import (
    Column, Integer, String, ForeignKey,
)
from sqlalchemy.orm import relationship
from backend.models.user_model import User


class Patient(User):
    __tablename__ = 'patients'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)

    # Clé étrangère pour le médecin associé
    doctor_id = Column(Integer, ForeignKey("users.id"))

    # Relation vers User (médecin)
    doctor = relationship("User", foreign_keys=[doctor_id])

    # Relation vers User (patient)
    user = relationship("User", backref="patient", foreign_keys=[id])

    # Spécification explicite de l'héritage
    __mapper_args__ = {
        'inherit_condition': id == User.id
    }
