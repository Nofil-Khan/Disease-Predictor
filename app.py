from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Disease Predictor API!"

@app.route("/<symptom>")
def print_symptom(symptom):
    return f"You entered the symptom: {symptom}"



if __name__ == '__main__':
    app.run(debug=True)