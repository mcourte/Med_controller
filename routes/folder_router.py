from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from controllers.folder_controller import FolderController
from controllers.schemas import (
    FolderCreate,
    FolderUpdate,
)

router = APIRouter()


# Folders Routes
@router.post("/folders", status_code=status.HTTP_201_CREATED)
def create_folder(folder_data: FolderCreate, db: Session = Depends(get_db)):
    return FolderController(db).create_folder(folder_data)


@router.get("/folders/{folder_id}")
def get_folder(folder_id: int, db: Session = Depends(get_db)):
    return FolderController(db).get_folder_by_id(folder_id)


@router.put("/folders/{folder_id}")
def update_folder(folder_id: int, folder_data: FolderUpdate, db: Session = Depends(get_db)):
    return FolderController(db).update_folder(folder_id, folder_data)


@router.delete("/folders/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    return FolderController(db).delete_folder(folder_id)


@router.get("/folders")
def get_all_folders(db: Session = Depends(get_db)):
    return FolderController(db).get_all_folders()
