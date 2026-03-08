from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('bp_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Helper to convert "Yes/No" to 1/0
    def bin(key): return 1 if request.form.get(key) == 'Yes' else 0
    
    # Capture all 10 inputs
    gender = 1 if request.form.get('gender') == 'Male' else 0
    age_group = int(request.form.get('age_group', 1))
    symptom_score = int(request.form.get('symptom_severity', 0))
    
    inputs = [
        gender, age_group, bin('family_history'), bin('medical_care'),
        bin('bp_meds'), symptom_score, bin('shortness_breath'),
        bin('vision_changes'), bin('nosebleeds'), bin('healthy_diet')
    ]
    
    prediction = model.predict([inputs])
    sys, dia = int(prediction[0][0]), int(prediction[0][1])

    # Risk Assessment Logic matching the screenshot guidelines
    if sys >= 180 or dia >= 120:
        stage, color, advice = "Hypertensive Crisis", "danger", "EMERGENCY: Seek immediate medical attention."
    elif sys >= 140 or dia >= 90:
        stage, color, advice = "Hypertension Stage 2", "danger", "High Risk: Consult your physician immediately."
    elif sys >= 130 or dia >= 80:
        stage, color, advice = "Hypertension Stage 1", "warning", "Moderate Risk: Regular monitoring and lifestyle changes needed."
    elif sys >= 120:
        stage, color, advice = "Elevated Blood Pressure", "info", "Increased Risk: Focus on diet and exercise."
    else:
        stage, color, advice = "Normal Blood Pressure", "success", "Healthy: Maintain your current heart-healthy habits."

    return render_template('index.html', stage=stage, color=color, advice=advice, sys=sys, dia=dia, scroll="results")

if __name__ == "__main__":
    app.run(debug=True)