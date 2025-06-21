import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. Streamlit 앱 기본 설정 ---
st.set_page_config(
    page_title="📈 글로벌 시가총액 TOP10 주식 변화",
    page_icon="💰",
    layout="wide" # 화면을 넓게 사용하도록 설정
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

    body {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #f0f2f6;
        color: #333;
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
        padding-top: 30px;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 30px;
    }
    h2 {
        color: #34495e;
        font-size: 1.8em;
        margin-top: 40px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e74c3c;
        padding-bottom: 10px;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }
    .stAlert {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. 글로벌 시가총액 TOP 10 기업 (대표적인 기업 리스트) ---
# 주의: 이 목록은 실시간 시가총액 TOP 10과 다를 수 있습니다.
# Yahoo Finance 티커를 사용합니다.
GLOBAL_TOP_COMPANIES = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL", # 또는 GOOG (클래스 A/C 차이)
    "Amazon": "AMZN",
    "Meta Platforms": "META",
    "Berkshire Hathaway": "BRK-B", # 클래스 B 주식
    "Eli Lilly": "LLY",
    "Taiwan Semiconductor (TSMC)": "TSM",
    "Broadcom": "AVGO"
}

# --- 3. 데이터 로딩 및 처리 함수 ---
@st.cache_data(ttl=3600) # 1시간 캐싱
def load_stock_data(tickers, period="1y"):
    """
    주어진 티커 목록에 대해 YFinance에서 주식 데이터를 다운로드하고
    첫 날 가격을 기준으로 정규화합니다.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # 최근 1년

    data = {}
    for company_name, ticker in tickers.items():
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if not df.empty:
                # 첫 날의 종가(Close)를 기준으로 정규화
                first_close_price = df['Close'].iloc[0]
                df[f'{company_name} Normalized'] = (df['Close'] / first_close_price) * 100
                data[company_name] = df
            else:
                st.warning(f"데이터를 찾을 수 없습니다: {company_name} ({ticker})")
        except Exception as e:
            st.error(f"데이터 로딩 중 오류 발생: {company_name} ({ticker}) - {e}")
    return data

# --- 4. Streamlit 앱 본문 ---
st.title("📈 글로벌 시가총액 TOP10 주식 변화 분석")

st.write(
    """
    이 앱은 **글로벌 시가총액 상위 (추정) 10개 기업**의 최근 1년간 주식 가격 변화를 시각화합니다.
    모든 주가는 시작일 가격을 100으로 정규화하여 상대적인 상승/하락률을 한눈에 비교할 수 있습니다.
    """
)
st.info("⚠️ 데이터는 Yahoo Finance에서 제공되며, 실시간 시가총액 TOP10 리스트와 다를 수 있습니다.")

# 데이터 로드 버튼
if st.button("📊 주식 데이터 로드 및 시각화"):
    with st.spinner("데이터를 로드하고 그래프를 생성 중입니다..."):
        stock_data = load_stock_data(GLOBAL_TOP_COMPANIES)

        if stock_data:
            st.subheader("🚀 최근 1년간 주식 가격 변화 (정규화)")

            fig = go.Figure()

            for company_name, df in stock_data.items():
                # 정규화된 데이터만 플롯
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[f'{company_name} Normalized'],
                    mode='lines',
                    name=company_name,
                    hovertemplate=f'<b>{{company_name}}</b><br>날짜: %{{x|%Y-%m-%d}}<br>정규화된 가격: %{{y:.2f}}<extra></extra>'.replace('{company_name}', company_name)
                ))

            fig.update_layout(
                title='최근 1년간 글로벌 Top 기업 주식 변화 (시작점 100으로 정규화)',
                xaxis_title='날짜',
                yaxis_title='정규화된 가격 (시작점=100)',
                hovermode='x unified', # 마우스를 올렸을 때 한 날짜의 모든 데이터를 보여줌
                height=600,
                legend_title_text='기업',
                template="plotly_white" # 깔끔한 배경
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.subheader("📋 데이터 요약")
            st.write("각 기업의 마지막 거래일 기준 정규화된 가격입니다.")

            # 마지막 날짜 기준 정규화된 가격 테이블
            summary_data = {}
            for company_name, df in stock_data.items():
                if not df.empty:
                    last_normalized_price = df[f'{company_name} Normalized'].iloc[-1]
                    summary_data[company_name] = f"{last_normalized_price:.2f}"
            st.json(summary_data) # JSON 형태로 간단하게 보여줌

        else:
            st.error("📉 데이터를 로드할 수 없습니다. 인터넷 연결을 확인하거나 잠시 후 다시 시도해주세요.")

st.markdown("---")
st.write("© 2025 주식 변화 분석기")
st.write("Made with ❤️ by AI")
