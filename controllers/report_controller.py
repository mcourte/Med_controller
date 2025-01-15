from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.entities import Report
from pydantic import BaseModel
from typing import List


# Pydantic models pour la validation des données
class ReportCreate(BaseModel):
    description: str
    report_state: str
    folder_id: int


class ReportUpdate(BaseModel):
    description: str = None
    report_state: str = None


class ReportController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_reports(self) -> List[Report]:
        """
        Get a list of all reports in the database.
        """
        reports = self.session.query(Report).all()
        return reports

    def get_report_by_id(self, report_id: int) -> Report:
        """
        Get a specific report by its ID.
        """
        report = self.session.query(Report).filter_by(report_id=report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

    def create_report(self, report: ReportCreate) -> dict:
        """
        Add a new report to the database.
        """
        new_report = Report(
            description=report.description,
            report_state=report.report_state,
            folder_id=report.folder_id
        )
        self.session.add(new_report)
        self.session.commit()
        return {"message": "Report added successfully"}

    def update_report(self, report_id: int, report_data: ReportUpdate) -> dict:
        """
        Update an existing report's information.
        """
        report = self.session.query(Report).filter_by(report_id=report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        report.description = report_data.description or report.description
        report.report_state = report_data.report_state or report.report_state

        self.session.commit()
        return {"message": "Report updated successfully"}

    def delete_report(self, report_id: int) -> dict:
        """
        Delete a report by its ID.
        """
        report = self.session.query(Report).filter_by(report_id=report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        self.session.delete(report)
        self.session.commit()
        return {"message": "Report deleted successfully"}
