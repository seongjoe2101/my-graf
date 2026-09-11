
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==================================================
# 기본 설정
# ==================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# 제목
# ==================================================
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.markdown(
    """
    **1년 동안의 일별 박스오피스 데이터를 이용해 영화의 시간에 따른 변화를 살펴봅니다.**

    개별 영화의 관객 변화부터 인기 영화 비교,
    전체 영화 관객 흐름과 월·요일별 관객 분포까지 확인합니다.
    """
)


# ==================================================
# 데이터 주소
# ==================================================
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


# ==================================================
# 데이터 불러오기
# ==================================================
@st.cache_data
def load_data():

    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    # 예: 20260101 → 2026-01-01
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 열 변환
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


# ==================================================
# 데이터 불러오기
# ==================================================
try:
    df = load_data()

except Exception:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.info("인터넷 연결과 데이터 주소를 확인해 주세요.")
    st.stop()


# ==================================================
# 데이터 정보
# ==================================================
with st.expander("📊 데이터 정보", expanded=False):

    st.write("**데이터 출처**")
    st.code(DATA_URL)

    st.write(
        f"전체 데이터: **{len(df):,}개 행**"
    )

    valid_dates = df["날짜"].dropna()

    if len(valid_dates) > 0:

        st.write(
            f"데이터 기간: **"
            f"{valid_dates.min().strftime('%Y-%m-%d')} ~ "
            f"{valid_dates.max().strftime('%Y-%m-%d')}**"
        )

    st.write("**열(컬럼)**")

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


# --------------------------------------------------
# 영화 목록
# --------------------------------------------------
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


# --------------------------------------------------
# 영화 선택
# --------------------------------------------------
selected_movie = st.selectbox(
    "🎥 영화 선택",
    movie_list
)


# --------------------------------------------------
# 선택한 영화 데이터
# --------------------------------------------------
movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

movie_df = movie_df.dropna(
    subset=["날짜", "일관객"]
)

movie_df = movie_df.sort_values("날짜")


if len(movie_df) == 0:

    st.warning(
        "선택한 영화의 날짜별 관객 데이터가 없습니다."
    )

else:

    fig1 = px.line(
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

    fig1.update_traces(
        hovertemplate=(
            "날짜: %{x|%Y-%m-%d}<br>"
            "일관객: %{y:,.0f}명"
            "<extra></extra>"
        )
    )

    fig1.update_layout(
        height=500,
        hovermode="x unified",
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
        fig1,
        use_container_width=True
    )


# --------------------------------------------------
# 그래프 1 해석
# --------------------------------------------------
st.markdown(
    """
    <div style="
        padding:18px;
        margin-top:10px;
        margin-bottom:30px;
        border-radius:12px;
        background-color:#FFF8E1;
        border:1px solid #FFD54F;
    ">
        <h4 style="margin:0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>

        <p style="margin:0; color:#555;">
            선택한 영화의 날짜별 관객 변화를 확인하고 관객이 증가하거나 감소한 시기를 파악할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 그래프 2
# ==================================================
st.divider()

st.header("2️⃣ 일관객 합계가 가장 큰 영화 5편 비교")

st.write(
    "이 기간 동안의 일관객 합계가 가장 큰 5편을 골라 "
    "날짜별 일관객 변화를 한 그래프에서 비교합니다."
)


# --------------------------------------------------
# 영화별 일관객 합계
# --------------------------------------------------
movie_total = (
    df.dropna(
        subset=["영화명", "일관객"]
    )
    .groupby(
        "영화명",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(5)
)


top5_movies = movie_total["영화명"].tolist()


# --------------------------------------------------
# TOP 5 데이터
# --------------------------------------------------
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.dropna(
    subset=["날짜", "일관객"]
)

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


if len(top5_df) == 0:

    st.warning("비교할 영화 데이터가 없습니다.")

else:

    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
        markers=True,
        title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 (명)",
            "영화명": "영화"
        }
    )

    fig2.update_traces(
        hovertemplate=(
            "날짜: %{x|%Y-%m-%d}<br>"
            "일관객: %{y:,.0f}명"
            "<extra>%{fullData.name}</extra>"
        )
    )

    fig2.update_layout(
        height=600,
        hovermode="x unified",
        xaxis=dict(
            tickformat="%Y-%m-%d"
        ),
        yaxis=dict(
            tickformat=",",
            title="일관객 (명)"
        ),
        legend=dict(
            title="영화",
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# --------------------------------------------------
# TOP 5 표
# --------------------------------------------------
st.markdown("#### 📌 그래프에 사용된 영화")

display_total = movie_total.copy()

display_total["일관객"] = (
    display_total["일관객"]
    .map(lambda x: f"{x:,.0f}명")
)

display_total.columns = [
    "영화명",
    "기간 일관객 합계"
]

st.dataframe(
    display_total,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 그래프 2 해석
# --------------------------------------------------
st.markdown(
    """
    <div style="
        padding:18px;
        margin-top:10px;
        margin-bottom:30px;
        border-radius:12px;
        background-color:#E8F5E9;
        border:1px solid #81C784;
    ">
        <h4 style="margin:0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>

        <p style="margin:0; color:#555;">
            기간 전체의 관객 합계가 큰 영화들의 날짜별 흥행 흐름을 서로 비교할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 그래프 3
# ==================================================
st.divider()

st.header("3️⃣ 날짜별 전체 10위권 일관객 합계")

st.write(
    "각 날짜마다 박스오피스 10위권 영화의 일관객을 모두 더해 "
    "그날 전체 관객 규모가 어떻게 변했는지 보여 줍니다."
)


# --------------------------------------------------
# 날짜별 일관객 합계
# --------------------------------------------------
daily_total = (
    df.dropna(
        subset=["날짜", "일관객"]
    )
    .groupby(
        "날짜",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values("날짜")
)


if len(daily_total) == 0:

    st.warning(
        "날짜별 관객 데이터를 계산할 수 없습니다."
    )

else:

    # --------------------------------------------------
    # 관객이 가장 많았던 날짜 TOP 3
    # --------------------------------------------------
    top3_days = (
        daily_total
        .nlargest(
            3,
            "일관객"
        )
        .sort_values(
            "일관객",
            ascending=False
        )
    )


    # --------------------------------------------------
    # 영역 그래프
    # --------------------------------------------------
    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=daily_total["날짜"],
            y=daily_total["일관객"],
            mode="lines",
            name="10위권 일관객 합계",
            fill="tozeroy",
            hovertemplate=(
                "날짜: %{x|%Y-%m-%d}<br>"
                "10위권 일관객 합계: %{y:,.0f}명"
                "<extra></extra>"
            )
        )
    )


    # --------------------------------------------------
    # TOP 3 날짜 표시
    # --------------------------------------------------
    for _, row in top3_days.iterrows():

        fig3.add_annotation(
            x=row["날짜"],
            y=row["일관객"],
            text=(
                f"{row['날짜'].strftime('%Y-%m-%d')}"
                f"<br>{row['일관객']:,.0f}명"
            ),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-55,
            bgcolor="white",
            bordercolor="#888",
            borderwidth=1,
            borderpad=5,
            font=dict(size=12)
        )


    fig3.update_layout(
        title="날짜별 박스오피스 10위권 일관객 합계",
        height=550,
        hovermode="x unified",
        xaxis=dict(
            title="날짜",
            tickformat="%Y-%m-%d"
        ),
        yaxis=dict(
            title="10위권 일관객 합계 (명)",
            tickformat=","
        ),
        margin=dict(
            l=20,
            r=20,
            t=80,
            b=20
        )
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    # --------------------------------------------------
    # TOP 3 표
    # --------------------------------------------------
    st.markdown(
        "#### 📌 일관객 합계가 가장 컸던 날 TOP 3"
    )

    top3_display = top3_days.copy()

    top3_display["날짜"] = (
        top3_display["날짜"]
        .dt.strftime("%Y-%m-%d")
    )

    top3_display["일관객"] = (
        top3_display["일관객"]
        .map(lambda x: f"{x:,.0f}명")
    )

    top3_display.columns = [
        "날짜",
        "10위권 일관객 합계"
    ]

    st.dataframe(
        top3_display,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 그래프 3 해석
# --------------------------------------------------
st.markdown(
    """
    <div style="
        padding:18px;
        margin-top:10px;
        margin-bottom:30px;
        border-radius:12px;
        background-color:#FCE4EC;
        border:1px solid #F48FB1;
    ">
        <h4 style="margin:0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>

        <p style="margin:0; color:#555;">
            날짜별 전체 관객 규모의 변화를 확인하고 관객이 특히 많았던 날짜를 찾을 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 그래프 4
# ==================================================
st.divider()

st.header("4️⃣ 영화별 기간 일관객 TOP 10")

st.write(
    "이 기간 동안 영화별 일관객을 모두 더해 "
    "관객이 가장 많았던 영화 10편을 비교합니다."
)


# --------------------------------------------------
# 영화별 일관객 합계
# --------------------------------------------------
movie_total_all = (
    df.dropna(
        subset=["영화명", "일관객"]
    )
    .groupby(
        "영화명",
        as_index=False
    )["일관객"]
    .sum()
)


# --------------------------------------------------
# 영화별 10위권 등장 일수
# --------------------------------------------------
movie_days = (
    df.dropna(
        subset=["영화명", "날짜"]
    )
    .groupby(
        "영화명",
        as_index=False
    )["날짜"]
    .nunique()
)


movie_days = movie_days.rename(
    columns={
        "날짜": "10위권_등장_일수"
    }
)


# --------------------------------------------------
# 두 데이터를 합치기
# --------------------------------------------------
movie_summary = pd.merge(
    movie_total_all,
    movie_days,
    on="영화명",
    how="left"
)


# --------------------------------------------------
# TOP 10 영화
# --------------------------------------------------
top10_movies = (
    movie_summary
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(10)
    .copy()
)


if len(top10_movies) == 0:

    st.warning(
        "영화별 관객 데이터를 계산할 수 없습니다."
    )

else:

    # 작은 값부터 정렬
    # → 가로 막대그래프에서 큰 값이 위에 표시됨
    chart_data = (
        top10_movies
        .sort_values(
            "일관객",
            ascending=True
        )
    )


    # --------------------------------------------------
    # 가로 막대그래프
    # --------------------------------------------------
    fig4 = px.bar(
        chart_data,
        x="일관객",
        y="영화명",
        orientation="h",
        title="영화별 기간 일관객 TOP 10",
        labels={
            "일관객": "기간 일관객 합계 (명)",
            "영화명": "영화"
        },
        custom_data=[
            "10위권_등장_일수"
        ]
    )


    # --------------------------------------------------
    # 마우스 오버
    # --------------------------------------------------
    fig4.update_traces(
        hovertemplate=(
            "영화: %{y}<br>"
            "기간 일관객 합계: %{x:,.0f}명<br>"
            "10위권에 든 날수: %{customdata[0]}일"
            "<extra></extra>"
        )
    )


    fig4.update_layout(
        height=600,
        xaxis=dict(
            title="기간 일관객 합계 (명)",
            tickformat=","
        ),
        yaxis=dict(
            title="",
            categoryorder="total ascending"
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )


    st.plotly_chart(
        fig4,
        use_container_width=True
    )


    # --------------------------------------------------
    # TOP 10 상세 정보
    # --------------------------------------------------
    st.markdown(
        "#### 📌 TOP 10 영화 상세 정보"
    )

    top10_display = top10_movies.copy()

    top10_display["일관객"] = (
        top10_display["일관객"]
        .map(lambda x: f"{x:,.0f}명")
    )

    top10_display["10위권_등장_일수"] = (
        top10_display["10위권_등장_일수"]
        .map(lambda x: f"{x}일")
    )

    top10_display.columns = [
        "영화명",
        "기간 일관객 합계",
        "10위권에 든 날수"
    ]

    st.dataframe(
        top10_display,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 그래프 4 해석
# --------------------------------------------------
st.markdown(
    """
    <div style="
        padding:18px;
        margin-top:10px;
        margin-bottom:30px;
        border-radius:12px;
        background-color:#FFF3E0;
        border:1px solid #FFB74D;
    ">
        <h4 style="margin:0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>

        <p style="margin:0; color:#555;">
            기간 전체에서 관객이 많았던 영화와 10위권에 오래 머문 영화를 비교할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 그래프 5
# ==================================================
st.divider()

st.header("5️⃣ 월 × 요일별 일관객 합계 히트맵")

st.write(
    "날짜에서 월과 요일을 뽑아 "
    "월별·요일별 일관객 합계를 히트맵으로 비교합니다."
)


# --------------------------------------------------
# 히트맵용 데이터
# --------------------------------------------------
heatmap_df = df.dropna(
    subset=["날짜", "일관객"]
).copy()


# --------------------------------------------------
# 월 추출
# --------------------------------------------------
heatmap_df["월"] = heatmap_df["날짜"].dt.month


# --------------------------------------------------
# 요일 추출
# 월요일 = 0
# 일요일 = 6
# --------------------------------------------------
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]


heatmap_df["요일번호"] = (
    heatmap_df["날짜"].dt.weekday
)


heatmap_df["요일"] = (
    heatmap_df["요일번호"]
    .map(
        lambda x: weekday_names[x]
    )
)


# --------------------------------------------------
# 월 × 요일별 일관객 합계
# --------------------------------------------------
heatmap_data = (
    heatmap_df
    .groupby(
        ["월", "요일번호", "요일"],
        as_index=False
    )["일관객"]
    .sum()
)


# --------------------------------------------------
# 피벗 테이블
# --------------------------------------------------
heatmap_pivot = heatmap_data.pivot(
    index="월",
    columns="요일번호",
    values="일관객"
)


# --------------------------------------------------
# 1~12월 / 월요일~일요일 순서로 고정
# --------------------------------------------------
heatmap_pivot = heatmap_pivot.reindex(
    index=range(1, 13),
    columns=range(7)
)


# --------------------------------------------------
# 요일 이름으로 변경
# --------------------------------------------------
heatmap_pivot.columns = weekday_names


# --------------------------------------------------
# 히트맵
# --------------------------------------------------
if heatmap_pivot.notna().sum().sum() == 0:

    st.warning(
        "월·요일별 관객 데이터를 계산할 수 없습니다."
    )

else:

    fig5 = go.Figure(
        data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=[
                f"{month}월"
                for month in heatmap_pivot.index
            ],
            colorscale="YlOrRd",
            colorbar=dict(
                title="일관객 합계"
            ),
            hovertemplate=(
                "월: %{y}<br>"
                "요일: %{x}<br>"
                "일관객 합계: %{z:,.0f}명"
                "<extra></extra>"
            ),
            xgap=2,
            ygap=2
        )
    )


    fig5.update_layout(
        title="월 × 요일별 일관객 합계",
        height=600,
        xaxis=dict(
            title="요일",
            categoryorder="array",
            categoryarray=weekday_names
        ),
        yaxis=dict(
            title="월",
            autorange="reversed"
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )


    st.plotly_chart(
        fig5,
        use_container_width=True
    )


    # --------------------------------------------------
    # 히트맵 데이터 표
    # --------------------------------------------------
    st.markdown(
        "#### 📌 월 × 요일별 일관객 합계"
    )


    heatmap_display = heatmap_pivot.copy()


    heatmap_display.index = [
        f"{month}월"
        for month in heatmap_display.index
    ]


    heatmap_display = heatmap_display.map(
        lambda x: (
            f"{x:,.0f}명"
            if pd.notna(x)
            else "-"
        )
    )


    st.dataframe(
        heatmap_display,
        use_container_width=True
    )


# --------------------------------------------------
# 그래프 5 해석
# --------------------------------------------------
st.markdown(
    """
    <div style="
        padding:18px;
        margin-top:10px;
        margin-bottom:30px;
        border-radius:12px;
        background-color:#F3E5F5;
        border:1px solid #CE93D8;
    ">
        <h4 style="margin:0 0 8px 0;">
            💡 이 그래프로 알 수 있는 것
        </h4>

        <p style="margin:0; color:#555;">
            월별·요일별로 관객이 많이 몰리는 시기를 색의 진하기를 통해 한눈에 비교할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

