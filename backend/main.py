from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.database import Base, engine
from backend.routes.doctor_router import router as doctor_router
from backend.routes.patient_router import router as patient_router
from backend.routes.appointment_router import router as appointment_router
from backend.routes.folder_router import router as folder_router
from backend.routes.report_router import router as report_router

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


# Montre les fichiers statiques (par exemple : JS et CSS générés par Vue.js)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
