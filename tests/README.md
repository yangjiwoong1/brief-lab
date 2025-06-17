# 테스트 실행 방법

## 환경 설정

1. 프로젝트 루트 디렉토리에서 가상환경 활성화:
```bash
source venv/bin/activate  # Mac/Linux
# Windows의 경우: .\venv\Scripts\activate
```

2. 필요한 의존성 패키지 설치:
```bash
pip install -r requirements.txt
```

## 테스트 실행

### 중요: 모든 테스트는 프로젝트 루트 디렉토리에서 실행해야 합니다!
```bash
cd /path/to/brief-lab
```

### 전체 테스트 실행
```bash
pytest tests/
```

### 특정 테스트 파일 실행
```bash
pytest tests/test_search.py -s
```

### 상세한 테스트 결과 보기
```bash
pytest -v tests/
```

### 실패한 테스트의 자세한 정보 보기
```bash
pytest -vv tests/
```

## 주의사항

1. 테스트를 실행하기 전에 `.env` 파일에 필요한 환경 변수가 설정되어 있는지 확인하세요:
   - GOOGLE_CLOUD_PROJECT
   - GOOGLE_APPLICATION_CREDENTIALS = path/to/your/service-account-key.json
   - VERTEX_AI_LOCATION

2. Google Cloud API 할당량을 고려하여 테스트를 실행하세요.
   - 테스트 실행 시 임베딩 API를 호출하므로 할당량 제한에 주의