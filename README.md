## **Self-Analysis Mental Health Model 🧠**  

This project predicts mental health conditions based on user-provided symptoms using a **machine learning model (Random Forest/SVM)** and provides explanations with **Gemini AI**. It also generates **PDF reports** summarizing the condition and coping strategies.  

---

## **🚀 Features**  

✅ Predicts mental health conditions (Mild, Moderate, Severe, etc.)  
✅ Uses **Random Forest/SVM** for classification  
✅ Calls **Gemini AI** to explain the condition and suggest coping strategies  
✅ Generates a **PDF report** for easy reference  

---

## **📁 Project Structure**  

```
mental_health_analysis/
│── api.py                 # Flask API for Gemini LLM
│── predict_mental_health.py  # ML model prediction
│── depression_anxiety_data.csv  # Dataset
│── randf.pkl               # Trained model file
│── label_encoders.pkl      # Encoders for categorical data
│── README.md               # Project documentation
│── requirements.txt        # Dependencies
```

---

## **🔧 Setup Instructions**  

### **1️⃣ Install Dependencies**  
Run the following command to install required libraries:  

```bash
pip install -r requirements.txt
```

### **2️⃣ Start the Flask API**  
Run the API to enable LLM explanations:  

```bash
python api.py
```

### **3️⃣ Make a Prediction**  
Run the prediction script with sample input:  

```bash
python predict_mental_health.py
```

OR send a request manually:  

```bash
curl -X POST http://127.0.0.1:5000/explain -H "Content-Type: application/json" -d '{"condition": "Moderate"}'
```

---

## **🧠 Machine Learning Model**  

- Uses **Random Forest** and **SVM** trained on `depression_anxiety_data.csv`.  
- Encodes categorical data using **LabelEncoder**.  
- Selects the best model based on **cross-validation accuracy**.  
- Saves the trained model in `randf.pkl`.  

---

## **🔗 API Endpoints**  

### **1️⃣ LLM Explanation API**  
- **Endpoint:** `/explain`  
- **Method:** `POST`  
- **Input:** `{ "condition": "Moderate depression" }`  
- **Output:**  
  ```json
  {
    "explanation": "Moderate depression involves persistent sadness and loss of interest. Suggested coping strategies include therapy, mindfulness, and physical activity."
  }
  ```

---

## **📜 PDF Report Generation**  
When a user requests an explanation, a **PDF file** is automatically generated summarizing:  
✔ **Condition Name**  
✔ **Gemini Explanation**  
✔ **Coping Strategies**  
