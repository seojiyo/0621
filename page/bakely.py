import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj

# 페이지 설정
st.set_page_config(layout="wide")
st.title("🥐 전국 빵집 지도 시각화")
st.markdown("📍 제과점의 프랜차이즈 여부, 시설 규모에 따라 색상과 크기를 다르게 표시합니다.")

# 데이터 로딩
df = pd.read_csv("bakery.csv", encoding="cp949")

# 전처리: 결측치 및 면적 0 제거
df = df.dropna(subset=["좌표정보x(epsg5174)", "좌표정보y(epsg5174)", "시설총규모"])
df = df[df["시설총규모"] > 0]

# 컬럼 이름 변경
df = df.rename(columns={
    '사업장명': 'name',
    '도로명전체주소': 'address',
    '좌표정보x(epsg5174)': 'x_5174',
    '좌표정보y(epsg5174)': 'y_5174',
    '영업상태명': 'status',
    '시설총규모': 'size'
})

# 좌표계 변환 (EPSG:5174 → EPSG:4326)
proj_5174 = pyproj.CRS("EPSG:5174")
proj_4326 = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(proj_5174, proj_4326, always_xy=True)
df["lon"], df["lat"] = transformer.transform(df["x_5174"].values, df["y_5174"].values)

# 그룹 지정 함수
def assign_group(row):
    if any(x in row["name"] for x in ["파리바게뜨", "파리바게트", "뚜레주르"]):
        return "프랜차이즈"
    elif row["size"] >= 100:
        return "대형 빵집"
    elif row["size"] >= 50:
        return "중형 빵집"
    else:
        return "소형 빵집"

df["group"] = df.apply(assign_group, axis=1)

# 체크박스 UI
col1, col2 = st.columns(2)
with col1:
    show_closed = st.checkbox("폐업 제과점 표시", value=True)
with col2:
    show_franchise = st.checkbox("프랜차이즈 표시", value=True)

# 필터링
if not show_closed:
    df = df[df["status"] != "폐업"]
if not show_franchise:
    df = df[df["group"] != "프랜차이즈"]

# 색상 맵핑
color_map = {
    "소형 빵집": "#A6CEE3",   # 밝은 파랑
    "중형 빵집": "#1F78B4",   # 중간 파랑
    "대형 빵집": "#08306B",   # 진한 파랑
    "프랜차이즈": "red"
}

# 마커 크기 설정 (면적 기반, 프랜차이즈는 고정)
df["marker_size"] = df["size"].apply(lambda s: max(s * 1.5, 10))
df.loc[df["group"] == "프랜차이즈", "marker_size"] = 20

# 툴팁 정보 제한
df["hover_name"] = df["name"]
df["hover_address"] = df["address"]

# 지도 생성
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color="group",
    size="marker_size",
    size_max=30,
    color_discrete_map=color_map,
    hover_name="hover_name",
    hover_data={"hover_address": True, "group": False, "lat": False, "lon": False, "marker_size": False},
    zoom=6,
    center={"lat": 36.5, "lon": 127.8},
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# 지도 출력
st.plotly_chart(fig, use_container_width=True)
