import streamlit as st
import pandas as pd
import joblib

# Dummy function to avoid joblib error
def binary_cleanup(x): return x

# Load model
model = joblib.load("attrition_model.joblib")

st.title("💼 Employee Attrition Predictor")

# Categorical inputs (keep as strings)
categorical_features = {
    'MaritalStatus': ['Single', 'Married', 'Divorced'],
    'BusinessTravel': ['Travel_Rarely', 'Travel_Frequently', 'Non-Travel'],
    'Department': ['Sales', 'Research & Development', 'Human Resources'],
    'EducationField': ['Life Sciences', 'Other', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources'],
    'JobRole': [
        'Sales Executive', 'Research Scientist', 'Laboratory Technician',
        'Manufacturing Director', 'Healthcare Representative', 'Manager',
        'Sales Representative', 'Research Director', 'Human Resources'
    ]
}

# Gender and OverTime need to be numeric (as per your binary_cleanup)
binary_map = {
    'Gender': {'Male': 1, 'Female': 0},
    'OverTime': {'Yes': 1, 'No': 0}
}

# Fixed fields
fixed_values = {
    'EmployeeCount': 1,
    'EmployeeNumber': 1,
    'Over18': 'Y',
    'StandardHours': 80
}

# Numerical inputs
numerical_fields = [
    'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
    'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome',
    'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
    'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
    'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
    'YearsWithCurrManager'
]

# Input collection
inputs = {}

# Gender and OverTime (convert to numeric)
for col, mapping in binary_map.items():
    choice = st.selectbox(f"{col}:", list(mapping.keys()))
    inputs[col] = mapping[choice]

# All other categorical features (send as string)
for feature, options in categorical_features.items():
    inputs[feature] = st.selectbox(f"{feature}:", options)

# Numerical features
for feature in numerical_fields:
    inputs[feature] = st.number_input(f"{feature}:", value=0)

# Add fixed values
inputs.update(fixed_values)

# Predict
if st.button("Predict"):
    df = pd.DataFrame([inputs])
    prediction = model.predict(df)[0]
    if prediction == 1:
        st.error("🔴 This employee is likely to leave.")
    else:
        st.success("🟢 This employee is likely to stay.")
