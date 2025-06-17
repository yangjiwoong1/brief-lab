## 디렉토리 구조
```
.
├── data/               # 데이터 저장 디렉토리
├── src/               # 소스 코드
│   ├── data_handlers/ # 데이터 처리 관련 모듈
│   ├── models/        # 모델 관련 코드
├── tests/             # 테스트 코드
└── requirements.txt   # 프로젝트 의존성
```

## 설치 방법

1. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# Windows의 경우: .\venv\Scripts\activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## Google Cloud 설정

이 프로젝트는 Google Vertex AI를 사용하므로 다음 설정이 필요합니다:

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성 또는 선택
2. Vertex AI API 활성화
3. 서비스 계정 생성 및 키 다운로드
4. 환경 변수 설정: 프로젝트 루트에 .env를 생성해주세요
```
GOOGLE_CLOUD_PROJECT=프로젝트 ID
GOOGLE_APPLICATION_CREDENTIALS = path/to/your/service-account-key.json
VERTEX_AI_LOCATION=Vertex AI API 리전
```

## 사용 방법
데이터 처리와 관련된 자세한 사용법은 `src/data_handlers` 디렉토리의 코드를 참고해주세요.