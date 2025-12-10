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
        <style>
            body {{ font-family: 'Malgun Gothic', sans-serif; margin: 40px; line-height: 1.6; }}
            .header {{ text-align: center; border-bottom: 3px solid #3B82F6; padding-bottom: 20px; margin-bottom: 30px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .summary-item {{ background: #f8fafc; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .summary-value {{ font-size: 2.5rem; font-weight: bold; color: #3B82F6; }}
            .section {{ margin-bottom: 30px; }}
            .section-title {{ color: #3B82F6; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #e5e7eb; padding: 12px; text-align: left; }}
            th {{ background: #f1f5f9; font-weight: 600; }}
            .pass {{ color: #10B981; font-weight: 600; }}
            .fail {{ color: #EF4444; font-weight: 600; }}
            .chart-placeholder {{ background: #f9fafb; border: 2px dashed #d1d5db; height: 300px; display: flex; align-items: center; justify-content: center; color: #6b7280; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 CEFR 영어 레벨 테스트 상세 리포트</h1>
            <p>생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
            <p>분석 데이터: {total_students}명의 테스트 결과</p>
        </div>

        <div class="summary">
            <div class="summary-item">
                <div class="summary-value">{total_students}</div>
                <div>전체 학생 수</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{avg_score}%</div>
                <div>평균 점수</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{pass_rate}%</div>
                <div>전체 합격률</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{passed_count}</div>
                <div>합격자 수</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">📊 레벨별 분석</h2>
            <table>
                <tr>
                    <th>레벨</th>
                    <th>응시자 수</th>
                    <th>평균 점수</th>
                    <th>합격자 수</th>
                    <th>레벨별 합격률</th>
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
            <h2 class="section-title">👥 학생별 상세 결과</h2>
            <table>
                <tr>
                    <th>이름</th>
                    <th>학교</th>
                    <th>학년/반</th>
                    <th>레벨</th>
                    <th>점수</th>
                    <th>결과</th>
                    <th>제출일</th>
                </tr>
    """

    for s in sorted(submissions, key=lambda x: x.get('submittedAt', ''), reverse=True)[:50]:  # 최근 50개만 표시
        student_info = s.get('studentInfo', {})
        submitted_date = datetime.fromisoformat(s.get('submittedAt', '')).strftime('%Y-%m-%d %H:%M')
        result_class = "pass" if s.get('passed', False) else "fail"
        result_text = "✅ 합격" if s.get('passed', False) else "❌ 불합격"

        html_report += f"""
                <tr>
                    <td>{student_info.get('name', '-')}</td>
                    <td>{student_info.get('school', '-')}</td>
                    <td>{student_info.get('grade', '-')}/{student_info.get('class', '-')}</td>
                    <td>{s.get('level', '-')}</td>
                    <td>{s.get('score', 0)}점</td>
                    <td class="{result_class}">{result_text}</td>
                    <td>{submitted_date}</td>
                </tr>
        """

    html_report += """
            </table>
        </div>

        <div style="text-align: center; margin-top: 50px; color: #6b7280;">
            <p>이 리포트는 CEFR Teacher Dashboard에서 생성되었습니다.</p>
            <p>더 자세한 분석은 대시보드에서 확인해주세요.</p>
        </div>
    </body>
    </html>
    """

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
        ["📊 종합 분석 리포트", "👥 학생별 진행 현황", "📈 레벨별 비교 분석", "⏰ 시간대별 분석"]
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

if __name__ == "__main__":
    main()