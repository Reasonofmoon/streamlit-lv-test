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
def login(username, password):
    # 간단한 인증 로직 (실제로는 데이터베이스 사용)
    users = {
        'darlbitt': {'password': 'darlbitt123', 'role': 'teacher'},
        'darlbit': {'password': 'darlbit123', 'role': 'student'}
    }

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
    st.title("🌟 CEFR English Level Test Platform")

    col1, col2 = st.columns(2)

    with col1:
        st.header("📝 학생용")
        st.markdown("""
        - CEFR 레벨 테스트 응시
        - 즉시 결과 확인
        - 상세 피드백 제공
        """)

    with col2:
        st.header("👨‍🏫 교사용")
        st.markdown("""
        - 학생 결과 관리
        - 통계 및 분석
        - 성적 리포트 생성
        """)

    st.markdown("---")
    st.info("💡 테스트 계정: 학생(darlbit/darlbit123), 교사(darlbitt/darlbitt123)")

    # CEFR 레벨 정보
    st.subheader("📚 CEFR 레벨 안내")
    levels_info = pd.DataFrame({
        '레벨': ['Pre-A1', 'A1', 'A2', 'B1', 'B2'],
        '설명': [
            '초보1 - 기초 영어',
            '초급 - 기본 영어',
            '중급1 - 독립적 사용자',
            '중급2 - 독립적 사용자',
            '고급 - 숙련된 사용자'
        ],
        '주요 능력': [
            '간단한 인사, 자기소개',
            '일상 대화, 기본 질문/응답',
            '친숙한 주제에 대한 대화',
            '경험, 사건, 계획 설명',
            '복잡한 주제에 대한 상세한 설명'
        ]
    })

    st.dataframe(levels_info, use_container_width=True)

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