from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base


class Analyse(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    date_requested = Column(DateTime, nullable=False)
    date_completed = Column(DateTime, nullable=True)
    result = Column(Text, nullable=True)

    # Relations
    folder = relationship("Folder", back_populates="analyses")
    reports = relationship("Report", back_populates="analyse")
