import streamlit as st
from utils import show_footer, hide_header

st.set_page_config(page_title="Company - Kfit", page_icon="🏢", layout="wide")

hide_header()

# 사이드바 강제 숨김
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 전역 스타일 (네비게이션, 배경, 카드, 미션 영역)
st.markdown(
    """
    <style>
    /* 네비게이션 스타일 */
    [data-testid="stPageLink-NavLink"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px 10px !important;
        margin: 0 !important;
    }
    [data-testid="stPageLink-NavLink"] p {
        color: #555555 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        padding: 5px 10px !important;
    }
    [data-testid="stPageLink-NavLink"]:hover p {
        color: #1E3A8A !important;
        font-weight: 900 !important;
        transform: scale(1.05);
        transition: all 0.2s ease-in-out;
    }

    /* 전체 배경 이미지 (pages/bg.jpg 파일 사용) */
    .stApp {
        background-image: url("pages/bg.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* CEO 섹션 카드 스타일 */
    .ceo-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 55%, #eff6ff 100%);
        border-radius: 24px;
        padding: 2.5rem 3rem;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
        margin-top: 1.5rem;
        margin-bottom: 2.5rem;
    }
    .ceo-name {
        font-weight: 700;
        font-size: 1rem;
        margin-top: 0.75rem;
        color: #111827;
        text-align: center;
    }
    .ceo-title {
        font-size: 0.85rem;
        color: #6B7280;
        text-align: center;
    }

    /* Mission 영역 스타일 */
    .mission-wrap {
        text-align: center;
        margin: 3rem 0 2.5rem 0;
    }
    .mission-label {
        font-size: 0.9rem;
        letter-spacing: 0.25em;
        color: #6B7280;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .mission-text {
        font-size: 2rem;
        font-weight: 800;
        color: #111827;
    }
    .mission-sub {
        font-size: 0.95rem;
        color: #6B7280;
        margin-top: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 상단 네비게이션
col_nav1, col_nav2, col_empty = st.columns([0.2, 0.2, 0.6])
with col_nav1:
    st.page_link("Home.py", label="Home", use_container_width=True)
with col_nav2:
    st.page_link("pages/Service.py", label="Service", use_container_width=True)

st.divider()

# 페이지 타이틀
st.markdown(
    '<div style="text-align: center; font-size: 2rem; font-weight: 700; '
    'color: #1E3A8A; margin-bottom: 0.5rem;">Company Introduction</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# =======================
# CEO 섹션 (카드 + 사진/텍스트)
# =======================
#st.markdown('<div class="ceo-card">', unsafe_allow_html=True)

c1, c2 = st.columns([1, 2])

with c1:
    # 내부 3컬럼으로 가운데 정렬
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(
            "pages/ceo.jpg",  # 대표 사진 파일 경로
            caption=None,
            width=220,
        )
        st.markdown('<div class="ceo-name">노일용 대표</div>', unsafe_allow_html=True)
        st.markdown('<div class="ceo-title">한국금융투자기술</div>', unsafe_allow_html=True)

with c2:
    st.markdown("### CEO Message")
    st.markdown(
        """
> **"금융은 어렵지 않아야 합니다. 기술은 사람을 향해야 합니다."**

안녕하세요, **한국금융투자기술 대표 노일용**입니다.  

한국금융투자기술은 보험·연금·투자·세무를 하나로 묶어 보는  
**통합 재무 설계 파트너**입니다.

기아자동차 총무, IT 프로그래머,  
그리고 20년이 넘는 보험·재무 설계 경험을 바탕으로  
숫자와 계약서를 **고객의 언어로** 해석합니다.

**우리가 집중하는 일은 세 가지입니다.**

- **은퇴·연금 전략** : 국민연금·퇴직연금·개인연금의 구조를 한 번에 설계  
- **위험 관리 & 보험 리모델링** : 과보장은 줄이고 꼭 필요한 보장은 채우는 구조 재정비  
- **기업·대표 재무 컨설팅** : 소득·세금·건보료·법인 자금을 함께 보는 입체 설계  

한 번의 계약으로 끝나는 관계가 아니라,  
오래 맡길 수 있는 ‘나만의 금융 담당자’를 지향합니다.
        """,
        unsafe_allow_html=False,
    )

st.markdown("</div>", unsafe_allow_html=True)  # ceo-card 닫기

# =======================
# Mission 영역 (하단 중앙 크게)
# =======================
st.markdown(
    """
    <div class="mission-wrap">
        <div class="mission-label">MISSION</div>
        <div class="mission-text">
            Bridge the Gap between possibility and reality
        </div>
        <div class="mission-sub">
            가능성과 현실의 간극을 메우는, 당신의 평생 금융 파트너
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

show_footer()
