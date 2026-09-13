import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

import joblib


# 1. Load the dataset
df = pd.read_csv("data/defence_scenario_data.csv")

print("Dataset loaded successfully!")
print("Number of rows:", len(df))


# 2. Select input features
X = df[
    [
        "weather",
        "visibility",
        "equipment_readiness",
        "communication",
        "resource_availability",
        "terrain"
    ]
]


# 3. Select the target
y = df["scenario_risk"]


# 4. Identify categorical and numerical columns
categorical_features = [
    "weather",
    "terrain"
]

numerical_features = [
    "visibility",
    "equipment_readiness",
    "communication",
    "resource_availability"
]


# 5. Convert text values into numbers
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# 6. Create the Machine Learning model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# 7. Create complete ML pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# 8. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("Training data:", len(X_train))
print("Testing data:", len(X_test))


# 9. Train the model
pipeline.fit(X_train, y_train)

print("Model training completed!")


# 10. Make predictions
y_pred = pipeline.predict(X_test)


# 11. Check accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")


# 12. Display detailed results
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# 13. Save the trained model
joblib.dump(
    pipeline,
    "models/scenario_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/scenario_model.pkl")