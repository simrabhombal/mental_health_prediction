import joblib
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

df = pd.read_csv("C://Users/PARVEZ BHOMBAL/OneDrive/Desktop/arogo-assessment/mental_health_analysis/depression_anxiety_data.csv")

# Handle missing values
categorical_cols = ['depression_severity', 'depressiveness', 'suicidal', 'depression_diagnosis',
                    'depression_treatment', 'anxiousness', 'anxiety_diagnosis', 'anxiety_treatment', 'sleepiness']
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])  # Fill categorical with mode
df['epworth_score'] = df['epworth_score'].fillna(df['epworth_score'].median())

# Encode categorical data
label_encoders = {}
for col in categorical_cols + ['gender', 'who_bmi', 'anxiety_severity', 'depression_severity']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
target = 'depression_severity'
X = df.drop(columns=['id', target])
y = df[target]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel='rbf', probability=True)
}

# Train models
best_model, best_accuracy = None, 0
for name, model in models.items():
    accuracy = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").mean()
    print(f"{name} CV Accuracy: {accuracy:.4f}")
    model.fit(X_train, y_train) 
    test_accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"{name} Test Accuracy: {test_accuracy:.4f}")
    if test_accuracy > best_accuracy:
        best_model, best_accuracy = model, test_accuracy

# Save best model
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(best_model, "randf.pkl")
print("✅ Best Model Saved")

# Call LLM API
def get_llm_explanation(condition):
    try:
        url = "http://127.0.0.1:5000/explain"
        response = requests.post(url, json={"condition": str(condition)})
        return response.json().get("explanation", "No explanation available.")
    except Exception as e:
        return f"API Error: {str(e)}"

# Predict function
def predict_mental_health(symptoms):
    model = joblib.load("randf.pkl")
    input_data = pd.DataFrame([symptoms], columns=X.columns)
    prediction = model.predict(input_data)[0]
    condition_map = {0: "Mild", 1: "None-minimal", 2: "Moderate", 3: "Moderately severe", 4: "Severe", 5: "None"}
    condition = condition_map.get(prediction, "Unknown")
    explanation = get_llm_explanation(condition)
    return condition, explanation

# Example prediction
example_input = X_test.iloc[0].values
predicted_condition, explanation = predict_mental_health(example_input)

print(f"🔹 Predicted Condition: {predicted_condition}")
print(f"🔹 LLM Explanation: {explanation}")

# Print classification report
print("\nClassification Report:")
print(classification_report(y_test, best_model.predict(X_test)))
