import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj

# Streamlit 설정
st.set_page_config(layout="wide")
st.title("🥐 전국 빵집 지도 시각화")
st.markdown("🗺️ 제과점의 영업상태, 프랜차이즈 여부, 시설 규모별 색상 표현 옵션을 제공합니다.")

# 데이터 불러오기
df = pd.read_csv("bakery.csv", encoding="cp949")

# 전처리
df = df.dropna(subset=["좌표정보x(epsg5174)", "좌표정보y(epsg5174)", "시설총규모"])
df = df[df["시설총규모"] > 0]
df = df.rename(columns={
    '사업장명': 'name',
    '도로명전체주소': 'address',
    '좌표정보x(epsg5174)': 'x_5174',
    '좌표정보y(epsg5174)': 'y_5174',
    '영업상태명': 'status',
    '시설총규모': 'size'
})

# 좌표 변환
proj_5174 = pyproj.CRS("EPSG:5174")
proj_4326 = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(proj_5174, proj_4326, always_xy=True)
df["lon"], df["lat"] = transformer.transform(df["x_5174"].values, df["y_5174"].values)

# 그룹 구분
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

# 🔘 UI 요소
col1, col2, col3 = st.columns(3)
with col1:
    show_closed = st.checkbox("폐업 제과점 표시", value=True)
with col2:
    show_franchise = st.checkbox("프랜차이즈 표시", value=True)
with col3:
    use_color_by_size = st.checkbox("규모별 색상 표현", value=True)

# 필터링
df = df[df["status"] != "폐업"] if not show_closed else df
df = df[df["group"] != "프랜차이즈"] if not show_franchise else df

# 색상 맵핑
if use_color_by_size:
    color_map = {
        "소형 빵집": "orange",
        "중형 빵집": "skyblue",
        "대형 빵집": "darkblue",
        "프랜차이즈": "red"
    }
else:
    color_map = {
        "소형 빵집": "gray",
        "중형 빵집": "gray",
        "대형 빵집": "gray",
        "프랜차이즈": "gray"
    }

# 툴팁 구성
df["hover_name"] = df["name"]
df["hover_address"] = df["address"]

# 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color="group",
    color_discrete_map=color_map,
    hover_name="hover_name",
    hover_data={"hover_address": True, "group": False, "lat": False, "lon": False},
    zoom=6,
    center={"lat": 36.5, "lon": 127.8},
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# 지도 출력
st.plotly_chart(fig, use_container_width=True)
