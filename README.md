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

이 프로젝트는 RAG 구축을 위한 임베딩 모델과 LLM에 Google Vertex AI를 사용하므로 다음 설정이 필요합니다:

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성 또는 선택
2. Vertex AI API 활성화
3. 서비스 계정 생성 및 키 다운로드(Vertex AI에 대한 권한이 있어야 함)
4. 환경 변수 설정: 프로젝트 루트에 .env를 생성
```
GOOGLE_CLOUD_PROJECT=프로젝트 ID
GOOGLE_APPLICATION_CREDENTIALS = path/to/your/service-account-key.json
VERTEX_AI_LOCATION=Vertex AI API 리전
```

## 사용 방법
데이터 처리와 관련된 자세한 사용법은 `src/data_handlers` 디렉토리의 코드를 참고해주세요.

### API 서버 실행
```
# 로컬 환경에서 grok 없이 실행하는 경우 
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 클라우드나 로컬에서 grok 서비스를 사용하는 경우
python run_colab_server.py
```
#### API 서버 실행 관련 설정
```
# .env 에 추가
LATEST_DIR_PATH=your_save_path    # summarizer 의 VECTOR_DB_PATH 와 같은 디렉토리로 설정
NGROK_AUTH_TOKEN=your_ngrok_token
```
