import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="CEFR English Level Test",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
with open('assets/styles.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'student_info' not in st.session_state:
    st.session_state['student_info'] = {}

# 로그인 함수
# 로그인 함수
def login(username, password):
    # 비밀번호 보안 처리 (Streamlit Secrets 사용)
    if 'users' not in st.secrets:
        st.error("설정 파일(secrets.toml)이 누락되었습니다. 관리자에게 문의하세요.")
        return False
        
    users = st.secrets['users']

    if username in users and users[username]['password'] == password:
        st.session_state['logged_in'] = True
        st.session_state['user_role'] = users[username]['role']
        if users[username]['role'] == 'student':
            st.session_state['student_info'] = {
                'name': username,
                'school': 'Default School',
                'grade': '1',
                'class': 'A'
            }
        return True
    return False

# 메인 페이지
def main():
    # 사이드바 - 로그인/로그아웃
    with st.sidebar:
        st.title("🎓 CEFR Test Platform")

        if not st.session_state['logged_in']:
            st.subheader("로그인")
            username = st.text_input("사용자 이름")
            password = st.text_input("비밀번호", type="password")

            if st.button("로그인"):
                if login(username, password):
                    st.success(f"{username}님 환영합니다!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
        else:
            st.success(f"로그인됨: {st.session_state['user_role']}")
            if st.button("로그아웃"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

    # 메인 콘텐츠
    if st.session_state['logged_in']:
        if st.session_state['user_role'] == 'student':
            student_dashboard()
        elif st.session_state['user_role'] == 'teacher':
            teacher_dashboard()
    else:
        welcome_page()

def welcome_page():
    # EduPrompT Hero Section
    st.markdown("""
    <div style="
        position: relative; 
        background: linear-gradient(180deg, #FDFCFA 0%, #F7F5F2 100%); 
        padding: 5rem 2rem; 
        border-radius: 20px; 
        overflow: hidden; 
        text-align: center;
        margin-bottom: 3rem;
    ">
        <!-- Background Orbs -->
        <div style="position: absolute; top: -50px; left: -50px; width: 300px; height: 300px; background: #E8785A; opacity: 0.15; filter: blur(80px); border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -50px; right: -50px; width: 300px; height: 300px; background: #7BA38C; opacity: 0.15; filter: blur(80px); border-radius: 50%;"></div>
        
        <!-- Content -->
        <div style="position: relative; z-index: 10;">
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #E8785A; letter-spacing: 0.3em; margin-bottom: 2rem; text-transform: uppercase;">
                EduPrompT v12.0 ULTIMATE
            </p>
            
            <h1 style="font-family: 'Cormorant Garamond', serif; font-size: 3.5rem; font-weight: 300; line-height: 1.2; color: #1A1A1A; margin-bottom: 1.5rem;">
                CEFR English <em style="font-family: 'Cormorant Garamond', serif; color: #7BA38C; font-style: italic;">Level Test</em>
            </h1>
            
            <p style="font-family: 'Sora', sans-serif; font-size: 1.1rem; color: #5A5A5A; font-weight: 300; line-height: 1.6; max-width: 600px; margin: 0 auto 3rem auto;">
                평가원 수준의 정밀한 문항 분석과 국제 표준 CEFR 레벨 진단.<br>
                당신의 영어 실력을 가장 완벽하게 증명하세요.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="edu-card card-hover" style="height: 100%;">
            <div style="width: 50px; height: 50px; background: rgba(123, 163, 140, 0.1); color: #7BA38C; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: 1.5rem;">📝</div>
            <h3 style="font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; margin-bottom: 1rem;">For Students</h3>
            <ul style="list-style: none; padding: 0; color: #5A5A5A; line-height: 1.8; font-family: 'Sora', sans-serif;">
                <li>✓ CEFR 레벨 정밀 진단</li>
                <li>✓ 실시간 점수 및 피드백</li>
                <li>✓ 취약 유형 상세 분석</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="edu-card card-hover" style="height: 100%;">
            <div style="width: 50px; height: 50px; background: rgba(232, 120, 90, 0.1); color: #E8785A; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: 1.5rem;">👨‍🏫</div>
            <h3 style="font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; margin-bottom: 1rem;">For Teachers</h3>
            <ul style="list-style: none; padding: 0; color: #5A5A5A; line-height: 1.8; font-family: 'Sora', sans-serif;">
                <li>✓ 학생 성적 통합 관리</li>
                <li>✓ 데이터 기반 학습 분석</li>
                <li>✓ 맞춤형 PDF 리포트 생성</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("---")
    st.info("💡 테스트 계정: 학생(darlbit/darlbit123), 교사(darlbitt/darlbitt123)")

    # CEFR 레벨 정보 (Use EduPrompT styled table if possible, for now keep standard dataframe or custom HTML)
    st.subheader("📚 CEFR Level Guide")
    st.dataframe(pd.DataFrame({
        'Level': ['Pre-A1', 'A1', 'A2', 'B1', 'B2'],
        'Description': ['Foundation', 'Basic', 'Independent 1', 'Independent 2', 'Proficient'],
        'Key Competency': ['Basic Greetings', 'Daily Conversation', 'Familiar Topics', 'Describing Experiences', 'Complex Discussions']
    }), use_container_width=True)


def student_dashboard():
    st.title("📝 학생 대시보드")

    # 학생 정보 표시
    student_name = st.session_state['student_info']['name']
    st.write(f"환영합니다, {student_name}님!")

    # 레벨 선택
    level = st.selectbox(
        "응시할 레벨을 선택하세요:",
        ['Pre-A1', 'A1', 'A2', 'B1', 'B2'],
        index=1
    )

    # 테스트 시작 버튼
    if st.button("테스트 시작", type="primary"):
        st.session_state['test_level'] = level
        st.switch_page("pages/1_Student_Test.py")

    # 이전 결과 확인
    st.subheader("📊 이전 테스트 결과")
    # 데이터베이스에서 해당 학생의 결과 가져오기
    # placeholder

    st.info("준비되셨다면 테스트 시작 버튼을 클릭하세요!")

def teacher_dashboard():
    st.title("👨‍🏫 교사 대시보드")

    # 빠른 통계
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("전체 학생", "0", "👥")
    with col2:
        st.metric("오늘 제출", "0", "📅")
    with col3:
        st.metric("평균 점수", "0%", "📊")
    with col4:
        st.metric("합격률", "0%", "✅")

    st.markdown("---")

    # 관리 기능
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 결과 관리", type="primary"):
            st.switch_page("pages/2_Teacher_Dashboard.py")

    with col2:
        if st.button("📈 리포트 생성"):
            st.switch_page("pages/3_Reports.py")

    with col3:
        if st.button("⚙️ 설정"):
            st.info("설정 페이지 준비 중...")

    st.markdown("---")

    # 최근 제출 목록
    st.subheader("📋 최근 제출 목록")
    # 데이터베이스에서 최근 제출 가져오기
    # placeholder

if __name__ == "__main__":
    main()