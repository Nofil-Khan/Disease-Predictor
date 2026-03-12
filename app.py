from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from func import Doctor

app = FastAPI()

# static folder for js/css
app.mount("/static", StaticFiles(directory="static"), name="static")

# template folder
templates = Jinja2Templates(directory="templates")

# load model once
doctor = Doctor()


class Message(BaseModel):
    message: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.post("/predict")
def predict(data: Message):

    text = data.message.strip()

    if not text:
        return {"prediction": "Please enter symptoms"}


    # comments hahahahahahahha

    prediction = doctor.predicting([text])
    print(prediction)   

    return {"prediction": prediction}