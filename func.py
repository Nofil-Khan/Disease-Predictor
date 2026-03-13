import os
import pandas as pd
import joblib
import numpy as np
import warnings
# import spacy
from google import genai
warnings.filterwarnings("ignore")
os.environ["GEMINI_API_KEY"]


class Doctor:

    def __init__(self):
        model_bundle = joblib.load("model_bundle.pkl")

        self.model = model_bundle["model"]
        self.symptoms = list(model_bundle["features"])
        self.length = len(self.symptoms)

        self.mapping = {symptom: i for i, symptom in enumerate(self.symptoms)}

        # diseases (labels)
        self.diseases = model_bundle.get("labels", None)

        # API setup
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable not found")

        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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
    

    def explain_disease(self, symptoms):
        top = self.top_predictions(symptoms)

        prompt = "User reported symptoms:\n"
        prompt += ", ".join(symptoms) + "\n\n"

        prompt += "Model predicted the following diseases:\n"

        for i, (disease, confidence) in enumerate(top, start=1):
            prompt += f"{i}. {disease} — {confidence}% confidence\n"

        prompt += """

        Task:
        Explain the prediction results to the user using the exact structure described below.

        Rules:
        - Only use the diseases listed in the predictions above.
        - Do NOT introduce new diseases.
        - Do NOT modify or rephrase the symptoms.
        - Replace underscores in symptoms with spaces when displaying them.
        - Keep the explanation calm, simple, and informative.
        - Keep the total length under 150 words.

        Required Output Structure:

        1. Start with this exact sentence:
        Here is a summary of the possible conditions based on your symptoms.

        2. Then write:

        Reported symptoms:
        [Each symptom listed on a new line with a bullet point, replacing underscores with spaces]

        3. Then write:

        Possible conditions identified by the model:
        [List the predicted diseases in a numbered format along with their confidence percentages]
        
       4. Confidence Interpretation Rules:
        - If a disease confidence score is greater than 60%, explain that the symptoms strongly match patterns associated with that condition.
        - If a disease confidence score is between 40% and 60%, explain that the symptoms show a moderate match.
        - If a disease confidence score is below 40%, explain that the symptoms only weakly match and the model is uncertain.
        - If all predictions are below 40%, clearly state that the model could not find a strong match and that the symptoms may relate to other conditions not strongly represented in the dataset.
                

        5. End with a disclaimer stating that the information is only guidance and that the user should consult a healthcare professional for proper diagnosis.

        Important:
        Follow this structure exactly.
        Do not add extra sections.
        Do not deviate from the required format.
        Everything should be under 250 words in total.
        Focus on the 4th point the most VERY VERY IMPORTANT, as it provides the reasoning behind the predictions, which is crucial for user understanding.
        """
        
        response = self.client.models.generate_content(
            model="gemma-3-27b-it",
            contents=prompt
        )
        
        return response.text


doctor = Doctor()
symptoms = ["fatigue",

"high_fever",

"runny_nose",

"abdominal_pain",

"blurred_and_distorted_vision"]

# prediction, confidence = doctor.predicting(symptoms)

# print("Predicted disease:", prediction)
# print("Confidence:", confidence)

# print("Explanation:")
# print(doctor.explain_disease(symptoms))

print(doctor.explain_disease(symptoms))