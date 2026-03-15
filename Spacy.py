import spacy

# Load the medium-sized English model for better semantic similarity
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_md")

symptom_dataset = [
"itching","skin_rash","nodal_skin_eruptions","continuous_sneezing","shivering","chills","joint_pain","stomach_pain","acidity",
"ulcers_on_tongue","muscle_wasting","vomiting","burning_micturition","spotting_ urination","fatigue","weight_gain","anxiety",
"cold_hands_and_feets","mood_swings","weight_loss","restlessness","lethargy","patches_in_throat","irregular_sugar_level","cough"
,"high_fever","sunken_eyes","breathlessness","sweating","dehydration","indigestion","headache","yellowish_skin","dark_urine","nausea"
,"loss_of_appetite","pain_behind_the_eyes","back_pain","constipation","abdominal_pain","diarrhoea","mild_fever","yellow_urine",
"yellowing_of_eyes","acute_liver_failure","fluid_overload","swelling_of_stomach","swelled_lymph_nodes","malaise","blurred_and_distorted_vision",
"phlegm","throat_irritation","redness_of_eyes","sinus_pressure","runny_nose","congestion","chest_pain","weakness_in_limbs","fast_heart_rate",
"pain_during_bowel_movements","pain_in_anal_region","bloody_stool","irritation_in_anus","neck_pain","dizziness","cramps","bruising","obesity",
"swollen_legs","swollen_blood_vessels","puffy_face_and_eyes","enlarged_thyroid","brittle_nails","swollen_extremeties","excessive_hunger",
"extra_marital_contacts","drying_and_tingling_lips","slurred_speech","knee_pain","hip_joint_pain","muscle_weakness","stiff_neck","swelling_joints"
,"movement_stiffness","spinning_movements","loss_of_balance","unsteadiness","weakness_of_one_body_side","loss_of_smell","bladder_discomfort"
,"foul_smell_of urine","continuous_feel_of_urine","passage_of_gases","internal_itching","toxic_look_(typhos)","depression","irritability",
"muscle_pain","altered_sensorium","red_spots_over_body","belly_pain","abnormal_menstruation","dischromic _patches","watering_from_eyes",
"increased_appetite","polyuria","family_history","mucoid_sputum","rusty_sputum","lack_of_concentration","visual_disturbances",
"receiving_blood_transfusion","receiving_unsterile_injections","coma","stomach_bleeding","distention_of_abdomen","history_of_alcohol_consumption"
,"fluid_overload","blood_in_sputum","prominent_veins_on_calf","palpitations","painful_walking","pus_filled_pimples","blackheads","scurring",
"skin_peeling","silver_like_dusting","small_dents_in_nails","inflammatory_nails","blister","red_sore_around_nose","yellow_crust_ooze"
]

# Provide a synonym map for highly specific semantic mappings that spacy vector similarity might miss
synonym_map = {
    # Headache / Head pain
    "pain in head": "headache",
    "pain in my head": "headache",
    "head hurts": "headache",
    "migraine": "headache",
    "throbbing head": "headache",
    "brain hurts": "headache",

    # Nausea / Vomiting
    "throwing up": "vomiting",
    "puking": "vomiting",
    "barfing": "vomiting",
    "feel like throwing up": "nausea",
    "feeling sick to my stomach": "nausea",
    "queasy": "nausea",
    "feel sick": "nausea",
    "want to throw up": "nausea",

    # Stomach / Abdominal
    "stomach ache": "stomach_pain",
    "tummy ache": "stomach_pain",
    "belly ache": "belly_pain",
    "pain in stomach": "stomach_pain",
    "abdominal cramps": "abdominal_pain",
    "stomach hurts": "stomach_pain",
    "belly hurts": "belly_pain",
    "upset stomach": "indigestion",
    "heartburn": "acidity",
    "acid reflux": "acidity",
    "gas": "passage_of_gases",
    "farting": "passage_of_gases",
    "bloating": "swelling_of_stomach",

    # Fever / Chills
    "feverish": "mild_fever",
    "temperature": "high_fever",
    "burning up": "high_fever",
    "shaking": "shivering",
    "feeling cold": "chills",
    "freezing": "chills",
    "cold sweats": "sweating",

    # Skin / Rash / Itching
    "itchy": "itching",
    "scratching": "itching",
    "hives": "skin_rash",
    "red spots": "red_spots_over_body",
    "pimples": "pus_filled_pimples",
    "acne": "pus_filled_pimples",
    "peeling skin": "skin_peeling",
    "skin falling off": "skin_peeling",
    "bruised": "bruising",
    "black and blue": "bruising",
    "yellow skin": "yellowish_skin",
    "jaundice": "yellowish_skin",
    "zits": "pus_filled_pimples",
    "blisters": "blister",
    
    # Muscle / Joint / Body pain
    "muscle ache": "muscle_pain",
    "muscles hurt": "muscle_pain",
    "sore muscles": "muscle_pain",
    "body ache": "muscle_pain",
    "joint hurts": "joint_pain",
    "aching joints": "joint_pain",
    "back hurts": "back_pain",
    "lower back pain": "back_pain",
    "neck hurts": "neck_pain",
    "knee hurts": "knee_pain",
    "legs swollen": "swollen_legs",
    "weak muscles": "muscle_weakness",
    "can't move easily": "movement_stiffness",
    "stiff joints": "swelling_joints",

    # Fatigue / Weakness
    "tired": "fatigue",
    "exhausted": "fatigue",
    "worn out": "fatigue",
    "no energy": "lethargy",
    "sluggish": "lethargy",
    "feeling weak": "weakness_in_limbs",
    "fainting": "dizziness",
    "lightheaded": "dizziness",
    "room spinning": "spinning_movements",
    "can't balance": "loss_of_balance",

    # Respiratory / Throat / Nose
    "can't breathe": "breathlessness",
    "short of breath": "breathlessness",
    "sneezing": "continuous_sneezing",
    "stuffy nose": "congestion",
    "blocked nose": "congestion",
    "snotty nose": "runny_nose",
    "sore throat": "throat_irritation",
    "throat hurts": "throat_irritation",
    "coughing": "cough",
    "spitting blood": "blood_in_sputum",

    # Eyes
    "eyes hurt": "pain_behind_the_eyes",
    "red eyes": "redness_of_eyes",
    "yellow eyes": "yellowing_of_eyes",
    "blurry vision": "blurred_and_distorted_vision",
    "can't see clearly": "blurred_and_distorted_vision",
    "eyes watering": "watering_from_eyes",
    "teary eyes": "watering_from_eyes",

    # Bowel / Urine
    "can't poop": "constipation",
    "loose motion": "diarrhoea",
    "watery stool": "diarrhoea",
    "blood in poop": "bloody_stool",
    "blood in stool": "bloody_stool",
    "pain when pooping": "pain_during_bowel_movements",
    "burning pee": "burning_micturition",
    "pain when peeing": "burning_micturition",
    "peeing a lot": "polyuria",
    "dark pee": "dark_urine",
    "yellow pee": "yellow_urine",

    # Appetite / Weight
    "not hungry": "loss_of_appetite",
    "don't want to eat": "loss_of_appetite",
    "eating a lot": "excessive_hunger",
    "always hungry": "excessive_hunger",
    "gaining weight": "weight_gain",
    "getting fat": "weight_gain",
    "losing weight": "weight_loss",
    "getting thin": "weight_loss",

    # Mental / Mood
    "depressed": "depression",
    "sad": "depression",
    "nervous": "anxiety",
    "anxious": "anxiety",
    "moody": "mood_swings",
    "angry easily": "irritability",
    "can't focus": "lack_of_concentration",

    # Heart
    "heart beating fast": "fast_heart_rate",
    "heart pounding": "palpitations",
    "chest hurts": "chest_pain"
}

def extract_symptoms(text):
    text_lower = text.lower()
    extracted = set()
    
    # 1. First, check direct matches and clean up text
    for symptom in symptom_dataset:
        symptom_clean = symptom.replace("_", " ").strip()
        if symptom_clean in text_lower:
            extracted.add(symptom)
            # Remove the found symptom text to prevent over-matching later
            text_lower = text_lower.replace(symptom_clean, " ")
            
    # 2. Check hardcoded synonyms
    for phrase, mapped_symptom in synonym_map.items():
        if phrase in text_lower:
            extracted.add(mapped_symptom)
            text_lower = text_lower.replace(phrase, " ")

    # 3. Use SpaCy Semantic Similarity for remaining text chunks
    doc = nlp(text_lower)
    
    # We will compute word embeddings similarity for noun chunks
    # against the symptom dataset. Note: similarity matching can be noisy, so we set a high threshold.
    similarity_threshold = 0.8
    symptom_docs = {s: nlp(s.replace("_", " ")) for s in symptom_dataset if s not in extracted}
    
    for chunk in doc.noun_chunks:
        if not chunk.text.strip():
            continue
        best_match = None
        best_score = 0
        
        for symptom, s_doc in symptom_docs.items():
            if chunk.vector_norm and s_doc.vector_norm:
                score = chunk.similarity(s_doc)
                if score > best_score:
                    best_score = score
                    best_match = symptom
        
        if best_match and best_score >= similarity_threshold:
            extracted.add(best_match)

    return list(extracted)

if __name__ == "__main__":
    print("-" * 50)
    print("Welcome to the Symptom Extractor!")
    print("Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nDescribe how you are feeling: ")
            if user_input.lower().strip() == 'exit':
                break
                
            symptoms = extract_symptoms(user_input)
            if symptoms:
                print(f"Extracted Symptoms: {', '.join(symptoms)}")
            else:
                print("Could not extract any clear symptoms from your description.")
        except EOFError:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break