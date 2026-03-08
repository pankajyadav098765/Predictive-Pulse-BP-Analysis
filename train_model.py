import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

df = pd.read_csv('clean_blood_pressure_dataset.csv')

# The 10 features from your screenshot
features = [
    'Gender', 'Age_Group', 'Family_HX', 'Med_Care', 'BP_Meds', 
    'Symptom_Score', 'Short_Breath', 'Vision_Chg', 'Nosebleeds', 'Healthy_Diet'
]

X = df[features]
y = df[['Systolic', 'Diastolic']]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

with open('bp_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Professional 10-Input Model Trained Successfully!")