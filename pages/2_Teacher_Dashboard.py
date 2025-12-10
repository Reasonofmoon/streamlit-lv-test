import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="Teacher Dashboard",
    page_icon="👨‍🏫",
    layout="wide"
)

# 커스텀 CSS
with open('assets/styles.css', 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 로그인 확인
if not st.session_state.get('logged_in', False) or st.session_state.get('user_role') != 'teacher':
    st.error("교사 계정으로 로그인해주세요.")
    st.switch_page("app.py")

# 데이터 로드 함수
def load_submissions():
    submissions = []
    submissions_dir = 'data/submissions'

    if os.path.exists(submissions_dir):
        for file in os.listdir(submissions_dir):
            if file.endswith('.json'):
                try:
                    with open(os.path.join(submissions_dir, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        submissions.append(data)
                except Exception as e:
                    st.error(f"파일 로드 오류: {file} - {e}")

    return submissions

# 통계 계산 함수
def calculate_statistics(submissions):
    if not submissions:
        return {
            'total_students': 0,
            'avg_score': 0,
            'pass_rate': 0,
            'today_submissions': 0,
            'level_distribution': {},
            'score_distribution': {},
            'section_averages': {}
        }

    total_students = len(submissions)
    avg_score = sum(s.get('score', 0) for s in submissions) / total_students
    passed_count = sum(1 for s in submissions if s.get('passed', False))
    pass_rate = (passed_count / total_students) * 100

    # 오늘 제출 수
    today = datetime.now().date()
    today_submissions = sum(1 for s in submissions
                          if datetime.fromisoformat(s.get('submittedAt', '')).date() == today)

    # 레벨별 분포
    level_distribution = {}
    for s in submissions:
        level = s.get('level', 'Unknown')
        level_distribution[level] = level_distribution.get(level, 0) + 1

    # 점수 분포
    score_ranges = {
        '90-100': 0, '80-89': 0, '70-79': 0,
        '60-69': 0, '50-59': 0, '0-49': 0
    }
    for s in submissions:
        score = s.get('score', 0)
        if score >= 90: score_ranges['90-100'] += 1
        elif score >= 80: score_ranges['80-89'] += 1
        elif score >= 70: score_ranges['70-79'] += 1
        elif score >= 60: score_ranges['60-69'] += 1
        elif score >= 50: score_ranges['50-59'] += 1
        else: score_ranges['0-49'] += 1

    # 섹션별 평균
    section_totals = {}
    section_counts = {}
    for s in submissions:
        section_results = s.get('sectionResults', {})
        for section, data in section_results.items():
            if section not in section_totals:
                section_totals[section] = 0
                section_counts[section] = 0
            if data.get('total', 0) > 0:
                percentage = (data.get('correct', 0) / data.get('total', 1)) * 100
                section_totals[section] += percentage
                section_counts[section] += 1

    section_averages = {
        section: section_totals[section] / section_counts[section]
        for section in section_totals
    }

    return {
        'total_students': total_students,
        'avg_score': round(avg_score),
        'pass_rate': round(pass_rate),
        'today_submissions': today_submissions,
        'level_distribution': level_distribution,
        'score_distribution': score_ranges,
        'section_averages': section_averages
    }

# 메인 함수
def main():
    st.title("👨‍🏫 교사용 대시보드")

    # 데이터 로드
    submissions = load_submissions()
    stats = calculate_statistics(submissions)

    # 통계 카드
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="전체 학생",
            value=stats['total_students'],
            delta="👥"
        )

    with col2:
        st.metric(
            label="오늘 제출",
            value=stats['today_submissions'],
            delta="📅"
        )

    with col3:
        st.metric(
            label="평균 점수",
            value=f"{stats['avg_score']}%",
            delta="📊"
        )

    with col4:
        st.metric(
            label="합격률",
            value=f"{stats['pass_rate']}%",
            delta="✅"
        )

    st.markdown("---")

    # 필터 컨트롤
    col1, col2, col3 = st.columns(3)

    with col1:
        level_filter = st.selectbox(
            "레벨 필터",
            ["전체", "Pre-A1", "A1", "A2", "B1", "B2"]
        )

    with col2:
        date_filter = st.selectbox(
            "기간 필터",
            ["전체", "오늘", "최근 7일", "최근 30일"]
        )

    with col3:
        sort_by = st.selectbox(
            "정렬 방식",
            ["최신순", "점수 높은순", "점수 낮은순", "이름순"]
        )

    # 데이터 필터링
    filtered_submissions = submissions.copy()

    if level_filter != "전체":
        filtered_submissions = [s for s in filtered_submissions if s.get('level') == level_filter]

    if date_filter != "전체":
        today = datetime.now().date()
        if date_filter == "오늘":
            filtered_submissions = [
                s for s in filtered_submissions
                if datetime.fromisoformat(s.get('submittedAt', '')).date() == today
            ]
        elif date_filter == "최근 7일":
            week_ago = today - timedelta(days=7)
            filtered_submissions = [
                s for s in filtered_submissions
                if datetime.fromisoformat(s.get('submittedAt', '')).date() >= week_ago
            ]
        elif date_filter == "최근 30일":
            month_ago = today - timedelta(days=30)
            filtered_submissions = [
                s for s in filtered_submissions
                if datetime.fromisoformat(s.get('submittedAt', '')).date() >= month_ago
            ]

    # 정렬
    if sort_by == "최신순":
        filtered_submissions.sort(key=lambda x: x.get('submittedAt', ''), reverse=True)
    elif sort_by == "점수 높은순":
        filtered_submissions.sort(key=lambda x: x.get('score', 0), reverse=True)
    elif sort_by == "점수 낮은순":
        filtered_submissions.sort(key=lambda x: x.get('score', 0))
    elif sort_by == "이름순":
        filtered_submissions.sort(key=lambda x: x.get('studentInfo', {}).get('name', ''))

    # 그래프 섹션
    if submissions:
        col1, col2 = st.columns(2)

        with col1:
            # 레벨별 분포
            if stats['level_distribution']:
                fig = px.pie(
                    values=list(stats['level_distribution'].values()),
                    names=list(stats['level_distribution'].keys()),
                    title="레벨별 분포"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # 점수 분포
            if stats['score_distribution']:
                fig = px.bar(
                    x=list(stats['score_distribution'].keys()),
                    y=list(stats['score_distribution'].values()),
                    title="점수 분포",
                    labels={'x': '점수 구간', 'y': '학생 수'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        # 시간별 추세
        if len(submissions) > 0:
            daily_stats = {}
            for s in submissions:
                date = datetime.fromisoformat(s.get('submittedAt', '')).date().strftime('%Y-%m-%d')
                if date not in daily_stats:
                    daily_stats[date] = []
                daily_stats[date].append(s.get('score', 0))

            dates = sorted(daily_stats.keys())
            avg_scores = [sum(daily_stats[d]) / len(daily_stats[d]) for d in dates]

            fig = px.line(
                x=dates,
                y=avg_scores,
                title="일별 평균 점수 추세",
                labels={'x': '날짜', 'y': '평균 점수'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    # 학생 결과 테이블
    st.subheader(f"📋 학생 결과 목록 (총 {len(filtered_submissions)}명)")

    if filtered_submissions:
        # 테이블 데이터 준비
        table_data = []
        for s in filtered_submissions:
            student_info = s.get('studentInfo', {})
            submitted_date = datetime.fromisoformat(s.get('submittedAt', ''))

            table_data.append({
                '이름': student_info.get('name', 'Unknown'),
                '학교': student_info.get('school', '-'),
                '학년/반': f"{student_info.get('grade', '-')}/{student_info.get('class', '-')}",
                '레벨': s.get('level', '-'),
                '점수': f"{s.get('score', 0)}점",
                '결과': '✅ 합격' if s.get('passed', False) else '❌ 불합격',
                '제출일': submitted_date.strftime('%Y-%m-%d %H:%M')
            })

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 내보내기 버튼
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 CSV로 내보내기"):
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="다운로드",
                    data=csv,
                    file_name=f"cefr_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("📄 JSON으로 내보내기"):
                json_data = json.dumps(filtered_submissions, ensure_ascii=False, indent=2)
                st.download_button(
                    label="다운로드",
                    data=json_data,
                    file_name=f"cefr_results_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

        with col3:
            if st.button("🔄 새로고침"):
                st.rerun()

    else:
        st.info("표시할 결과가 없습니다.")

    # 섹션별 분석
    if stats['section_averages']:
        st.subheader("📈 섹션별 평균 점수")
        section_df = pd.DataFrame([
            {'섹션': section, '평균 점수': f"{round(avg)}%"}
            for section, avg in stats['section_averages'].items()
        ])
        st.dataframe(section_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()