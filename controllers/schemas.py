from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


# Doctor Schemas
class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class DoctorResponse(DoctorBase):
    id: int

    class Config:
        orm_mode = True


# Patient Schemas
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    doctor_id: int


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    doctor_id: Optional[int] = None


class PatientResponse(PatientBase):
    id: int

    class Config:
        orm_mode = True


# Appointment Schemas
class AppointmentBase(BaseModel):
    description: str
    appointment_date: str  # Format "DD-MM-YYYY HH:MM:SS"
    doctor_id: int
    patient_id: int

    @validator("appointment_date")
    def validate_appointment_date(cls, v):
        try:
            return datetime.strptime(v, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            raise ValueError("Le format de la date doit être DD-MM-YYYY HH:MM:SS")


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    description: Optional[str] = None
    appointment_date: Optional[str] = None  # Format "DD-MM-YYYY HH:MM:SS"
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None

    @validator("appointment_date")
    def validate_appointment_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, "%d-%m-%Y %H:%M:%S")
            except ValueError:
                raise ValueError("Le format de la date doit être DD-MM-YYYY HH:MM:SS")
        return v


class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True


# Folder Schemas
class FolderBase(BaseModel):
    title: str
    description: str
    patient_id: int


class FolderCreate(FolderBase):
    pass


class FolderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    patient_id: Optional[int] = None


class FolderResponse(FolderBase):
    id: int

    class Config:
        orm_mode = True


# Report Schemas
class ReportBase(BaseModel):
    title: str
    content: str
    folder_id: int


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    folder_id: Optional[int] = None


class ReportResponse(ReportBase):
    id: int

    class Config:
        orm_mode = True
