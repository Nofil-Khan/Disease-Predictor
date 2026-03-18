import os
import joblib
import numpy as np
import joblib
import pandas as pd
class Doctor:
    def __init__(self):
        # Load model bundle
        model_bundle = joblib.load("model_bundle.pkl")

        self.model = model_bundle["model"]
        self.symptoms = list(model_bundle["features"])
        self.length = len(self.symptoms)

        # Mapping symptom → index
        self.mapping = {symptom: i for i, symptom in enumerate(self.symptoms)}

    # -----------------------------
    # 🔧 Preprocess input text
    # -----------------------------
    def preprocess(self, text: str):
        if not text:
            return []

        return [
            s.strip().lower().replace(" ", "_")
            for s in text.split(",")
        ]

    # -----------------------------
    # 🧬 Convert to feature vector
    # -----------------------------
    

    def extract_features(self, symptoms):
        feature_dict = {symptom: 0 for symptom in self.symptoms}
        unknown = []

        for symptom in symptoms:
            if symptom in feature_dict:
                feature_dict[symptom] = 1
            else:
                unknown.append(symptom)

        df = pd.DataFrame([feature_dict])   

        return df, unknown

    # -----------------------------
    # 🤖 Predict disease
    # -----------------------------
    def predict(self, text: str):
        symptoms = self.preprocess(text)

        if not symptoms:
            return {
                "error": "No valid symptoms provided"
            }

        features, unknown = self.extract_features(symptoms)

        prediction = self.model.predict(features)[0]

        confidence = None
        top_results = {}

        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(features)[0]

            # Confidence of best prediction
            confidence = round(np.max(prob) * 100, 2)

            # Top 3 predictions
            top_indices = np.argsort(prob)[::-1][:3]

            for idx in top_indices:
                disease = self.model.classes_[idx]
                top_results[disease] = round(prob[idx] * 100, 2)

        return {
            "disease": str(prediction),
            "confidence": confidence,
            "top_predictions": top_results,
            "recognized_symptoms": symptoms,
            "unknown_symptoms": unknown
        }