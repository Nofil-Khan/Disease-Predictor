from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from func import Doctor

app = FastAPI()
doctor = Doctor()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "form.html",
        {"request": request}
    )

@app.post("/predict")
async def predict(data: dict):

    message = data["message"]

    symptoms = preprocess(message)         # This function should return a list of symmptoms

    ans = doctor.predicting(symptoms)

    return {"prediction": ans}