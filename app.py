import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
import time
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Insider Threat Detection System",
    page_icon="🛡️",
    layout="wide"
)
st.markdown("""
<style>

.main{
    background-color:#F4F7FC;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

h1{
    color:#0E4C92;
    text-align:center;
    font-weight:bold;
}

h2,h3{
    color:#0E4C92;
}

div.stButton > button{
    width:100%;
    background:#0E4C92;
    color:white;
    border-radius:12px;
    border:none;
    font-size:18px;
    font-weight:bold;
    height:3.2em;
}

div.stButton > button:hover{
    background:#1565C0;
    color:white;
}

[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.15);
}

[data-testid="stSidebar"]{
    background-color:#0E4C92;
}

[data-testid="stSidebar"] *{
    color:white;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

.main{
    background: #f5f7fb;
}

.main h1{
    color:#0E4C92;
}

.header-box{
    background:linear-gradient(90deg,#0E4C92,#1976D2);
    padding:25px;
    border-radius:15px;
    color:white;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.25);
    margin-bottom:20px;
}

.header-box h1{
    color:white;
    margin-bottom:8px;
}

.header-box p{
    font-size:18px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">

<h1>🛡️ Insider Threat Detection System</h1>

<p>AI Powered Insider Threat Detection using Machine Learning</p>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#f5f7fb;
}

.block-container{
    padding-top:2rem;
}

h1{
    color:#0E4C92;
    text-align:center;
}

[data-testid="stMetric"]{
    background:white;
    color:black !important;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.15);
}

[data-testid="stMetric"] *{
    color:black !important;
}

[data-testid="stMetricLabel"]{
    color:black !important;
}

[data-testid="stMetricValue"]{
    color:black !important;
    font-weight:bold;
    font-size:28px;
}

div.stButton > button{
    width:100%;
    height:3.2em;
    border-radius:10px;
    font-size:18px;
    font-weight:bold;
    background:#0E4C92;
    color:white;
}

div.stButton > button:hover{
    background:#1565C0;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------



st.markdown("---")

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)

model_path = os.path.join(
    project_dir,
    "models",
    "random_forest_model.pkl"
)

model = joblib.load(model_path)

st.success("✅ AI Model Loaded Successfully")

st.markdown("---")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

# -----------------------------
# PROFESSIONAL SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("""
    <style>

    .sidebar-title{
        font-size:28px;
        font-weight:bold;
        color:#0E4C92;
        text-align:center;
    }

    .sidebar-card{
        background:white;
        padding:15px;
        border-radius:15px;
        box-shadow:0px 3px 10px rgba(0,0,0,0.15);
        margin-bottom:15px;
    }

    </style>
    """, unsafe_allow_html=True)



    st.markdown("---")

    st.sidebar.info("""
        📌 TITLE:-

        • An Automated Threat Intelligence Framework for Insider Threat Detection.

        """)


    st.sidebar.info("""
        🎓 Technology Used

        • Python
        • Streamlit
        • Pandas
        • Plotly
        • Scikit-learn
        • Random Forest
        """)

    st.sidebar.info("""
        🏫 Computer Science & Engineering (B.Tech)

        [FINAL YEAR PROJECT]


        GROUP:- GC-5


        GUIDE:- Prof. Sapana G. Nandanwar
        """)


    

    st.markdown("---")

    st.subheader("👨‍💻 Developed By")

    st.write("""
• Vinay Nikhar

• Vishal Jadahv

• Saurabh Mohod

• Nandini Pund

• Prachi Dahapute
""")

    st.markdown("---")

    st.info("B.Tech Final Year Project")

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload Feature CSV File",
    type=["csv"]
)

# ---------------------------------------------------
# READ CSV
# ---------------------------------------------------

if uploaded_file is not None:

    try:
        data = pd.read_csv(uploaded_file)
    except Exception:
        st.error("❌ Invalid or Corrupted CSV File. Please upload a valid CSV.")
        st.stop()

    required_columns = [
        "user",
        "login_count",
        "logoff_count",
        "usb_connect_count",
        "usb_disconnect_count",
        "email_count",
        "file_activity_count",
        "unique_pc_count",
        "after_hours_login",
        "weekend_activity",
        "attachment_count"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:

        st.error(
            "❌ Invalid CSV File!\n\nMissing Columns:\n"
            + ", ".join(missing_columns)
        )

        st.stop()

    if data.empty:
        st.error("❌ Uploaded CSV is empty.")
        st.stop()


    st.subheader("📄 Uploaded Data")
    st.dataframe(data)

    st.markdown("---")

    # ---------------------------------------------------
    # PREDICT BUTTON
    # ---------------------------------------------------

    if st.button("🚀 Predict"):

        with st.spinner("🤖 AI Model is Predicting..."):

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # ---------------------------------------------
            # MODEL PREDICTION
            # ---------------------------------------------

            X = data.drop(columns=["user"])

            prediction = model.predict(X)

            result = data.copy()

            result["Prediction"] = prediction

            result["Prediction"] = result["Prediction"].replace(
                {
                    0: "🟢 Normal User",
                    1: "🔴 Insider Threat"
                }
            )

            st.success("✅ Prediction Completed Successfully")

            current_time = datetime.now().strftime("%d %B %Y | %I:%M %p")
            st.info(f"🕒 Prediction Generated On: {current_time}")

            st.subheader("📋 Prediction Results")

            def highlight_prediction(row):

                if row["Prediction"] == "🔴 Insider Threat":

                    return [
                        "background-color:#ffb3b3; color:black; font-weight:bold;"
                    ] * len(row)

                else:

                    return [
                        "background-color:#b6fcb6; color:black; font-weight:bold;"
                    ] * len(row)

            st.dataframe(
                result.style.apply(
                    highlight_prediction,
                    axis=1
                ),
                use_container_width=True
            )

            st.markdown("---")

            # ---------------------------------------------
            # DASHBOARD METRICS
            # ---------------------------------------------

            total_users = len(result)

            normal_users = (
                result["Prediction"] == "🟢 Normal User"
            ).sum()

            insider_users = (
                result["Prediction"] == "🔴 Insider Threat"
            ).sum()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                label="👥 Total Users",
                value=total_users,
                delta="Uploaded"
            )

            col2.metric(
                label="🟢 Normal Users",
                value=normal_users,
                delta="Safe"
            )

            col3.metric(
                label="🔴 Insider Threats",
                value=insider_users,
                delta="Detected"
            )


            st.markdown("---")


            # ---------------------------------------------------
            # PIE CHART
            # ---------------------------------------------------

            st.subheader("📊 Prediction Distribution")

            pie_data = pd.DataFrame({
                "Category": [
                    "Normal Users",
                    "Insider Threats"
                ],
                "Count": [
                    normal_users,
                    insider_users
                ]
            })

            fig1 = px.pie(
                pie_data,
                names="Category",
                values="Count",
                title="Prediction Distribution",
                hole=0.45,
                color="Category",
                color_discrete_map={
                    "Normal Users": "#2ecc71",
                    "Insider Threats": "#e74c3c"
                }
            )

            fig1.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            st.markdown("---")

            # ---------------------------------------------------
            # BAR CHART
            # ---------------------------------------------------

            st.subheader("📈 User Count")

            fig2 = px.bar(
                pie_data,
                x="Category",
                y="Count",
                text="Count",
                title="Normal vs Insider Threat Users",
                color="Category",
                color_discrete_map={
                    "Normal Users": "#2ecc71",
                    "Insider Threats": "#e74c3c"
                }
            )

            fig2.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            st.markdown("---")

            # ---------------------------------------------------
            # SHOW ONLY INSIDER THREATS
            # ---------------------------------------------------

            st.subheader("🚨 Insider Threat Users")

            threat_users = result[
                result["Prediction"] == "🔴 Insider Threat"
            ]

            if len(threat_users) > 0:
                st.dataframe(threat_users)
            else:
                st.success("✅ No Insider Threat Detected")

            st.markdown("---")

            # ---------------------------------------------------
            # DOWNLOAD RESULT
            # ---------------------------------------------------

            csv = result.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download Prediction Report (CSV)",
                data=csv,
                file_name="Insider_Threat_Prediction_Report.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("---")

            st.subheader("📋 Prediction Summary")

            threat_percentage = round(
                (insider_users / total_users) * 100,
                2
            )

            safe_percentage = round(
                (normal_users / total_users) * 100,
                2
            )

            summary = pd.DataFrame({
                "Metric": [
                    "👥 Total Users",
                    "🟢 Normal Users",
                    "🔴 Insider Threats",
                    "🛡 Safe %",
                    "⚠ Threat %"
                ],
                "Value": [
                    total_users,
                    normal_users,
                    insider_users,
                    f"{safe_percentage}%",
                    f"{threat_percentage}%"
                ]
            })

            st.table(summary)

            if insider_users > 0:

                st.error(
                    f"🚨 ALERT : {insider_users} Insider Threat(s) Detected!"
                )

            else:

                st.success(
                    "✅ No Insider Threat Detected."
                )

            st.markdown("---")


            # ---------------------------------------------------
            # SEARCH USER
            # ---------------------------------------------------

            st.markdown("---")

            st.subheader("🔍 Search User")

            search_user = st.text_input("Enter User ID")

            if search_user.strip():

                user_data = result[
                    result["user"].astype(str).str.strip().str.lower() ==
                    search_user.strip().lower()
                ]

                if not user_data.empty:
                    st.success("✅ User Found")
                    st.dataframe(user_data)
                else:
                    st.warning("⚠ User Not Found")

            st.markdown("---")

            

            st.markdown("---")

            # ---------------------------------------------------
            # ALERT MESSAGE
            # ---------------------------------------------------

            if insider_users > 0:

                st.error(
                    f"🚨 Warning! {insider_users} Insider Threat(s) Detected."
                )

            else:

                st.success(
                    "✅ All Users are Safe."
                )

            st.markdown("---")


            # ---------------------------------------------------
            # ANALYSIS COMPLETED
            # ---------------------------------------------------

            st.success("✅ Analysis Completed Successfully")

            st.info("""
# 👋 Welcome

### AI Based Insider Threat Detection System

This application uses a Machine Learning model to detect Insider Threats from uploaded user activity data.

### Steps

1️⃣ Upload CSV File

2️⃣ Click **🚀 Predict**

3️⃣ View Dashboard

4️⃣ Analyze Results

5️⃣ Download Prediction Report
""")

            # ---------------------------------------------------
            # FOOTER
            # ---------------------------------------------------

            st.markdown("---")

            st.markdown(
                """
                <center>

                <h4>🛡️ AI Based Insider Threat Detection System</h4>

                <b>Department of Computer Science & Engineering</b>

                <br>

                B.Tech Final Year Project

                <br><br>

                <b>Developed By</b>

                <br><br>

                Vinay Nikhar |
                Vishal Jadhav |
                Saurabh Mohod

                <br>

                Nandini Pund |
                Prachi Dahapute

                <br><br>

                © 2026 All Rights Reserved

                </center>
                """,
                unsafe_allow_html=True
            )