import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("bakery.csv", encoding="cp949")

# 필수 좌표 정보가 있는 행만 필터링
df_map = df[['사업장명', '도로명전체주소', '좌표정보x(epsg5174)', '좌표정보y(epsg5174)']]
df_map = df_map.dropna(subset=['좌표정보x(epsg5174)', '좌표정보y(epsg5174)'])

# 컬럼 이름 변경 (가독성 향상)
df_map = df_map.rename(columns={
    '사업장명': 'name',
    '도로명전체주소': 'address',
    '좌표정보x(epsg5174)': 'lon',
    '좌표정보y(epsg5174)': 'lat'
})

# Streamlit 앱 구성
st.set_page_config(layout='wide')
st.title("🥐 전국 빵집 지도 시각화")

st.markdown("🗺️ 아래는 위생 정보 기반 제과점들의 위치입니다.")

# 지도 시각화 (Plotly)
fig = px.scatter_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data=["address"],
    zoom=5,
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
