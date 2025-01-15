from fastapi import FastAPI
from database import Base, engine
from routes.doctor_router import router as doctor_router
from routes.patient_router import router as patient_router
from routes.appointment_router import router as appointment_router
from routes.folder_router import router as folder_router
from routes.report_router import router as report_router

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclure les routeurs
app.include_router(doctor_router, prefix="/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/patients", tags=["Patients"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(folder_router, prefix="/folders", tags=["Folders"])
app.include_router(report_router, prefix="/reports", tags=["Reports"])


@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Bienvenue sur l'API CRM Médical !"}
