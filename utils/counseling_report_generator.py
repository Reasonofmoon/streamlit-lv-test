"""
개별 학생 상담 리포트 생성기
A4 형식의 프린트 가능한 PDF 리포트 생성
"""

from datetime import datetime
import json
import pandas as pd

def generate_student_counseling_report(student_info, test_results, analysis, detailed_questions):
    """
    개별 학생 상담용 A4 PDF 리포트 HTML 생성
    
    Args:
        student_info: 학생 정보 딕셔너리
        test_results: 시험 결과 딕셔너리
        analysis: CEFR 분석 결과 딕셔너리
        detailed_questions: 상세 문항 및 답안 정보
    
    Returns:
        str: A4 형식에 최적화된 HTML 문서
    """
    
    # 기본 정보 추출
    student_name = student_info.get('full_name', student_info.get('name', '학생'))
    student_id = student_info.get('name', '')
    school = student_info.get('school', '')
    grade = student_info.get('grade', '')
    class_name = student_info.get('class', '')
    
    test_date = test_results.get('submitted_at', datetime.now().strftime('%Y년 %m월 %d일'))
    test_level = test_results.get('level', 'A1')
    test_duration = test_results.get('duration', '0분')
    
    # 점수 정보
    total_questions = test_results.get('total', 0)
    correct_count = test_results.get('correct', 0)
    score = test_results.get('score', 0)
    accuracy = test_results.get('accuracy', 0)
    passed = test_results.get('passed', False)
    
    # CEFR 레벨
    current_cefr = analysis.get('current_cefr_level', 'Pre-A1')
    next_cefr = analysis.get('next_level_goal', {}).get('level', 'A1')
    
    # 섹션별 분석
    section_analysis = analysis.get('section_analysis', {})
    strengths = analysis.get('strengths', [])
    weaknesses = analysis.get('weaknesses', [])
    improvements = analysis.get('improvement_areas', [])
    
    # 학습 가이드
    curriculum = analysis.get('learning_curriculum', {})
    priority_areas = curriculum.get('priority_areas', [])
    daily_practice = curriculum.get('daily_practice', [])
    learning_tips = analysis.get('learning_tips', [])
    
    # 도표 데이터 생성
    radar_labels = list(section_analysis.keys()) if section_analysis else ['Reading', 'Vocabulary', 'Grammar', 'Writing', 'Listening']
    radar_data = [section_analysis.get(s, {}).get('percentage', 60) for s in radar_labels]
    
    # 문항별 상세 분석
    question_details = []
    for q in detailed_questions:
        question_details.append({
            'question': q.get('question', ''),
            'options': q.get('options', []),
            'user_answer': q.get('user_answer', -1),
            'correct_answer': q.get('correct', 0),
            'is_correct': q.get('is_correct', False),
            'section': q.get('section', 'General'),
            'explanation': q.get('explanation', '')
        })
    
    # 오답 분석
    incorrect_questions = [q for q in question_details if not q['is_correct']]
    
    # 성과 평가
    if accuracy >= 90:
        performance_grade = '수'
        performance_comment = '매우 우수한 실력을 보여주었습니다. 다음 레벨로 도전할 준비가 되었습니다.'
    elif accuracy >= 80:
        performance_grade = '우'
        performance_comment = '우수한 실력입니다. 조금만 더 노력하면 완벽해질 것입니다.'
    elif accuracy >= 70:
        performance_grade = '미'
        performance_comment = '좋은 성과입니다. 꾸준한 학습으로 더 발전할 수 있습니다.'
    elif accuracy >= 60:
        performance_grade = '양'
        performance_comment = '기본이 되어가고 있습니다. 집중적인 보충 학습이 필요합니다.'
    else:
        performance_grade = '가'
        performance_comment = '기초부터 다시 시작해야 합니다. 학습법 점검이 필요합니다.'
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>개별 학생 상담 리포트 - {student_name}</title>
    <style>
        @page {{
            size: A4;
            margin: 15mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: '맑은 고딕', 'Malgun Gothic', 'Apple Gothic', sans-serif;
            font-size: 11px;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}
        
        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            padding: 15mm;
            background: #fff;
            page-break-after: always;
        }}
        
        .header {{
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .header-title {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .header-subtitle {{
            font-size: 14px;
            color: #7f8c8d;
        }}
        
        .section {{
            margin-bottom: 20px;
        }}
        
        .section-title {{
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            background: #ecf0f1;
            padding: 8px 12px;
            margin-bottom: 12px;
            border-left: 4px solid #3498db;
        }}
        
        .student-info {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .info-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .info-label {{
            font-weight: bold;
            color: #7f8c8d;
            font-size: 10px;
            margin-bottom: 3px;
        }}
        
        .info-value {{
            font-size: 12px;
            color: #2c3e50;
        }}
        
        .score-overview {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .score-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .score-box.large {{
            grid-column: span 2;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .score-box.pass {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .score-box.fail {{
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }}
        
        .score-value {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .score-label {{
            font-size: 10px;
            opacity: 0.9;
        }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .chart-box {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background: #fafafa;
        }}
        
        .chart-title {{
            font-size: 12px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        .chart-placeholder {{
            height: 180px;
            background: #ecf0f1;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
        
        .analysis-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .analysis-box {{
            border-radius: 8px;
            padding: 15px;
        }}
        
        .analysis-box.strength {{
            background: #d5f4e6;
            border-left: 4px solid #27ae60;
        }}
        
        .analysis-box.weakness {{
            background: #ffeaa7;
            border-left: 4px solid #e74c3c;
        }}
        
        .analysis-box.tips {{
            background: #dfe6e9;
            border-left: 4px solid #3498db;
        }}
        
        .analysis-title {{
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 12px;
        }}
        
        .analysis-content {{
            font-size: 11px;
            line-height: 1.8;
        }}
        
        .analysis-content ul {{
            list-style-position: inside;
            padding-left: 5px;
        }}
        
        .analysis-content li {{
            margin-bottom: 5px;
        }}
        
        .roadmap {{
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .roadmap-item {{
            display: flex;
            align-items: flex-start;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px dashed #ddd;
        }}
        
        .roadmap-item:last-child {{
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }}
        
        .roadmap-number {{
            background: #3498db;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
            margin-right: 12px;
            flex-shrink: 0;
        }}
        
        .roadmap-content {{
            flex: 1;
        }}
        
        .roadmap-title {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 3px;
        }}
        
        .roadmap-desc {{
            color: #7f8c8d;
            font-size: 10px;
        }}
        
        .questions-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 10px;
        }}
        
        .questions-table th,
        .questions-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        
        .questions-table th {{
            background: #2c3e50;
            color: white;
            font-weight: bold;
        }}
        
        .questions-table tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        .status-correct {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        .status-incorrect {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .teacher-comments {{
            background: #fff9c4;
            border: 2px dashed #f39c12;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        .teacher-comments h4 {{
            color: #f39c12;
            margin-bottom: 10px;
        }}
        
        .footer {{
            border-top: 2px solid #2c3e50;
            padding-top: 10px;
            margin-top: 20px;
            text-align: center;
            color: #7f8c8d;
            font-size: 10px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: bold;
            margin-right: 5px;
        }}
        
        .badge-reading {{ background: #e74c3c; color: white; }}
        .badge-vocabulary {{ background: #3498db; color: white; }}
        .badge-grammar {{ background: #2ecc71; color: white; }}
        .badge-writing {{ background: #9b59b6; color: white; }}
        .badge-listening {{ background: #f39c12; color: white; }}
        .badge-general {{ background: #95a5a6; color: white; }}
        
        @media print {{
            body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .page {{ page-break-after: always; }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <!-- 페이지 1: 개요 및 분석 -->
        <div class="header">
            <div class="header-title">🎓 CEFR 개별 학생 상담 리포트</div>
            <div class="header-subtitle">Comprehensive English Proficiency Assessment & Counseling Report</div>
        </div>
        
        <div class="section">
            <div class="section-title">📋 학생 기본 정보 (Student Information)</div>
            <div class="student-info">
                <div class="info-item">
                    <span class="info-label">이름 (Name)</span>
                    <span class="info-value">{student_name}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">학교 (School)</span>
                    <span class="info-value">{school or '-'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">학년/반 (Grade/Class)</span>
                    <span class="info-value">{grade or '-'}학년 {class_name or '-'}반</span>
                </div>
                <div class="info-item">
                    <span class="info-label">시험일자 (Test Date)</span>
                    <span class="info-value">{test_date}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">시험레벨 (Test Level)</span>
                    <span class="info-value">{test_level}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">소요시간 (Duration)</span>
                    <span class="info-value">{test_duration}</span>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📊 시험 결과 요약 (Test Results Summary)</div>
            <div class="score-overview">
                <div class="score-box large">
                    <div class="score-value">{score}점</div>
                    <div class="score-label">총점 (Total Score)</div>
                </div>
                <div class="score-box {'pass' if passed else 'fail'}">
                    <div class="score-value">{'합격' if passed else '불합격'}</div>
                    <div class="score-label">Pass/Fail</div>
                </div>
                <div class="score-box">
                    <div class="score-value">{accuracy}%</div>
                    <div class="score-label">정답률 (Accuracy)</div>
                </div>
                <div class="score-box">
                    <div class="score-value">{correct_count}/{total_questions}</div>
                    <div class="score-label">정답/전체</div>
                </div>
                <div class="score-box">
                    <div class="score-value">{performance_grade}</div>
                    <div class="score-label">성취도 (Grade)</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📈 능력 분석 도표 (Proficiency Charts)</div>
            <div class="charts-container">
                <div class="chart-box">
                    <div class="chart-title">영역별 성취도 (Section Performance)</div>
                    <canvas id="radarChart" width="400" height="200"></canvas>
                </div>
                <div class="chart-box">
                    <div class="chart-title">정답/오답 분포 (Answer Distribution)</div>
                    <canvas id="doughnutChart" width="400" height="200"></canvas>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">🎯 상세 분석 (Detailed Analysis)</div>
            <div class="analysis-grid">
                <div class="analysis-box strength">
                    <div class="analysis-title">💪 강점 분석 (Strengths)</div>
                    <div class="analysis-content">
                        <ul>
                            {"".join([f"<li>{s}</li>" for s in (strengths if strengths else ["학습 의지가 보입니다", "꾸준한 연습으로 발전 가능합니다"])])}
                        </ul>
                    </div>
                </div>
                
                <div class="analysis-box weakness">
                    <div class="analysis-title">⚠️ 개선 필요 사항 (Areas for Improvement)</div>
                    <div class="analysis-content">
                        <ul>
                            {"".join([f"<li>{w}</li>" for w in (weaknesses if weaknesses else improvements if improvements else ["기초 학습이 필요합니다", "정답 전략 점검이 필요합니다"])])}
                        </ul>
                    </div>
                </div>
                
                <div class="analysis-box tips">
                    <div class="analysis-title">📚 학습 팁 (Learning Tips)</div>
                    <div class="analysis-content">
                        <ul>
                            {"".join([f"<li>{t}</li>" for t in (learning_tips if learning_tips else ["매일 30분씩 꾸준히 학습하세요", "오답 노트 작성을 권장합니다"])])}
                        </ul>
                    </div>
                </div>
                
                <div class="analysis-box tips">
                    <div class="analysis-title">🎓 성과 평가 (Performance Review)</div>
                    <div class="analysis-content">
                        <p><strong>현재 CEFR 레벨:</strong> {current_cefr}</p>
                        <p><strong>목표 CEFR 레벨:</strong> {next_cefr}</p>
                        <p style="margin-top: 10px; font-style: italic;">"{performance_comment}"</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="page">
        <!-- 페이지 2: 학습 로드맵 및 문항 분석 -->
        <div class="header">
            <div class="header-title">🎓 개별 학습 로드맵 (Personalized Learning Roadmap)</div>
            <div class="header-subtitle">Step-by-Step Learning Guide</div>
        </div>
        
        <div class="section">
            <div class="roadmap">
                <div class="roadmap-item">
                    <div class="roadmap-number">1</div>
                    <div class="roadmap-content">
                        <div class="roadmap-title">우선 학습 영역 (Priority Focus)</div>
                        <div class="roadmap-desc">
                            {priority_areas[0] if priority_areas else "현재 레벨에 맞는 기초 학습에 집중하세요."}
                        </div>
                    </div>
                </div>
                
                <div class="roadmap-item">
                    <div class="roadmap-number">2</div>
                    <div class="roadmap-content">
                        <div class="roadmap-title">일일 학습 루틴 (Daily Practice)</div>
                        <div class="roadmap-desc">
                            {daily_practice[0] if daily_practice else "매일 30분씩 꾸준히 학습하세요. 아침/저녁으로 나누어 학습하면 효과적입니다."}
                        </div>
                    </div>
                </div>
                
                <div class="roadmap-item">
                    <div class="roadmap-number">3</div>
                    <div class="roadmap-content">
                        <div class="roadmap-title">주간 학습 목표 (Weekly Goals)</div>
                        <div class="roadmap-desc">
                            매주 새로운 어휘 20개 암기, 문법 포인트 3개 마스터, 짧은 글 읽기 5편 완료
                        </div>
                    </div>
                </div>
                
                <div class="roadmap-item">
                    <div class="roadmap-number">4</div>
                    <div class="roadmap-content">
                        <div class="roadmap-title">다음 단계 (Next Level)</div>
                        <div class="roadmap-desc">
                            CEFR {current_cefr} → {next_cefr} 레벨 도달을 목표로 3-6개월간 체계적인 학습 계획을 세웁니다.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📝 문항별 상세 분석 (Question-by-Question Analysis)</div>
            <table class="questions-table">
                <thead>
                    <tr>
                        <th width="5%">No</th>
                        <th width="30%">문항 (Question)</th>
                        <th width="10%">영역</th>
                        <th width="15%">정답</th>
                        <th width="15%">학생답</th>
                        <th width="10%">결과</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f"""
                    <tr>
                        <td>{i+1}</td>
                        <td>{q['question'][:50]}{'...' if len(q['question']) > 50 else ''}</td>
                        <td><span class="badge badge-{q['section'].lower()}">{q['section']}</span></td>
                        <td>{['A','B','C','D'][q['correct_answer']] if q['correct_answer'] >= 0 else '-'}</td>
                        <td>{['A','B','C','D'][q['user_answer']] if q['user_answer'] >= 0 else '-'}</td>
                        <td class="{'status-correct' if q['is_correct'] else 'status-incorrect'}">
                            {'O' if q['is_correct'] else 'X'}
                        </td>
                    </tr>
                    """ for i, q in enumerate(question_details[:15])])}
                </tbody>
            </table>
            
            {f'<p style="margin-top: 10px; text-align: center; color: #7f8c8d;">※ 총 {len(question_details)}문항 중 15문항만 표시 (상세 내용은 별도 파일 참조)</p>' if len(question_details) > 15 else ''}
        </div>
        
        {f'''
        <div class="section">
            <div class="section-title">❌ 오답 분석 (Incorrect Answers Analysis)</div>
            <div class="analysis-grid">
                {"".join([f"""
                <div class="analysis-box weakness">
                    <div class="analysis-title">오답 문항 #{i+1} ({q['section']})</div>
                    <div class="analysis-content">
                        <p style="margin-bottom: 5px;"><strong>문제:</strong> {q['question'][:80]}{'...' if len(q['question']) > 80 else ''}</p>
                        <p style="margin-bottom: 5px;"><strong>학생 답:</strong> {['A','B','C','D'][q['user_answer']] if q['user_answer'] >= 0 else '미응답'}</p>
                        <p style="margin-bottom: 5px;"><strong>정답:</strong> {['A','B','C','D'][q['correct_answer']] if q['correct_answer'] >= 0 else '-'}</p>
                        <p style="color: #e74c3c; font-style: italic;">{q['explanation'] if q['explanation'] else '정답을 선택하지 못했습니다.'}</p>
                    </div>
                </div>
                """ for i, q in enumerate(incorrect_questions[:4])])}
            </div>
        </div>
        ''' if incorrect_questions else ''}
        
        <div class="section">
            <div class="teacher-comments">
                <h4>👨‍🏫 선생님 코멘트 (Teacher's Comments)</h4>
                <div class="analysis-content">
                    <p><strong>전반적인 평가:</strong> {performance_comment}</p>
                    <p style="margin-top: 10px;"><strong>학습 조언:</strong></p>
                    <ul>
                        {"".join([f"<li>{daily_practice[i] if i < len(daily_practice) else '꾸준한 학습이 중요합니다.'}</li>" for i in range(3)])}
                    </ul>
                    <p style="margin-top: 10px; color: #2c3e50;"><strong>다음 상담일:</strong> _________ 년 _______ 월 _______ 일</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>📄 CEFR 개별 학생 상담 리포트 | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p>Student ID: {student_id} | Test Level: {test_level} | Report Ref: {datetime.now().strftime('%Y%m%d')}-{student_name.replace(' ', '')}</p>
            <p style="margin-top: 5px;">© 2024 CEFR Test Platform. All rights reserved.</p>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
        // 레이더 차트 (영역별 성취도)
        const radarCtx = document.getElementById('radarChart');
        new Chart(radarCtx, {{
            type: 'radar',
            data: {{
                labels: {json.dumps(radar_labels)},
                datasets: [{{
                    label: '현재 성취도',
                    data: {json.dumps(radar_data)},
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    borderColor: '#3498db',
                    pointBackgroundColor: '#3498db',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#3498db'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    r: {{
                        angleLines: {{ color: 'rgba(0, 0, 0, 0.1)' }},
                        grid: {{ color: 'rgba(0, 0, 0, 0.1)' }},
                        pointLabels: {{
                            font: {{ size: 10 }},
                            color: '#333'
                        }},
                        ticks: {{
                            display: false,
                            max: 100
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // 도넛 차트 (정답/오답 분포)
        const doughnutCtx = document.getElementById('doughnutChart');
        new Chart(doughnutCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['정답 (Correct)', '오답 (Incorrect)'],
                datasets: [{{
                    data: [{accuracy}, {100-accuracy}],
                    backgroundColor: ['#27ae60', '#e74c3c'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                cutout: '60%',
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            font: {{ size: 10 }},
                            padding: 10
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html_content


def generate_printable_report_html(student_info, test_results, analysis, detailed_questions):
    """
    프린트 가능한 단일 페이지 HTML 리포트 생성
    """
    html = generate_student_counseling_report(student_info, test_results, analysis, detailed_questions)
    return html


def save_report_as_html(html_content, filename):
    """
    HTML 리포트를 파일로 저장
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return filename
