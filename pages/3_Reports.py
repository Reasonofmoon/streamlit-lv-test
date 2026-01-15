import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.counseling_report_generator import (
    generate_student_counseling_report,
    generate_printable_report_html,
    save_report_as_html
)

# 페이지 설정
st.set_page_config(
    page_title="Reports",
    page_icon="📊",
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
    from utils.db_manager import DatabaseManager
    try:
        db = DatabaseManager()
        return db.load_submissions()
    except Exception as e:
        st.error(f"데이터베이스 로드 오류: {e}")
        return []

# 학생별 진행 추적 함수
def track_student_progress(submissions, student_name):
    student_submissions = [s for s in submissions if s.get('studentInfo', {}).get('name') == student_name]
    student_submissions.sort(key=lambda x: x.get('submittedAt', ''))

    if not student_submissions:
        return None

    progress = {
        'student_name': student_name,
        'total_tests': len(student_submissions),
        'test_history': [],
        'average_score': 0,
        'best_score': 0,
        'current_level': student_submissions[-1].get('level', 'Unknown'),
        'improvement_trend': 'stable'
    }

    scores = []
    for s in student_submissions:
        progress['test_history'].append({
            'date': s.get('submittedAt', ''),
            'level': s.get('level', 'Unknown'),
            'score': s.get('score', 0),
            'passed': s.get('passed', False)
        })
        scores.append(s.get('score', 0))

    if scores:
        progress['average_score'] = round(sum(scores) / len(scores))
        progress['best_score'] = max(scores)

        # 향상 추세 계산
        if len(scores) >= 2:
            recent_avg = sum(scores[-3:]) / len(scores[-3:])  # 최근 3개 평균
            earlier_avg = sum(scores[:-3]) / len(scores[:-3]) if len(scores) > 3 else scores[0]  # 이전 평균
            improvement = recent_avg - earlier_avg

            if improvement > 15:
                progress['improvement_trend'] = 'significant_improvement'
            elif improvement > 5:
                progress['improvement_trend'] = 'moderate_improvement'
            elif improvement > -5:
                progress['improvement_trend'] = 'stable'
            else:
                progress['improvement_trend'] = 'decline'

    return progress

# 상세 리포트 생성 함수
def generate_detailed_report(submissions):
    if not submissions:
        return "리포트를 생성할 데이터가 없습니다."

    # 기본 통계
    total_students = len(submissions)
    avg_score = round(sum(s.get('score', 0) for s in submissions) / total_students)
    passed_count = sum(1 for s in submissions if s.get('passed', False))
    pass_rate = round((passed_count / total_students) * 100)

    # 레벨별 분석
    level_stats = {}
    for s in submissions:
        level = s.get('level', 'Unknown')
        if level not in level_stats:
            level_stats[level] = {'count': 0, 'total_score': 0, 'passed': 0}
        level_stats[level]['count'] += 1
        level_stats[level]['total_score'] += s.get('score', 0)
        if s.get('passed', False):
            level_stats[level]['passed'] += 1

    # HTML 리포트 생성
    html_report = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>CEFR 테스트 상세 리포트</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
            .header {{ text-align: center; border-bottom: 3px solid #3B82F6; padding-bottom: 20px; margin-bottom: 30px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .summary-item {{ background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
            .summary-value {{ font-size: 2.5rem; font-weight: bold; color: #3B82F6; }}
            .section {{ margin-bottom: 40px; page-break-inside: avoid; }}
            .section-title {{ color: #1e3a8a; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; margin-bottom: 20px; font-size: 1.5rem; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #e5e7eb; padding: 12px; text-align: center; }}
            th {{ background: #f1f5f9; font-weight: 600; color: #1e293b; }}
            .pass {{ color: #10B981; font-weight: bold; }}
            .fail {{ color: #EF4444; font-weight: bold; }}
            .level-badge {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.9em; }}
            
            /* 인쇄 최적화 스타일 */
            @media print {{
                body {{ margin: 0; padding: 20px; -webkit-print-color-adjust: exact; }}
                .no-print {{ display: none; }}
                .section {{ page-break-inside: avoid; }}
                .header {{ margin-top: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 CEFR 영어 레벨 테스트 상세 리포트</h1>
            <p><strong>생성일:</strong> {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
            <p><strong>분석 대상:</strong> {total_students}명의 학생 결과</p>
        </div>

        <div class="summary">
            <div class="summary-item">
                <div class="summary-value">{total_students}명</div>
                <div>전체 학생</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{avg_score}점</div>
                <div>평균 점수</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{pass_rate}%</div>
                <div>전체 합격률</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{passed_count}명</div>
                <div>합격 성공</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">📊 레벨별 성취도 분석</h2>
            <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px;">
                <div style="width: 400px; height: 300px;">
                    <canvas id="levelChart"></canvas>
                </div>
            </div>
            <table>
                <tr>
                    <th>레벨</th>
                    <th>응시자 수</th>
                    <th>평균 점수</th>
                    <th>합격자 수</th>
                    <th>합격률</th>
                </tr>
    """

    for level, stats in level_stats.items():
        avg_level_score = round(stats['total_score'] / stats['count'])
        level_pass_rate = round((stats['passed'] / stats['count']) * 100)
        html_report += f"""
                <tr>
                    <td><span class="level-badge level-{level.lower().replace('-', '')}">{level}</span></td>
                    <td>{stats['count']}</td>
                    <td>{avg_level_score}%</td>
                    <td>{stats['passed']}</td>
                    <td>{level_pass_rate}%</td>
                </tr>
        """

    html_report += """
            </table>
        </div>

        <div class="section">
            <h2 class="section-title">📝 종합 분석 의견</h2>
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; height: 150px; background: #f9fafb;">
                <p style="color: #6b7280; font-style: italic;">(이곳에 교사 코멘트를 수기로 작성하거나 입력할 수 있습니다.)</p>
            </div>
        </div>

        <div style="text-align: center; margin-top: 50px; color: #6b7280; font-size: 0.9em;">
            <p>본 리포트는 CEFR Teacher Dashboard 시스템에서 자동 생성되었습니다.</p>
            <p>© 2025 CEFR English Level Test System</p>
        </div>

        <script>
            // 차트 데이터 준비
            const levelLabels = {level_labels};
            const levelScores = {level_scores};
            const levelPassRates = {level_pass_rates};

            const ctx = document.getElementById('levelChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: levelLabels,
                    datasets: [{
                        label: '평균 점수',
                        data: levelScores,
                        backgroundColor: 'rgba(59, 130, 246, 0.5)',
                        borderColor: 'rgb(59, 130, 246)',
                        borderWidth: 1
                    },
                    {
                        label: '합격률 (%)',
                        data: levelPassRates,
                        backgroundColor: 'rgba(16, 185, 129, 0.5)',
                        borderColor: 'rgb(16, 185, 129)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        </script>
    </body>
    </html>
    """

    # JS 데이터 포맷팅
    levels = list(level_stats.keys())
    scores = [round(level_stats[l]['total_score'] / level_stats[l]['count']) for l in levels]
    pass_rates = [round((level_stats[l]['passed'] / level_stats[l]['count']) * 100) for l in levels]

    html_report = html_report.format(
        level_labels=json.dumps(levels),
        level_scores=json.dumps(scores),
        level_pass_rates=json.dumps(pass_rates)
    )

    return html_report

# 메인 함수
def main():
    st.title("📊 리포트 및 분석")

    # 데이터 로드
    submissions = load_submissions()

    if not submissions:
        st.warning("리포트를 생성할 데이터가 없습니다. 학생들이 먼저 테스트를 응시해주세요.")
        return

    # 리포트 타입 선택
    report_type = st.selectbox(
        "리포트 유형 선택:",
        ["📊 종합 분석 리포트", "👥 학생별 진행 현황", "📈 레벨별 비교 분석", "⏰ 시간대별 분석", "🎓 개별 학생 상담 리포트 (NEW)"]
    )

    if report_type == "📊 종합 분석 리포트":
        st.subheader("종합 분석 리포트")

        # 기간 선택
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("시작일", datetime.now().date() - timedelta(days=30))
        with col2:
            end_date = st.date_input("종료일", datetime.now().date())

        # 필터링
        filtered_submissions = [
            s for s in submissions
            if start_date <= datetime.fromisoformat(s.get('submittedAt', '')).date() <= end_date
        ]

        if filtered_submissions:
            # 통계 계산
            total = len(filtered_submissions)
            avg_score = round(sum(s.get('score', 0) for s in filtered_submissions) / total)
            pass_count = sum(1 for s in filtered_submissions if s.get('passed', False))
            pass_rate = round((pass_count / total) * 100)

            # 통계 카드
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("분석 기간 응시자", total)
            with col2:
                st.metric("평균 점수", f"{avg_score}%")
            with col3:
                st.metric("합격자 수", pass_count)
            with col4:
                st.metric("합격률", f"{pass_rate}%")

            # 리포트 생성 버튼
            if st.button("📄 상세 리포트 생성 (HTML)", type="primary"):
                html_report = generate_detailed_report(filtered_submissions)
                st.download_button(
                    label="HTML 리포트 다운로드",
                    data=html_report,
                    file_name=f"cefr_detailed_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )

    elif report_type == "👥 학생별 진행 현황":
        st.subheader("학생별 진행 현황")

        # 학생 목록
        students = list(set(s.get('studentInfo', {}).get('name', 'Unknown') for s in submissions))
        selected_student = st.selectbox("학생 선택:", students)

        if selected_student and selected_student != 'Unknown':
            progress = track_student_progress(submissions, selected_student)

            if progress:
                # 학생 정보
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("총 테스트 횟수", progress['total_tests'])
                with col2:
                    st.metric("평균 점수", f"{progress['average_score']}점")
                with col3:
                    st.metric("최고 점수", f"{progress['best_score']}점")
                with col4:
                    st.metric("현재 레벨", progress['current_level'])

                # 진행 추세
                trend_messages = {
                    'significant_improvement': '🎉 매우 큰 향상이 있습니다!',
                    'moderate_improvement': '📈 꾸준한 향상이 있습니다.',
                    'stable': '📊 안정적인 성과를 보입니다.',
                    'decline': '📉 하락세가 있습니다.'
                }
                st.info(f"학습 추세: {trend_messages.get(progress['improvement_trend'], '📋 데이터 부족')}")

                # 테스트 기록 그래프
                if progress['test_history']:
                    df = pd.DataFrame(progress['test_history'])
                    df['date'] = pd.to_datetime(df['date']).dt.date

                    fig = px.line(
                        df, x='date', y='score',
                        title=f"{selected_student}의 점수 변화",
                        markers=True,
                        text='score'
                    )
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)

                    # 테스트 기록 표
                    st.subheader("테스트 기록")
                    df_display = df[['date', 'level', 'score', 'passed']].copy()
                    df_display.columns = ['날짜', '레벨', '점수', '합격 여부']
                    df_display['합격 여부'] = df_display['합격 여부'].apply(lambda x: '✅ 합격' if x else '❌ 불합격')
                    st.dataframe(df_display, use_container_width=True, hide_index=True)

    elif report_type == "📈 레벨별 비교 분석":
        st.subheader("레벨별 비교 분석")

        # 레벨별 통계
        level_stats = {}
        for s in submissions:
            level = s.get('level', 'Unknown')
            if level not in level_stats:
                level_stats[level] = {'scores': [], 'passed': 0, 'total': 0}
            level_stats[level]['scores'].append(s.get('score', 0))
            level_stats[level]['total'] += 1
            if s.get('passed', False):
                level_stats[level]['passed'] += 1

        # 레벨별 점수 분포 박스플롯
        if level_stats:
            fig = go.Figure()

            for level, stats in level_stats.items():
                if level != 'Unknown' and stats['scores']:
                    fig.add_trace(go.Box(
                        y=stats['scores'],
                        name=level,
                        boxpoints='outliers'
                    ))

            fig.update_layout(
                title="레벨별 점수 분포",
                yaxis_title="점수",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            # 레벨별 통계 표
            level_data = []
            for level, stats in level_stats.items():
                if level != 'Unknown' and stats['scores']:
                    avg_score = round(sum(stats['scores']) / len(stats['scores']))
                    pass_rate = round((stats['passed'] / stats['total']) * 100)
                    level_data.append({
                        '레벨': level,
                        '응시자 수': stats['total'],
                        '평균 점수': f"{avg_score}점",
                        '최고 점수': f"{max(stats['scores'])}점",
                        '최저 점수': f"{min(stats['scores'])}점",
                        '합격률': f"{pass_rate}%"
                    })

            df_levels = pd.DataFrame(level_data)
            st.dataframe(df_levels, use_container_width=True, hide_index=True)

    elif report_type == "⏰ 시간대별 분석":
        st.subheader("시간대별 분석")

        # 요일별 분석
        weekday_data = {}
        for s in submissions:
            date = datetime.fromisoformat(s.get('submittedAt', ''))
            weekday = date.strftime('%A')
            if weekday not in weekday_data:
                weekday_data[weekday] = []
            weekday_data[weekday].append(s.get('score', 0))

        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_names_ko = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

        weekday_stats = []
        for i, weekday in enumerate(weekday_order):
            if weekday in weekday_data:
                avg_score = round(sum(weekday_data[weekday]) / len(weekday_data[weekday]))
                count = len(weekday_data[weekday])
                weekday_stats.append({
                    '요일': weekday_names_ko[i],
                    '응시자 수': count,
                    '평균 점수': f"{avg_score}점"
                })

        if weekday_stats:
            df_weekday = pd.DataFrame(weekday_stats)
            fig = px.bar(
                df_weekday, x='요일', y='평균 점수',
                title="요일별 평균 점수",
                text='응시자 수'
            )
            st.plotly_chart(fig, use_container_width=True)

        # 시간대별 분석
        hourly_data = {}
        for s in submissions:
            hour = datetime.fromisoformat(s.get('submittedAt', '')).hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(s.get('score', 0))

        if hourly_data:
            hours = sorted(hourly_data.keys())
            avg_scores = [round(sum(hourly_data[h]) / len(hourly_data[h])) for h in hours]
            counts = [len(hourly_data[h]) for h in hours]

            fig = make_subplots(
                specs=[[{"secondary_y": True}]],
                subplot_titles=["시간대별 응시자 수 및 평균 점수"]
            )

            fig.add_trace(
                go.Scatter(x=hours, y=avg_scores, name="평균 점수", line=dict(color='blue')),
                secondary_y=False
            )

            fig.add_trace(
                go.Bar(x=hours, y=counts, name="응시자 수", marker_color='lightblue'),
                secondary_y=True
            )

            fig.update_xaxes(title_text="시간")
            fig.update_yaxes(title_text="평균 점수", secondary_y=False)
            fig.update_yaxes(title_text="응시자 수", secondary_y=True)

            st.plotly_chart(fig, use_container_width=True)

    elif report_type == "🎓 개별 학생 상담 리포트 (NEW)":
        st.subheader("개별 학생 상담 리포트 생성")
        st.info("📄 A4 형식의 프린트 가능한 상담 리포트를 생성합니다.")
        
        # 학생 선택
        students = list(set(s.get('studentInfo', {}).get('name', 'Unknown') for s in submissions))
        students = [s for s in students if s != 'Unknown']
        
        if not students:
            st.warning("리포트를 생성할 학생 데이터가 없습니다.")
            return
        
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_student = st.selectbox("학생 선택:", students)
        with col2:
            test_count = st.number_input("최근 테스트 개수", min_value=1, max_value=10, value=1)
        
        if selected_student:
            # 해당 학생의 최근 테스트 데이터 가져오기
            student_submissions = [
                s for s in submissions
                if s.get('studentInfo', {}).get('name') == selected_student
            ]
            student_submissions.sort(key=lambda x: x.get('submittedAt', ''), reverse=True)
            
            if student_submissions:
                # 테스트 선택
                st.subheader("테스트 기록 선택")
                test_options = []
                for i, sub in enumerate(student_submissions[:test_count]):
                    date = datetime.fromisoformat(sub.get('submittedAt', '')).strftime('%Y-%m-%d %H:%M')
                    level = sub.get('level', 'Unknown')
                    score = sub.get('score', 0)
                    status = "합격" if sub.get('passed', False) else "불합격"
                    test_options.append(f"{date} | {level} | {score}점 | {status}")
                
                selected_test_idx = st.selectbox(
                    "리포트를 생성할 테스트 선택:",
                    range(len(test_options[:test_count])),
                    format_func=lambda x: test_options[x]
                )
                
                selected_submission = student_submissions[selected_test_idx]
                
                # 상세 정보 표시
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("테스트 레벨", selected_submission.get('level', 'Unknown'))
                with col2:
                    st.metric("점수", f"{selected_submission.get('score', 0)}점")
                with col3:
                    st.metric("정답률", f"{selected_submission.get('accuracy', 0)}%")
                with col4:
                    status = "✅ 합격" if selected_submission.get('passed', False) else "❌ 불합격"
                    st.metric("합격 여부", status)
                
                # 리포트 생성 버튼
                st.markdown("---")
                st.subheader("리포트 생성 옵션")
                
                col1, col2 = st.columns(2)
                with col1:
                    include_charts = st.checkbox("📊 차표 포함", value=True)
                    include_detailed_analysis = st.checkbox("🔍 상세 분석 포함", value=True)
                with col2:
                    include_roadmap = st.checkbox("🗺️ 학습 로드맵 포함", value=True)
                    include_questions = st.checkbox("📝 문항별 분석 포함", value=True)
                
                # 리포트 생성
                if st.button("📄 A4 상담 리포트 생성", type="primary", use_container_width=True):
                    # 학생 정보 추출
                    student_info = {
                        'name': selected_student,
                        'full_name': selected_submission.get('studentInfo', {}).get('full_name', selected_student),
                        'school': selected_submission.get('studentInfo', {}).get('school', ''),
                        'grade': selected_submission.get('studentInfo', {}).get('grade', ''),
                        'class': selected_submission.get('studentInfo', {}).get('class', '')
                    }
                    
                    # 테스트 결과 추출
                    test_results = {
                        'level': selected_submission.get('level', 'A1'),
                        'score': selected_submission.get('score', 0),
                        'correct': selected_submission.get('correct', 0),
                        'total': selected_submission.get('total', 0),
                        'accuracy': selected_submission.get('accuracy', 0),
                        'passed': selected_submission.get('passed', False),
                        'submitted_at': datetime.fromisoformat(selected_submission.get('submittedAt', '')).strftime('%Y년 %m월 %d일'),
                        'duration': selected_submission.get('duration', '0분')
                    }
                    
                    # 분석 결과 추출 (간단한 기본값 사용)
                    analysis = selected_submission.get('analysis', {})
                    if not analysis:
                        # 기본 분석 생성
                        from utils.cefr_analyzer import CEFRAnalyzer
                        analyzer = CEFRAnalyzer()
                        
                        # 섹션별 결과 계산
                        section_results = {}
                        section_data = {}
                        for q_data in questions_data:
                            section = q_data.get('section', 'General')
                            if section not in section_data:
                                section_data[section] = {'correct': 0, 'total': 0}
                            section_data[section]['total'] += 1
                        
                        # 정답 체크
                        for ans, q_data in zip(answers, questions_data):
                            section = q_data.get('section', 'General')
                            if ans.get('correct', False):
                                section_data[section]['correct'] += 1
                        
                        # 섹션 결과 변환
                        for section, data in section_data.items():
                            section_results[section] = data
                        
                        # 테스트 결과 준비
                        test_results_for_analysis = {
                            'level': selected_submission.get('level', 'A1'),
                            'score': selected_submission.get('score', 0),
                            'sectionResults': section_results,
                            'submittedAt': selected_submission.get('submittedAt', ''),
                            'studentInfo': selected_submission.get('studentInfo', {})
                        }
                        
                        analysis = analyzer.analyze_test_results(test_results_for_analysis)
                    
                    # 상세 문항 정보
                    detailed_questions = []
                    answers = selected_submission.get('answers', [])
                    questions_data = selected_submission.get('questions', [])
                    
                    for i, (ans, q_data) in enumerate(zip(answers, questions_data)):
                        detailed_questions.append({
                            'question': q_data.get('question', ''),
                            'options': q_data.get('options', []),
                            'user_answer': ans.get('answer', -1),
                            'correct_answer': q_data.get('correct', 0),
                            'is_correct': ans.get('correct', False),
                            'section': q_data.get('section', 'General'),
                            'explanation': q_data.get('explanation', '')
                        })
                    
                    # 리포트 생성
                    try:
                        html_report = generate_student_counseling_report(
                            student_info,
                            test_results,
                            analysis,
                            detailed_questions
                        )
                        
                        # 미리보기
                        st.success("✅ 리포트가 생성되었습니다!")
                        st.markdown("### 리포트 미리보기")
                        components.html(html_report, height=1000, scrolling=True)
                        
                        # 다운로드 버튼
                        st.markdown("---")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                label="📥 HTML 파일 다운로드",
                                data=html_report,
                                file_name=f"counseling_report_{selected_student}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                mime="text/html",
                                use_container_width=True
                            )
                        with col2:
                            st.info("💡 팁: HTML 파일을 브라우저에서 열고 Ctrl+P(또는 Cmd+P)로 인쇄하여 PDF로 저장하세요.")
                        
                    except Exception as e:
                        st.error(f"리포트 생성 중 오류가 발생했습니다: {str(e)}")
                        import traceback
                        st.error(traceback.format_exc())

if __name__ == "__main__":
    main()