import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj

# 기본 설정
st.set_page_config(layout="wide")
st.title("🥐 전국 빵집 지도 시각화")
st.markdown("🗺️ 아래는 위생 정보 기반 제과점들의 위치입니다.")

# 데이터 불러오기
df = pd.read_csv("bakery.csv", encoding="cp949")

# 전처리
df = df.dropna(subset=["좌표정보x(epsg5174)", "좌표정보y(epsg5174)"])
df = df.rename(columns={
    '사업장명': 'name',
    '도로명전체주소': 'address',
    '좌표정보x(epsg5174)': 'x_5174',
    '좌표정보y(epsg5174)': 'y_5174',
    '영업상태명': 'status'
})

# 좌표 변환
proj_5174 = pyproj.CRS("EPSG:5174")
proj_4326 = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(proj_5174, proj_4326, always_xy=True)
df["lon"], df["lat"] = transformer.transform(df["x_5174"].values, df["y_5174"].values)

# 색상 라벨 지정
def assign_group(row):
    if "파리바게뜨" in row["name"] or "뚜레주르" in row["name"]:
        return "프랜차이즈"
    elif row["status"] == "폐업":
        return "폐업"
    else:
        return "일반제과점"

df["group"] = df.apply(assign_group, axis=1)

# 체크박스 UI
col1, col2 = st.columns(2)
with col1:
    show_closed = st.checkbox("폐업 제과점 표시", value=False)
with col2:
    show_franchise = st.checkbox("프랜차이즈(파리바게뜨·뚜레주르) 표시", value=True)

# 상태 저장용 초기 중심
if "zoom" not in st.session_state:
    st.session_state.zoom = 6
if "center" not in st.session_state:
    st.session_state.center = {"lat": 36.5, "lon": 127.8}

# 지도용 데이터 필터링
filter_conditions = ["일반제과점"]
if show_closed:
    filter_conditions.append("폐업")
if show_franchise:
    filter_conditions.append("프랜차이즈")

filtered = df[df["group"].isin(filter_conditions)].copy()

# 색상 지정
color_map = {
    "프랜차이즈": "rgb(0,255,0)",
    "폐업": "rgb(120,120,120)",
    "일반제과점": "blue"
}

# 툴팁 제한: 표시된 데이터만 툴팁 활성화
filtered["hover_name"] = filtered["name"]
filtered["hover_address"] = filtered["address"]

# 지도 시각화
fig = px.scatter_mapbox(
    filtered,
    lat="lat",
    lon="lon",
    color="group",
    color_discrete_map=color_map,
    hover_name="hover_name",
    hover_data={"hover_address": True, "group": False, "lat": False, "lon": False},
    zoom=st.session_state.zoom,
    center=st.session_state.center,
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
