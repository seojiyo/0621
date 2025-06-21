import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj

# 1. 데이터 로딩 및 전처리
df = pd.read_csv("bakery.csv", encoding="cp949")

# 필수 컬럼 정리 및 결측 제거
df = df.dropna(subset=["좌표정보x(epsg5174)", "좌표정보y(epsg5174)"])
df = df.rename(columns={
    '사업장명': 'name',
    '도로명전체주소': 'address',
    '좌표정보x(epsg5174)': 'x_5174',
    '좌표정보y(epsg5174)': 'y_5174',
    '영업상태명': 'status'
})

# 2. 좌표계 변환 (EPSG:5174 → WGS84)
proj_5174 = pyproj.CRS("EPSG:5174")
proj_4326 = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(proj_5174, proj_4326, always_xy=True)

df["lon"], df["lat"] = transformer.transform(df["x_5174"].values, df["y_5174"].values)

# 3. Streamlit UI 설정
st.set_page_config(layout="wide")
st.title("🥐 전국 빵집 지도 시각화")
st.markdown("🗺️ 아래는 위생 정보 기반 제과점들의 위치입니다.")

# 체크박스 설정
show_closed = st.checkbox("폐업한 제과점도 지도에 표시하기", value=False)

# 4. 시각화용 데이터 필터링
if not show_closed:
    df_map = df[df["status"] == "영업/정상"]
    color_col = "status"
else:
    df_map = df[df["status"].isin(["영업/정상", "폐업"])]
    # 색상 지정: 폐업은 회색, 영업은 기본색
    df_map["color"] = df_map["status"].apply(lambda x: "gray" if x == "폐업" else "blue")
    color_col = "color"

# 5. 지도 시각화
fig = px.scatter_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data=["address", "status"],
    color=color_col,
    zoom=6,
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
