# 🛡️ Insider Threat Detection Platform

An Automated Threat Intelligence Framework for Insider Threat Detection — using behavioral analytics and machine learning to identify users whose activity patterns deviate from normal organizational behavior.

## 📌 Project Overview

This project detects potential insider threats by analyzing user behavior logs (logins, USB usage, email activity, file access) and classifying users as Normal or Insider Threat using a Random Forest model. The system includes explainable AI (reason codes) and an interactive Streamlit dashboard for real-time threat analysis.

## 🎓 Academic Details

- **Project Type:** B.Tech Final Year Project — Computer Science & Engineering
- **Group:** GC-5
- **Guide:** Prof. Sapana G. Nandanwar
- **Team:** Vinay Nikhar, Vishal Jadhav, Saurabh Mohod, Nandini Pund, Prachi Dahapute

## 🧠 Features

- Behavioral feature extraction from raw activity logs (login, USB, email, file access)
- Time-windowed behavioral-drift features (deviation from user's own baseline)
- Random Forest classifier with Stratified 5-Fold Cross-Validation
- Explainable AI — human-readable reason codes for each flagged prediction
- Risk scoring (0–100%) with Low/Medium/High risk levels
- Interactive Streamlit dashboard with single-user lookup and batch CSV analysis

## 🛠️ Tech Stack

Python · Pandas · Scikit-learn (Random Forest) · Streamlit · Plotly · NumPy

## 📊 Dataset

CMU CERT Insider Threat Dataset (r6.2) — includes logon, device, email, file, and psychometric logs for 1000 users.

## 🖥️ Screenshots

### Dashboard
![Dashboard](<img width="742" height="767" alt="image" src="https://github.com/user-attachments/assets/9782c3e9-934c-4128-a978-64d9a88c08ca" />
)

### Single User Lookup
![User Lookup](<img width="495" height="672" alt="image" src="https://github.com/user-attachments/assets/b52d24ea-e7da-4857-83c3-11c65dc762fb" />)


### Batch Threat Analysis
![Batch Analysis](<img width="501" height="736" alt="Screenshot 2026-09-10 233422" src="https://github.com/user-attachments/assets/558c25e4-29b5-4707-a71b-8457764dda69" />
)

### Model Insights
![Model Insights](<img width="732" height="830" alt="image" src="https://github.com/user-attachments/assets/be2c24f6-ef16-4521-be90-0104ad32525c" />
)

## 📂 Project Structure

notebooks/ → Data understanding, preprocessing, feature engineering, model building, testing
Dataset/ → Processed feature datasets
models/ → Trained model, baseline data, metadata
app.py → Streamlit web application


## ⚙️ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the notebooks in order (01 → 05) to regenerate features and train the model

# Launch the app
streamlit run app.py
```

## 📈 Model Performance

Validated using Stratified 5-Fold Cross-Validation — train-test gap under 2%, confirming the model generalizes well and is not overfitting.

## 🔬 Research Gap Addressed

Existing insider threat detection systems rely on static, aggregate behavioral counts and non-interpretable classifiers. This project addresses this gap through:
- Behavioral-drift features capturing deviation from a user's own historical baseline
- An explainability layer providing analyst-readable reasoning for each prediction

## 📜 License

This project is for academic purposes only.
