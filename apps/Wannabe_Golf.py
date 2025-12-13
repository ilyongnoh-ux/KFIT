import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils import send_data_to_api, render_common_form 
from models import GolfData

def app(input_col):
    # --------------------------------------------------------------------------
    # [UI 함수] 통일된 스타일 적용 및 함수 단순화
    # --------------------------------------------------------------------------
    st.markdown("""
        <style>
        /* 메인 타이틀 색상을 Primary Color로 통일 (다크모드 대응) */
        .responsive-title { 
            font-size: clamp(1.8rem, 6vw, 4rem); 
            font-weight: 900; 
            color: var(--primary-color); /* 브랜드 색상 통일 */
            white-space: nowrap; 
            text-align: center; 
            line-height: 1.2;
            margin-bottom: 20px; 
        }
        /* 좌측 프레임 제목 스타일 (Life Plan과 통일) */
        .sidebar-title { 
            font-size: clamp(1.2rem, 13cqw, 2.5rem); 
            font-weight: 900; 
            color: var(--primary-color); 
            text-align: center; 
        } 
        /* 입력 항목 캡션 및 라벨 폰트 크기 통일 */
        .stSlider label p, .stNumberInput label p, .stSelectbox label p {
            font-size: clamp(0.9rem, 1.2vw, 1.1rem) !important;
            font-weight: 500;
        }
        /* 결과 텍스트 */
        .result_unified { 
            font-size: clamp(20px, 6vw, 40px); 
            font-weight: 900; 
            line-height: 1.3; 
            letter-spacing: -1px; 
            text-align: center; 
        }
        /* 서브헤더 (자산 현황) 중앙 정렬 스타일 */
        .subheader_golf {
            font-size: clamp(1.2rem, 4vw, 1.5rem);
            font-weight: 700;
            text-align: center; 
            margin-top: 40px; 
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 함수를 CSS 기반으로 단순화
    def display_title(text, type="title"):
        if type == "title":
            st.markdown(f'<div class="responsive-title">{text}</div>', unsafe_allow_html=True)
        elif type == "result":
            st.markdown(f'<div class="result_unified">{text}</div>', unsafe_allow_html=True)
        elif type == "subheader":
             st.markdown(f'<div class="subheader_golf">{text}</div>', unsafe_allow_html=True) 
        else:
            st.markdown(f'<div>{text}</div>', unsafe_allow_html=True)
            
    # [UX] 결과 해설 박스 (원본 유지)
    def emphasized_box(msg, status="SAFE"):
        if status == "DANGER": bg_color = "#FF4B4B"; icon = "🚨"
        elif status == "WARNING": bg_color = "#FFA421"; icon = "⚠️"
        else: bg_color = "#3DD56D"; icon = "🎉"
            
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 25px; border-radius: 15px; margin-top: 20px; margin-bottom: 30px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            <div style="font-size: clamp(22px, 7vw, 40px); font-weight: 800; color: white; line-height: 1.3; word-break: keep-all;">
                {icon} {msg}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # [로직] 핵심 계산 엔진 (원본 그대로 유지)
    # --------------------------------------------------------------------------
    def calculate_golf_life(current_age, retire_age, target_age, assets, saving, rounds, cost_per_round):
        inflation_rate = 0.03
        roi_rate = 0.04
        balance = assets
        bankruptcy_age = target_age + 1
        status = "SAFE"
        history = []
        
        for age in range(current_age, target_age + 5):
            annual_income = (saving * 12) if age < retire_age else 0
            years_passed = age - current_age
            current_annual_cost = rounds * cost_per_round * 12
            inflated_cost = current_annual_cost * ((1 + inflation_rate) ** years_passed)
            
            balance = balance * (1 + roi_rate) + annual_income - inflated_cost
            history.append({"age": age, "balance": int(balance)})
            
            if balance < 0 and status == "SAFE":
                bankruptcy_age = age
                status = "DANGER"
        
        return bankruptcy_age, status, pd.DataFrame(history)

    # --------------------------------------------------------------------------
    # [UI] 입력창 배치 (왼쪽 프레임 input_col 로 이동)
    # --------------------------------------------------------------------------
    with input_col:
        # Client Info 타이틀
        st.markdown("""
            <div class="sidebar-container">
                <h3 class="sidebar-title">🏌️‍♂️ Client Info</h3>
            </div>
        """, unsafe_allow_html=True)
    
        current_age = st.number_input("현재 나이", value=54, min_value=30, max_value=80)
        retire_age = st.slider("은퇴 예정 나이", 50, 75, 60)
        rounds = st.slider("월 라운딩 횟수 (회)", 0, 10, 4)
        cost = st.select_slider(
            "회당 비용 (그늘집 포함)",
            options=[20, 30, 35, 40, 50, 70],
            value=35,
        ) * 10000
        
        st.divider()
        
        display_title("💰 자산 현황", type="subheader") # CSS 기반 서브헤더 (중앙 정렬됨)
        
        # [수정 완료] 억 단위로 변경
        assets_eok = st.slider("현재 골프 자금 (억)", 0.0, 5.0, 1.0, step=0.1, format="%.1f") 
        assets = assets_eok * 100000000 # 원 단위로 환산하여 계산에 사용
        saving = st.slider("월 추가 저축액 (만원)", 0, 500, 0, step=10) * 10000

    # --------------------------------------------------------------------------
    # [UI] 메인 결과 화면 (오른쪽 프레임)
    # --------------------------------------------------------------------------
    display_title("⛳ Golf Life Checkup", type="title") # CSS 기반 타이틀
    st.markdown("<div style='text-align: center; opacity: 0.7; font-size: 1.0em; margin-bottom: 25px;'>👇 좌측 메뉴의 값을 조정하여 미래를 확인하세요</div>", unsafe_allow_html=True)
    st.divider()

    # 계산 실행
    target_age = 85
    bankruptcy_age, status, df_history = calculate_golf_life(current_age, retire_age, target_age, assets, saving, rounds, cost)

    # 결과 표시
    display_title("📊 진단 결과", type="result") # CSS 기반 결과
    display_title(f"예상 골프 수명: {bankruptcy_age}세", type="result") # CSS 기반 결과

    total_years = target_age - current_age
    survive_years = bankruptcy_age - current_age
    battery_percent = min(100, max(0, int((survive_years / total_years) * 100)))

    st.progress(battery_percent / 100)

    if battery_percent >= 100:
        msg = f"완벽합니다!<br>{target_age}세까지 거뜬합니다!"
        status_code = "SAFE"
        result_msg = "자산 충분 (건강 리스크 대비 필요)"
    elif battery_percent >= 70:
        msg = f"아슬아슬합니다.<br>{bankruptcy_age}세에 바닥납니다."
        status_code = "WARNING"
        shortfall = df_history[df_history['age'] == target_age]['balance'].values[0]
        result_msg = f"85세까지 {abs(shortfall):,.0f}원 부족"
    else:
        msg = f"위험합니다!<br>{bankruptcy_age}세부터 파산입니다."
        status_code = "DANGER"
        shortfall = df_history[df_history['age'] == target_age]['balance'].values[0]
        result_msg = f"85세까지 {abs(shortfall):,.0f}원 부족"

    emphasized_box(msg, status=status_code)

    if status_code != "SAFE":
        st.markdown(f"<div style='text-align: center; font-size: 1.2em; font-weight: bold; color: gray;'>📉 85세까지 약 {abs(shortfall // 10000):,.0f}만 원이 더 필요합니다.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: center; font-size: 1.2em; font-weight: bold; color: gray;'>📈 자금은 충분합니다. 이제 건강을 지키세요.</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 공통 상담 폼 호출
    # --------------------------------------------------------------------------
    render_common_form(
        app_type="golf",
        DataModelClass=GolfData,
        # 아래는 GolfData에 필요한 나머지 변수들을 전달
        current_age=current_age,
        retire_age=retire_age,
        assets=assets,
        saving=saving,
        rounds=rounds,
        cost=cost,
        bankruptcy_age=bankruptcy_age,
        result_msg=result_msg
    )