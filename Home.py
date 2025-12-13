import streamlit as st
from utils import set_bg_hack, show_footer, hide_header

st.set_page_config(
    page_title="한국금융투자기술",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

hide_header()
set_bg_hack("background.jpg")

# 사이드바 강제 숨김
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 네비게이션 스타일
st.markdown(
    """
    <style>
    [data-testid="stPageLink-NavLink"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px 10px !important;
        margin: 0 !important;
        text-decoration: none !important;
    }
    [data-testid="stPageLink-NavLink"] p {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 5px 10px !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.9), 0px 0px 10px rgba(0,0,0,0.7);
    }
    [data-testid="stPageLink-NavLink"]:hover p {
        color: #FFD700 !important;
        font-weight: 900 !important;
        transform: scale(1.05);
        text-shadow: 0px 0px 15px rgba(255, 215, 0, 0.8), 0px 2px 5px rgba(0,0,0,1);
        transition: all 0.2s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 상단 네비게이션
col_nav1, col_nav2, col_empty = st.columns([0.2, 0.2, 0.6])
with col_nav1:
    st.page_link("pages/Company.py", label="Company", use_container_width=True)
with col_nav2:
    st.page_link("pages/Service.py", label="Service", use_container_width=True)

# 메인 타이틀 영역
# [수정 핵심] HTML 태그 앞의 들여쓰기(공백)를 모두 제거하여 왼쪽으로 붙였습니다.
st.markdown(
    """
<div style="text-align: center; margin-top: 150px; margin-bottom: 30px;">
<h1 style="color: #FFFFFF; font-size: 4.5rem; font-family: 'Arial Black', sans-serif; text-shadow: 0px 4px 3px rgba(0,0,0,0.4), 0px 8px 13px rgba(0,0,0,0.1), 0px 18px 23px rgba(0,0,0,0.1), 0px 0px 30px rgba(0,0,0,0.9); font-weight: 900; margin-bottom: 15px; letter-spacing: -2px;">Bridge the Gap</h1>
<div style="background: linear-gradient(to right, transparent, rgba(0,0,0,0.3), transparent); padding: 20px 0;">
<h3 style="color: #FFFFFF; font-size: 1.7rem; text-shadow: 0px 2px 4px rgba(0,0,0,0.9), 0px 0px 20px rgba(0,0,0,0.8); font-weight: 700; margin-top: 0; margin-bottom: 10px; letter-spacing: -1px;">가능성과 현실의 간극을 메우는,</h3>
<h3 style="color: #FFFFFF; font-size: 2.2rem; text-shadow: 0px 2px 4px rgba(0,0,0,0.9), 0px 0px 20px rgba(0,0,0,0.8); font-weight: 800; margin-top: 0;">당신의 평생 금융파트너, 한국금융투자기술(KFIT)®</h3>
</div>
</div>
    """,
    unsafe_allow_html=True,
)

# 페이지 하단 여유 공간
st.markdown(
    "<div style='height: 40vh;'></div>",
    unsafe_allow_html=True,
)

# 항상 맨 마지막에 호출

show_footer()


