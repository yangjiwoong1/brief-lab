import os
from dotenv import load_dotenv
from src.data_handlers.rss_crawler import YonhapNewsCrawler
from src.data_handlers.vector_store import NewsVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime
import json
from email.utils import parsedate_to_datetime
from src.models.embeddings import NewsEmbeddings

def get_version_info(news_items: list) -> str:
    """
    뉴스 데이터의 특성을 기반으로 버전 정보 생성
    """
    news_count = len(news_items)
    
    # RFC 2822 형식의 날짜 문자열을 datetime 객체로 변환
    dates = [parsedate_to_datetime(item['published']) for item in news_items]
    oldest_date = min(dates).strftime('%Y%m%d')
    newest_date = max(dates).strftime('%Y%m%d')
    
    # 현재 시간
    current_time = datetime.now().strftime('%Y%m%d_%H%M')
    
    return f"{current_time}_news{news_count}_range{oldest_date}-{newest_date}"

def main():
    # 환경 변수 로드
    load_dotenv()
    
    print("1. 뉴스 기사 수집 중...")
    crawler = YonhapNewsCrawler()
    news_items = crawler.fetch_news()
    print(f"수집된 뉴스 기사 수: {len(news_items)}")
    
    print("\n2. 임베딩 모델과 텍스트 분할기 초기화 중...")
    embeddings_model = NewsEmbeddings()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 청크 크기 (한글 기준 약 500글자)
        chunk_overlap=200,  # 청크 간 중복 (문맥 유지를 위해)
        length_function=len,
        separators=["\n\n", "\n", ".", "。", "!", "?", "！", "？", " ", ""]  # 한중일 문장 구분자 포함
    )
    
    print("\n3. 뉴스 기사 분할 및 임베딩 생성 중...")
    all_splits = []
    all_metadatas = []
    
    # 각 뉴스 기사를 분할하고 메타데이터 준비
    for item in news_items:
        full_text = f"제목: {item['title']}\n본문: {item['content']}"
        splits = text_splitter.split_text(full_text)
        
        for split_idx, split in enumerate(splits):
            all_splits.append(split)
            metadata = {
                'title': item['title'],
                'link': item['link'],
                'published': item['published'],
                'author': item.get('author', ''),
                'image_url': item.get('image_url', ''),
                'summary': item.get('summary', ''),
                'chunk_idx': split_idx,
                'total_chunks': len(splits)
            }
            all_metadatas.append(metadata)
    
    # 분할된 텍스트에 대해 임베딩 생성
    embeddings = embeddings_model.create_embeddings(all_splits)
    print(f"생성된 임베딩 수: {len(embeddings)}")
    
    print("\n4. FAISS 벡터 저장소 구축 중...")
    vector_store = NewsVectorStore()
    vector_store.add_news(embeddings, all_splits, all_metadatas)
    
    print("\n5. 벡터 저장소 저장 중...")
    # 버전 정보를 포함한 저장 경로 생성
    version = get_version_info(news_items)
    save_directory = os.path.join("data", "vector_store", version)
    os.makedirs(save_directory, exist_ok=True)
    
    # 벡터 저장소와 원본 뉴스 데이터 저장
    vector_store.save(save_directory)
    vector_store.save_original_news(news_items, save_directory)
    
    # 버전 메타데이터 저장
    metadata = {
        'version': version,
        'created_at': datetime.now().isoformat(),
        'news_count': len(news_items),
        'total_chunks': len(all_splits),
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'embedding_model': 'text-multilingual-embedding-002',
        'oldest_news': min(parsedate_to_datetime(item['published']) for item in news_items).isoformat(),
        'newest_news': max(parsedate_to_datetime(item['published']) for item in news_items).isoformat()
    }
    
    with open(f"{save_directory}/metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"벡터 저장소가 {save_directory}에 저장되었습니다.")
    print("\n저장된 버전 정보:")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()