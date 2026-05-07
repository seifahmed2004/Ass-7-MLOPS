import os
import sys
import pandas as pd

DATA_PATH = "data/Titanic-Dataset.csv"

required_columns = [
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked"
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

if df.shape[0] < 100:
    fail("Dataset has too few rows")

if df.shape[1] < 8:
    fail("Dataset must contain at least 8 columns")

if df["PassengerId"].duplicated().any():
    fail("PassengerId contains duplicate values")

if not df["Survived"].isin([0, 1]).all():
    fail("Survived column must contain only 0 or 1")

if not df["Pclass"].isin([1, 2, 3]).all():
    fail("Pclass column must contain only 1, 2, or 3")

if not pd.api.types.is_numeric_dtype(df["Age"]):
    fail("Age column must be numeric")

if not pd.api.types.is_numeric_dtype(df["Fare"]):
    fail("Fare column must be numeric")

if (df["Age"].dropna() < 0).any():
    fail("Age column contains invalid negative values")

if (df["Fare"].dropna() < 0).any():
    fail("Fare column contains invalid negative values")

if df["Survived"].isnull().sum() > 0:
    fail("Target column Survived contains missing values")

if df["Sex"].isnull().sum() > 0:
    fail("Sex column contains missing values")

print("Data validation passed successfully.")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Missing values found but allowed in non-critical columns:")
print(df.isnull().sum())