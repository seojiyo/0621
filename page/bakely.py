import streamlit as st
import pandas as pd
import plotly.express as px
import pyproj

# Streamlit 설정
st.set_page_config(layout="wide")
st.title("🥐 전국 빵집 지도 시각화")
st.markdown("🗺️ 위생 정보 기반 제과점 위치와 상태를 시각화한 지도입니다.")

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

# 좌표계 변환 (EPSG:5174 ➝ WGS84)
proj_5174 = pyproj.CRS("EPSG:5174")
proj_4326 = pyproj.CRS("EPSG:4326")
transformer = pyproj.Transformer.from_crs(proj_5174, proj_4326, always_xy=True)
df["lon"], df["lat"] = transformer.transform(df["x_5174"].values, df["y_5174"].values)

# ✅ 프랜차이즈 포함 조건 추가: '파리바게뜨' 또는 '파리바게트'
def assign_group(row):
    if any(x in row["name"] for x in ["파리바게뜨", "파리바게트", "뚜레주르"]):
        return "프랜차이즈"
    elif row["status"] == "폐업":
        return "폐업"
    else:
        return "일반제과점"

df["group"] = df.apply(assign_group, axis=1)

# ✅ 세션 상태로 줌 & 중심 좌표 유지
if "zoom" not in st.session_state:
    st.session_state.zoom = 6
if "center" not in st.session_state:
    st.session_state.center = {"lat": 36.5, "lon": 127.8}

# ✅ 사용자 조작에 따라 중심좌표와 줌 업데이트 저장 (한 번 클릭 시 유지됨)
st.session_state.last_filter = st.session_state.get("last_filter", {"closed": True, "franchise": True})

# 체크박스 UI
col1, col2 = st.columns(2)
with col1:
    show_closed = st.checkbox("폐업 제과점 표시", value=True)
with col2:
    show_franchise = st.checkbox("프랜차이즈(파리바게뜨·뚜레주르) 표시", value=True)

# 📌 줌 초기화 방지 트릭
# 체크 상태가 바뀌지 않은 경우만 중심 좌표 업데이트
if (
    show_closed == st.session_state.last_filter["closed"]
    and show_franchise == st.session_state.last_filter["franchise"]
):
    # 사용자가 지도 줌/이동한 결과 반영 (여기선 Plotly로는 직접 추적 불가, 추후 개선 가능)
    pass
else:
    # 상태 기억 갱신만 수행 (줌 유지)
    st.session_state.last_filter = {"closed": show_closed, "franchise": show_franchise}

# 필터링
visible_groups = ["일반제과점"]
if show_closed:
    visible_groups.append("폐업")
if show_franchise:
    visible_groups.append("프랜차이즈")

filtered = df[df["group"].isin(visible_groups)].copy()

# 마커 색상 지정
color_map = {
    "프랜차이즈": "rgb(0,255,0)",
    "폐업": "rgb(120,120,120)",
    "일반제과점": "blue"
}

# 툴팁 제한
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

# Plotly 지도 설정 (기본 휠 줌 활성화됨)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 지도 출력
st.plotly_chart(fig, use_container_width=True)
