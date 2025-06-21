import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj

# 데이터 불러오기
df = pd.read_csv("bakery.csv", encoding="cp949")

# 유효한 좌표만 필터링
df = df.dropna(subset=["좌표정보x(epsg5174)", "좌표정보y(epsg5174)"])
df = df.rename(columns={
    '사업장명': 'name',
    '도로명전체주소': 'address',
    '좌표정보x(epsg5174)': 'x_5174',
    '좌표정보y(epsg5174)': 'y_5174'
})

# 좌표계 변환 (EPSG:5174 ➜ WGS84)
proj_5174 = pyproj.CRS("EPSG:5174")
proj_4326 = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(proj_5174, proj_4326, always_xy=True)

df["lon"], df["lat"] = transformer.transform(df["x_5174"].values, df["y_5174"].values)

# 지도 시각화
st.set_page_config(layout="wide")
st.title("🥐 전국 빵집 지도 시각화")
st.markdown("🗺️ 아래는 위생 정보 기반 제과점들의 위치입니다.")

fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data=["address"],
    zoom=6,
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
