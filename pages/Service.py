import streamlit as st
from utils import show_footer, hide_header
from apps import Wannabe_Golf, Wannabe_Tax, Wannabe_Life_Plan

st.set_page_config(page_title="Services - Kfit", page_icon="🚀", layout="wide")

hide_header()

# [CSS] 사이드바 숨김 & 스타일링
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }

    [data-testid="stPageLink-NavLink"] { 
        border: none !important; 
        background: transparent !important; 
        padding: 0px !important; 
    }

    /* 기본 상태 */
    [data-testid="stPageLink-NavLink"] p { 
        font-size: 1.2rem;            /* 고정 크기 */
        font-weight: 600; 
        color: #444; 
        padding: 4px 6px;             
        margin: 0; 
        transition: all 0.15s ease-in-out; 
    }

    /* [수정 완료] 호버 상태: 폰트 크기 변경(1.3rem) 제거하여 울렁거림 방지 */
    [data-testid="stPageLink-NavLink"]:hover p { 
        color: #FFFFFF !important; /* 다크모드 대비 흰색 유지 */
        font-weight: 900 !important; /* 굵기만 증가 */
        font-size: 1.2rem;            /* 기본 크기(1.2rem) 유지 */
    }

    .block-container { padding-top: 1rem !important; }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# URL 꼬리표(Query Params) 감지 로직 (유지)
# ==============================================================================
query_params = st.query_params
target_tool = query_params.get("tool", "life")  # 기본값 'life'

tool_options = ["Wannabe Life Plan", "Wannabe Tax", "Wannabe Golf"]
tool_map = {
    "life": 0,  
    "tax": 1,   
    "golf": 2   
}

default_idx = tool_map.get(str(target_tool).lower(), 0)

# ==============================================================================
# 화면 분할 및 실행
# ==============================================================================
left_col, right_col = st.columns([3, 7], gap="medium")

with left_col:
    st.write("") 
    c1, c2 = st.columns(2)
    with c1: st.page_link("Home.py", label="Home", use_container_width=True)
    with c2: st.page_link("pages/Company.py", label="Company", use_container_width=True)
    
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin: 0 0 10px 0; font-size: 1.2rem;'>Solution Menu</h3>", unsafe_allow_html=True)
    
    selected_app = st.selectbox(
        "솔루션 선택", 
        tool_options, 
        index=default_idx,  
        label_visibility="collapsed"
    )
    st.markdown("---")

with right_col:
    if selected_app == "Wannabe Golf":
        Wannabe_Golf.app(left_col)
    elif selected_app == "Wannabe Tax":
        Wannabe_Tax.app(left_col)
    elif selected_app == "Wannabe Life Plan":
        Wannabe_Life_Plan.app(left_col)

show_footer()
