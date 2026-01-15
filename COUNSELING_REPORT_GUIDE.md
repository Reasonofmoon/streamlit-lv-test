# 개별 학생 상담 리포트 가이드

## 개요

A4 형식의 프린트 가능한 개별 학생 상담 리포트 생성 기능을 제공합니다. 이 리포트는 학생의 시험 결과를 포괄적으로 분석하고, 시각화된 도표, 상세 분석, 학습 로드맵을 포함합니다.

## 기능

### 1. 리포트 생성 (Reports 페이지)
- 교사 계정으로 로그인 후 "📊 Reports" 페이지로 이동
- "🎓 개별 학생 상담 리포트 (NEW)" 옵션 선택

### 2. 학생 선택 및 테스트 기록
- 리포트를 생성할 학생 선택
- 최근 테스트 개수 지정 (1-10개)
- 특정 테스트 기록 선택

### 3. 리포트 옵션
- 📊 **차표 포함**: 영역별 성취도 레이더 차트, 정답/오답 분포 도넛 차트
- 🔍 **상세 분석 포함**: 강점, 약점, 학습 팁 분석
- 🗺️ **학습 로드맵 포함**: 개인화된 4단계 학습 가이드
- 📝 **문항별 분석 포함**: 문항별 결과 표 및 오답 분석

## 리포트 구성

### 페이지 1: 개요 및 분석
1. **헤더**: 리포트 제목, 학생 기본 정보
2. **학생 기본 정보**: 이름, 학교, 학년/반, 시험일자, 레벨, 소요시간
3. **시험 결과 요약**:
   - 총점 (Total Score)
   - 합격/불합격 (Pass/Fail)
   - 정답률 (Accuracy)
   - 정답/전체 수
   - 성취도 등급 (수/우/미/양/가)

4. **능력 분석 도표**:
   - 레이더 차트: 영역별 성취도
   - 도넛 차트: 정답/오답 분포

5. **상세 분석**:
   - 💪 강점 분석 (Strengths)
   - ⚠️ 개선 필요 사항 (Areas for Improvement)
   - 📚 학습 팁 (Learning Tips)
   - 🎓 성과 평가 (Performance Review)

### 페이지 2: 학습 로드맵 및 문항 분석
1. **개별 학습 로드맵**: 4단계 학습 가이드
   - STEP 1: 우선 학습 영역
   - STEP 2: 일일 학습 루틴
   - STEP 3: 주간 학습 목표
   - STEP 4: 다음 단계 (다음 CEFR 레벨)

2. **문항별 상세 분석 표**:
   - 문항 번호, 문제 내용, 영역
   - 정답, 학생 답, 결과 (O/X)

3. **오답 분석** (최대 4개):
   - 오답 문항별 상세 분석
   - 문제 내용, 학생 답, 정답, 설명

4. **선생님 코멘트**:
   - 전반적인 평가
   - 학습 조언
   - 다음 상담일 작성란

5. **푸터**:
   - 생성일, 학생 ID, 테스트 레벨
   - 리포트 참조 번호

## 시각화 도표

### 1. 영역별 성취도 레이더 차트
- Reading, Vocabulary, Grammar, Writing, Listening 영역별 점수
- 100점 만점 기준
- 시각적으로 강점과 약점 파악

### 2. 정답/오답 분포 도넛 차트
- 정답 (초록색), 오답 (빨간색) 비율
- 중앙에 정답률 퍼센트 표시

## 사용 방법

### 1. 리포트 생성
```python
# utils/counseling_report_generator.py에서 제공되는 함수 사용

from utils.counseling_report_generator import generate_student_counseling_report

# 학생 정보
student_info = {
    'name': '학생ID',
    'full_name': '홍길동',
    'school': '서울고등학교',
    'grade': '1',
    'class': 'A'
}

# 테스트 결과
test_results = {
    'level': 'A1',
    'score': 85,
    'correct': 34,
    'total': 40,
    'accuracy': 85,
    'passed': True,
    'submitted_at': '2024년 12월 15일',
    'duration': '25분'
}

# 분석 결과
analysis = {
    'current_cefr_level': 'A1',
    'next_level_goal': {'level': 'A2'},
    'section_analysis': {
        'Reading': {'percentage': 80, 'correct': 8, 'total': 10},
        'Vocabulary': {'percentage': 90, 'correct': 9, 'total': 10},
        'Grammar': {'percentage': 85, 'correct': 17, 'total': 20}
    },
    'strengths': ['어휘력이 우수합니다.', '문법 기초가 탄탄합니다.'],
    'weaknesses': ['독해 속도를 높이세요.', '복잡한 문장 구조 연습이 필요합니다.'],
    'learning_curriculum': {
        'priority_areas': ['독해 속도 향상', '복잡한 문장 구조 이해'],
        'daily_practice': ['매일 20분 독해 연습', '어휘 10개 암기']
    },
    'learning_tips': ['문맥 속에서 단어 학습', '다양한 장르의 글 읽기']
}

# 상세 문항 정보
detailed_questions = [
    {
        'question': 'What is your name?',
        'options': ['A)Tom', 'B)Mary', 'C)John', 'D)Lisa'],
        'user_answer': 0,
        'correct_answer': 0,
        'is_correct': True,
        'section': 'Conversation',
        'explanation': '자기소개 질문에 대한 올바른 답변입니다.'
    }
]

# 리포트 생성
html_report = generate_student_counseling_report(
    student_info,
    test_results,
    analysis,
    detailed_questions
)

# HTML 저장
with open('report.html', 'w', encoding='utf-8') as f:
    f.write(html_report)
```

### 2. PDF로 저장
1. HTML 파일을 브라우저에서 엽니다
2. Ctrl+P (Windows) 또는 Cmd+P (Mac)로 인쇄 메뉴 엽니다
3. "대상"에서 "PDF로 저장"을 선택합니다
4. 용지 크기를 A4로 설정하고 인쇄합니다

## 디자인 특징

### A4 형식 최적화
- 페이지 크기: 210mm × 297mm
- 여백: 15mm
- 글꼴: 맑은 고딕, Malgun Gothic
- 폰트 크기: 11px (본문), 10-14px (섹션 제목, 라벨)

### 색상 스킴
- **주요 색상**:
  - 코랄 (#f5576c): 강조, 합격/불합격
  - 스카이 (#6b9ac4): 차표, 기본 정보
  - 세이지 (#27ae60): 강점, 합격 상태
  - 골드 (#f39c12): 경고, 주의

### 영역 배지
- Reading: 빨간색 (#e74c3c)
- Vocabulary: 파란색 (#3498db)
- Grammar: 초록색 (#2ecc71)
- Writing: 보라색 (#9b59b6)
- Listening: 주황색 (#f39c12)
- General: 회색 (#95a5a6)

## 성과 평가 기준

| 성과 등급 | 점수 범위 | 평가 |
|---------|----------|------|
| 수 (Excellent) | 90% 이상 | 매우 우수한 실력, 다음 레벨 도전 가능 |
| 우 (Very Good) | 80% ~ 89% | 우수한 실력, 조금만 더 노력하면 완벽 |
| 미 (Good) | 70% ~ 79% | 좋은 성과, 꾸준한 학습으로 발전 가능 |
| 양 (Fair) | 60% ~ 69% | 기본이 되어가고 있음, 보충 학습 필요 |
| 가 (Poor) | 60% 미만 | 기초부터 다시 시작, 학습법 점검 필요 |

## 기술 스택

- **템플릿 엔진**: Python f-strings
- **시각화**: Chart.js 3.9.1
- **스타일링**: CSS Grid, Flexbox
- **프린트 최적화**: CSS @media print
- **PDF 변환**: 브라우저 인쇄 기능 (별도 라이브러리 불필요)

## 사용자 지정

### 색상 변경
```python
# HTML 템플릿의 CSS 변수 수정
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --accent-color: #f39c12;
}
```

### 레이아웃 수정
```python
# Grid 구조 변경
.student-info {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;  /* 3열 */
    gap: 10px;
}
```

### 새로운 섹션 추가
```python
# HTML 템플릿에 새로운 섹션 추가
<div class="section">
    <div class="section-title">새 섹션 제목</div>
    <div class="section-content">
        섹션 내용
    </div>
</div>
```

## 트러블슈팅

### 차표가 표시되지 않음
- Chart.js CDN이 로드되었는지 확인
- 인터넷 연결 상태 확인
- 브라우저 콘솔에서 자바스크립트 오류 확인

### PDF 인쇄 시 레이아웃 깨짐
- 브라우저 인쇄 미리보기 확인
- "배경 그래픽 인쇄" 옵션 활성화
- 여백 설정 확인 (기본값: 15mm)

### 한글 깨짐 현상
- UTF-8 인코딩 확인
- 글꼴 설치 확인 (맑은 고딕, Malgun Gothic)

## 향후 개선 계획

1. **다국어 지원**: 한국어, 영어, 중국어, 일본어
2. **PDF 직접 생성**: WeasyPrint 또는 ReportLab 라이브러리 사용
3. **이메일 발송**: 생성된 리포트를 학생/학부모에게 이메일로 발송
4. **비교 리포트**: 이전 테스트와 비교한 진척도 리포트
5. **맞춤형 피드백**: AI 기반 개인화된 학습 조언 생성

## 참고 문헌

- [CEFR 공식 가이드라인](https://www.coe.int/en/web/common-european-framework-reference-languages)
- [Chart.js 문서](https://www.chartjs.org/docs/latest/)
- [CSS Grid 레이아웃](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_Grid_Layout)
