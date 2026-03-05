import pandas as pd
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore")


class Doctor:

    def __init__(self):

        self.df = pd.read_csv("Testing.csv")

        model_bundle = joblib.load("model_bundle.pkl")
        self.model = model_bundle["model"]
        self.symptoms = list(model_bundle["features"])
        self.length = len(self.symptoms)
        self.mapping = {symptom: i for i, symptom in enumerate(self.symptoms)}

    def extract_feature(self, symptoms):

        feature_vector = np.zeros(self.length)

        for symptom in symptoms:

            if symptom in self.mapping:

                feature_vector[self.mapping[symptom]] = 1

        return feature_vector

    def predicting(self, symptoms):

        features = self.extract_feature(symptoms)

        features = features.reshape(1, -1)

        prediction = self.model.predict(features)

        return prediction[0]


# create once
doctor = Doctor()
# print(doctor.predicting(symptoms=['skin_rash' , 'chills' , 'muscle_wasting']))
importance = doctor.model.feature_importances_

df = pd.DataFrame({
    "symptom": doctor.symptoms,
    "importance": importance
}).sort_values("importance", ascending=False)

print(df.head(10))
# print(doctor.predicting(['itching', 'skin_rash']))
# print(doctor.predicting(['vomiting', 'nausea']))
# print(doctor.predicting(['chest_pain', 'breathlessness']))