import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import send_data_to_api, render_common_form
import json
from models import LifeData

def app(input_col):
    # ==============================================================================
    # 0. 설정 및 CSS
    # ==============================================================================
    st.markdown("""
        <style>
        .responsive-title { font-size: clamp(1.5rem, 5vw, 2.5rem); white-space: nowrap; text-align: left; margin-bottom: 20px; }
        .metric-container { display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 16px 20px; border-radius: 16px; background: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border: 1px solid #e0e0e0; height: 140px; }
        .metric-label { font-size: 1.2rem; color: #333333; font-weight: 800; margin-bottom: 10px; letter-spacing: -0.5px; white-space: nowrap; }
        .metric-value { font-size: 1.4rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
        .metric-subtext { font-size: 0.9rem; color: #6b7280; }
        .score-circle { width: 120px; height: 120px; border-radius: 60px; background: radial-gradient(circle at 30% 30%, #fef3c7, #fbbf24); display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); margin: 0 auto; }
        .score-text { font-size: 2.2rem; font-weight: 800; color: #92400e; }
        .score-label { text-align: center; margin-top: 8px; font-size: 1rem; font-weight: 600; color: #4b5563; }
        .grade-pill { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px; background: #eff6ff; color: #1d4ed8; font-weight: 600; font-size: 0.9rem; }
        .grade-dot { width: 8px; height: 8px; border-radius: 4px; background: #1d4ed8; }
        .highlight-box { border-radius: 12px; padding: 16px 18px; background: #fef3c7; border: 1px solid #fbbf24; font-size: 0.95rem; color: #78350f; margin-top: 10px; }
        .section-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; color: #111827; }
        .sub-tag { display: inline-block; padding: 2px 8px; border-radius: 999px; background: #e5e7eb; color: #374151; font-size: 0.8rem; margin-right: 4px; }
        .small-label { font-size: 0.85rem; color: #6b7280; margin-top: 4px; }
        .chart-card { background: #ffffff; padding: 16px 18px; border-radius: 16px; border: 1px solid #e5e7eb; box-shadow: 0 4px 10px rgba(0,0,0,0.04); margin-top: 10px; }
        .chart-title { font-size: 1rem; font-weight: 700; margin-bottom: 4px; color: #111827; }
        .chart-sub { font-size: 0.85rem; color: #6b7280; margin-bottom: 10px; }
        .remark-box { background: #f9fafb; border-radius: 12px; padding: 12px 14px; font-size: 0.9rem; color: #374151; border: 1px dashed #d1d5db; margin-top: 10px; }
        .warn-text { color: #b91c1c; font-weight: 600; }
        .good-text { color: #065f46; font-weight: 600; }
        .neutral-text { color: #4b5563; }
        </style>
    """, unsafe_allow_html=True)

    # 세션 상태 초기화
    if "properties" not in st.session_state:
        st.session_state.properties = []

    # ==============================================================================
    # 1. [왼쪽 프레임] 입력 영역
    # ==============================================================================
    with input_col:
        st.markdown('<div class="responsive-title">🏝️ Wannabe Life Plan – 은퇴 시뮬레이션</div>', unsafe_allow_html=True)
        st.caption("은퇴 이후 30년을 가정하고, 자산이 어떻게 버티는지 시뮬레이션합니다.")

        # 1-1. 기본 정보
        st.markdown("### 1. 기본 정보")
        c1, c2, c3 = st.columns(3)
        age_curr = c1.number_input("현재 나이", 20, 80, 50)
        age_retire = c2.number_input("은퇴 목표 나이", 40, 80, 60)
        age_death = c3.number_input("기대 수명", 70, 100, 90)

        # 1-2. 금융 자산
        st.markdown("### 2. 금융 자산")
        c1, c2 = st.columns(2)
        liquid_asset = c1.number_input("💰 유동자산(억)", 0.0, 100.0, 3.0, step=0.1)
        monthly_save = c2.number_input("📥 월 저축(만원)", 0, 5000, 100)
        return_rate_int = st.slider("📈 투자 수익률(연간, %)", 0, 15, 4)
        return_rate = return_rate_int / 100.0

        # 1-3. 부동산 자산
        st.markdown("### 3. 부동산 자산")
        with st.expander("보유 부동산 입력", expanded=True):
            c1, c2 = st.columns(2)
            p_name = c1.text_input("자산명 (예: 서초 아파트)", "")
            p_curr = c2.number_input("현재 시가(억)", 0.0, 100.0, 10.0, step=0.1)
            c3, c4 = st.columns(2)
            p_buy = c3.number_input("매입가(억)", 0.0, 100.0, 5.0, step=0.1)
            p_loan = c4.number_input("대출 잔액(억)", 0.0, 100.0, 2.0, step=0.1)
            c5, c6 = st.columns(2)
            p_strat = c5.selectbox("전략", ["보유", "은퇴 전 매각", "상속 계획"], index=0)
            p_sell = c6.number_input("매각/상속 시점 나이", age_curr, age_death, age_retire)

            if st.button("➕ 부동산 추가", use_container_width=True):
                if p_name.strip():
                    st.session_state.properties.append({
                        "name": p_name,
                        "current_val": p_curr,
                        "buy_price": p_buy,
                        "loan": p_loan,
                        "strategy": p_strat,
                        "sell_age": p_sell,
                        "is_sold": False,
                    })
                    st.success(f"'{p_name}' 자산이 추가되었습니다.")
                else:
                    st.warning("자산명을 입력해 주세요.")

            if st.session_state.properties:
                st.markdown("#### 보유 자산 목록")
                df_props = pd.DataFrame(st.session_state.properties)
                st.dataframe(df_props, use_container_width=True)

        # 1-4. 라이프스타일
        st.markdown("### 4. 은퇴 후 생활 스타일")
        monthly_spend = st.number_input("은퇴 월 생활비(만원)", 0, 5000, 300)
        c1, c2 = st.columns(2)
        golf_freq = c1.selectbox("골프 라운딩", ["안 함", "월 1회", "월 2회", "월 4회", "VIP"]); c1.caption("회당 40만원")
        travel_freq = c2.selectbox("해외 여행", ["안 함", "연 1회", "연 2회", "분기별"]); c2.caption("회당 400만원")
        inflation = st.select_slider("물가상승률", ["안정(2%)", "보통(3.5%)", "심각(5%)"], value="보통(3.5%)")

    # ==============================================================================
    # 2. 시뮬레이션 엔진 (중앙 로직)
    # ==============================================================================

    class WannabeEngine:
        def __init__(self, current_age, retire_age, death_age):
            self.current_age = current_age
            self.retire_age = retire_age
            self.death_age = death_age

        def run_simulation(self, liquid_asset, properties, monthly_save, monthly_spend, inf_val, return_rate):
            ages = []
            liquid = []
            re_equity = []
            ob_age = None

            years = self.death_age - self.current_age + 1
            current_liquid = liquid_asset * 100000000
            annual_save = monthly_save * 12 * 10000
            base_annual_spend = monthly_spend * 12 * 10000

            props = [p.copy() for p in properties]

            for i in range(years):
                age = self.current_age + i
                ages.append(age)

                current_liquid = current_liquid * (1 + return_rate)
                if age < self.retire_age:
                    current_liquid += annual_save
                else:
                    current_liquid -= base_annual_spend * ((1 + inf_val) ** i)

                current_re_net_val = 0
                for p in props:
                    if p.get("is_sold", False):
                        continue
                    years_from_now = age - self.current_age
                    gross_val = (p["current_val"] * 100000000) * ((1 + inf_val) ** years_from_now)
                    loan_amt = p.get("loan", 0) * 100000000
                    net_equity = max(0, gross_val - loan_amt)

                    if p["strategy"] == "은퇴 전 매각" and age >= p["sell_age"]:
                        current_liquid += net_equity
                        p["is_sold"] = True
                    else:
                        current_re_net_val += net_equity

                liquid.append(current_liquid)
                re_equity.append(current_re_net_val)

                if ob_age is None and current_liquid < 0:
                    ob_age = age

            return ages, liquid, re_equity, ob_age

        def normalize_results(self, ages, liquid, re_equity, ob_age):
            def to_eok(x):
                return int(round(x / 100000000, 0))

            liq_eok = [to_eok(v) for v in liquid]
            re_eok = [to_eok(v) for v in re_equity]

            return ages, liq_eok, re_eok, ob_age

        def score_retirement(self, ages, liquid, re_equity, ob_age):
            if ob_age is None:
                remain_years = self.death_age - self.retire_age
                base_score = 70 + min(30, remain_years)
            else:
                gap = ob_age - self.retire_age
                if gap >= 20:
                    base_score = 80
                elif gap >= 10:
                    base_score = 65
                else:
                    base_score = 40

            max_liq = max(liquid) if liquid else 0
            max_re = max(re_equity) if re_equity else 0
            total_max = max_liq + max_re

            leverage_penalty = 0
            if total_max > 0 and max_re / total_max > 0.8:
                leverage_penalty = 5

            score = max(0, min(100, base_score - leverage_penalty))

            if score >= 85:
                grade = "A"
            elif score >= 70:
                grade = "B"
            elif score >= 50:
                grade = "C"
            else:
                grade = "D"

            return score, grade

    # ==============================================================================
    # 3. [오른쪽 프레임] 메인 화면
    # ==============================================================================
    right_col = st.container()

    with right_col:
        st.markdown("### 🔍 은퇴 시뮬레이션 결과")

        inf_val = {"안정(2%)": 0.02, "보통(3.5%)": 0.035, "심각(5%)": 0.05}[inflation]

        golf_map = {"안 함": 0, "월 1회": 12, "월 2회": 24, "월 4회": 48, "VIP": 100}
        travel_map = {"안 함": 0, "연 1회": 1, "연 2회": 2, "분기별": 4}
        annual_hobby_cost = (golf_map[golf_freq] * 400000) + (travel_map[travel_freq] * 4000000)

        total_monthly_spend = monthly_spend + int(annual_hobby_cost / 12 / 10000)

        engine = WannabeEngine(age_curr, age_retire, age_death)
        ages, liq_raw, re_raw, ob_age = engine.run_simulation(
            liquid_asset, st.session_state.properties, monthly_save, total_monthly_spend, inf_val, return_rate
        )
        ages, liq_norm, re_norm, ob_norm = engine.normalize_results(ages, liq_raw, re_raw, ob_age)
        score, grade = engine.score_retirement(ages, liq_raw, re_raw, ob_age)

        # 상단 점수/요약
        top1, top2, top3 = st.columns([1, 1, 1])

        with top1:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-label">은퇴 준비 점수</div>
                    <div class="score-circle">
                        <span class="score-text">{score}</span>
                    </div>
                    <div class="score-label">100점 만점 기준</div>
                </div>
            """.format(score=score), unsafe_allow_html=True)

        with top2:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-label">등급 & 요약</div>
                    <div class="metric-value">
                        <span class="grade-pill">
                            <span class="grade-dot"></span>
                            은퇴 준비 {grade}등급
                        </span>
                    </div>
                    <div class="metric-subtext">
                        {summary}
                    </div>
                </div>
            """.format(
                grade=grade,
                summary=(
                    "자산 대비 은퇴생활비가 적정 수준입니다." if grade in ["A", "B"]
                    else "은퇴생활비를 줄이거나 저축/투자를 늘릴 필요가 있습니다."
                )
            ), unsafe_allow_html=True)

        with top3:
            if ob_norm is None:
                shortfall_text = "자산 고갈 위험 낮음"
                detail_text = "현재 계획대로라면 기대수명까지 자산이 유지될 가능성이 높습니다."
                color_class = "good-text"
            else:
                shortfall_text = f"{ob_norm}세에 자산 고갈 가능성"
                if ob_norm <= age_retire + 5:
                    detail_text = "은퇴 직후 자산이 빠르게 감소합니다. 은퇴 시점과 생활비 계획을 다시 점검해야 합니다."
                elif ob_norm <= age_death - 5:
                    detail_text = "은퇴 이후 중반부에서 자산 고갈 가능성이 있습니다. 생활비·투자전략·부동산 매각 시점을 조정해야 합니다."
                else:
                    detail_text = "기대수명 직전에 자산이 고갈될 수 있습니다. 약간의 추가 저축 또는 리스크 관리가 필요합니다."
                color_class = "warn-text"

            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">자산 버티는 기간</div>
                    <div class="metric-value {color_class}">{shortfall_text}</div>
                    <div class="metric-subtext">{detail_text}</div>
                </div>
            """, unsafe_allow_html=True)

        # 그래프
        st.markdown("### 📊 자산 추이 시각화")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ages, y=liq_norm, name="유동자산(억)", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=ages, y=re_norm, name="부동산 순자산(억)", mode="lines+markers"))

        if ob_norm is not None:
            fig.add_vline(x=ob_norm, line_dash="dash", line_color="red",
                          annotation_text=f"자산 고갈 가능 {ob_norm}세", annotation_position="top right")

        fig.update_layout(
            xaxis_title="나이",
            yaxis_title="자산(억원)",
            template="plotly_white",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

        # 리스크 분석 / 코멘트
        st.markdown("### 🧭 리스크 분석 및 코멘트")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### 1) 부동산 비중 & 레버리지")
            if st.session_state.properties:
                net_re = sum([max(0, p["current_val"] - p["loan"]) for p in st.session_state.properties])
                total_asset = liquid_asset + net_re
                ratio = net_re / total_asset if total_asset > 0 else 0

                if ratio >= 0.8:
                    st.markdown("""
                        <div class="highlight-box">
                            <div class="section-title">⚠️ 부동산 편중 심각</div>
                            <div>전체 자산의 80% 이상이 부동산에 묶여 있습니다. 은퇴 직후 <b>현금 흐름 부족</b> 위험이 큽니다.</div>
                        </div>
                    """, unsafe_allow_html=True)
                elif ratio >= 0.6:
                    st.markdown("""
                        <div class="highlight-box">
                            <div class="section-title">📌 부동산 비중 다소 높음</div>
                            <div>은퇴 전후 일부 매각을 통해 현금 비중을 늘리는 전략을 고민해 보셔야 합니다.</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="highlight-box">
                            <div class="section-title">✅ 부동산/현금 비중 양호</div>
                            <div>유동성과 자산가치의 균형이 비교적 잘 맞는 편입니다. 상속·증여 계획만 별도로 보완하시면 좋겠습니다.</div>
                        </div>
                    """, unsafe_allow_html=True)

                loans = sum([p["loan"] for p in st.session_state.properties])
                if loans > 0:
                    st.markdown(f"📉 **부채 관리:** 현재 보유 부채 **{loans}억 원**은 은퇴 전 반드시 상환하여 고정비 지출을 없애야 합니다.")
            else:
                st.markdown("현재 입력된 부동산 자산이 없습니다. 보유 중인 아파트/상가 등이 있다면 반드시 함께 고려해야 합니다.")

        with col_b:
            st.markdown("#### 2) 생활비 & 취미 지출")
            st.markdown(f"- 기본 은퇴생활비: **월 {monthly_spend}만원**")
            st.markdown(f"- 골프/여행 포함 추정 지출: **월 {total_monthly_spend}만원 수준**")

            if total_monthly_spend >= 400:
                st.markdown("""
                    <div class="remark-box">
                        <span class="warn-text">⚠️ 고비용 라이프스타일</span><br/>
                        현재 계획하신 생활비는 꽤 높은 편입니다. 은퇴 초기에 지출을 조금 줄이고,
                        70대 이후에 취미 활동 강도를 조정하는 전략을 고려해 보세요.
                    </div>
                """, unsafe_allow_html=True)
            elif total_monthly_spend >= 250:
                st.markdown("""
                    <div class="remark-box">
                        <span class="neutral-text">📌 적정 수준의 생활비</span><br/>
                        현재 수준은 평균적인 중상위 은퇴생활에 해당합니다. 다만, 의료비·요양비가 늘어나는
                        70대 이후를 대비해 별도의 예비 자금을 마련해 두시면 좋겠습니다.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="remark-box">
                        <span class="good-text">✅ 안정적인 지출 구조</span><br/>
                        비교적 검소한 은퇴생활 계획입니다. 자녀 지원·여행·취미 활동에 여유를 조금 더 배분해도 됩니다.
                    </div>
                """, unsafe_allow_html=True)

        # 3-3. 투자 전략 코멘트
        st.markdown("### 📌 투자 전략 코멘트")
        with st.expander("3. 변동성 관리 및 투자 전략", expanded=True):
            if return_rate_int < 3:
                st.markdown("**🛡️ 보수적 운용 (Low Risk)**")
                st.write("원금 보존에 중점을 두고 계십니다. 하지만 **실질 구매력**을 지키기 위해서는 최소한 물가상승률(2~3%) + 1~2% 수준의 수익이 필요합니다. 채권형 펀드나 고배당주 ETF를 포트폴리오에 일부 편입하는 것을 권장합니다.")
            elif return_rate_int > 7:
                st.markdown("**🚀 공격적 운용 (High Risk)**")
                st.write("높은 목표 수익률은 자산 증식에 유리하지만, 은퇴 직전의 폭락장(**Sequence Risk**)에 취약합니다. 50대 후반부터는 주식 비중을 줄이고 안전 자산을 늘리는 **현금 쐐기(Cash Wedge)** 전략을 실행해야 합니다.")
            else:
                st.markdown("**⚖️ 중위험·중수익 (Moderate Risk)**")
                st.write("가장 권장되는 운용 방식입니다. 은퇴 시점이 다가올수록 위험 자산 비중을 자동으로 줄여주는 **TDF(Target Date Fund)** 활용이 적합합니다.")

    # 4-2. 공통 상담 신청 폼
    props_str = ", ".join([p["name"] for p in st.session_state.properties]) if st.session_state.properties else "없음"
    props_json = json.dumps(st.session_state.properties, ensure_ascii=False)

    # 부동산 순자산(억) 재계산 (혹시 위에서 net_re가 계산되지 않았을 경우를 대비)
    if "net_re" not in locals():
        net_re = sum(
            [max(0, p.get("current_val", 0) - p.get("loan", 0)) for p in st.session_state.properties]
        ) if st.session_state.properties else 0.0

    render_common_form(
        app_type="life",
        DataModelClass=LifeData,
        # [데이터 전달] 모델 필드와 일치시킴
        age=age_curr,
        retire_age=age_retire,
        death_age=age_death,
        asset=liquid_asset,
        save=monthly_save,
        rate_pct=return_rate_int,
        re_asset=net_re,
        props_str=props_str,
        props_json=props_json,
        spend=monthly_spend,
        golf_freq=golf_freq,
        travel_freq=travel_freq,
        inflation_label=inflation,
        inflation_pct=inf_val * 100,
        score=score,
        grade=grade,
        shortfall_txt=f"{ob_norm}세" if ob_norm else "Safe",
    )
