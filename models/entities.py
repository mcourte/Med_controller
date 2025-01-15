from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, TIMESTAMP, Sequence
)
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType

# Définir la base pour les modèles
Base = declarative_base()


# Classe Doctor
class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    state = Column(Enum('Actif', 'Inactif', name='doctor_state'), default='Actif', nullable=False)

    # Relation avec les patients
    patients = relationship("Patient", back_populates="doctor", cascade="all, delete-orphan")

    def set_inactive(self):
        """Marquer le médecin comme inactif et notifier l'administrateur."""
        self.state = 'Inactif'
        session = object_session(self)
        session.commit()

        # Notifier l'administrateur
        self.notify_admin_to_reassign_patients()

    def notify_admin_to_reassign_patients(self):
        """Notifier l'administrateur de la nécessité de réattribuer les patients."""
        message = f"Le médecin {self.first_name} {self.last_name} est passé à l'état inactif. Veuillez réattribuer ses patients."
        self.notify_admin(message)

    def notify_admin(self, message):
        """Envoyer une notification à l'administrateur."""
        session = object_session(self)

        # Rechercher un administrateur existant
        admin = session.query(Admin).first()
        if not admin:
            print("Aucun administrateur trouvé pour recevoir la notification.")
            return

        # Créer et enregistrer une notification
        notification = Notification(message=message, admin_id=admin.id)
        session.add(notification)
        session.commit()

        print(f"Notification envoyée à l'administrateur {admin.first_name} {admin.last_name} : {message}")


# Classe Patient
class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)

    # Relation avec le médecin
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=True)
    doctor = relationship("Doctor", back_populates="patients")


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)

    # Relation avec les notifications
    notifications = relationship("Notification", back_populates="admin")


# Classe Folders
class Folder(Base):
    __tablename__ = 'folders'

    folder_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    # Relations
    doctor = relationship('Doctor', back_populates='folders', foreign_keys=[doctor_id])
    patient = relationship('Patient', back_populates='folders', foreign_keys=[patient_id])
    reports = relationship('Report', back_populates='folder')


# Classe Appointment
class Appointment(Base):
    __tablename__ = 'appointments'

    appointment_id = Column(Integer, Sequence('appointment_id_seq'), primary_key=True)
    description = Column(String(500), nullable=False)
    appointment_date = Column(TIMESTAMP, nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))

    # Relations
    doctor = relationship('Doctor', back_populates='appointments', foreign_keys=[doctor_id])
    patient = relationship('Patient', back_populates='appointments', foreign_keys=[patient_id])

    def __repr__(self):
        return f"Appointment({self.description})"


# Classe Report
class Report(Base):
    __tablename__ = 'reports'

    REPORT_STATES = (
        ('D', 'Doctors'),
        ('B', 'Both'),
    )

    report_id = Column(Integer, primary_key=True)
    description = Column(String(500), nullable=False)
    date_report = Column(TIMESTAMP, nullable=False, default=func.now())
    report_state = Column(ChoiceType(REPORT_STATES, impl=String(length=1)), default='D')
    folder_id = Column(Integer, ForeignKey('folders.folder_id'), nullable=False)

    # Relations
    folder = relationship('Folder', back_populates='reports')

    def __init__(self, description, report_state, folder_id):
        self.description = description
        self.report_state = report_state
        self.folder_id = folder_id


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    message = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    admin_id = Column(Integer, ForeignKey('admins.id'))

    # Relation avec l'administrateur
    admin = relationship("Admin", back_populates="notifications")
