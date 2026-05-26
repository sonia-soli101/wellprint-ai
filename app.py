
import streamlit as st
import pandas as pd

st.title("Wellprint AI")
st.caption("Your Daily Wellness Fingerprint")

st.subheader("Sample Wellness Data")

df = pd.read_csv("data/sample_wellness_data.csv")

st.write("데이터 미리보기")
st.dataframe(df.head())

st.write("데이터 크기")
st.write(df.shape)

st.subheader("Quick Wellness Summary")

avg_sleep = df["sleep_hours"].mean()
avg_steps = df["steps"].mean()
avg_stress = df["stress_level_1_10"].mean()
avg_gratitude = df["gratitude_said_count"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Sleep", f"{avg_sleep:.1f} hrs")
col2.metric("Avg Steps", f"{avg_steps:,.0f}")
col3.metric("Avg Stress", f"{avg_stress:.1f}/10")
col4.metric("Avg Gratitude", f"{avg_gratitude:.1f} times")