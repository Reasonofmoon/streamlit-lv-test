# Streamlit CEFR 테스트 플랫폼 배포 안내

## 현재 Vercel 배포 현황

### 문제점
Vercel 배포 시 다음 오류가 발생했습니다:
```
Error: A Serverless Function has exceeded the unzipped maximum size of 250 MB.
```

### 원인
1. **Streamlit 아키텍처 특성**:
   - Streamlit은 WebSocket 기반의 상태 유지 애플리케이션
   - 지속적인 서버-클라이언트 연결 필요
   - Vercel은 기본적으로 서버리스 함수 배포 플랫폼

2. **Vercel 제약사항**:
   - 서버리스 함수는 250MB 제한
   - WebSocket은 Pro 계획에서만 지원
   - Streamlit과 호환성 문제

## 권장 배포 옵션

### 옵션 1: Streamlit Community Cloud (무료, 가장 권장) ⭐

**장점**:
- 완전 무료
- Streamlit 공식 호스팅
- 별도 설정 불필요
- 자동 HTTPS 지원
- 쉬운 배포

**배포 방법**:
```bash
# 1. GitHub에 코드 푸시 (완료됨)
# 2. Streamlit Community Cloud로 이동
#    https://share.streamlit.io
# 3. "New app" 클릭
# 4. GitHub 저장소 선택
# 5. app.py 메인 파일 지정
# 6. Deploy 클릭
```

**결과 URL**: `https://[username]-streamlit-lv-test.streamlit.app`

---

### 옵션 2: Railway (무료 티어 있음)

**장점**:
- Streamlit 완벽 지원
- Git 자동 배포
- PostgreSQL, Redis 지원
- 무료 티어 제공

**배포 방법**:
```bash
# 1. Railway 가입
#    https://railway.app
# 2. "New Project" → "Deploy from GitHub repo"
# 3. GitHub 저장소 연결
# 4. 환경 변수 설정:
#    - STREAMLIT_USERS
#    - PORT=8501
# 5. Deploy
```

**결과 URL**: `https://[app-name].up.railway.app`

---

### 옵션 3: Render (무료 티어 있음)

**장점**:
- Streamlit 지원
- 자동 HTTPS
- PostgreSQL 무료 제공
- Docker 지원

**배포 방법**:
```bash
# 1. Render 가입
#    https://render.com
# 2. "New Web Service"
# 3. "Build and deploy from a Git repository"
# 4. GitHub 저장소 선택
# 5. 런타임: Python 3
# 6. Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
# 7. 환경 변수 추가
# 8. Deploy
```

**결과 URL**: `https://[app-name].onrender.com`

---

### 옵션 4: Hugging Face Spaces (무료)

**장점**:
- 완전 무료
- ML 앱에 최적화
- Streamlit 완벽 지원
- GPU 옵션 (유료)

**배포 방법**:
```bash
# 1. Hugging Face 가입
#    https://huggingface.co
# 2. "Spaces" → "Create new Space"
# 3. 이름 설정
# 4. SDK: Streamlit
# 5. "Duplicate from repository"
# 6. GitHub 저장소 입력
# 7. Create Space
```

**결과 URL**: `https://huggingface.co/spaces/[username]/[space-name]`

---

## Vercel에 계속 배포하기 (권장하지 않음)

만약 Vercel에 꼭 배포해야 한다면, 다음과 같이 Streamlit을 Vercel에 맞게 수정해야 합니다:

### 필요한 변경사항
1. **서버리스 함수로 변환**: Streamlit의 상태 기반 UI를 요청-응답 기반으로 재작성
2. **WebSocket 제거**: 실시간 업데이트 기능 제거
3. **상태 관리 재설계**: 클라이언트 측 상태 관리로 변경

⚠️ **참고**: 이는 Streamlit의 주요 기능을 많이 잃게 되므로 권장하지 않습니다.

---

## 현재 추천

### 최선의 옵션: Streamlit Community Cloud

이유:
- ✅ 완전 무료
- ✅ Streamlit 공식 호스팅
- ✅ 5분 내 배포 완료
- ✅ 자동 HTTPS
- ✅ 쉬운 유지보수
- ✅ 최신 Streamlit 기능 완벽 지원

### 배포 절차 (Streamlit Community Cloud)

1. **GitHub 준비** ✅ (이미 완료됨)
   - 저장소: https://github.com/Reasonofmoon/streamlit-lv-test

2. **Streamlit Cloud 가입**
   - 웹사이트: https://share.streamlit.io
   - GitHub 계정으로 로그인

3. **새 앱 생성**
   - "New app" 버튼 클릭
   - 저장소: `streamlit-lv-test`
   - 메인 파일: `app.py`
   - 이름: `cefr-level-test` (또는 원하는 이름)

4. **환경 변수 설정**
   - Settings → Secrets
   - `STREAMLIT_USERS` 추가:
   ```toml
   STREAMLIT_USERS='{"darlbit": {"password": "darlbit123", "role": "student"}, "darlbitt": {"password": "darlbitt123", "role": "teacher"}}'
   ```

5. **배포**
   - "Deploy" 클릭
   - 2-5분 내 완료

6. **접속**
   - URL: `https://[username]-cefr-level-test.streamlit.app`

---

## 환경 변수 설정 (모든 플랫폼 공통)

```bash
# 사용자 인증 (JSON 형식)
STREAMLIT_USERS='{
  "student_id": {
    "password": "password123",
    "role": "student"
  },
  "teacher_id": {
    "password": "teacher123",
    "role": "teacher"
  }
}'

# 서버 포트
PORT=8501
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 도메인 커스터마이징

### Streamlit Community Cloud
- 무료 커스텀 도메인 지원하지 않음
- `.streamlit.app` 하위 도메인 사용

### Railway/Render
- 자체 도메인 설정 가능
- DNS CNAME 레코드 설정 필요

---

## 데이터베이스

### 현재 사용 (SQLite)
- 로컬 파일 기반 (`data/cefr_test.db`)
- 간단하지만 여러 인스턴스에서 공유 불가

### 클라우드 배포용 권장
- **Railway PostgreSQL**: 무료 티어 제공
- **Render PostgreSQL**: 무료 티어 제공
- **Supabase**: PostgreSQL 무료
- **Cloudflare D1**: SQLite 클라우드 버전 (무료)

---

## 비용 비교

| 플랫폼 | 무료 티어 | 제한사항 | 권장도 |
|---------|----------|----------|--------|
| Streamlit Community Cloud | ✅ | 넉업, 메모리 제한 | ⭐⭐⭐⭐⭐ |
| Railway | ✅ | 500시간/월 | ⭐⭐⭐⭐ |
| Render | ✅ | 750시간/월 | ⭐⭐⭐⭐ |
| Hugging Face Spaces | ✅ | 메모리 제한 | ⭐⭐⭐⭐⭐ |
| Vercel | ❌ | 서버리스 함수만 | ⭐ |

---

## 다음 단계

### 1. Streamlit Community Cloud 배포 (권장)
1. https://share.streamlit.io 접속
2. GitHub로 로그인
3. `streamlit-lv-test` 저장소 선택
4. `app.py` 선택
5. Deploy

### 2. 데이터베이스 마이그레이션 (선택)
현재 SQLite 사용 중. 클라우드 배포 시 PostgreSQL로 마이그레이션 권장.

### 3. 모니터링 설정
- 배포 후 정기적 점검
- 로그 모니터링
- 사용자 피드백 수집

---

## 도움이 필요하시면

- **Streamlit 문서**: https://docs.streamlit.io
- **Streamlit Cloud 가이드**: https://docs.streamlit.io/streamlit-cloud
- **Railway 문서**: https://docs.railway.app
- **Render 문서**: https://render.com/docs

---

**현재 상태**: GitHub에 코드는 푸시 완료됨 ✅
**권장**: Streamlit Community Cloud에 배포하여 앱 테스트 ⭐
