from flask import Flask , request , jsonify , render_template
import joblib
from func import Doctor

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home_page')



@app.route("/predict")
def predict():
    data = request.get_json()
    # data pe preprocessing from PIYUSH function to get symptom
    # lets take dummy symptoms for the time being
    symptoms = ['itching' , 'continuous_sneezing' , 'acidity']
    helper = Doctor(symptoms)
    ans = helper.predicting(symptoms)
    return jsonify({ans})

    
    


