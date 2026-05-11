import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from Data_checks.checks.final_assemling import Phase5_Overall_Score

st.set_page_config(layout="wide", page_title="Data Quality Monitor", page_icon="🔍")

st.title("🔍 Data Quality Monitor")
st.markdown("**Upload your dataset and get a complete quality report instantly**")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Settings")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
target_col = st.sidebar.text_input("Target Column (optional)")
problem_type = st.sidebar.selectbox("Problem Type", ["classification", "regression"])
run_btn = st.sidebar.button("🚀 Run Analysis", use_container_width=True)

if uploaded_file is None:
    st.info("Upload a CSV file from the sidebar to get started.")
    st.stop()

df = pd.read_csv(uploaded_file)
columns=df.columns
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Total Cells", df.shape[0] * df.shape[1])

if not run_btn:
    st.stop()

target = target_col if target_col and target_col in df.columns else None

# =========================
# RUN PHASE 5
# =========================
with st.spinner("Running all phases..."):
    p5 = Phase5_Overall_Score(df, target=target, problem=problem_type)
    final_score = p5.calculate()
    grade = p5.grade()

# Shortcuts
p1 = p5.phase1
p2 = p5.phase2
p3 = p5.phase3
p4 = p5.phase4

s1 = p5.scores_phase1
s2 = p5.scores_phase2
s3 = p5.scores_phase3
s4 = p5.scores_phase4 if p4 else None

i1 = p5.issue1
i2 = p5.issue2
i3 = p5.issue3
i4 = p5.issue4

# =========================
# FINAL SCORE
# =========================
st.markdown("---")
st.subheader("🏆 Overall Data Quality Score")

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=final_score,
        title={'text': "Quality Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "#FF4B4B"},
                {'range': [40, 60], 'color': "#FCA311"},
                {'range': [60, 75], 'color': "#FFD700"},
                {'range': [75, 90], 'color': "#90EE90"},
                {'range': [90, 100], 'color': "#00CC00"},
            ]
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"### {grade}")
    st.markdown("#### Phase Scores")
    st.metric("Phase 1 — Basic Health", f"{s1}/100")
    st.metric("Phase 2 — Distribution", f"{s2}/100")
    st.metric("Phase 3 — Feature Analysis", f"{s3}/100")
    if s4 and isinstance(s4, (int, float)):
        st.metric("Phase 4 — Target Analysis", f"{s4}/100")
    else:
        st.info("Phase 4 — Target not provided")

# =========================
# PHASE 1
# =========================
st.markdown("---")
st.subheader("📋 Phase 1 — Basic Health")

col1, col2, col3 = st.columns(3)
col1.metric("Total Missing Values", int(p1.total_sum_nan))
col2.metric("Duplicate Rows", int(p1.duplicates))
col3.metric("Shape", f"{p1.Shapex[0]} × {p1.Shapex[1]}")

if p1.total_sum_nan > 0:
    st.markdown("**Missing Values Per Column**")
    missing_df = pd.DataFrame({
        'Column': list(p1.missing_values.keys()),
        'Missing Count': list(p1.missing_values.values())
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0]
    fig = px.bar(missing_df, x='Column', y='Missing Count', color='Missing Count')
    st.plotly_chart(fig, use_container_width=True)

for k, v in i1.items():
    if "critical" in str(v).lower() or "high" in str(v).lower():
        st.error(f"{k}: {v}")
    elif "moderate" in str(v).lower() or "warning" in str(v).lower():
        st.warning(f"{k}: {v}")
    else:
        st.success(f"{k}: {v}")

# =========================
# PHASE 2
# =========================
st.markdown("---")
st.subheader("📊 Phase 2 — Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Skewness Per Column**")
    skew_df = pd.DataFrame({
        'Column': list(p2.skewness.keys()),
        'Skewness': list(p2.skewness.values())
    })
    fig = px.bar(
        skew_df, x='Column', y='Skewness',
        color='Skewness',
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Outliers Per Column**")
    numeric_cols = list(p2.numeric_data)
    outlier_data = []
    for i, col in enumerate(numeric_cols):
        outlier_data.append({
            'Column': col,
            'Outliers': p2.outliers[i] if i < len(p2.outliers) else 0
        })
    outlier_df = pd.DataFrame(outlier_data)
    fig = px.bar(outlier_df, x='Column', y='Outliers', color='Outliers')
    st.plotly_chart(fig, use_container_width=True)

if p2.zero_variance:
    st.error(f"Zero Variance Columns: {p2.zero_variance}")

for k, v in i2.items():
    if "critical" in str(v).lower() or "high" in str(v).lower():
        st.error(f"{k}: {v}")
    elif "moderate" in str(v).lower():
        st.warning(f"{k}: {v}")
    else:
        st.success(f"{k}: {v}")

# =========================
# PHASE 3
# =========================
st.markdown("---")
st.subheader("🔗 Phase 3 — Feature Analysis")

numeric_df = df.select_dtypes(include=[np.number])
if target:
    numeric_df = numeric_df.drop(columns=[target], errors='ignore')

if len(numeric_df.columns) >= 2:
    st.markdown("**Correlation Heatmap**")
    corr = numeric_df.corr()
    fig = px.imshow(
        corr,
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1
    )
    st.plotly_chart(fig, use_container_width=True)

if p3.constant_columns:
    st.error(f"Constant Columns: {p3.constant_columns}")

if p3.high_cardinality:
    st.warning(f"High Cardinality Columns: {list(p3.high_cardinality.keys())}")

if p3.high_correlation_pairs:
    st.warning(f"Highly Correlated Pairs: {len(p3.high_correlation_pairs)} found")
    corr_df = pd.DataFrame(p3.high_correlation_pairs)
    st.dataframe(corr_df)

for k, v in i3.items():
    if "critical" in str(v).lower():
        st.error(f"{k}: {v}")
    elif "moderate" in str(v).lower():
        st.warning(f"{k}: {v}")
    else:
        st.success(f"{k}: {v}")

# =========================
# PHASE 4
# =========================
if target and p4 and isinstance(s4, (int, float)):
    st.markdown("---")
    st.subheader("🎯 Phase 4 — Target Analysis")

    if problem_type == "classification":
        st.markdown("**Class Distribution**")
        class_df = pd.DataFrame({
            'Class': [str(k) for k in p4.class_distribution.keys()],
            'Count': list(p4.class_distribution.values())
        })
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(class_df, names='Class', values='Count')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(class_df, x='Class', y='Count', color='Count')
            st.plotly_chart(fig, use_container_width=True)
        st.metric("Imbalance Ratio (minority/majority)", p4.imbalance_ratio)

    elif problem_type == "regression":
        st.markdown("**Target Distribution**")
        fig = px.histogram(df, x=target, nbins=30)
        st.plotly_chart(fig, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Skewness", p4.target_skewness)
        col2.metric("Mean", p4.target_mean)
        col3.metric("Std", p4.target_std)

    st.markdown("**Feature-Target Correlation**")
    ft_df = pd.DataFrame({
        'Feature': list(p4.feature_target_corr.keys()),
        'Correlation': list(p4.feature_target_corr.values())
    }).sort_values('Correlation', ascending=False)
    fig = px.bar(ft_df, x='Feature', y='Correlation', color='Correlation')
    st.plotly_chart(fig, use_container_width=True)

    for k, v in i4.items():
        if "critical" in str(v).lower():
            st.error(f"{k}: {v}")
        elif "moderate" in str(v).lower():
            st.warning(f"{k}: {v}")
        else:
            st.success(f"{k}: {v}")