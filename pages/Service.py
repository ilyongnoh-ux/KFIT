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
        font-size: 1.2rem;            
        font-weight: 600; 
        color: var(--text-color); /* 다크/라이트 모드 자동 대응 */
        padding: 4px 6px;             
        margin: 0; 
        transition: all 0.15s ease-in-out; 
    }

    /* 호버 상태: 크기 변화 제거하여 울렁거림 방지, Primary Color로 통일 */
    [data-testid="stPageLink-NavLink"]:hover p { 
        color: var(--primary-color) !important; /* 초록색 계열로 변경하여 대비 및 강조 */
        font-weight: 900 !important; 
        font-size: 1.2rem;            
    }

    .block-container { padding-top: 1rem !important; }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# URL 꼬리표(Query Params) 감지 로직 - [수정됨] 순서 변경 반영
# ==============================================================================
# 1. URL에서 '?tool=xxx' 값을 가져옵니다.
query_params = st.query_params
target_tool = query_params.get("tool", "life")  # [요청 반영] 기본값 'life' 유지

# 2. 꼬리표와 셀렉트박스 순서 매핑
# [수정] 요청하신 대로 Life Plan이 Index 0이 되도록 순서를 변경
tool_options = ["Wannabe Life Plan", "Wannabe Tax", "Wannabe Golf"]
tool_map = {
    "life": 0,  # [수정] Life Plan이 Index 0
    "tax": 1,   # [수정] Tax가 Index 1
    "golf": 2   # [수정] Golf가 Index 2
}

# 3. 선택해야 할 인덱스 찾기 (오타나 엉뚱한 값이면 0번 Life Plan)
default_idx = tool_map.get(str(target_tool).lower(), 0) # [수정] 기본 인덱스를 0 (Life Plan)로 변경

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
    
    # [수정] index 파라미터에 위에서 계산한 default_idx를 넣어줍니다.
    selected_app = st.selectbox(
        "솔루션 선택", 
        tool_options, 
        index=default_idx, 
        label_visibility="collapsed"
    )
    st.markdown("---")

with right_col:
    # 선택된 앱 실행 (왼쪽 컬럼 넘겨주기)
    if selected_app == "Wannabe Golf":
        Wannabe_Golf.app(left_col)
    elif selected_app == "Wannabe Tax":
        Wannabe_Tax.app(left_col)
    elif selected_app == "Wannabe Life Plan":
        Wannabe_Life_Plan.app(left_col)

show_footer()