# 뉴스 벡터 스토어 사용 가이드

## 1. 기본 검색 사용하기
```python
from src.data_handlers.vector_store import NewsVectorStore

# 벡터 스토어 인스턴스 생성 및 로드
news_store = NewsVectorStore()
news_store.load("data/vector_store/[최신_날짜_디렉토리]") # 경로 주의

# 검색 예시
results = news_store.search_similar(
    query="검색하고 싶은 내용",
    k=3  # 원하는 결과 개수
)

# 결과 사용하기
for result in results:
    print(f"제목: {result['metadata']['title']}")
    print(f"내용: {result['content']}")
    print(f"링크: {result['metadata']['link']}")
    print(f"유사도: {result['score']}")
```

## 2. LangChain 통합하여 사용하기
고급 기능(대화형 검색, 에이전트 등)이 필요한 경우 LangChain 통합을 사용할 수 있습니다:

```python
# LangChain 리트리버로 변환
retriever = news_store.vector_store.as_retriever()

# 1. 기본 QA 체인
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,  # 사용할 LLM 모델
    retriever=retriever,
    chain_type="stuff"
)
answer = qa_chain.run("질문")

# 2. 대화형 체인
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
)

# 3. 고급 검색 (여러 쿼리 자동 생성)
from langchain.retrievers import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)
```

## 사용 시 주의사항
1. 기본 검색(`search_similar`)
   - 뉴스 전용 메타데이터와 중복 제거 로직이 포함되어 있음
   - 대부분의 경우 이 방식을 권장

2. LangChain 통합
   - 고급 기능이 필요한 경우에만 사용 권장
   - 메타데이터 처리나 중복 제거는 직접 구현해야 할 수 있음
   - LangChain의 다양한 기능(체인, 메모리, 에이전트 등) 활용 가능

3. 연합뉴스 RSS 관련
   - 비상업적 블로그와 개인적인 용도로만 사용 가능
   - 상업적 이용 시 연합뉴스의 사전 서면 허가 필요