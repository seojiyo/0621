import streamlit as st
# 데이터를 담은 파일을 불러옵니다.
from mbti_data_content import mbti_data

# 페이지 설정
st.set_page_config(
    page_title="✨ MBTI 진로 탐험대 ✨",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS 스타일링 (화려하고 예쁘게!) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap'); /* 귀여운 폰트 추가 */

    body {
        font-family: 'Jua', sans-serif;
        background: linear-gradient(135deg, #f0f9ff 0%, #cbebff 100%); /* 그라데이션 배경 */
        color: #333;
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
        padding-top: 30px;
    }
    .stButton>button {
        background-color: #FF69B4; /* 핑크 버튼 */
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF1493; /* 진한 핑크 */
        transform: translateY(-2px);
    }
    .stSelectbox>div>div {
        border-radius: 12px;
        border: 2px solid #6A5ACD; /* 보라색 테두리 */
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stMarkdown h1 {
        color: #8A2BE2; /* 보라색 헤더 */
        text-align: center;
        font-size: 3.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    .stMarkdown h2 {
        color: #4B0082; /* 진한 보라색 서브 헤더 */
        font-size: 2.2em;
        border-bottom: 3px solid #FFD700; /* 황금색 밑줄 */
        padding-bottom: 10px;
        margin-top: 40px;
        margin-bottom: 25px;
    }
    .stMarkdown h3 {
        color: #DA70D6; /* 연한 보라색 */
        font-size: 1.8em;
        margin-top: 30px;
    }
    .stMarkdown p {
        font-size: 1.1em;
        line-height: 1.8;
        color: #555;
    }
    .stContainer {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        margin-bottom: 30px;
    }
    .emoji-large {
        font-size: 3em;
        margin-right: 15px;
    }
    .job-card {
        background-color: #fffacd; /* 레몬 쉬폰 */
        border-left: 5px solid #FFD700;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
    }
    /* 새로운 CSS: 중앙 정렬을 위한 flexbox */
    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 앱 시작 ---
st.markdown("<h1>✨ MBTI 진로 탐험대 🚀</h1>", unsafe_allow_html=True)

# 환영 메시지와 이미지, 선택 박스를 중앙 정렬하기 위해 컨테이너 사용
with st.container():
    st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.3em; color: #6A5ACD; margin-bottom: 20px;'>👋 반가워요! 당신의 잠재력을 찾아줄 MBTI 진로 탐험 🗺️에 오신 것을 환영합니다! 🎉</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 2em;'>🎇</p>", unsafe_allow_html=True) # 폭죽 이모지 간격 추가

    # 이미지 경로 수정: 로컬에 저장된 이미지 경로 사용
    # images 폴더 안에 main_image.jpg 파일이 있다고 가정합니다.
    try:
        st.image("images/main_image.jpg",
                 caption="💡 당신의 잠재력을 찾아보세요!",
                 use_container_width=True)
    except FileNotFoundError:
        st.warning("이미지 파일 (images/main_image.jpg)을 찾을 수 없습니다. 경로를 확인해주세요! 🚨")
        st.markdown("<p style='text-align: center; font-size: 1.1em; color: gray;'>임시 이미지: 🖼️</p>", unsafe_allow_html=True)


    st.markdown("<p style='text-align: center; font-size: 1.3em; margin-top: 30px;'><h2>🔍 당신의 MBTI를 선택해주세요! 🤔</h2></p>", unsafe_allow_html=True) # 제목을 H2로 변경하고 간격 추가
    
    # 선택 박스 중앙 정렬을 위해 컬럼 사용
    col1, col2, col3 = st.columns([1, 2, 1]) # 가운데 컬럼을 넓게 설정
    with col2: # 가운데 컬럼에 selectbox 배치
        mbti_options = ["MBTI 선택"] + sorted(list(mbti_data.keys()))
        selected_mbti = st.selectbox("", mbti_options, help="당신의 MBTI 유형을 골라보세요!")

    st.markdown("</div>", unsafe_allow_html=True) # centered-content 닫기

st.markdown("---") # 구분선 추가

if selected_mbti != "MBTI 선택":
    data = mbti_data[selected_mbti]

    st.markdown(f"<div class='stContainer'>", unsafe_allow_html=True)
    st.markdown(f"<h2>✨ {selected_mbti} 분석: 당신은 이런 사람! ✨</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>{data['description']}</p>", unsafe_allow_html=True)

    st.markdown("<h3>💪 강점</h3>", unsafe_allow_html=True)
    for strength in data['strengths']:
        st.markdown(f"<p>{strength}</p>", unsafe_allow_html=True)

    st.markdown("<h3>🚧 약점 (개선할 점)</h3>", unsafe_allow_html=True)
    for weakness in data['weaknesses']:
        st.markdown(f"<p>{weakness}</p>", unsafe_allow_html=True)

    st.markdown("<h3>🤝 대인 관계</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>{data['relationships']}</p>", unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)


    st.markdown(f"<div class='stContainer'>", unsafe_allow_html=True)
    st.markdown(f"<h2>🌈 {selected_mbti}에게 추천하는 직업! 당신의 미래를 빛낼 선택! 🌟</h2>", unsafe_allow_html=True)
    for job in data['careers']:
        # 직업 이름에서 이모지를 추출하거나 기본 이모지 사용
        job_parts = job['name'].split(" ")
        job_emoji = '💼'
        job_name_display = job['name']
        
        if len(job_parts) > 1:
            last_part = job_parts[-1]
            # 이모지인지 판단 (알파벳, 숫자가 아니고 길이가 짧은 경우)
            if not last_part.isalpha() and not last_part.isdigit() and len(last_part) <= 4:
                job_emoji = last_part
                job_name_display = " ".join(job_parts[:-1]) # 이모지 제외한 이름
            else:
                job_name_display = job['name'] # 이모지가 아니면 전체 이름 사용
        else:
            job_name_display = job['name'] # 단어 하나면 그대로 사용

        st.markdown(f"""
            <div class="job-card">
                <span class="emoji-large">{job_emoji}</span>
                <div>
                    <h3>{job_name_display}</h3>
                    <p>{job['desc']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown(f"</div>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; font-size: 1.5em; margin-top: 50px; color: #8A2BE2;'>💖 당신의 멋진 미래를 응원합니다! 🚀 꿈을 향해 나아가세요! 💖</p>", unsafe_allow_html=True)
else:
    # 선택 전 안내 메시지도 중앙 정렬 및 디자인 강조
    st.markdown("<div class='stContainer' style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.5em; color: #6A5ACD;'>⬆️ 위에 MBTI 유형을 선택하여 당신의 잠재력을 탐색해보세요! 💫</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 2.5em;'>💡🚀</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# 사이드바
with st.sidebar:
    st.header("📖 MBTI란?")
    st.write("MBTI(Myers-Briggs Type Indicator)는 개인의 선호도를 바탕으로 성격을 16가지 유형으로 분류하는 성격 유형 검사입니다.")
    st.write("MBTI를 통해 자신을 이해하고 타인과의 관계를 개선하며, 적절한 진로를 탐색하는 데 도움을 받을 수 있습니다.")
    st.markdown("---")
    st.write("© 2025 MBTI 진로 탐험대")
    st.write("Made with ❤️ by AI")
    st.markdown("[MBTI 무료 테스트 하러 가기](https://www.16personalities.com/ko/무료-성격-유형-검사)")
