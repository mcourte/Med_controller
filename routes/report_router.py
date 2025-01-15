from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from controllers.report_controller import ReportController
from controllers.schemas import (
    ReportCreate,
    ReportUpdate,
)

router = APIRouter()


# Reports Routes
@router.post("/reports", status_code=status.HTTP_201_CREATED)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    return ReportController(db).create_report(report_data)


@router.get("/reports/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    return ReportController(db).get_report_by_id(report_id)


@router.put("/reports/{report_id}")
def update_report(report_id: int, report_data: ReportUpdate, db: Session = Depends(get_db)):
    return ReportController(db).update_report(report_id, report_data)


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return ReportController(db).delete_report(report_id)


@router.get("/reports")
def get_all_reports(db: Session = Depends(get_db)):
    return ReportController(db).get_all_reports()
