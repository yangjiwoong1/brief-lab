# Vector Database

## 폴더 이름 형식 설명

폴더 이름은 다음과 같은 형식으로 구성됩니다:
`{생성일자}_{생성시간}_{데이터종류}{데이터수}_range{기사 발행 범위}`

예시) `20250617_1741_news120_range20250617-20250617`
- `20250617`: 벡터 스토어가 생성된 날짜 (2025년 6월 17일)
- `1741`: 생성 시간 (17시 41분)
- `news120`: 뉴스 데이터 120개
- `range20250617-20250617`: 기사 발행 범위 (2025년 6월 17일부터 2025년 6월 17일까지 발행된 기사)

## 환경 변수 설정

프로젝트 루트의 [`README.md`](../../README.md#google-cloud-설정)파일을 참고하여 프로젝트 루트 디렉토리 아래 `.env`파일을 생성합니다.

## 벡터 데이터베이스 구축

프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 벡터 데이터베이스를 구축할 수 있습니다.

```bash
python -m src.data_handlers.build_vectordb
```

API로 호출하려면 다음과 같이 핸들러함수에서 main()만 호출합니다.
```python
# src/api/vector_builder.py

from fastapi import APIRouter
from src.data_handlers.build_vectordb import main

router = APIRouter()

@router.post("/build-vectordb")
def build_vectordb():
    main()
    return {"message": "벡터 DB 생성 완료"}

```

이 명령어는 현재 시각 기준 연합뉴스 RSS에서 기사를 크롤링해 제미나이 임베딩 모델(`text-multilingual-embedding-002`)로 임베딩 후, FAISS를 사용하여 벡터 DB에 저장합니다. 이 때 원본 데이터(news_items.json)도 같이 저장합니다.

