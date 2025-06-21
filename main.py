import streamlit as st
import os

# --- 1. MBTI 데이터 정의 (main.py 내부에 직접 포함) ---
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
    "ISFJ": {
        "description": "💖 **용감한 수호자!** ISFJ는 온화하고 헌신적이며, 타인을 돕는 데 큰 기쁨을 느끼는 성격입니다. 책임감이 강하고 실용적이며, 세심한 관찰력으로 주변 사람들을 배려합니다. 조용하지만 강한 내면을 가진 당신은 언제나 주변을 밝히는 등대입니다! 🕯️",
        "strengths": ["👍 헌신적이고 따뜻함", "👍 책임감이 강하고 성실함", "👍 뛰어난 관찰력", "👍 타인의 감정에 민감함"],
        "weaknesses": ["👎 거절에 어려움을 느낌", "👎 변화에 대한 불안감", "👎 자신의 필요를 뒷전으로 둘 수 있음"],
        "relationships": "🤝 주변 사람들을 극진히 보살피고 보호하려는 경향이 강합니다. 갈등을 피하고 조화를 추구하며, 깊고 안정적인 관계를 선호합니다.",
        "careers": [
            {"name": "간호사 💉", "desc": "타인을 돌보고 돕는 데 있어 당신의 헌신적인 성격이 큰 힘이 됩니다."},
            {"name": "교사 🧑‍🏫", "desc": "학생들을 돌보고 가르치는 데 있어 당신의 인내심과 따뜻함이 발휘됩니다."},
            {"name": "사회복지사 🫂", "desc": "어려움에 처한 사람들을 돕고 지원하는 데 보람을 느낄 수 있습니다."},
            {"name": "사서 📚", "desc": "정리 정돈을 좋아하고 조용한 환경에서 봉사하는 데 적합합니다."},
        ]
    },
    "INFJ": {
        "description": "🌌 **선의의 옹호자!** INFJ는 깊은 통찰력과 강한 신념을 가진 이상주의자입니다. 타인의 성장을 돕고 세상을 더 나은 곳으로 만들고자 하는 열망이 강합니다. 복잡한 문제를 직관적으로 이해하고, 남들이 보지 못하는 잠재력을 발견하는 데 능숙합니다. 💫",
        "strengths": ["👍 통찰력이 뛰어남", "👍 강한 이상과 신념", "👍 타인의 감정에 깊이 공감", "👍 높은 도덕성"],
        "weaknesses": ["👎 너무 높은 이상", "👎 혼자만의 세계에 갇힐 수 있음", "👎 비판에 민감함"],
        "relationships": "🤝 소수의 깊고 의미 있는 관계를 추구합니다. 타인의 고통에 깊이 공감하며, 진정성 있는 소통을 통해 유대감을 형성하려 노력합니다.",
        "careers": [
            {"name": "심리학자 🧠", "desc": "인간의 내면을 탐구하고 타인의 문제를 해결하는 데 기여할 수 있습니다."},
            {"name": "상담사 🛋️", "desc": "타인의 어려움에 공감하고 실질적인 조언을 제공하는 데 능숙합니다."},
            {"name": "작가 ✍️", "desc": "자신의 깊은 통찰과 메시지를 글로 표현하여 사람들에게 영감을 줄 수 있습니다."},
            {"name": "인권 운동가 ⚖️", "desc": "세상을 더 정의롭게 만들려는 당신의 강한 신념을 발휘할 수 있습니다."},
        ]
    },
    "INTJ": {
        "description": "🧠 **전략가, 과학자!** INTJ는 논리적이고 분석적이며, 복잡한 시스템을 이해하고 개선하는 데 탁월한 능력을 발휘합니다. 독립적이고 목표 지향적이며, 미래를 내다보는 통찰력으로 장기적인 계획을 수립합니다. 당신의 지적 탐구심은 한계가 없습니다! 🔬",
        "strengths": ["👍 뛰어난 분석력과 논리력", "👍 독립적이고 결단력 있음", "👍 장기적인 비전 제시", "👍 효율성 추구"],
        "weaknesses": ["👎 타인의 감정에 둔감할 수 있음", "👎 완벽주의 경향", "👎 비판적 사고가 강함"],
        "relationships": "🤝 감정보다는 논리를 우선시하는 경향이 있어 차가워 보일 수 있습니다. 하지만 한번 신뢰를 쌓은 사람에게는 매우 충실하며, 지적인 교류를 즐깁니다.",
        "careers": [
            {"name": "소프트웨어 개발자 💻", "desc": "복잡한 시스템을 설계하고 구현하는 데 있어 당신의 분석력이 빛을 발합니다."},
            {"name": "과학자 🧪", "desc": "미지의 영역을 탐구하고 새로운 이론을 정립하는 데 적합합니다."},
            {"name": "전략 컨설턴트 📈", "desc": "기업의 문제를 분석하고 혁신적인 해결책을 제시하는 데 능숙합니다."},
            {"name": "건축가 🏗️", "desc": "복잡한 구조물을 설계하고 현실화하는 데 당신의 논리적인 사고가 필요합니다."},
        ]
    },
    "ISTP": {
        "description": "🔧 **만능 재주꾼!** ISTP는 호기심 많고 모험심이 강하며, 손으로 직접 만들고 탐구하는 것을 즐깁니다. 논리적이고 실용적이며, 위기 상황에서도 침착하게 문제를 해결하는 능력이 뛰어납니다. 당신의 손재주와 문제 해결 능력은 누구도 따라올 수 없습니다! 🛠️",
        "strengths": ["👍 뛰어난 문제 해결 능력", "👍 실용적이고 현실적", "👍 독립적이고 적응력 뛰어남", "👍 손재주가 좋음"],
        "weaknesses": ["👎 충동적일 수 있음", "👎 장기 계획에 약함", "👎 감정 표현에 서툴 수 있음"],
        "relationships": "🤝 개인적인 공간과 자유를 중요시하며, 불필요한 감정 소모나 드라마를 싫어합니다. 직접적인 경험을 공유하며 유대감을 형성하는 것을 선호합니다.",
        "careers": [
            {"name": "엔지니어 ⚙️", "desc": "기계나 시스템을 설계하고 고치는 데 당신의 실용적인 능력이 필요합니다."},
            {"name": "파일럿 ✈️", "desc": "새로운 환경에 빠르게 적응하고 위기 상황에 침착하게 대처하는 데 능숙합니다."},
            {"name": "경찰 특공대 👮‍♂️", "desc": "빠른 판단력과 뛰어난 신체 능력을 요구하는 직업에 적합합니다."},
            {"name": "목수 🔨", "desc": "손으로 직접 무언가를 만들고 완성하는 데 보람을 느낄 수 있습니다."},
        ]
    },
    "ISFP": {
        "description": "🎨 **호기심 많은 예술가!** ISFP는 온화하고 겸손하며, 아름다움과 조화를 추구하는 예술적인 성격입니다. 현재를 즐기고 자유로운 영혼을 가지고 있으며, 주변 세상의 아름다움을 예민하게 포착합니다. 당신의 감성과 창의력은 세상을 더욱 풍요롭게 만듭니다! 🌸",
        "strengths": ["👍 예술적 감각이 뛰어남", "👍 온화하고 겸손함", "👍 현재를 즐김", "👍 타인의 감정에 공감"],
        "weaknesses": ["👎 비판에 취약함", "👎 결단력이 부족할 수 있음", "👎 계획성이 부족할 수 있음"],
        "relationships": "🤝 진솔하고 자연스러운 관계를 선호하며, 타인의 개성을 존중합니다. 갈등을 피하고 평화로운 분위기를 유지하려 노력합니다.",
        "careers": [
            {"name": "예술가 🧑‍🎨", "desc": "자유롭게 자신을 표현하고 아름다움을 창조하는 데 재능을 발휘할 수 있습니다."},
            {"name": "디자이너 👗", "desc": "시각적인 아름다움을 만들고 사람들의 삶에 색을 더하는 직업입니다."},
            {"name": "플로리스트 💐", "desc": "자연의 아름다움을 다루고 섬세한 감각을 표현하는 데 적합합니다."},
            {"name": "요리사 🧑‍🍳", "desc": "오감을 통해 창의력을 발휘하고 사람들에게 즐거움을 선사할 수 있습니다."},
        ]
    },
    "INFP": {
        "description": "💖 **열정적인 중재자!** INFP는 이상주의적이고 상상력이 풍부하며, 따뜻한 마음으로 세상을 더 좋게 만들고자 하는 성격입니다. 자신의 가치를 중요하게 여기고, 타인의 감정에 깊이 공감합니다. 당신의 아름다운 내면은 세상을 밝히는 등불입니다! ✨",
        "strengths": ["👍 이상주의적이고 창의적", "👍 타인의 감정에 깊이 공감", "👍 높은 윤리 의식", "👍 강한 탐구심"],
        "weaknesses": ["👎 비현실적일 수 있음", "👎 완벽주의 경향", "👎 갈등 회피 경향"],
        "relationships": "🤝 깊고 진실한 관계를 추구하며, 영적인 유대감을 중요시합니다. 타인의 감정에 민감하고, 그들의 잠재력을 끌어내주는 데 능숙합니다.",
        "careers": [
            {"name": "작가 ✍️", "desc": "자신의 내면세계와 이상을 글로 표현하여 사람들에게 영감을 줄 수 있습니다."},
            {"name": "심리 상담사 🛋️", "desc": "타인의 감정을 이해하고 그들의 성장을 돕는 데 탁월합니다."},
            {"name": "사회 운동가 🕊️", "desc": "자신의 이상을 실현하고 세상을 더 나은 곳으로 만드는 데 기여할 수 있습니다."},
            {"name": "음악가 🎶", "desc": "감성을 표현하고 사람들에게 위안과 영감을 주는 데 적합합니다."},
        ]
    },
    "INTP": {
        "description": "🧐 **논리적인 사색가!** INTP는 끊임없이 지식을 탐구하고 분석하며, 복잡한 문제를 논리적으로 해결하는 것을 즐깁니다. 독립적이고 창의적이며, 기존의 틀을 깨는 혁신적인 아이디어를 제시하는 데 능숙합니다. 당신의 지적 호기심은 끝이 없습니다! 💡",
        "strengths": ["👍 뛰어난 분석력과 논리력", "👍 창의적이고 혁신적", "👍 독립적이고 지적 호기심 강함", "👍 문제 해결 능력 탁월"],
        "weaknesses": ["👎 비현실적일 수 있음", "👎 대인 관계에 어려움을 느낄 수 있음", "👎 실행력이 부족할 수 있음"],
        "relationships": "🤝 감정보다는 논리를 중요시하며, 지적인 대화를 통해 유대감을 형성합니다. 개인적인 공간을 존중하며, 솔직하고 직접적인 소통을 선호합니다.",
        "careers": [
            {"name": "과학자 🔬", "desc": "미지의 영역을 탐구하고 새로운 지식을 발견하는 데 적합합니다."},
            {"name": "프로그래머 💻", "desc": "복잡한 시스템을 설계하고 논리적으로 구현하는 데 능숙합니다."},
            {"name": "수학자 ➕", "desc": "추상적인 개념을 다루고 복잡한 문제를 해결하는 데 강점을 보입니다."},
            {"name": "철학자 📚", "desc": "세상과 인간에 대한 근본적인 질문을 탐구하는 데 적합합니다."},
        ]
    },
    "ESTP": {
        "description": "💥 **활동적인 사업가!** ESTP는 에너지가 넘치고 현실적이며, 즉흥적으로 행동하고 새로운 경험을 즐기는 성격입니다. 뛰어난 순발력과 적응력을 바탕으로 위기 상황에서도 침착하게 대처합니다. 당신의 에너지와 대담함은 언제나 주변을 활기차게 만듭니다! ⚡",
        "strengths": ["👍 현실적이고 실용적", "👍 뛰어난 적응력과 순발력", "👍 대담하고 활동적", "👍 설득력이 뛰어남"],
        "weaknesses": ["👎 충동적일 수 있음", "👎 장기 계획에 약함", "👎 규칙이나 권위에 저항할 수 있음"],
        "relationships": "🤝 사람들과 어울리고 새로운 경험을 공유하는 것을 즐깁니다. 솔직하고 유쾌하며, 유머 감각으로 분위기를 밝게 만듭니다.",
        "careers": [
            {"name": "영업직 🗣️", "desc": "뛰어난 설득력과 즉흥성으로 고객을 사로잡고 목표를 달성할 수 있습니다."},
            {"name": "경찰관 👮‍♀️", "desc": "현장에서 빠르게 판단하고 행동하는 데 당신의 순발력이 필요합니다."},
            {"name": "기업가 💰", "desc": "새로운 기회를 포착하고 과감하게 도전하는 데 능숙합니다."},
            {"name": "스포츠 선수 🥇", "desc": "활동적이고 경쟁적인 환경에서 최고의 성과를 낼 수 있습니다."},
        ]
    },
    "ESFP": {
        "description": "🥳 **자유로운 연예인!** ESFP는 낙천적이고 사교적이며, 사람들과 어울리고 주목받는 것을 즐기는 성격입니다. 현재를 만끽하고 주변을 즐겁게 만드는 데 능숙합니다. 당신의 밝은 에너지와 넘치는 끼는 언제나 주변을 축제로 만듭니다! 🎊",
        "strengths": ["👍 낙천적이고 사교적", "👍 뛰어난 유머 감각", "👍 즉흥적이고 유연함", "👍 현재를 즐김"],
        "weaknesses": ["👎 장기 계획에 약함", "👎 쉽게 지루해함", "👎 비판에 민감할 수 있음"],
        "relationships": "🤝 사람들과의 만남을 즐기고, 분위기 메이커 역할을 자처합니다. 감정 표현에 솔직하고, 유쾌한 에너지를 주변에 전달합니다.",
        "careers": [
            {"name": "연예인 🎤", "desc": "무대 위에서 자신을 표현하고 사람들에게 즐거움을 선사하는 데 탁월합니다."},
            {"name": "이벤트 기획자 🎈", "desc": "사람들이 즐거워할 만한 행사를 기획하고 실행하는 데 능숙합니다."},
            {"name": "가이드 🗺️", "desc": "새로운 장소를 탐험하고 사람들에게 즐거움을 선사하는 데 적합합니다."},
            {"name": "헤어 디자이너 💇‍♀️", "desc": "사람들과 소통하며 아름다움을 만들어내는 데 재능을 발휘할 수 있습니다."},
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
    "ENTP": {
        "description": "🗣️ **뜨거운 논쟁을 즐기는 변론가!** ENTP는 영리하고 논리적이며, 새로운 아이디어를 끊임없이 탐색하고 도전하는 것을 즐깁니다. 재치 있는 입담과 뛰어난 설득력을 바탕으로 사람들과 활발하게 교류합니다. 당신의 혁신적인 사고는 세상을 변화시킬 잠재력을 가지고 있습니다! 🚀",
        "strengths": ["👍 뛰어난 논리력과 분석력", "👍 창의적이고 혁신적", "👍 설득력이 뛰어남", "👍 새로운 아이디어에 개방적"],
        "weaknesses": ["👎 논쟁을 즐김", "👎 비판적 사고가 강함", "👎 쉽게 지루해함"],
        "relationships": "🤝 지적인 자극과 토론을 즐기며, 솔직하고 거침없는 대화를 선호합니다. 틀에 박힌 관계보다는 자유롭고 유쾌한 관계를 추구합니다.",
        "careers": [
            {"name": "변호사 ⚖️", "desc": "뛰어난 논리력과 설득력으로 자신의 주장을 펼치고 승소를 이끌어낼 수 있습니다."},
            {"name": "기업가 💡", "desc": "새로운 아이디어를 사업화하고 끊임없이 도전하는 데 적합합니다."},
            {"name": "컨설턴트 📈", "desc": "다양한 분야의 문제를 분석하고 혁신적인 해결책을 제시하는 데 능숙합니다."},
            {"name": "기자 ✍️", "desc": "새로운 정보를 탐색하고 날카로운 질문으로 진실을 파헤치는 데 적합합니다."},
        ]
    },
    "ESTJ": {
        "description": "👑 **엄격한 관리자!** ESTJ는 현실적이고 실용적이며, 뛰어난 조직력과 실행력을 바탕으로 일을 효율적으로 처리합니다. 책임감이 강하고 리더십이 뛰어나며, 규칙과 질서를 중요하게 생각합니다. 당신의 탁월한 리더십은 어떤 조직이든 안정적으로 이끌 수 있습니다! 📊",
        "strengths": ["👍 뛰어난 조직력과 실행력", "👍 책임감이 강하고 현실적", "👍 리더십이 뛰어남", "👍 공정하고 객관적"],
        "weaknesses": ["👎 융통성이 부족할 수 있음", "👎 변화에 대한 저항", "👎 감정 표현에 서툴 수 있음"],
        "relationships": "🤝 솔직하고 직접적인 소통을 선호하며, 비효율적인 관계를 싫어합니다. 신뢰를 바탕으로 한 안정적인 관계를 중요시하며, 가족과 공동체에 대한 책임감이 강합니다.",
        "careers": [
            {"name": "경영자 💼", "desc": "조직을 이끌고 비즈니스 목표를 달성하는 데 당신의 리더십이 빛을 발합니다."},
            {"name": "군인 🎖️", "desc": "명령과 규율을 중요시하고 조직적인 활동에 적합합니다."},
            {"name": "판사 👨‍⚖️", "desc": "공정하고 객관적인 판단력으로 법과 질서를 유지하는 데 기여합니다."},
            {"name": "은행원 🏦", "desc": "정확성과 신뢰성을 바탕으로 재정을 관리하는 데 능숙합니다."},
        ]
    },
    "ESFJ": {
        "description": "🫂 **사교적인 외교관!** ESFJ는 따뜻하고 사교적이며, 주변 사람들을 돌보고 화합을 도모하는 데 능숙합니다. 책임감이 강하고 성실하며, 타인의 감정에 공감하고 지지하는 데 탁월합니다. 당신의 다정함과 배려심은 언제나 주변을 밝힙니다! 💖",
        "strengths": ["👍 따뜻하고 사교적", "👍 책임감이 강하고 성실함", "👍 타인의 감정에 공감", "👍 뛰어난 공감 능력"],
        "weaknesses": ["👎 비판에 취약함", "👎 과도한 자기 희생", "👎 거절에 어려움을 느낌"],
        "relationships": "🤝 사람들과의 관계를 최우선으로 생각하며, 갈등을 조정하고 조화를 이루는 데 능숙합니다. 타인의 필요를 먼저 살피고 도와주는 데 큰 기쁨을 느낍니다.",
        "careers": [
            {"name": "교사 🧑‍🏫", "desc": "학생들을 따뜻하게 지도하고 성장시키는 데 당신의 배려심이 발휘됩니다."},
            {"name": "간호사 👩‍⚕️", "desc": "환자들을 돌보고 정서적으로 지지하는 데 탁월한 능력을 발휘합니다."},
            {"name": "사회복지사 🤝", "desc": "어려운 사람들을 돕고 공동체의 화합을 도모하는 데 기여합니다."},
            {"name": "영업 관리자 📈", "desc": "팀원들과 소통하고 목표 달성을 위해 협력하는 데 능숙합니다."},
        ]
    },
    "ENFJ": {
        "description": "🗣️ **정의로운 사회 운동가!** ENFJ는 카리스마 넘치고 따뜻하며, 사람들에게 영감을 주고 긍정적인 변화를 이끌어내는 데 능숙합니다. 높은 공감 능력과 뛰어난 소통 능력을 바탕으로 타인의 잠재력을 끌어냅니다. 당신의 리더십은 세상을 더 나은 곳으로 만듭니다! 🌍",
        "strengths": ["👍 뛰어난 리더십과 설득력", "👍 높은 공감 능력", "👍 타인의 잠재력을 발휘시킴", "👍 강한 책임감"],
        "weaknesses": ["👎 과도한 자기 희생", "👎 비판에 민감할 수 있음", "👎 완벽주의 경향"],
        "relationships": "🤝 사람들과의 깊은 유대감을 중요시하며, 그들의 성장과 행복을 위해 헌신합니다. 탁월한 소통 능력으로 사람들의 마음을 움직이고 변화를 이끌어냅니다.",
        "careers": [
            {"name": "정치인 🏛️", "desc": "사람들에게 영감을 주고 사회의 긍정적인 변화를 이끌어내는 데 기여합니다."},
            {"name": "교육자 🧑‍🎓", "desc": "학생들의 성장을 돕고 그들의 잠재력을 끌어내는 데 탁월합니다."},
            {"name": "심리 상담사 🗣️", "desc": "타인의 어려움을 공감하고 그들의 삶에 긍정적인 영향을 미칩니다."},
            {"name": "HR 전문가 🧑‍💼", "desc": "직원들의 역량을 개발하고 조직의 화합을 도모하는 데 능숙합니다."},
        ]
    },
    "ENTJ": {
        "description": "🦁 **대담한 통솔자!** ENTJ는 타고난 리더이며, 목표 지향적이고 전략적인 사고로 비전을 현실로 만듭니다. 강력한 추진력과 뛰어난 조직력을 바탕으로 어떤 어려움도 극복하고 성공을 이끌어냅니다. 당신의 결단력과 통솔력은 세상을 움직입니다! 🚀",
        "strengths": ["👍 뛰어난 리더십과 통솔력", "👍 전략적이고 논리적", "👍 강한 추진력", "👍 효율성 추구"],
        "weaknesses": ["👎 독단적일 수 있음", "👎 타인의 감정에 둔감할 수 있음", "👎 완벽주의 경향"],
        "relationships": "🤝 효율적이고 목표 지향적인 관계를 선호하며, 비효율적인 감정 소모를 싫어합니다. 한번 목표를 정하면 강력하게 추진하며, 상대방의 능력과 잠재력을 중요시합니다.",
        "careers": [
            {"name": "기업 CEO 📊", "desc": "조직을 이끌고 비즈니스 목표를 달성하는 데 당신의 리더십이 빛을 발합니다."},
            {"name": "변호사 ⚖️", "desc": "논리적인 사고와 설득력으로 소송에서 승리하고 정의를 실현할 수 있습니다."},
            {"name": "사업가 💰", "desc": "새로운 사업을 기획하고 강력한 추진력으로 성공을 이끌어낼 수 있습니다."},
            {"name": "경영 컨설턴트 📈", "desc": "기업의 문제를 분석하고 전략적인 해결책을 제시하는 데 능숙합니다."},
        ]
    }
}


# --- 2. Streamlit 앱 설정 및 CSS 스타일링 ---
st.set_page_config(
    page_title="✨ MBTI 진로 탐험대 ✨",
    page_icon="🚀",
    layout="wide", # 화면을 넓게 사용하도록 설정
    initial_sidebar_state="expanded"
)

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
    /* 중앙 정렬을 위한 flexbox */
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

# --- 3. 앱 본문 내용 ---
st.markdown("<h1>✨ MBTI 진로 탐험대 🚀</h1>", unsafe_allow_html=True)

# 환영 메시지와 이미지, 선택 박스를 중앙 정렬하기 위해 컨테이너 사용
with st.container():
    st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.3em; color: #6A5ACD; margin-bottom: 20px;'>👋 반가워요! 당신의 잠재력을 찾아줄 MBTI 진로 탐험 🗺️에 오신 것을 환영합니다! 🎉</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 2em;'>🎇</p>", unsafe_allow_html=True) # 폭죽 이모지 간격 추가

    # 이미지 경로 설정 및 로딩 시도 (로컬 이미지 우선, 없으면 경고)
    local_image_path = "images/main_image.png" # 사용자에게 받은 파일 이름과 확장자 고려 (image_68c1a5.png)
    
    # Check if the images directory exists, if not, create it
    if not os.path.exists("images"):
        os.makedirs("images")

    # If you have directly uploaded image_68c1a5.png and want to use it
    # You need to manually save the base64 image from the context or instruct the user to place it.
    # For now, let's assume 'main_image.png' is placed by the user.

    image_loaded = False
    if os.path.exists(local_image_path):
        try:
            st.image(local_image_path,
                     caption="💡 당신의 잠재력을 찾아보세요!",
                     use_container_width=True)
            image_loaded = True
        except Exception as e:
            st.warning(f"로컬 이미지 ({local_image_path}) 로딩 중 오류 발생: {e}. 경로를 확인해주세요! 🚨")
    
    if not image_loaded:
        st.warning(f"로컬 이미지 ({local_image_path})를 찾을 수 없습니다. 'images' 폴더에 'main_image.png' 파일을 넣어주세요! 🚨")
        # 대체 이미지 (CDN)
        st.image("https://images.unsplash.com/photo-1543269865-cbf427352390?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                 caption="💡 당신의 잠재력을 찾아보세요! (대체 이미지)",
                 use_container_width=True)


    st.markdown("<p style='text-align: center; font-size: 1.3em; margin-top: 30px;'><h2>🔍 당신의 MBTI를 선택해주세요! 🤔</h2></p>", unsafe_allow_html=True)
    
    # 선택 박스 중앙 정렬을 위해 컬럼 사용
    col1, col2, col3 = st.columns([1, 2, 1]) # 가운데 컬럼을 넓게 설정
    with col2: # 가운데 컬럼에 selectbox 배치
        mbti_options = ["MBTI 선택"] + sorted(list(mbti_data.keys()))
        selected_mbti = st.selectbox("", mbti_options, help="당신의 MBTI 유형을 골라보세요!")

    st.markdown("</div>", unsafe_allow_html=True) # centered-content 닫기

st.markdown("---") # 구분선 추가

# MBTI 선택 결과에 따른 내용 표시
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
        
        # 이모지가 이름 뒤에 붙어있을 경우를 고려하여 처리
        if len(job_parts) > 1:
            last_part = job_parts[-1]
            # 이모지인지 판단 (알파벳, 숫자가 아니고 길이가 짧은 문자열)
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


# --- 4. 사이드바 ---
with st.sidebar:
    st.header("📖 MBTI란?")
    st.write("MBTI(Myers-Briggs Type Indicator)는 개인의 선호도를 바탕으로 성격을 16가지 유형으로 분류하는 성격 유형 검사입니다.")
    st.write("MBTI를 통해 자신을 이해하고 타인과의 관계를 개선하며, 적절한 진로를 탐색하는 데 도움을 받을 수 있습니다.")
    st.markdown("---")
    st.write("© 2025 MBTI 진로 탐험대")
    st.write("Made with ❤️ by AI")
    # 무료 테스트 링크 추가
    st.markdown("[MBTI 무료 테스트 하러 가기](https://www.16personalities.com/ko/무료-성격-유형-검사)")
