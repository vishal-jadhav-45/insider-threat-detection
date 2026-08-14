# 🛡️ AI-Based Insider Threat Detection System

## 📌 Project Overview

This project presents an AI-based Insider Threat Detection System that uses Machine Learning to identify potentially suspicious insider activity from user activity data.

The system uses a Random Forest classification model to classify users into two categories:

- 🟢 Normal User
- 🔴 Insider Threat

The project covers the complete Machine Learning workflow, including data understanding, data preprocessing, feature engineering, model building, testing, and prediction.

## 🎯 Objective

The main objective of this project is to develop a Machine Learning-based system that can analyze user activity patterns and help identify potential insider threats.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Random Forest
- Streamlit
- Plotly
- Joblib
- Jupyter Notebook

## 🤖 Machine Learning Model

### Random Forest Classifier

The project uses a Random Forest classification model for insider threat prediction.

The trained model is saved as:

`random_forest_model.pkl`

## 📊 Features Used

The prediction application uses user activity features including:

- User ID
- Login Count
- Logoff Count
- USB Connect Count
- USB Disconnect Count
- Email Count
- File Activity Count
- Unique PC Count
- After-Hours Login
- Weekend Activity
- Attachment Count

These features are used to identify patterns associated with normal and potentially suspicious user activity.

## 🔄 Project Workflow

```text
Data Understanding
       ↓
Data Preprocessing
       ↓
Feature Engineering
       ↓
Feature Dataset Creation
       ↓
Random Forest Model Training
       ↓
Model Testing & Prediction
       ↓
Streamlit Application
       ↓
Insider Threat Detection

Project Structure
insider-threat-detection/
│
├── 01_Data_Understanding.ipynb
├── 02_Data_Preprocessing.ipynb
├── 03_Feature_Engineering.ipynb
├── 04_Model_Building.ipynb
├── 05_Model_Testing_And_Prediction.ipynb
│
├── app.py
├── random_forest_model.pkl
├── final_features.csv
├── insiders.csv
└── README.md


🖥️ Streamlit Application

The project includes an interactive Streamlit application that allows users to:

Upload a feature CSV file.
Validate the required columns.
Run predictions using the trained Random Forest model.
View prediction results.
View total users, normal users, and detected insider threats.
Visualize prediction distribution using charts.
View detected insider threat users.
Search for a specific User ID.
Download the prediction report as a CSV file.
📋 Prediction Output

The system classifies users as:

🟢 Normal User

or

🔴 Insider Threat

The application also provides summary metrics and visualizations to help analyze the prediction results.

🎓 Academic Project

Project Type: B.Tech Final Year Major Project
Domain: Machine Learning / Cybersecurity
Model: Random Forest Classifier
Application: Streamlit

👨‍💻 Team
Vinay Nikhar
Vishal Jadhav
Saurabh Mohod
Nandini Pund
Prachi Dahapute
🚀 Future Improvements
Real-time user activity monitoring
Advanced anomaly detection techniques
Model optimization and hyperparameter tuning
Real-time alert and notification system
Cloud deployment
Integration with enterprise security systems

📌 Disclaimer
This project is developed for academic and educational purposes to demonstrate the application of Machine Learning techniques for insider threat detection.
