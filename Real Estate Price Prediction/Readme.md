# 🏠 Real Estate Price Prediction (End-to-End ML Project)

An end-to-end machine learning project that predicts house prices in **Bengaluru** based on property features.  
The project covers the complete data science lifecycle — from data preprocessing and model training to deploying the model as a **RESTful API using FastAPI**.

---

## 📌 Project Overview

This project aims to estimate real estate prices using historical housing data and serve predictions through a production-ready backend API.  
It demonstrates how machine learning models can be integrated into real-world applications.

---

## 🚀 What I Built

### 🔍 Machine Learning & Data Science
During model building, the following core **data science concepts** were applied:

- Data loading and data cleaning  
- Outlier detection and removal  
- Feature engineering  
- Dimensionality reduction  
- Model selection and evaluation  
- Hyperparameter tuning using **GridSearchCV**  
- Model validation using **k-fold cross-validation**  

A regression model was trained and evaluated to achieve reliable price predictions.

---

### ⚙️ Backend & Deployment
- Deployed the trained model as a **RESTful API using FastAPI**
- Implemented input validation using **Pydantic**
- Returned real-time house price predictions in JSON format
- Enabled **CORS** to support frontend integration
- Built a simple **web client (HTML/CSS/JavaScript)** for testing and interaction
- Serialized trained model and feature metadata for reproducible inference

---

## 🧠 Features

- Predict house prices based on:
  - Total square feet
  - Number of bedrooms
  - Number of bathrooms
  - Number of balconies
  - Location
- Fetch supported locations dynamically
- Clean and structured API responses
- Ready for frontend or third-party integration

---

## 🛠 Tech Stack

- **Programming Language:** Python  
- **Backend:** FastAPI  
- **Machine Learning:** scikit-learn  
- **Data Processing:** NumPy, Pandas  
- **Validation:** Pydantic  
- **Model Training:** Jupyter Notebook  
- **Frontend (Testing):** HTML, CSS, JavaScript  

---

## 📡 API Endpoints

### Get available locations
```
GET /get_location_names
```

### Predict house price
```
POST /predict_home_price
```

**Request Body Example:**
```json
{
  "total_sqft": 1200,
  "balcony": 1,
  "bedroom": 2,
  "bath": 2,
  "location": "whitefield"
}
```

**Response Example:**
```json
{
  "estimated_price": 85.75
}
```

---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 2️⃣ Start the FastAPI server
```bash
uvicorn main:app --reload
```

### 3️⃣ Open the client
Open `Client/app.html` in your browser to test predictions.

---

## 📈 Future Improvements

- Add unit and integration tests
- Cache model artifacts on application startup
- Containerize the application using Docker
- Add authentication and rate limiting
- Deploy on a cloud platform (AWS / GCP / Azure)

---

## 🙏 Acknowledgements

Some concepts and best practices used in this project were learned from online learning resources, including the **Codebasics YouTube channel**.

---

⭐ If you like this project, consider giving it a star!
