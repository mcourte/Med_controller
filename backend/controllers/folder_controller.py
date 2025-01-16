from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.folder_model import Folder
from pydantic import BaseModel
from typing import List


# Pydantic models pour la validation des données
class FolderCreate(BaseModel):
    title: str
    description: str
    doctor_id: int
    patient_id: int


class FolderUpdate(BaseModel):
    title: str = None
    description: str = None
    doctor_id: int = None
    patient_id: int = None


class FolderController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_folders(self) -> List[Folder]:
        """
        Get a list of all folders in the database.
        """
        folders = self.session.query(Folder).all()
        return folders

    def get_folder_by_id(self, folder_id: int) -> Folder:
        """
        Get a specific folder by its ID.
        """
        folder = self.session.query(Folder).filter_by(folder_id=folder_id).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
        return folder

    def create_folder(self, folder: FolderCreate) -> dict:
        """
        Add a new folder to the database.
        """
        new_folder = Folder(
            title=folder.title,
            description=folder.description,
            doctor_id=folder.doctor_id,
            patient_id=folder.patient_id
        )
        self.session.add(new_folder)
        self.session.commit()
        return {"message": "Folder added successfully"}

    def update_folder(self, folder_id: int, folder_data: FolderUpdate) -> dict:
        """
        Update an existing folder's information.
        """
        folder = self.session.query(Folder).filter_by(folder_id=folder_id).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")

        folder.title = folder_data.title or folder.title
        folder.description = folder_data.description or folder.description
        folder.doctor_id = folder_data.doctor_id or folder.doctor_id
        folder.patient_id = folder_data.patient_id or folder.patient_id

        self.session.commit()
        return {"message": "Folder updated successfully"}

    def delete_folder(self, folder_id: int) -> dict:
        """
        Delete a folder by its ID.
        """
        folder = self.session.query(Folder).filter_by(folder_id=folder_id).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")

        self.session.delete(folder)
        self.session.commit()
        return {"message": "Folder deleted successfully"}
