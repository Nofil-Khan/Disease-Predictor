import os
import joblib
import numpy as np
import warnings
import shap
from google import genai
warnings.filterwarnings("ignore")

class Doctor:

    def __init__(self):
        model_bundle = joblib.load("model_bundle.pkl")

        self.model = model_bundle["model"]
        self.symptoms = list(model_bundle["features"])
        self.length = len(self.symptoms)

        self.mapping = {symptom: i for i, symptom in enumerate(self.symptoms)}

        self.diseases = model_bundle.get("labels", None)

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable not found")

        self.client = genai.Client(api_key=api_key)

        self.explainer = shap.Explainer(self.model)


    def extract_feature(self, symptoms):

        feature_vector = np.zeros(self.length, dtype=int)

        for symptom in symptoms:
            if symptom in self.mapping:
                feature_vector[self.mapping[symptom]] = 1

        return feature_vector


    def predicting(self, symptoms):

        features = self.extract_feature(symptoms)
        features = features.reshape(1, -1)

        prediction = self.model.predict(features)[0]

        probability = None
        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(features)[0]
            confidence = np.max(prob) * 100
            probability = round(confidence, 2)

        return prediction, probability


    def top_predictions(self, symptoms, top_n=3):

        features = self.extract_feature(symptoms)
        features = features.reshape(1, -1)

        prob = self.model.predict_proba(features)[0]

        top_indices = np.argsort(prob)[::-1][:top_n]

        results = []

        for idx in top_indices:
            disease = self.model.classes_[idx]
            confidence = round(prob[idx] * 100, 2)
            results.append((disease, confidence))
        
        return results
    

    # def symptom_contribution(self, symptoms):

    #     features = self.extract_feature(symptoms).reshape(1, -1)

    #     shap_values = self.explainer(features)

    #     disease_index = np.argmax(self.model.predict_proba(features)[0])

    #     contributions = shap_values.values[0][:, disease_index]

    #     results = []

        # for symptom in symptoms:
        #     idx = self.mapping[symptom]
        #     results.append((symptom, contributions[idx]))

        # results.sort(key=lambda x: abs(x[1]), reverse=True)

        # return results
            

    def explain_disease(self, symptoms):
        top = self.top_predictions(symptoms)

        # contributions = self.symptom_contribution(symptoms)
        # top_symptoms = contributions[:3]

        contribution_text = ""
        # for symptom, score in top_symptoms:
        #     contribution_text += f"- {symptom} (model influence: {round(score,3)})\n"

        prompt = "User reported symptoms:\n"
        prompt += ", ".join(symptoms) + "\n\n"

        prompt += "Model predicted the following diseases:\n"

        for i, (disease, confidence) in enumerate(top, start=1):
            prompt += f"{i}. {disease} — {confidence}% confidence\n"

        prompt += "\nSymptoms that contributed most to the prediction:\n"
        prompt += contribution_text
        
        prompt += f"""

Important symptom contributions:
{contribution_text}

Task:
Explain the prediction results to the user using the structure below.

Formatting rules:
- Use Markdown formatting
- Do not include code blocks
- Use bullet points with "-"
- Use **bold** for disease names
- Keep the explanation under 250 words

Output structure:

Start exactly with this sentence:

Here is a summary of the possible conditions based on your symptoms.

Sections to include:

Reported symptoms:
[List symptoms as bullet points]

Possible conditions identified by the model:
[List diseases in numbered order with confidence]

Confidence interpretation:
[Explain each disease confidence level]

End with a disclaimer advising consultation with a healthcare professional.
"""
        
    
        
        response = self.client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt
        )

        return response.text.strip()


# doctor = Doctor()
# symptoms = ["nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills", "joint_pain"]

# print(doctor.explain_disease(symptoms))