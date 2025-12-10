# CEFR English Level Test - Streamlit Version

Streamlit으로 구축된 CEFR 영어 레벨 테스트 플랫폼입니다. 학생용 시험지와 교사용 대시보드가 통합되어 있어 테스트 관리가 용이합니다.

## ✨ 주요 기능

### 📝 학생용 기능
- CEFR 레벨별 (Pre-A1, A1, A2, B1, B2) 영어 테스트
- 즉시 채점 및 결과 확인
- 상세한 피드백 제공
- 섹션별 점수 분석

### 👨‍🏫 교사용 기능
- 학생 테스트 결과 관리
- 실시간 통계 및 분석
- 다양한 필터링 및 정렬 기능
- CSV/Excel 결과 내보내기
- 종합 리포트 생성

### 📊 리포트 및 분석
- 학생별 진행 현황 추적
- 레벨별 비교 분석
- 시간대별 통계
- 다양한 차트 시각화

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd cefr-level-test
```

### 2. Python 환경 설정
```bash
# Python 3.8+ 필요
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

## 🎯 테스트 계정

- **학생 계정**: 아이디 `student`, 비밀번호 `student123`
- **교사 계정**: 아이디 `teacher`, 비밀번호 `teacher123`

## 📁 프로젝트 구조

```
cefr-level-test/
├── app.py                          # 메인 페이지
├── requirements.txt                # 의존성 패키지
├── README.md                      # 프로젝트 설명
├── assets/
│   └── styles.css                 # 스타일시트
├── pages/
│   ├── 1_📝_Student_Test.py       # 학생용 시험지
│   ├── 2_👨‍🏫_Teacher_Dashboard.py # 교사용 대시보드
│   └── 3_📊_Reports.py            # 리포트 페이지
├── utils/
│   └── data_manager.py            # 데이터 관리 유틸리티
├── data/
│   └── submissions/               # 제출 데이터 저장소
└── moon-cefr-level-test/          # 기존 HTML/JS 버전 (참고용)
```

## 🌐 Streamlit Cloud 배포

### 1. GitHub에 코드 푸시
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/cefr-level-test.git
git push -u origin main
```

### 2. Streamlit Cloud 설정
1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소, 브랜치, 메인 파일 선택:
   - Repository: `username/cefr-level-test`
   - Branch: `main`
   - Main file path: `app.py`
5. "Deploy" 클릭

### 3. 환경 변수 설정 (선택사항)
Streamlit Cloud의 Advanced settings에서 필요한 환경 변수를 설정할 수 있습니다.

## 🔧 설정 및 커스터마이징

### 1. 문제 데이터 추가
`data/questions/` 디렉토리에 각 레벨별 문제 JSON 파일을 추가합니다.

### 2. 인증 시스템 확장
`app.py`의 `login()` 함수를 수정하여 실제 데이터베이스 연동을 구현할 수 있습니다.

### 3. 스타일 수정
`assets/styles.css` 파일을 수정하여 원하는 디자인으로 변경할 수 있습니다.

## 📊 데이터 관리

### 저장 위치
- 학생 테스트 결과: `data/submissions/` (JSON 파일)
- 통계 및 분석: 자동으로 계산됨

### 데이터 백업
정기적으로 `data/` 디렉토리를 백업하세요.

### 데이터 내보내기
교사 대시보드에서 다음 형식으로 내보내기 가능:
- CSV
- JSON
- Excel
- HTML 리포트

## 🎨 기술 스택

- **Frontend**: Streamlit, HTML, CSS
- **Backend**: Python
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **File Handling**: JSON, CSV, Excel

## 🐛 문제 해결

### 일반적인 문제
1. **파일 로딩 오류**: `data/submissions/` 디렉토리 권한 확인
2. **스타일 미적용**: `assets/styles.css` 파일 경로 확인
3. **페이지 전환 오류**: `pages/` 디렉토리 파일명 형식 확인 (숫자_이모지_이름.py)

### 성능 최적화
- 대용량 데이터 처리 시 데이터 로딩 최적화
- 정기적인 오래된 파일 정리 (`utils/data_manager.py`의 `cleanup_old_files()` 함수)

## 🤝 기여하기

1. Fork 저장소
2. 기능 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면 다음 방법으로 문의하세요:
- GitHub Issues
- 이메일: your-email@example.com

## 🔄 업데이트 로그

### v1.0.0 (2024-12-10)
- 초기 Streamlit 버전 릴리스
- 학생용 테스트 기능 구현
- 교사용 대시보드 구현
- 데이터 관리 시스템 구현
- 리포트 생성 기능 구현

---

⭐ 이 프로젝트가 도움이 되셨다면 스타를 눌러주세요!