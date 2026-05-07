import os
import sys
import pandas as pd

DATA_PATH = "data/patient_risk.csv"

required_columns = [
    "patient_id",
    "age",
    "gender",
    "blood_pressure",
    "cholesterol",
    "diabetes",
    "risk_score",
    "timestamp"
]

def fail(message):
    print(f"DATA VALIDATION FAILED: {message}")
    sys.exit(1)

if not os.path.exists(DATA_PATH):
    fail(f"Dataset not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    fail(f"Missing columns: {missing_columns}")

if df.empty:
    fail("Dataset is empty")

if df.isnull().sum().sum() > 0:
    fail("Dataset contains missing values")

if not pd.api.types.is_numeric_dtype(df["age"]):
    fail("age column must be numeric")

if not pd.api.types.is_numeric_dtype(df["risk_score"]):
    fail("risk_score column must be numeric")

if (df["age"] < 0).any():
    fail("age column contains invalid negative values")

if ((df["risk_score"] < 0) | (df["risk_score"] > 1)).any():
    fail("risk_score must be between 0 and 1")

print("Data validation passed successfully.")