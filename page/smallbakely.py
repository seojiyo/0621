# 🍞 작은 빵집 판매 데이터 분석 및 시각화 Streamlit 앱

## 📁 파일 구조 (예정)
# bakery-insight-app/
# ├── app.py                 ← Streamlit 메인 앱
# ├── data/
# │   └── bakery_sales.csv   ← 업로드된 데이터 파일
# ├── utils/
# │   ├── preprocessing.py   ← 데이터 전처리 함수들
# │   └── analysis.py       ← 분석 함수들 (요일별, 세트분석 등)
# └── requirements.txt      ← 필요한 라이브러리 목록

# — app.py (메인 앱 코드) —
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils.preprocessing import clean_data
from utils.analysis import *

st.set_page_config(page_title="반제반제 방지보도 앱 테스트", layout="wide")
st.title("🍞반제 정보를 통해 복잡한 보물만 보내주는 지도 앱")

uploaded_file = st.file_uploader("파일을 업로드해주세요 (CSV)", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df = clean_data(df_raw)

    st.sidebar.header("패널 선택")
    panel = st.sidebar.radio("시간대별 통계/요일\uubcc4 반응/제품 목록/연관회계", [
        "통계 보기", "요일 보기", "제품 통계", "세트 방법"
    ])

    if panel == "통계 보기":
        st.subheader("토토에 일자별 매출 차포")
        daily = df.groupby("date")["total"].sum().reset_index()
        fig = px.line(daily, x="date", y="total", title="일별 매출 가격 초점")
        st.plotly_chart(fig)

    elif panel == "요일 보기":
        st.subheader("요일별 매출 통계")
        dow = df.groupby("day of week")["total"].mean().reset_index()
        fig = px.bar(dow, x="day of week", y="total", title="요일이 무엇일때 가장 잘 보내요?")
        st.plotly_chart(fig)

    elif panel == "제품 통계":
        st.subheader("TOP 인기 제품")
        item_sum = df.iloc[:, 4:].sum().sort_values(ascending=False).head(10)
        st.bar_chart(item_sum)

    elif panel == "세트 방법":
        st.subheader("자주 같이 판매되는 제품 조합")
        pair_df = get_frequent_pairs(df)
        fig = px.treemap(pair_df, path=["item1", "item2"], values="count",
                         title="매일 판매되는 세트 조합")
        st.plotly_chart(fig)

else:
    st.info("업로드한 CSV 파일을 기본으로 통계합니다")

# — preprocessing.py —
def clean_data(df):
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["date"] = df["datetime"].dt.date
    df = df.dropna(subset=["datetime", "total"])
    df.fillna(0, inplace=True)
    return df

# — analysis.py —
from itertools import combinations

def get_frequent_pairs(df):
    df_items = df.iloc[:, 4:]  # product columns
    pairs = {}
    for _, row in df_items.iterrows():
        items = row[row > 0].index.tolist()
        for pair in combinations(items, 2):
            pair = tuple(sorted(pair))
            pairs[pair] = pairs.get(pair, 0) + 1

    pair_df = pd.DataFrame([{"item1": k[0], "item2": k[1], "count": v} for k, v in pairs.items()])
    pair_df = pair_df.sort_values(by="count", ascending=False).head(20)
    return pair_df

# — requirements.txt —
# streamlit
# pandas
# plotly
# seaborn
