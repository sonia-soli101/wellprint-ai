# 필요한 라이브러리와 점수 계산 함수 불러오기
from src.scoring import calculate_wellness_score, get_wellness_level
import streamlit as st
import pandas as pd
import plotly.express as px


# 앱 기본 제목과 설명 표시
st.title("Wellprint AI")
st.caption("나의 하루 웰니스 패턴을 확인하는 AI 대시보드")


# 샘플 웰니스 데이터 불러오기
st.subheader("샘플 웰니스 데이터")

df = pd.read_csv("data/sample_wellness_data.csv")


# 웰니스 점수와 등급 계산
df["wellness_score"] = df.apply(calculate_wellness_score, axis=1)
df["wellness_level"] = df["wellness_score"].apply(get_wellness_level)


# 영어 등급명을 한글 등급명으로 변환
level_name_map = {
    "Strong": "좋음",
    "Balanced": "보통",
    "Needs Attention": "주의 필요",
    "High Burden": "부담 높음",
}

df["wellness_level_kr"] = df["wellness_level"].map(level_name_map)


# 데이터 미리보기와 크기 표시
st.write("데이터 미리보기")
st.dataframe(df.head())

st.write("데이터 크기")
st.write(df.shape)


# 주요 웰니스 지표 평균 계산
st.subheader("웰니스 요약 지표")

avg_score = df["wellness_score"].mean()
avg_sleep = df["sleep_hours"].mean()
avg_steps = df["steps"].mean()
avg_stress = df["stress_level_1_10"].mean()
avg_gratitude = df["gratitude_said_count"].mean()


# 평균 지표를 카드 형태로 표시
row1_col1, row1_col2, row1_col3 = st.columns(3)

row1_col1.metric("평균 웰니스 점수", f"{avg_score:.1f}/100")
row1_col2.metric("평균 수면 시간", f"{avg_sleep:.1f}시간")
row1_col3.metric("평균 걸음 수", f"{avg_steps:,.0f}보")

row2_col1, row2_col2 = st.columns(2)

row2_col1.metric("평균 스트레스", f"{avg_stress:.1f}/10")
row2_col2.metric("평균 감사 표현", f"{avg_gratitude:.1f}회")


# 웰니스 등급별 분포 계산
st.subheader("웰니스 등급 분포")

level_order_kr = ["좋음", "보통", "주의 필요", "부담 높음"]

level_counts = (
    df["wellness_level_kr"]
    .value_counts()
    .reindex(level_order_kr, fill_value=0)
    .reset_index()
)

level_counts.columns = ["웰니스 등급", "데이터 수"]


# 등급 분포 표 표시
st.dataframe(level_counts, hide_index=True)


# 도넛 차트 표시
fig = px.pie(
    level_counts,
    names="웰니스 등급",
    values="데이터 수",
    hole=0.45,
    title="웰니스 등급별 비율",
)

st.plotly_chart(fig, use_container_width=True)


# 가장 많은 등급 요약 문장 표시
most_common_level = level_counts.sort_values("데이터 수", ascending=False).iloc[0]

st.write(
    f"현재 샘플 데이터에서는 **{most_common_level['웰니스 등급']}** 등급이 "
    f"가장 많습니다. 총 {len(df)}개 기록 중 "
    f"{most_common_level['데이터 수']}개가 해당 등급입니다."
)