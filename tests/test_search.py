import pytest
from src.data_handlers.vector_store import NewsVectorStore
import os

def test_vector_store_search():
    """벡터 스토어 검색 기능 테스트"""
    # 가장 최근 벡터 스토어 디렉토리 찾기
    vector_store_dir = "data/vector_store"
    subdirs = [d for d in os.listdir(vector_store_dir) 
              if os.path.isdir(os.path.join(vector_store_dir, d)) and not d.startswith('.')]
    latest_dir = sorted(subdirs)[-1]  # 가장 최근 디렉토리 선택
    vector_store_path = os.path.join(vector_store_dir, latest_dir)

    # 벡터 스토어 로드
    vector_store = NewsVectorStore()
    vector_store.load(vector_store_path)
    
    # 테스트할 검색 쿼리들
    test_queries = [
        "AI 소식"
    ]
    
    # 각 쿼리에 대해 검색 실행 및 결과 확인
    for query in test_queries:
        print(f"\n[검색 쿼리] {query}")
        
        # 상위 3개 결과 검색
        results = vector_store.search_similar(query, k=3)
        
        # 검증
        assert len(results) > 0, f"쿼리 '{query}'에 대한 검색 결과가 없습니다."
        
        # 결과 출력
        for i, result in enumerate(results, 1):
            print(f"\n결과 {i}:")
            print(f"제목: {result['metadata']['title']}")
            print(f"유사도 점수: {result['score']:.4f}")
            print(f"내용: {result['content']}")
            print(f"요약: {result['metadata']['summary']}")
            print(f"링크: {result['metadata']['link']}")
            
            # 유사도 점수가 0과 1 사이인지 확인
            assert 0 <= result['score'] <= 1, f"유사도 점수가 범위를 벗어났습니다: {result['score']}"
            
            # 필수 메타데이터 필드 확인
            assert 'title' in result['metadata'], "메타데이터에 제목이 없습니다."
            assert 'link' in result['metadata'], "메타데이터에 링크가 없습니다."
            assert 'summary' in result['metadata'], "메타데이터에 요약이 없습니다." 