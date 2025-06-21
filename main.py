import streamlit as st

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
    </style>
    """,
    unsafe_allow_html=True
)

# --- 데이터 (MBTI 분석 및 직업 추천) ---
# 실제 콘텐츠는 이 부분을 풍성하게 채워야 합니다!
mbti_data = {
    "ISTJ": {
        "description": "👩‍🏫 **세상의 소금, 만물의 기둥!** ISTJ는 책임감이 강하고 현실적인 성격으로, 뛰어난 집중력과 분석력을 바탕으로 일을 완벽하게 처리합니다. 논리적이고 체계적이며, 규칙과 전통을 중요하게 생각해요. 꼼꼼하고 신뢰할 수 있는 당신은 언제나 든든한 존재입니다! 🌟",
        "strengths": ["👍 현실적이고 실용적", "👍 책임감이 강함", "👍 꼼꼼하고 정확함", "👍 신뢰할 수 있음"],
        "weaknesses": ["👎 융통성이 부족할 수 있음", "👎 변화에 대한 저항", "👎 감정 표현에 서툴 수 있음"],
        "relationships": "🤝 인간관계에서는 진실성과 일관성을 중시하며, 한번 맺은 인연은 소중히 여깁니다. 불필요한 감정 소모를 싫어하고, 실질적인 도움을 주는 관계를 선호해요.",
        "careers": [
            {"name": "공무원 🏛️", "desc": "안정적이고 체계적인 환경에서 당신의 책임감을 발휘할 수 있습니다."},
            {"name": "회계사 📊", "desc": "정확성과 꼼꼼함이 요구되는 직업으로, 당신의 강점이 빛을 발할 거예요."},
            {"name": "경찰관 👮‍♂️", "desc": "규칙을 준수하고 질서를 유지하는 데 기여하며, 사회에 봉사하는 보람을 느낄 수 있습니다."},
            {"name": "연구원 🔬", "desc": "꼼꼼한 분석과 체계적인 연구 과정을 통해 새로운 사실을 밝혀낼 수 있습니다."},
        ]
    },
    "ENFP": {
        "description": "🎉 **자유로운 영혼의 옹호자!** ENFP는 넘치는 에너지와 호기심으로 가득 찬 따뜻하고 열정적인 성격입니다. 새로운 아이디어를 탐색하고 사람들과 교류하는 것을 즐기며, 긍정적인 영향력을 주변에 퍼뜨리는 존재입니다. 당신의 상상력과 포용력은 세상을 더 다채롭게 만들어요! ✨",
        "strengths": ["👍 창의적이고 상상력이 풍부함", "👍 사람들과의 관계를 즐김", "👍 긍정적이고 낙천적", "👍 새로운 아이디어에 개방적"],
        "weaknesses": ["👎 과도한 낙관주의", "👎 쉽게 지루해함", "👎 시작은 많으나 끝은 미미할 수 있음"],
        "relationships": "🤝 사람들과의 깊은 유대감을 중요시하며, 타인의 감정에 공감하고 지지하는 데 능숙합니다. 당신의 밝은 에너지는 주변 사람들에게 큰 기쁨을 줍니다.",
        "careers": [
            {"name": "컨설턴트 💡", "desc": "다양한 문제에 대한 창의적인 해결책을 제시하며 사람들을 도울 수 있습니다."},
            {"name": "마케터 📢", "desc": "새로운 아이디어를 기획하고 사람들의 마음을 사로잡는 데 재능을 발휘할 수 있습니다."},
            {"name": "예술가 🎨", "desc": "자유로운 상상력과 표현력을 통해 자신만의 독창적인 작품을 만들 수 있습니다."},
            {"name": "작가 ✍️", "desc": "독특한 관점과 스토리를 통해 사람들에게 영감을 줄 수 있습니다."},
        ]
    },
    # 여기에 다른 MBTI 유형들을 추가하세요!
    # "ISFJ", "INFJ", "ISTP", "INFP", "INTJ", "INTP",
    # "ESTP", "ESFP", "ENFJ", "ENTP",
    # "ESTJ", "ESFJ", "ENTJ"
}

# --- 앱 시작 ---
st.markdown("<h1>✨ MBTI 진로 탐험대 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3em; color: #6A5ACD;'>👋 반가워요! 당신의 잠재력을 찾아줄 MBTI 진로 탐험 🗺️에 오신 것을 환영합니다! 🎉</p>", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1543269865-cbf427352390?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
         caption="💡 당신의 잠재력을 찾아보세요!", use_column_width=True)

st.markdown("---")

with st.container():
    st.markdown("<h2>🔍 당신의 MBTI를 선택해주세요! 🤔</h2>", unsafe_allow_html=True)
    mbti_options = ["MBTI 선택"] + list(mbti_data.keys())
    selected_mbti = st.selectbox("", mbti_options, help="당신의 MBTI 유형을 골라보세요!")

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
            st.markdown(f"""
                <div class="job-card">
                    <span class="emoji-large">{job['name'].split(" ")[1] if len(job['name'].split(" ")) > 1 else '💼'}</span>
                    <div>
                        <h3>{job['name'].split(" ")[0]}</h3>
                        <p>{job['desc']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"</div>", unsafe_allow_html=True)

        st.markdown("<p style='text-align: center; font-size: 1.5em; margin-top: 50px; color: #8A2BE2;'>💖 당신의 멋진 미래를 응원합니다! 🚀 꿈을 향해 나아가세요! 💖</p>", unsafe_allow_html=True)
    else:
        st.info("⬆️ 위에 MBTI 유형을 선택하여 당신의 진로를 탐색해보세요!")

# 사이드바 (선택 사항)
with st.sidebar:
    st.header("📖 MBTI란?")
    st.write("MBTI(Myers-Briggs Type Indicator)는 개인의 선호도를 바탕으로 성격을 16가지 유형으로 분류하는 성격 유형 검사입니다.")
    st.write("MBTI를 통해 자신을 이해하고 타인과의 관계를 개선하며, 적절한 진로를 탐색하는 데 도움을 받을 수 있습니다.")
    st.markdown("---")
    st.write("© 2025 MBTI 진로 탐험대")
    st.write("Made with ❤️ by AI")
