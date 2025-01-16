from sqlalchemy import Column, String, Integer, Enum
from backend.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Stocker les mots de passe hachés !
    role = Column(Enum("patient", "doctor", name="user_roles"), nullable=False)
