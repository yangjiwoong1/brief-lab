from src.data_handlers.vector_store import NewsVectorStore

# 벡터 스토어 인스턴스 생성 및 로드
news_store = NewsVectorStore()
news_store.load("data/vector_store/20250617_1034_news120_range20250617-20250617") # 경로 주의

# 검색 예시
results = news_store.search_similar(
    query="AI 뉴스",
    k=3  # 원하는 결과 개수
)

# 결과 사용하기
for result in results:
    print(f"제목: {result['metadata']['title']}")
    print(f"내용: {result['content']}")
    print(f"링크: {result['metadata']['link']}")
    print(f"유사도: {result['score']}")