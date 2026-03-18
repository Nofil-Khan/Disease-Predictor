from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from func import Doctor

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve homepage
@app.get("/")
def serve_home():
    return FileResponse("templates/home.html")
# Allow frontend access (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
doctor = Doctor()


# Request schema
class SymptomInput(BaseModel):
    symptoms: str


# -----------------------------
# 🧠 Prediction endpoint
# -----------------------------
@app.post("/predict")
def predict(data: SymptomInput):
    try:
        print("INPUT:", data.symptoms)

        result = doctor.predict(data.symptoms)

        print("OUTPUT:", result)

        if "error" in result:
            return {"prediction": None, "error": result["error"]}

        return {"prediction": result}

    except Exception as e:
        print("🔥 BACKEND ERROR:", str(e))
        return {"prediction": None, "error": str(e)}