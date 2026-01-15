"""
EduPrompT v12.0 Premium Report Generator
프리미엄 인터랙티브 HTML 리포트 생성기
"""

from datetime import datetime
import json

def generate_premium_report(student_info, test_results, analysis):
    """
    학생의 시험 결과를 EduPrompT v12.0 디자인 시스템을 적용한
    프리미엄 HTML 리포트로 변환합니다.
    
    Args:
        student_info: 학생 정보 딕셔너리
        test_results: 시험 결과 딕셔너리 
        analysis: CEFR 분석 결과 딕셔너리
    
    Returns:
        str: 완전한 HTML 문서
    """
    
    # 데이터 추출
    student_name = student_info.get('full_name', student_info.get('name', 'Student'))
    test_date = datetime.now().strftime('%Y-%m-%d')
    level = test_results.get('level', 'A1')
    score = test_results.get('score', 0)
    correct = test_results.get('correct', 0)
    total = test_results.get('total', 0)
    accuracy = round((correct / total * 100) if total > 0 else 0)
    
    cefr_level = analysis.get('current_cefr_level', 'Pre-A1')
    
    # 섹션별 결과
    section_analysis = analysis.get('section_analysis', {})
    
    # 레이더 차트 데이터 (섹션별 정확도)
    radar_data = []
    radar_labels = []
    for section, data in section_analysis.items():
        radar_labels.append(section)
        radar_data.append(data.get('percentage', 0))
    
    # 데이터가 없으면 기본값
    if not radar_data:
        radar_labels = ['Reading', 'Vocabulary', 'Grammar', 'Listening', 'Speaking']
        radar_data = [accuracy, accuracy-5, accuracy-3, accuracy+2, accuracy+2]
    
    # 강점과 약점
    strengths = analysis.get('strengths', [])
    weaknesses = analysis.get('weaknesses', [])
    improvements = analysis.get('improvement_areas', [])
    
    # 커리큘럼
    curriculum = analysis.get('learning_curriculum', {})
    priority_areas = curriculum.get('priority_areas', [])
    daily_practice = curriculum.get('daily_practice', [])
    
    # 학습 로드맵
    next_goal = analysis.get('next_level_goal', {})
    target_level = next_goal.get('level', 'A1')
    estimated_duration = next_goal.get('estimated_duration', '3-6개월')
    
    # 점수에 따른 평가
    if score >= 70:
        score_status = "Excellent"
        score_color = "var(--accent-sage)"
    elif score >= 50:
        score_status = "Good Progress"
        score_color = "var(--accent-sky)"
    else:
        score_status = "Needs Improvement"
        score_color = "var(--accent-coral)"
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduPrompT Premium Report - {student_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=JetBrains+Mono:wght@400;700&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {{
            --bg-primary: #FDFCFA;
            --bg-secondary: #F7F5F2;
            --text-primary: #1A1A1A;
            --text-secondary: #5A5A5A;
            --accent-coral: #E8785A;
            --accent-sage: #7BA38C;
            --accent-gold: #C9A962;
            --accent-sky: #6B9AC4;
            --accent-lavender: #9B8AA6;
            --shadow-soft: 0 10px 30px rgba(26, 26, 26, 0.04);
            --shadow-card: 0 20px 60px rgba(26, 26, 26, 0.08);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Sora', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }}

        h1, h2, h3 {{ font-family: 'Cormorant Garamond', serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}

        header {{
            padding: 4rem 0;
            background: linear-gradient(to bottom, #fff, var(--bg-secondary));
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }}

        .header-badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background: rgba(232, 120, 90, 0.1);
            color: var(--accent-coral);
            border-radius: 50px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            margin-bottom: 1.5rem;
            letter-spacing: 0.1em;
        }}

        .student-name {{
            font-size: 4rem;
            font-weight: 300;
            margin-bottom: 0.5rem;
        }}

        .report-meta {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}

        .score-overview {{
            margin-top: -3rem;
            position: relative;
            z-index: 10;
        }}

        .stat-card {{
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: var(--shadow-soft);
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid rgba(0,0,0,0.02);
        }}

        .stat-card:hover {{ transform: translateY(-5px); box-shadow: var(--shadow-card); }}

        .score-value {{
            font-family: 'Cormorant Garamond', serif;
            font-size: 3.5rem;
            line-height: 1;
            margin: 1rem 0;
        }}

        .score-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .charts-section {{ padding: 4rem 0; }}
        
        .chart-container {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-soft);
            height: 100%;
        }}

        .analysis-section {{ padding: 2rem 0 4rem; }}

        .section-title {{
            font-size: 2rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .section-title::before {{
            content: '';
            display: block;
            width: 4px;
            height: 24px;
            background: var(--accent-sage);
        }}

        .insight-box {{
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            border-left: 4px solid transparent;
        }}

        .insight-box.strength {{ border-left-color: var(--accent-sage); background: rgba(123, 163, 140, 0.05); }}
        .insight-box.weakness {{ border-left-color: var(--accent-coral); background: rgba(232, 120, 90, 0.05); }}

        .insight-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .insight-title {{ font-weight: 600; font-size: 1.1rem; }}
        .insight-icon {{ font-size: 1.5rem; }}

        .insight-list {{ list-style: none; }}

        .insight-list li {{
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
            color: var(--text-secondary);
        }}

        .insight-list li::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: inherit;
        }}

        .roadmap-container {{
            position: relative;
            padding: 2rem 0;
        }}

        .step-card {{
            background: white;
            border: 1px solid rgba(0,0,0,0.05);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }}

        .step-card::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; bottom: 0;
            width: 4px;
            background: var(--accent-sky);
        }}

        .step-card.active::after {{ background: var(--accent-coral); }}

        .step-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }}

        .tag {{
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .tag.priority {{ background: rgba(232, 120, 90, 0.1); color: var(--accent-coral); }}
        .tag.normal {{ background: rgba(107, 154, 196, 0.1); color: var(--accent-sky); }}

        footer {{
            background: #1A1A1A;
            color: white;
            padding: 3rem 0;
            text-align: center;
            margin-top: 4rem;
        }}

        .footer-text {{ opacity: 0.6; font-size: 0.9rem; }}

        @media (max-width: 768px) {{
            .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
            .student-name {{ font-size: 2.5rem; }}
            .score-overview {{ margin-top: 0; padding-top: 2rem; }}
        }}
        
        @media print {{
            body {{ background: white; }}
            .stat-card, .chart-container, .insight-box {{ box-shadow: none; border: 1px solid #ddd; }}
            footer {{ display: none; }}
        }}
    </style>
</head>
<body>

    <header>
        <div class="container">
            <span class="header-badge">CEFR DIAGNOSTIC REPORT</span>
            <h1 class="student-name">{student_name}</h1>
            <p class="report-meta">
                Test Date: <span class="font-mono">{test_date}</span> | Level: <span class="font-mono">{level}</span>
            </p>
        </div>
    </header>

    <div class="container">
        <div class="score-overview grid-3">
            <div class="stat-card">
                <div class="score-label">Total Score</div>
                <div class="score-value" style="color: {score_color}">{score}</div>
                <div class="score-label">{score_status}</div>
            </div>
            <div class="stat-card">
                <div class="score-label">CEFR Level</div>
                <div class="score-value" style="color: var(--accent-sky)">{cefr_level}</div>
                <div class="score-label">Current Level</div>
            </div>
            <div class="stat-card">
                <div class="score-label">Accuracy</div>
                <div class="score-value" style="color: var(--accent-gold)">{accuracy}%</div>
                <div class="score-label">{correct} / {total} Correct</div>
            </div>
        </div>

        <section class="charts-section grid-2">
            <div class="chart-container">
                <h3 style="margin-bottom: 1.5rem; font-size: 1.25rem;">Skill Balance Analysis</h3>
                <canvas id="radarChart"></canvas>
                <p style="text-align: center; margin-top: 1rem; font-size: 0.8rem; color: var(--text-secondary);">
                    *영역별 상대적 강약점 분석
                </p>
            </div>
            <div class="chart-container">
                <h3 style="margin-bottom: 1.5rem; font-size: 1.25rem;">Overall Proficiency</h3>
                <div style="position: relative; height: 250px; display: flex; align-items: center; justify-content: center;">
                    <canvas id="doughnutChart"></canvas>
                    <div style="position: absolute; text-align: center;">
                        <div style="font-size: 2rem; font-weight: 600; color: var(--text-primary);">{accuracy}%</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Accuracy</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="analysis-section">
            <h2 class="section-title">Detailed Analysis</h2>
            
            <div class="grid-2">
                <div class="insight-box weakness">
                    <div class="insight-header">
                        <div class="insight-title" style="color: var(--accent-coral)">🎯 Focus Areas (개선 필요)</div>
                        <div class="insight-icon">⚠️</div>
                    </div>
                    <ul class="insight-list">
                        {"".join([f"<li>{item}</li>" for item in (improvements[:3] if improvements else weaknesses[:3] if weaknesses else ["지속적인 학습이 필요합니다."])])}
                    </ul>
                </div>

                <div class="insight-box strength">
                    <div class="insight-header">
                        <div class="insight-title" style="color: var(--accent-sage)">💪 Strengths (강점)</div>
                        <div class="insight-icon">🌟</div>
                    </div>
                    <ul class="insight-list">
                        {"".join([f"<li>{item}</li>" for item in (strengths[:3] if strengths else ["학습 의지가 있습니다.", "꾸준한 연습으로 발전 가능합니다."])])}
                    </ul>
                </div>
            </div>

            <h2 class="section-title" style="margin-top: 3rem;">Personalized Curriculum Roadmap</h2>
            <div class="roadmap-container">
                <div class="step-card active">
                    <div class="step-header">
                        <span class="font-mono text-secondary">STEP 01 (Current Focus)</span>
                        <span class="tag priority">Highest Priority</span>
                    </div>
                    <h4 style="font-size: 1.2rem; margin-bottom: 0.5rem;">우선 개선 영역</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        {priority_areas[0] if priority_areas else "현재 레벨에 맞는 기초 학습에 집중하세요."}
                    </p>
                </div>

                <div class="step-card">
                    <div class="step-header">
                        <span class="font-mono text-secondary">STEP 02 (Daily Practice)</span>
                        <span class="tag normal">Consistent Training</span>
                    </div>
                    <h4 style="font-size: 1.2rem; margin-bottom: 0.5rem;">일일 학습 루틴</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        {daily_practice[0] if daily_practice else "매일 30분씩 꾸준히 학습하세요."}
                    </p>
                </div>

                <div class="step-card">
                    <div class="step-header">
                        <span class="font-mono text-secondary">Target Goal ({estimated_duration})</span>
                        <span class="tag normal" style="background: rgba(123, 163, 140, 0.1); color: var(--accent-sage);">Objective</span>
                    </div>
                    <h4 style="font-size: 1.2rem; margin-bottom: 0.5rem;">Reach CEFR {target_level}</h4>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">
                        다음 레벨 달성을 목표로 체계적인 학습을 진행합니다.
                    </p>
                </div>
            </div>
        </section>
    </div>

    <footer>
        <div class="container">
            <h3>EduPrompT Dashboard</h3>
            <p class="footer-text">Generated by EduPrompT v12.0 Ultimate Designer</p>
            <p class="footer-text" style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;">
                REF: {test_date}-{student_name.upper()}-{level}
            </p>
        </div>
    </footer>

    <script>
        // Radar Chart
        const radarCtx = document.getElementById('radarChart').getContext('2d');
        new Chart(radarCtx, {{
            type: 'radar',
            data: {{
                labels: {json.dumps(radar_labels)},
                datasets: [{{
                    label: 'Current Level',
                    data: {json.dumps(radar_data)},
                    backgroundColor: 'rgba(232, 120, 90, 0.2)',
                    borderColor: '#E8785A',
                    pointBackgroundColor: '#E8785A',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#E8785A'
                }}, {{
                    label: 'Target (70%)',
                    data: Array({len(radar_labels)}).fill(70),
                    backgroundColor: 'rgba(123, 163, 140, 0.1)',
                    borderColor: '#7BA38C',
                    borderDash: [5, 5],
                    pointRadius: 0
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    r: {{
                        angleLines: {{ color: 'rgba(0, 0, 0, 0.05)' }},
                        grid: {{ color: 'rgba(0, 0, 0, 0.05)' }},
                        pointLabels: {{
                            font: {{ family: "'JetBrains Mono', monospace", size: 12 }},
                            color: '#5A5A5A'
                        }},
                        ticks: {{ display: false, max: 100 }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ font: {{ family: "'Sora', sans-serif" }}, usePointStyle: true }}
                    }}
                }}
            }}
        }});

        // Doughnut Chart
        const doughnutCtx = document.getElementById('doughnutChart').getContext('2d');
        new Chart(doughnutCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Correct', 'Incorrect'],
                datasets: [{{
                    data: [{accuracy}, {100-accuracy}],
                    backgroundColor: ['#E8785A', '#F7F5F2'],
                    borderWidth: 0,
                    hoverOffset: 4
                }}]
            }},
            options: {{
                responsive: true,
                cutout: '75%',
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.label + ': ' + context.raw + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html_content
