import os
from dotenv import load_dotenv
from rss_crawler import YonhapNewsCrawler
from vector_store import NewsVectorStore
from ..models.embeddings import NewsEmbeddings
from datetime import datetime
import json

def get_version_info(news_items: list) -> str:
    """
    뉴스 데이터의 특성을 기반으로 버전 정보 생성
    """
    # 수집된 뉴스 개수
    news_count = len(news_items)
    
    # 뉴스 기사의 날짜 범위
    dates = [datetime.fromisoformat(item['timestamp'].split('T')[0]) 
            for item in news_items]
    oldest_date = min(dates).strftime('%Y%m%d')
    newest_date = max(dates).strftime('%Y%m%d')
    
    # 현재 시간
    current_time = datetime.now().strftime('%Y%m%d_%H%M')
    
    return f"{current_time}_news{news_count}_range{oldest_date}-{newest_date}"

def main():
    # 환경 변수 로드
    load_dotenv()
    
    # Google Cloud 프로젝트 ID 확인
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT 환경 변수가 설정되지 않았습니다.")
    
    print("1. 뉴스 기사 수집 중...")
    crawler = YonhapNewsCrawler()
    news_items = crawler.fetch_news()
    print(f"수집된 뉴스 기사 수: {len(news_items)}")
    
    print("\n2. 임베딩 모델 초기화 중...")
    embeddings_model = NewsEmbeddings(project_id=project_id)
    
    print("\n3. 뉴스 기사 임베딩 생성 중...")
    # 제목, 요약, 본문을 모두 포함하여 임베딩 생성
    texts = [
        f"제목: {item['title']}\n요약: {item['summary']}\n본문: {item['content']}"
        for item in news_items
    ]
    embeddings = embeddings_model.create_embeddings(texts)
    print(f"생성된 임베딩 수: {len(embeddings)}")
    
    print("\n4. FAISS 벡터 저장소 구축 중...")
    vector_store = NewsVectorStore()
    vector_store.add_news(embeddings, news_items)
    
    print("\n5. 벡터 저장소 저장 중...")
    # 버전 정보를 포함한 저장 경로 생성
    version = get_version_info(news_items)
    save_directory = f"../data/vector_store/{version}"
    os.makedirs(save_directory, exist_ok=True)  # 디렉토리가 없으면 생성
    vector_store.save(save_directory)
    
    # 버전 메타데이터 저장
    metadata = {
        'version': version,
        'created_at': datetime.now().isoformat(),
        'news_count': len(news_items),
        'embedding_model': 'textembedding-gecko-multilingual',
        'oldest_news': min(item['published'] for item in news_items),
        'newest_news': max(item['published'] for item in news_items)
    }
    
    with open(f"{save_directory}/metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"벡터 저장소가 {save_directory}에 저장되었습니다.")
    print("\n저장된 버전 정보:")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()