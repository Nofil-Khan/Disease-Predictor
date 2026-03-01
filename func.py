import pandas as pd
import joblib
import numpy as np

class Doctor:

    def __init__(self):
        self.df = pd.read_csv('Testing.csv')
        self.model = joblib.load('Model_saved.pkl')
        self.all_symptoms = self.df.columns
        self.length = len(self.all_symptoms)

    def extract_feature(self, symptoms):
        initial = [0] * (self.length - 1)

        for i in range(self.length - 1):
            if self.all_symptoms[i] in symptoms:
                initial[i] = 1

        return initial

    def predicting(self, symptoms):
        final = self.extract_feature(symptoms)

        final = np.array(final).reshape(1, -1)

        final_df = pd.DataFrame(
            final,
            columns=self.all_symptoms[:self.length - 1]
        )

        ans = self.model.predict(final_df)

        return ans[0]