from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from backend.models.user_model import User

# Définir la base pour les modèles
Base = declarative_base()


# Classe Doctor
class Doctor(User):
    __tablename__ = 'doctors'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    state = Column(Enum('Actif', 'Inactif', name='doctor_state'), default='Actif', nullable=False)
    specialty = Column(String(50), nullable=False)

    # Relation avec les patients
    patients = relationship("Patient", back_populates="doctor", cascade="all, delete-orphan")
    user = relationship("User", backref="doctor")

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


class Admin(User):
    __tablename__ = 'admins'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(254), unique=True, nullable=False)

    # Relation avec les notifications
    notifications = relationship("Notification", back_populates="admin")
    user = relationship("User", backref="admin")


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    message = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    admin_id = Column(Integer, ForeignKey('admins.id'))

    # Relation avec l'administrateur
    admin = relationship("Admin", back_populates="notifications")
