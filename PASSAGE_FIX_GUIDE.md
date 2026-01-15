# 문제와 지문 연결 문제 해결 가이드

## 문제 상황
기존 시스템에서 **모든 문제**에 지문이 연결되는 문제가 발생했습니다. 예를 들어:
- Grammar 문제 ("My name _____ Alex.") → 지문 표시됨 (잘못됨)
- Vocabulary 문제 ("What color is the sky?") → 지문 표시됨 (잘못됨)

## 근본 원인
1. **잘못된 섹션 분류**: `extracted_questions.json`에서 모든 문제가 `"section": "Reading"`으로 저장됨
2. **하드코딩된 ID 기반 지문 연결**: `1_Student_Test.py`에서 특정 ID(1-8번)의 문제에 무조건 지문을 연결
3. **결과**: 모든 문제가 Reading으로 분류되어 있으므로 → 모든 문제에 지문이 연결됨

## 해결 방법

### 1단계: 섹션 분류 수정
`fix_question_sections.py` 스크립트 실행:
```bash
python fix_question_sections.py
```

**작동 방식:**
- 문제 텍스트를 분석하여 적절한 섹션으로 재분류
- Conversation: "say when", "best response", "A:", "B:" 포함
- Grammar: "\_\_\_\_\_\_\_" (빈칸) 포함
- Vocabulary: "color", "opposite", "number" 등 키워드 포함
- Reading: 실제로 지문 기반 질문만 (where, what, who, when, how 질문)

**결과:**
- 총 183개 문제 중 121개의 섹션 수정
- PRE-A1: 25개 → Reading 1개만 남음
- A1: 34개 → Reading 8개 (실제 지문 기반 질문)
- A2: 40개 → Reading 5개
- B1: 42개 → Reading 3개
- B2: 42개 → Reading 13개

### 2단계: 코드 로직 개선
`1_Student_Test.py` 수정:

**이전 로직:**
```python
# 모든 문제의 ID만 보고 지문 연결
if q_id in [1, 2]:
    question['passage'] = passages[1]
```

**개선된 로직:**
```python
# Reading 섹션 + passage 필드가 없을 때만 fallback 지문 연결
if question.get('section') == 'Reading' and 'passage' not in question:
    if q_id in [1, 2]:
        question['passage'] = passages[1]
```

**개선 사항:**
1. JSON에 `passage` 필드가 있으면 그것을 우선 사용
2. 섹션이 'Reading'인 경우에만 지문 연결
3. ID 기반 지문 연결은 fallback으로만 사용

### 3단계: 데이터 흐름
```
HTML 파일 (원본)
    ↓
extract_questions_with_passages.py (지문 추출)
    ↓
extracted_questions.json (passage 필드 포함)
    ↓
fix_question_sections.py (섹션 재분류)
    ↓
1_Student_Test.py (JSON 로드 + 필요시 fallback 지문 연결)
    ↓
사용자에게 표시
```

## 결과

### 이제 정상 작동:
- **Reading 문제만** 지문이 표시됨
- **Grammar, Vocabulary, Conversation 문제**에는 지문이 표시되지 않음
- 각 레벨별로 적절한 문제 수의 지문만 연결됨

### 레벨별 Reading 문제 및 지문:
- **A1 (8문제)**:
  - Q1-2: Mia의 편지 지문 공유
  - Q3-4: Henry와 Mudge의 캠핑 지문 공유
  - Q5-8: Nate the Detective 지문 공유

## 향후 개선 사항

### 1. HTML 파일에서 실제 지문 추출
현재는 하드코딩된 3개의 지문만 사용 중입니다. 실제 HTML 파일이 있다면:
1. `extract_questions_with_passages.py`를 실행하여 지문 추출
2. JSON에 `passage` 필드가 자동으로 포함됨
3. 각 레벨별로 고유한 지문 사용 가능

### 2. 지문 데이터베이스 구축
```python
# passages.json
{
  "PRE-A1": {
    "passage_1": {"text": "...", "questions": [1, 2]},
    "passage_2": {"text": "...", "questions": [3, 4]}
  },
  "A1": {
    "passage_1": {"text": "Mia's letter...", "questions": [1, 2]},
    "passage_2": {"text": "Henry camping...", "questions": [3, 4]},
    "passage_3": {"text": "Nate detective...", "questions": [5, 6, 7, 8]}
  }
}
```

### 3. 관리자 인터페이스
- 지문 업로드/수정 기능
- 문제-지문 연결 관리
- 섹션 자동 분류 검증

## 테스트 체크리스트
- [ ] A1 Reading 문제 1-2번에 Mia 지문 표시됨
- [ ] A1 Reading 문제 3-4번에 Henry 지문 표시됨
- [ ] A1 Reading 문제 5-8번에 Nate 지문 표시됨
- [ ] A1 Grammar 문제에 지문이 표시되지 않음
- [ ] A1 Vocabulary 문제에 지문이 표시되지 않음
- [ ] A1 Conversation 문제에 지문이 표시되지 않음
- [ ] 다른 레벨(PRE-A1, A2, B1, B2)도 동일하게 작동

## 관련 파일
- `fix_question_sections.py` - 섹션 재분류 스크립트
- `pages/1_Student_Test.py` - 문제 로딩 및 지문 연결 로직
- `extracted_questions.json` - 문제 데이터 (수정됨)
- `extract_questions_with_passages.py` - HTML에서 지문 추출 (HTML 파일 필요)

## 문의
문제가 계속 발생하면:
1. `extracted_questions.json`에서 해당 문제의 `section` 필드 확인
2. `1_Student_Test.py`의 지문 연결 로직 확인
3. 콘솔에 디버그 메시지 출력하여 확인
