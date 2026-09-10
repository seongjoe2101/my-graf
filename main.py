import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.markdown(
    """
    **1년 동안의 일별 박스오피스 데이터를 이용해 영화의 시간에 따른 변화를 살펴봅니다.**

    영화를 선택하면 날짜별 일관객 변화를 그래프로 확인할 수 있습니다.
    """
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # 날짜순 정렬
    df = df.sort_values("날짜")

    return df


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.info("인터넷 연결과 데이터 주소를 확인해 주세요.")
    st.stop()


# --------------------------------------------------
# 데이터 정보
# --------------------------------------------------
with st.expander("📊 데이터 정보", expanded=False):
    st.write("**데이터 출처**")
    st.code(DATA_URL)

    st.write(
        f"전체 데이터: **{len(df):,}개 행**"
    )

    if "날짜" in df.columns:
        valid_dates = df["날짜"].dropna()

        if len(valid_dates) > 0:
            st.write(
                f"데이터 기간: "
                f"**{valid_dates.min().strftime('%Y-%m-%d')} ~ "
                f"{valid_dates.max().strftime('%Y-%m-%d')}**"
            )

    st.write("**주요 열**")
    st.write(
        "날짜 · 순위 · 영화코드 · 영화명 · 일관객 · "
        "누적관객 · 스크린수 · 상영횟수"
    )


# ==================================================
# 그래프 1
# ==================================================
st.divider()

st.header("1️⃣ 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)


# 영화 목록
movie_list = (
    df["영화명"]
    .dropna()
    .astype(str)
    .drop_duplicates()
    .sort_values()
    .tolist()
)


if len(movie_list) == 0:
    st.warning("선택할 수 있는 영화 데이터가 없습니다.")
    st.stop()


selected_movie = st.selectbox(
    "🎥 영화 선택",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# 날짜와 일관객이 모두 있는 데이터만 사용
movie_df = movie_df.dropna(
    subset=["날짜", "일관객"]
)


if len(movie_df) == 0:
    st.warning(
        "선택한 영화의 날짜별 관객 데이터가 없습니다."
    )

else:
    # Plotly 선 그래프
    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        title=f"{selected_movie} - 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 (명)"
        }
    )

    # 마우스를 올렸을 때 날짜와 관객수가 표시되도록 설정
    fig.update_traces(
        hovertemplate=(
            "날짜: %{x|%Y-%m-%d}<br>"
            "일관객: %{y:,.0f}명"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        hovermode="x unified",
        height=500,
        xaxis=dict(
            tickformat="%Y-%m-%d"
        ),
        yaxis=dict(
            tickformat=","
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# 그래프 1 해석 문구
# --------------------------------------------------
st.markdown(
    """
    <div style="
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 30px;
        border-radius: 12px;
        background-color: #FFF8E1;
        border: 1px solid #FFD54F;
    ">
        <h4 style="margin: 0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>
        <p style="margin: 0; color: #555;">
            "주말에 관객수가 평일대비 5배이상 많다"
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 그래프 2 - 앞으로 추가할 영역
# ==================================================
st.divider()

st.header("2️⃣ 두 번째 그래프")

st.info(
    "여기에 앞으로 두 번째 그래프를 추가할 수 있습니다."
)

st.markdown(
    """
    <div style="
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 30px;
        border-radius: 12px;
        background-color: #E8F5E9;
        border: 1px solid #81C784;
    ">
        <h4 style="margin: 0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>
        <p style="margin: 0; color: #555;">
            여기에 두 번째 그래프에서 알 수 있는 내용을 적어 주세요.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 그래프 3 - 앞으로 추가할 영역
# ==================================================
st.divider()

st.header("3️⃣ 세 번째 그래프")

st.info(
    "여기에 앞으로 세 번째 그래프를 추가할 수 있습니다."
)

st.markdown(
    """
    <div style="
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 30px;
        border-radius: 12px;
        background-color: #FCE4EC;
        border: 1px solid #F48FB1;
    ">
        <h4 style="margin: 0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>
        <p style="margin: 0; color: #555;">
            여기에 세 번째 그래프에서 알 수 있는 내용을 적어 주세요.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
