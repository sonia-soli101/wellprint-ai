from src.scoring import (
    calculate_wellness_score,
    get_wellness_level,
    calculate_sub_scores,
)
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Wellprint AI",
    page_icon="🌿",
    layout="wide"
)

st.title("Wellprint AI")
st.caption("나의 하루 웰니스 패턴을 확인하는 AI 대시보드")

st.divider()


# 데이터 불러오기
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


# 웰니스 요약 지표
st.subheader("웰니스 요약 지표")

avg_score = df["wellness_score"].mean()
avg_sleep = df["sleep_hours"].mean()
avg_steps = df["steps"].mean()
avg_stress = df["stress_level_1_10"].mean()
avg_gratitude = df["gratitude_said_count"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("평균 웰니스 점수", f"{avg_score:.1f}/100")
col2.metric("평균 수면 시간", f"{avg_sleep:.1f}시간")
col3.metric("평균 걸음 수", f"{avg_steps:,.0f}보")
col4.metric("평균 스트레스", f"{avg_stress:.1f}/10")
col5.metric("평균 감사 표현", f"{avg_gratitude:.1f}회")

st.divider()


# 데이터 미리보기
with st.expander("샘플 데이터 미리보기"):
    st.write(f"전체 데이터 크기: {df.shape[0]}행 × {df.shape[1]}열")
    st.dataframe(df.head(), use_container_width=True)


# 웰니스 등급 분포
st.subheader("웰니스 등급 분포")

level_order_kr = ["좋음", "보통", "주의 필요", "부담 높음"]

level_counts = (
    df["wellness_level_kr"]
    .value_counts()
    .reindex(level_order_kr, fill_value=0)
    .reset_index()
)

level_counts.columns = ["웰니스 등급", "데이터 수"]

chart_col1, chart_col2 = st.columns([1, 2])

with chart_col1:
    st.dataframe(level_counts, hide_index=True, use_container_width=True)

with chart_col2:
    fig_level = px.bar(
        level_counts,
        x="웰니스 등급",
        y="데이터 수",
        text="데이터 수",
        title="웰니스 등급별 데이터 수",
    )

    fig_level.update_traces(textposition="outside")
    fig_level.update_layout(
        xaxis_title="웰니스 등급",
        yaxis_title="데이터 수",
        yaxis_range=[0, level_counts["데이터 수"].max() + 5],
        height=380,
        showlegend=False,
    )

    st.plotly_chart(fig_level, use_container_width=True)


# 웰니스 점수 분포
st.subheader("웰니스 점수 분포")

fig_score = px.histogram(
    df,
    x="wellness_score",
    nbins=20,
    title="웰니스 점수 분포",
    labels={"wellness_score": "웰니스 점수"},
)

fig_score.update_layout(
    xaxis_title="웰니스 점수",
    yaxis_title="데이터 수",
    height=380,
    showlegend=False,
)

st.plotly_chart(fig_score, use_container_width=True)

st.divider()


# 하위 웰니스 점수 계산
sub_score_rows = df.apply(calculate_sub_scores, axis=1)
sub_score_df = pd.DataFrame(list(sub_score_rows))

avg_sub_scores = sub_score_df.mean().reset_index()
avg_sub_scores.columns = ["score_key", "평균 점수"]

score_name_map = {
    "sleep_score": "수면 회복",
    "activity_score": "활동",
    "stress_score": "스트레스 균형",
    "food_score": "식사 품질",
    "hydration_score": "수분 습관",
    "gut_score": "장 컨디션",
    "social_score": "사회적 환경",
}

avg_sub_scores["하위 점수"] = avg_sub_scores["score_key"].map(score_name_map)
avg_sub_scores = avg_sub_scores.sort_values("평균 점수", ascending=True)

st.subheader("하위 웰니스 점수")

sub_col1, sub_col2 = st.columns([1, 2])

with sub_col1:
    display_sub_scores = avg_sub_scores[["하위 점수", "평균 점수"]].copy()
    display_sub_scores["평균 점수"] = display_sub_scores["평균 점수"].round(1)

    st.dataframe(
        display_sub_scores,
        hide_index=True,
        use_container_width=True
    )

with sub_col2:
    fig_sub = px.bar(
        avg_sub_scores,
        x="평균 점수",
        y="하위 점수",
        orientation="h",
        text="평균 점수",
        title="하위 웰니스 점수 평균",
    )

    fig_sub.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_sub.update_layout(
        xaxis_title="평균 점수",
        yaxis_title="하위 점수",
        xaxis_range=[0, 110],
        height=420,
        showlegend=False,
    )

    st.plotly_chart(fig_sub, use_container_width=True)


# 주요 요약 문장
lowest_score = avg_sub_scores.iloc[0]
highest_score = avg_sub_scores.iloc[-1]
most_common_level = level_counts.sort_values("데이터 수", ascending=False).iloc[0]

st.info(
    f"현재 샘플 데이터에서는 **{most_common_level['웰니스 등급']}** 등급이 가장 많습니다. "
    f"하위 점수 중 평균이 가장 낮은 항목은 **{lowest_score['하위 점수']} "
    f"({lowest_score['평균 점수']:.1f}점)**이고, "
    f"가장 높은 항목은 **{highest_score['하위 점수']} "
    f"({highest_score['평균 점수']:.1f}점)**입니다."
)


# 개발 메모
with st.expander("개발 메모"):
    st.write(
        """
        현재 화면은 샘플 데이터를 기준으로 계산됩니다.
        
        식사 품질, 수분 습관, 장 컨디션 점수가 자연스럽게 나오려면
        sample_wellness_data.csv에 아래 컬럼이 포함되어야 합니다.
        
        - sugary_drink_count
        - ultra_processed_food_count
        - water_intake_l
        - bloating_level_1_10
        """
    )