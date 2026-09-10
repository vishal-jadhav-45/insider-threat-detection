import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =====================================================================
# PAGE CONFIG
# =====================================================================

st.set_page_config(
    page_title="Insider Threat Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# GLOBAL THEME / CSS  (Industry-grade dark theme)
# =====================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(ellipse at 15% 0%, #0f1b33 0%, #0a1120 40%, #060a12 100%);
    color: #E7ECF5;
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 3.5rem;
    max-width: 1320px;
}

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(125deg, #0B2E5E 0%, #123B7A 40%, #1a5bb8 100%);
    border-radius: 18px;
    padding: 32px 38px;
    box-shadow: 0 12px 40px rgba(10, 30, 70, 0.55);
    border: 1px solid rgba(255,255,255,0.09);
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute; right: -50px; top: -50px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
}
.hero h1 {
    color: #FFFFFF; font-size: 30px; font-weight: 800; margin: 0 0 8px 0;
    letter-spacing: -0.3px;
}
.hero p {
    color: #C5D8FF; font-size: 15px; margin: 0; max-width: 760px; line-height: 1.5;
}
.badge-row { margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap; }
.pill {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(255,255,255,0.10); color: #EAF1FF;
    padding: 5px 13px; border-radius: 999px; font-size: 12px; font-weight: 600;
    border: 1px solid rgba(255,255,255,0.16);
}
.pill.live {
    background: rgba(46,204,113,0.18); color: #7CFFB2;
    border-color: rgba(124,255,178,0.35);
}

/* ---------- KPI cards ---------- */
.kpi-card {
    background: linear-gradient(165deg, rgba(255,255,255,0.06), rgba(255,255,255,0.015));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 16px 18px;
    height: 112px;
    display: flex; flex-direction: column; justify-content: space-between;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: rgba(100,160,255,0.35); }
.kpi-label {
    color: #8BA3C7; font-size: 11.5px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.07em;
}
.kpi-value { color: #FFFFFF; font-size: 26px; font-weight: 800; line-height: 1.1; }
.kpi-sub { color: #6FE3A4; font-size: 11.5px; font-weight: 600; }
.kpi-sub.warn { color: #FF8A8A; }
.kpi-sub.neutral { color: #8BA3C7; }

/* ---------- Section ---------- */
.section-title {
    color: #FFFFFF; font-size: 18px; font-weight: 700;
    margin: 4px 0 6px 0; display: flex; align-items: center; gap: 8px;
}
.section-sub {
    color: #8CA0C4; font-size: 13px; margin-bottom: 14px;
}

/* ---------- Glass card ---------- */
.glass-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}

/* ---------- Risk badges ---------- */
.risk-high {
    background: rgba(255,69,58,0.18); color: #FF8A80;
    padding: 3px 11px; border-radius: 7px; font-weight: 700; font-size: 12px;
    border: 1px solid rgba(255,138,128,0.35);
}
.risk-medium {
    background: rgba(255,196,0,0.16); color: #FFD666;
    padding: 3px 11px; border-radius: 7px; font-weight: 700; font-size: 12px;
    border: 1px solid rgba(255,214,102,0.35);
}
.risk-low {
    background: rgba(46,204,113,0.16); color: #7CFFB2;
    padding: 3px 11px; border-radius: 7px; font-weight: 700; font-size: 12px;
    border: 1px solid rgba(124,255,178,0.35);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1425 0%, #080e1a 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #DCE6F7 !important; }
.sidebar-logo {
    display: flex; align-items: center; gap: 10px; margin-bottom: 4px;
}
.sidebar-logo .icon { font-size: 24px; }
.sidebar-logo .txt { font-size: 15px; font-weight: 800; color: #fff; line-height: 1.2; }
.sidebar-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 11px;
    padding: 11px 13px;
    margin-bottom: 10px;
    font-size: 12.5px;
    line-height: 1.45;
}
.sidebar-card b { color: #8FB8FF; }

/* ---------- Buttons ---------- */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #1C64F2, #3B82F6);
    color: white !important;
    border-radius: 10px;
    border: none;
    font-size: 15px;
    font-weight: 700;
    height: 2.9em;
    box-shadow: 0 5px 16px rgba(28,100,242,0.35);
    transition: all 0.2s;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #1653C7, #2F6FE0);
    box-shadow: 0 7px 20px rgba(28,100,242,0.45);
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.03);
    border: 1.5px dashed rgba(120,160,255,0.38);
    border-radius: 12px;
}

/* ---------- DataFrame ---------- */
[data-testid="stDataFrame"] {
    border-radius: 11px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    font-size: 14px; font-weight: 700; color: #8CA0C4 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
}

/* ---------- Inputs ---------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #E7ECF5 !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 8px !important;
}

/* ---------- Alert boxes ---------- */
.stAlert { border-radius: 10px; }

hr { border-color: rgba(255,255,255,0.07) !important; }

/* ---------- Result card for single user ---------- */
.result-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 24px 26px;
    margin-top: 12px;
}
.result-card.high { border-left: 5px solid #FF453A; }
.result-card.medium { border-left: 5px solid #FFC400; }
.result-card.low { border-left: 5px solid #2ecc71; }

.mode-selector {
    display: flex; gap: 10px; margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# LOAD MODEL + METADATA
# =====================================================================

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
models_dir = os.path.join(project_dir, "models")

# Fallback paths (works both when run from project root or from app folder)
possible_model_paths = [
    os.path.join(models_dir, "random_forest_model.pkl"),
    os.path.join(current_dir, "models", "random_forest_model.pkl"),
    os.path.join(current_dir, "random_forest_model.pkl"),
    "models/random_forest_model.pkl",
]

model = None
model_path_used = None
for p in possible_model_paths:
    if os.path.exists(p):
        try:
            model = joblib.load(p)
            model_path_used = p
            break
        except Exception:
            continue

if model is None:
    st.error(
        "❌ Model file `random_forest_model.pkl` not found.\n\n"
        "Please ensure the model is present in the `models/` folder "
        "(run `04_Model_Building.ipynb` first)."
    )
    st.stop()

baseline_path = os.path.join(os.path.dirname(model_path_used), "normal_baseline.csv")
metadata_path = os.path.join(os.path.dirname(model_path_used), "model_metadata.json")

try:
    normal_baseline = pd.read_csv(baseline_path)
except Exception:
    normal_baseline = None

try:
    with open(metadata_path) as f:
        metadata = json.load(f)
except Exception:
    metadata = None

MODEL_FEATURES = list(model.feature_names_in_)
feature_importances = pd.Series(model.feature_importances_, index=MODEL_FEATURES)


def explain_row(row, top_n=3):
    """Generate human-readable reason codes using ratio-to-normal baseline."""
    if normal_baseline is None:
        return "Baseline unavailable"
    try:
        normal_median = normal_baseline.median().replace(0, 0.5)
        ratio = (row + 1) / (normal_median + 1)
        score = ratio * feature_importances
        top = score.sort_values(ascending=False).head(top_n)
        return "; ".join(
            f"{feat} is {ratio[feat]:.1f}× typical normal user"
            for feat in top.index
        )
    except Exception:
        return "Unable to generate explanation"


def risk_badge_html(level):
    cls = {"High": "risk-high", "Medium": "risk-medium", "Low": "risk-low"}.get(level, "risk-low")
    return f'<span class="{cls}">{level}</span>'


def get_risk_level(proba):
    if proba >= 0.6:
        return "High"
    elif proba >= 0.3:
        return "Medium"
    return "Low"


# =====================================================================
# SIDEBAR
# =====================================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="icon">🛡️</div>
        <div class="txt">Insider Threat<br>Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <b>📌 Project</b><br>
        An Automated Threat Intelligence Framework for Insider Threat Detection
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-card">
        <b>🧠 Model</b><br>
        Random Forest Classifier<br>
        {len(MODEL_FEATURES)} behavioural features<br>
        Stratified 5-fold CV · Explainable
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <b>🎓 Technology Stack</b><br>
        Python · Streamlit · Scikit-learn<br>
        Pandas · Plotly · Random Forest
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <b>🏫 Academic</b><br>
        B.Tech Final Year Project<br>
        Computer Science &amp; Engineering<br>
        Group: GC-5<br>
        Guide: Prof. Sapana G. Nandanwar
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <b>👨‍💻 Developed By</b><br>
        Vinay Nikhar · Vishal Jadhav<br>
        Saurabh Mohod · Nandini Pund<br>
        Prachi Dahapute
    </div>
    """, unsafe_allow_html=True)

    if metadata:
        st.markdown(f"""
        <div class="sidebar-card">
            <b>🕒 Model Last Trained</b><br>
            {metadata.get("trained_on", "N/A")}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v2.0 · Production Ready")

# =====================================================================
# HERO HEADER
# =====================================================================

st.markdown("""
<div class="hero">
    <h1>🛡️ Insider Threat Intelligence Platform</h1>
    <p>
        Enterprise-grade behavioural analytics for detecting insider threats from user activity logs.
        Cross-validated risk scoring with transparent, analyst-ready reason codes.
    </p>
    <div class="badge-row">
        <span class="pill live">● Model Loaded</span>
        <span class="pill">Random Forest</span>
        <span class="pill">Explainable AI</span>
        <span class="pill">Batch + Single User</span>
        <span class="pill">Risk Scoring</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# TABS
# =====================================================================

tab_dashboard, tab_predict, tab_insights, tab_about = st.tabs(
    ["🏠  Dashboard", "🔍  Threat Analysis", "📊  Model Insights", "ℹ️  About"]
)

# ---------------------------------------------------------------------
# TAB 1 — DASHBOARD
# ---------------------------------------------------------------------
with tab_dashboard:

    if metadata:
        test_acc = metadata["cv_metrics"]["accuracy"]["test_mean"] * 100
        test_recall = metadata["cv_metrics"]["recall"]["test_mean"] * 100
        n_samples = metadata.get("n_samples", "—")
        n_insider = metadata.get("n_insider", "—")
    else:
        test_acc = test_recall = n_samples = n_insider = None

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Users Monitored</div>
            <div class="kpi-value">{n_samples if n_samples is not None else "—"}</div>
            <div class="kpi-sub neutral">Training population</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Validated Accuracy</div>
            <div class="kpi-value">{f"{test_acc:.1f}%" if test_acc else "—"}</div>
            <div class="kpi-sub">5-fold cross-validated</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Threat Recall</div>
            <div class="kpi-value">{f"{test_recall:.1f}%" if test_recall else "—"}</div>
            <div class="kpi-sub">Insiders correctly flagged</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Features Analysed</div>
            <div class="kpi-value">{len(MODEL_FEATURES)}</div>
            <div class="kpi-sub neutral">Behavioural signals</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    colL, colR = st.columns([1.35, 1])

    with colL:
        st.markdown('<div class="section-title">🧭 How This Platform Works</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
        <b>1. Behavioural Feature Extraction</b><br>
        Login patterns, USB activity, email behaviour, file access and drift-based signals
        are aggregated per user from raw activity logs.<br><br>
        <b>2. Machine Learning Classification</b><br>
        A regularised Random Forest (stratified 5-fold CV) scores each user's likelihood
        of insider-threat behaviour.<br><br>
        <b>3. Risk Scoring &amp; Explainability</b><br>
        Every user receives a 0–100% risk score and transparent reason codes that highlight
        the exact behaviours driving the alert — no black-box decisions.<br><br>
        <b>4. Analyst Workflow</b><br>
        Security analysts can triage High → Medium → Low risk users, perform single-user
        investigations, or process entire batches from the Threat Analysis tab.
        </div>
        """, unsafe_allow_html=True)

    with colR:
        st.markdown('<div class="section-title">🧬 Feature Set</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        for feat in MODEL_FEATURES:
            st.markdown(f"• `{feat}`")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info("👉 Go to the **🔍 Threat Analysis** tab to upload a CSV or analyse a single user manually.")

# ---------------------------------------------------------------------
# TAB 2 — THREAT ANALYSIS
# ---------------------------------------------------------------------
with tab_predict:

    st.markdown('<div class="section-title">🔍 Threat Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Choose analysis mode — process an entire batch via CSV or investigate a single user manually.</div>',
        unsafe_allow_html=True
    )

    # Mode selector
    analysis_mode = st.radio(
        "Analysis Mode",
        options=["📁 Batch CSV Upload", "👤 Single User Manual Entry"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # =============================================================
    # MODE A — BATCH CSV UPLOAD
    # =============================================================
    if analysis_mode == "📁 Batch CSV Upload":

        st.markdown('<div class="section-title">📂 Upload User Activity Data</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-sub">Upload a CSV containing the required behavioural features. '
            'Download the sample template if you are unsure about the format.</div>',
            unsafe_allow_html=True
        )

        # ---- Required columns info + Sample CSV download ----
        required_columns = ["user"] + MODEL_FEATURES

        col_info, col_sample = st.columns([2.2, 1])
        with col_info:
            with st.expander("📋 Required Columns (click to view)", expanded=False):
                st.markdown("**Mandatory columns:**")
                st.code("user, " + ", ".join(MODEL_FEATURES), language="text")
                st.caption(f"Total columns required: {len(required_columns)}")
        with col_sample:
            # Generate a small sample CSV on the fly
            sample_data = {"user": ["USER001", "USER002", "USER003"]}
            for feat in MODEL_FEATURES:
                sample_data[feat] = [round(float(np.random.uniform(0, 10)), 2) for _ in range(3)]
            sample_df = pd.DataFrame(sample_data)
            sample_csv = sample_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Sample CSV",
                data=sample_csv,
                file_name="sample_insider_threat_features.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download a correctly formatted sample file with dummy data"
            )

        uploaded_file = st.file_uploader(
            "Upload Feature CSV File",
            type=["csv"],
            label_visibility="collapsed",
            key="batch_uploader"
        )

        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
            except Exception:
                st.error("❌ **Invalid CSV file**\n\nThe uploaded file could not be read. Please make sure it is a valid CSV file.")
                st.stop()

            # ---- Better validation ----
            missing_columns = [c for c in required_columns if c not in data.columns]
            extra_columns = [c for c in data.columns if c not in required_columns]

            if missing_columns:
                st.error(
                    f"❌ **Missing {len(missing_columns)} required column(s)**\n\n"
                    f"The following columns are required but not found in your file:\n\n"
                    f"`{'`, `'.join(missing_columns)}`\n\n"
                    f"👉 Please download the **Sample CSV** above and match the column names exactly."
                )
                st.stop()

            if data.empty:
                st.error("❌ **Empty file**\n\nThe uploaded CSV contains no rows. Please upload a file with data.")
                st.stop()

            # Soft warning for extra columns (not blocking)
            if extra_columns:
                st.warning(
                    f"⚠️ Your file contains {len(extra_columns)} extra column(s) that will be ignored: "
                    f"`{'`, `'.join(extra_columns[:8])}`"
                    + (" ..." if len(extra_columns) > 8 else "")
                )

            # Check for non-numeric values in feature columns
            try:
                data[MODEL_FEATURES] = data[MODEL_FEATURES].astype(float)
            except Exception:
                st.error(
                    "❌ **Invalid data type**\n\n"
                    "One or more feature columns contain non-numeric values. "
                    "All feature columns must contain numbers only."
                )
                st.stop()

            with st.expander("📄 Preview Uploaded Data", expanded=False):
                st.dataframe(data.head(20), use_container_width=True)
                st.caption(f"Showing first 20 rows • Total rows: {len(data)}")

            if st.button("🚀 Run Threat Detection", key="run_batch", use_container_width=True):

                with st.spinner("Analysing behavioural patterns across all users..."):
                    X = data[MODEL_FEATURES]
                    prediction = model.predict(X)
                    proba = model.predict_proba(X)[:, 1]

                result = data.copy()
                result["Risk Score (%)"] = (proba * 100).round(1)
                result["Risk Level"] = [get_risk_level(p) for p in proba]
                result["Top Reason"] = [
                    explain_row(X.iloc[i]) if prediction[i] == 1 else "—"
                    for i in range(len(X))
                ]
                result["Prediction"] = np.where(
                    prediction == 1, "🔴 Insider Threat", "🟢 Normal User"
                )

                # Persist in session state so search & download remain available
                st.session_state["last_result"] = result
                st.session_state["last_prediction"] = prediction
                st.session_state["last_proba"] = proba

                st.success("✅ Analysis complete")
                st.caption(f"🕒 Generated on {datetime.now().strftime('%d %B %Y | %I:%M %p')}")

        # ---- Show results if available in session ----
        if "last_result" in st.session_state:
            result = st.session_state["last_result"]
            prediction = st.session_state["last_prediction"]
            proba = st.session_state["last_proba"]

            total_users = len(result)
            normal_users = int((prediction == 0).sum())
            insider_users = int((prediction == 1).sum())
            avg_risk = float(proba.mean() * 100)

            # KPI row
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Total Users</div>
                    <div class="kpi-value">{total_users}</div>
                    <div class="kpi-sub neutral">Uploaded</div>
                </div>""", unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Normal Users</div>
                    <div class="kpi-value">{normal_users}</div>
                    <div class="kpi-sub">Safe</div>
                </div>""", unsafe_allow_html=True)
            with k3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Insider Threats</div>
                    <div class="kpi-value">{insider_users}</div>
                    <div class="kpi-sub {'warn' if insider_users else ''}">
                    {'⚠ Action Required' if insider_users else '✓ None Detected'}
                    </div>
                </div>""", unsafe_allow_html=True)
            with k4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Avg Risk Score</div>
                    <div class="kpi-value">{avg_risk:.1f}%</div>
                    <div class="kpi-sub neutral">Across all users</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Charts
            ch1, ch2 = st.columns([1, 1.25])
            with ch1:
                st.markdown('<div class="section-title">🎯 Overall Risk Gauge</div>', unsafe_allow_html=True)
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_risk,
                    number={'suffix': "%", 'font': {'color': 'white', 'size': 34}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': "#8CA0C4"},
                        'bar': {'color': "#3B82F6"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(46,204,113,0.30)'},
                            {'range': [30, 60], 'color': 'rgba(255,196,0,0.30)'},
                            {'range': [60, 100], 'color': 'rgba(255,69,58,0.30)'},
                        ],
                    }
                ))
                gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", font={'color': "#E7ECF5"},
                    height=250, margin=dict(l=18, r=18, t=18, b=8)
                )
                st.plotly_chart(gauge, use_container_width=True)

            with ch2:
                st.markdown('<div class="section-title">📊 Risk Level Distribution</div>', unsafe_allow_html=True)
                risk_counts = (
                    result["Risk Level"]
                    .value_counts()
                    .reindex(["Low", "Medium", "High"])
                    .fillna(0)
                )
                fig_donut = px.pie(
                    names=risk_counts.index,
                    values=risk_counts.values,
                    hole=0.55,
                    color=risk_counts.index,
                    color_discrete_map={"Low": "#2ecc71", "Medium": "#FFC400", "High": "#FF453A"}
                )
                fig_donut.update_traces(textinfo="percent+label", textfont_color="white")
                fig_donut.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "#E7ECF5"}, height=250, showlegend=False,
                    margin=dict(l=8, r=8, t=8, b=8)
                )
                st.plotly_chart(fig_donut, use_container_width=True)

            st.markdown("---")

            if insider_users > 0:
                st.error(f"🚨 **ALERT:** {insider_users} potential insider threat(s) detected — review ranked list below.")
            else:
                st.success("✅ No insider threats detected in this batch.")

            # Flagged users
            st.markdown('<div class="section-title">🚨 Flagged Users — Ranked by Risk</div>', unsafe_allow_html=True)
            threat_users = (
                result[result["Prediction"] == "🔴 Insider Threat"]
                .sort_values("Risk Score (%)", ascending=False)
            )

            if len(threat_users) > 0:
                display_cols = ["user", "Risk Score (%)", "Risk Level", "Top Reason"]
                st.dataframe(
                    threat_users[display_cols],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("✅ No insider threat detected.")

            with st.expander("📋 View Full Results Table (all users)", expanded=False):
                st.dataframe(result, use_container_width=True, hide_index=True)

            # ---- Search by User (now works correctly via session state) ----
            st.markdown('<div class="section-title">🔍 Search User in Results</div>', unsafe_allow_html=True)
            search_user = st.text_input(
                "Enter User ID to search",
                placeholder="e.g. AAF0535",
                key="search_user_input"
            )
            if search_user.strip():
                mask = (
                    result["user"].astype(str).str.strip().str.lower()
                    == search_user.strip().lower()
                )
                user_data = result[mask]
                if not user_data.empty:
                    st.dataframe(user_data, use_container_width=True, hide_index=True)
                    # Quick visual summary
                    row = user_data.iloc[0]
                    risk_lvl = row["Risk Level"]
                    st.markdown(
                        f"**Prediction:** {row['Prediction']} &nbsp;|&nbsp; "
                        f"**Risk Score:** {row['Risk Score (%)']}% &nbsp;|&nbsp; "
                        f"**Level:** {risk_badge_html(risk_lvl)}",
                        unsafe_allow_html=True
                    )
                    if row["Top Reason"] and row["Top Reason"] != "—":
                        st.caption(f"Reason: {row['Top Reason']}")
                else:
                    st.warning("⚠ User not found in the uploaded batch.")

            # Download
            csv_bytes = result.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Full Prediction Report (CSV)",
                data=csv_bytes,
                file_name=f"Insider_Threat_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    # =============================================================
    # MODE B — SINGLE USER MANUAL ENTRY
    # =============================================================
    else:
        st.markdown('<div class="section-title">👤 Single User Investigation</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-sub">Enter a User ID and the behavioural feature values to instantly assess insider-threat risk.</div>',
            unsafe_allow_html=True
        )

        with st.form(key="single_user_form", clear_on_submit=False):
            user_id = st.text_input(
                "User ID",
                placeholder="e.g. AAF0535 / EMP-1024",
                help="Any unique identifier for the user being investigated."
            )

            st.markdown("**Behavioural Features**")
            st.caption("Enter numerical values observed for this user. Leave at 0 if unknown.")

            # Dynamic feature inputs in a clean multi-column layout
            n_feats = len(MODEL_FEATURES)
            cols_per_row = 3
            feature_values = {}

            for i in range(0, n_feats, cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < n_feats:
                        feat = MODEL_FEATURES[idx]
                        with col:
                            feature_values[feat] = st.number_input(
                                label=feat,
                                min_value=0.0,
                                value=0.0,
                                step=0.1,
                                format="%.4f",
                                key=f"feat_{feat}"
                            )

            submitted = st.form_submit_button(
                "🚀 Analyse This User",
                use_container_width=True
            )

        if submitted:
            if not user_id.strip():
                st.error("❌ Please enter a User ID.")
            else:
                # Build single-row dataframe
                row_dict = {f: feature_values[f] for f in MODEL_FEATURES}
                X_single = pd.DataFrame([row_dict], columns=MODEL_FEATURES)

                with st.spinner("Running behavioural analysis..."):
                    pred = model.predict(X_single)[0]
                    proba = model.predict_proba(X_single)[0, 1]
                    risk_score = round(proba * 100, 1)
                    risk_level = get_risk_level(proba)
                    reason = explain_row(X_single.iloc[0]) if pred == 1 else "No anomalous patterns detected relative to baseline."

                # Result card
                card_class = risk_level.lower()
                prediction_label = "🔴 Insider Threat" if pred == 1 else "🟢 Normal User"
                badge = risk_badge_html(risk_level)

                st.markdown(f"""
                <div class="result-card {card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                        <div>
                            <div style="font-size:13px; color:#8BA3C7; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">User</div>
                            <div style="font-size:22px; font-weight:800; color:#fff; margin-top:2px;">{user_id.strip()}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:13px; color:#8BA3C7; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">Prediction</div>
                            <div style="font-size:20px; font-weight:800; margin-top:2px;">{prediction_label}</div>
                        </div>
                    </div>
                    <div style="margin-top:18px; display:flex; gap:28px; flex-wrap:wrap;">
                        <div>
                            <div style="font-size:12px; color:#8BA3C7; font-weight:600;">Risk Score</div>
                            <div style="font-size:28px; font-weight:800; color:#fff;">{risk_score}%</div>
                        </div>
                        <div>
                            <div style="font-size:12px; color:#8BA3C7; font-weight:600;">Risk Level</div>
                            <div style="margin-top:6px;">{badge}</div>
                        </div>
                    </div>
                    <div style="margin-top:16px; padding-top:14px; border-top:1px solid rgba(255,255,255,0.08);">
                        <div style="font-size:12px; color:#8BA3C7; font-weight:600; margin-bottom:4px;">Top Contributing Factors</div>
                        <div style="font-size:14px; color:#D0DCF0; line-height:1.45;">{reason}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Mini gauge
                st.markdown("<br>", unsafe_allow_html=True)
                gcol1, gcol2 = st.columns([1, 1.4])
                with gcol1:
                    mini_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=risk_score,
                        number={'suffix': "%", 'font': {'color': 'white', 'size': 30}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': "#8CA0C4"},
                            'bar': {'color': "#3B82F6"},
                            'bgcolor': "rgba(0,0,0,0)",
                            'steps': [
                                {'range': [0, 30], 'color': 'rgba(46,204,113,0.30)'},
                                {'range': [30, 60], 'color': 'rgba(255,196,0,0.30)'},
                                {'range': [60, 100], 'color': 'rgba(255,69,58,0.30)'},
                            ],
                        }
                    ))
                    mini_gauge.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", font={'color': "#E7ECF5"},
                        height=220, margin=dict(l=15, r=15, t=15, b=5)
                    )
                    st.plotly_chart(mini_gauge, use_container_width=True)

                with gcol2:
                    st.markdown('<div class="section-title">Feature Snapshot</div>', unsafe_allow_html=True)
                    feat_df = pd.DataFrame({
                        "Feature": MODEL_FEATURES,
                        "Value": [feature_values[f] for f in MODEL_FEATURES]
                    })
                    st.dataframe(feat_df, use_container_width=True, hide_index=True)

                if pred == 1:
                    st.error("🚨 This user has been flagged as a potential insider threat. Escalate for further investigation.")
                else:
                    st.success("✅ No strong indicators of insider threat behaviour detected for this user.")

# ---------------------------------------------------------------------
# TAB 3 — MODEL INSIGHTS
# ---------------------------------------------------------------------
with tab_insights:

    if metadata is None:
        st.warning(
            "⚠ `model_metadata.json` not found. "
            "Re-run `04_Model_Building.ipynb` to generate model performance artefacts."
        )
    else:
        st.markdown('<div class="section-title">📈 Cross-Validated Performance (5-Fold)</div>', unsafe_allow_html=True)

        cv = metadata["cv_metrics"]
        rows = []
        for m, v in cv.items():
            rows.append({
                "Metric": m.capitalize(),
                "Train (avg)": f"{v['train_mean']*100:.1f}%",
                "Test (avg)": f"{v['test_mean']*100:.1f}%",
                "Gap": f"{(v['train_mean']-v['test_mean'])*100:+.1f}%"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.caption("A small train–test gap indicates good generalisation and low overfitting risk.")

        st.markdown("<br>", unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:
            st.markdown('<div class="section-title">🧠 Feature Importance</div>', unsafe_allow_html=True)
            imp = pd.Series(metadata["feature_importances"]).sort_values(ascending=True)
            fig_imp = px.bar(
                x=imp.values, y=imp.index, orientation="h",
                labels={"x": "Importance", "y": ""},
                color=imp.values, color_continuous_scale="Blues"
            )
            fig_imp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "#E7ECF5"}, height=380, showlegend=False,
                coloraxis_showscale=False, margin=dict(l=8, r=8, t=8, b=8)
            )
            st.plotly_chart(fig_imp, use_container_width=True)

        with colB:
            st.markdown('<div class="section-title">🧮 Confusion Matrix (Holdout)</div>', unsafe_allow_html=True)
            cm = np.array(metadata["confusion_matrix"])
            fig_cm = px.imshow(
                cm, text_auto=True, color_continuous_scale="Blues",
                labels=dict(x="Predicted", y="Actual", color="Count"),
                x=["Normal", "Insider"], y=["Normal", "Insider"]
            )
            fig_cm.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "#E7ECF5"}, height=380, coloraxis_showscale=False,
                margin=dict(l=8, r=8, t=8, b=8)
            )
            st.plotly_chart(fig_cm, use_container_width=True)

        st.markdown('<div class="section-title">📋 Holdout Classification Report</div>', unsafe_allow_html=True)
        hm = metadata["holdout_metrics"]
        report_df = pd.DataFrame(hm).T
        report_df = report_df.rename(index={"0": "Normal", "1": "Insider Threat"})
        st.dataframe(report_df.round(3), use_container_width=True)

# ---------------------------------------------------------------------
# TAB 4 — ABOUT
# ---------------------------------------------------------------------
with tab_about:
    st.markdown('<div class="section-title">🛡️ About This Project</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
    <b>An Automated Threat Intelligence Framework for Insider Threat Detection</b><br><br>
    This platform applies behavioural analytics and supervised machine learning to identify users
    whose activity patterns deviate from established organisational norms — a core indicator of
    insider threat risk.<br><br>
    Unlike traditional rule-based monitoring, the system learns from historical behavioural data,
    fuses multiple signal families (login, device/USB, email, file activity and drift features),
    and surfaces every decision with transparent, human-readable explanations that security
    analysts can act upon immediately.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🎓 Academic Details</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
    <b>B.Tech Final Year Project</b> — Department of Computer Science &amp; Engineering<br>
    Group: GC-5 &nbsp;|&nbsp; Guide: Prof. Sapana G. Nandanwar<br><br>
    <b>Team:</b> Vinay Nikhar · Vishal Jadhav · Saurabh Mohod · Nandini Pund · Prachi Dahapute
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🛠️ Technology Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
    Python · Pandas · Scikit-learn (Random Forest) · Streamlit · Plotly<br>
    Stratified K-Fold Cross-Validation · Ratio-based Explainability · Session-state Workflows
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">✨ Key Capabilities (v2.0)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
    • Batch CSV analysis with ranked risk list and downloadable report<br>
    • Single-user manual investigation form (no CSV required)<br>
    • Instant risk score + human-readable reason codes<br>
    • Persistent session results with working user search<br>
    • Cross-validated model metrics &amp; feature importance visualisation
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:#6B7A99; padding-top:22px; font-size:12.5px;">
    © 2026 Insider Threat Intelligence Platform · All Rights Reserved
    </div>
    """, unsafe_allow_html=True)
