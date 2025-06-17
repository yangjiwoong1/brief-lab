# News Vector Store

뉴스 데이터를 벡터화하여 저장하고 검색하는 프로젝트입니다.

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
4. 환경 변수 설정:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

## 사용 방법

```python
from src.data_handlers.vector_store import NewsVectorStore

# 벡터 저장소 초기화
store = NewsVectorStore()
``` 