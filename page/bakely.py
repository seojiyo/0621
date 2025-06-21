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

# 색상 컬럼 생성
def assign_color(row):
    if "파리바게뜨" in row["name"] or "뚜레주르" in row["name"]:
        return "프랜차이즈"
    elif row["status"] == "폐업":
        return "폐업"
    else:
        return "일반제과점"

df["marker_color"] = df.apply(assign_color, axis=1)

# 상태 저장을 위한 기본 zoom & center (한반도 중앙 기준)
if "zoom" not in st.session_state:
    st.session_state.zoom = 6
if "center" not in st.session_state:
    st.session_state.center = {"lat": 36.5, "lon": 127.8}

# 체크박스 설정
show_closed = st.checkbox("폐업한 제과점도 지도에 표시하기", value=False)

# 지도용 데이터 필터링
if not show_closed:
    df_map = df[df["status"] == "영업/정상"]
    df_map = df_map[df_map["marker_color"] != "폐업"]
else:
    df_map = df.copy()

# 지도 시각화
fig = px.scatter_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data=["address", "status"],
    color="marker_color",
    color_discrete_map={
        "프랜차이즈": "rgb(0,255,0)",    # 초록색
        "폐업": "rgb(120,120,120)",     # 회색
        "일반제과점": "blue"
    },
    zoom=st.session_state.zoom,
    center=st.session_state.center,
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
