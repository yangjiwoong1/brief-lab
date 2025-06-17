from typing import List, Dict
import json
import os
from langchain_community.vectorstores.faiss import FAISS
from src.models.embeddings import NewsEmbeddings

class NewsVectorStore:
    def __init__(self):
        """
        FAISS 벡터 저장소 초기화
        """
        self.vector_store = None
    
    def add_news(self, embeddings: List[List[float]], texts: List[str], metadatas: List[Dict]):
        """
        param:
            embeddings: 임베딩 벡터 리스트
            texts: 분할된 텍스트 리스트
            metadatas: 각 텍스트 청크의 메타데이터 리스트
        """
        # FAISS 벡터 저장소 생성
        self.vector_store = FAISS.from_embeddings(
            text_embeddings=list(zip(texts, embeddings)),
            embedding=NewsEmbeddings().embeddings,  # LangChain 인터페이스 호환을 위해
            metadatas=metadatas
        )

        # 원본 뉴스 데이터도 저장 (중복 제거하여 저장)
        unique_news = {}
        for metadata in metadatas:
            if metadata['title'] not in unique_news:
                unique_news[metadata['title']] = {
                    'title': metadata['title'],
                    'link': metadata['link'],
                    'published': metadata['published'],
                    'author': metadata['author'],
                    'image_url': metadata['image_url'],
                    'summary': metadata['summary']
                }
        self.save_original_news(list(unique_news.values()))
    
    def save(self, directory: str):
        """
        param:
            directory: 저장할 디렉토리 경로
            
        벡터 저장소와 뉴스 데이터를 파일로 저장
        """
        if not self.vector_store:
            raise ValueError("저장할 벡터 저장소가 없습니다.")
        
        # FAISS 인덱스와 메타데이터 저장
        self.vector_store.save_local(directory)
    
    def save_original_news(self, news_items: List[Dict], directory: str = None):
        """
        원본 뉴스 데이터를 JSON 파일로 저장
        
        param:
            news_items: 저장할 뉴스 데이터 리스트
            directory: 저장할 디렉토리 경로 (None인 경우 벡터 저장소와 같은 경로 사용)
        """
        if directory:
            with open(os.path.join(directory, "news_items.json"), "w", encoding="utf-8") as f:
                json.dump(news_items, f, ensure_ascii=False, indent=2)
    
    def load(self, directory: str) -> None:
        """벡터 저장소를 로드합니다.

        Args:
            directory: 벡터 저장소가 저장된 디렉토리 경로
        """
        embeddings_model = NewsEmbeddings()
        self.vector_store = FAISS.load_local(
            directory,
            embeddings_model.embeddings,
            allow_dangerous_deserialization=True
        )
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        """
        유사한 뉴스 검색
        
        param:
            query: 검색할 쿼리 문자열
            k: 반환할 결과 개수
            
        return:
            유사도 점수와 뉴스 메타데이터를 포함한 결과 리스트
        """
        if not self.vector_store:
            raise ValueError("벡터 저장소가 로드되지 않았습니다.")
            
        # 쿼리로 유사한 문서 검색
        results = self.vector_store.similarity_search_with_score(
            query,
            k=k
        )
        
        # 결과 포매팅 및 중복 제거
        seen_titles = set()
        formatted_results = []
        
        for doc, score in results:
            title = doc.metadata['title']
            
            # 같은 뉴스의 다른 청크는 건너뛰기
            if title in seen_titles:
                continue
                
            seen_titles.add(title)
            result = {
                'score': float(score),
                'content': doc.page_content,
                'metadata': doc.metadata,
                'chunk_info': f"청크 {doc.metadata['chunk_idx'] + 1}/{doc.metadata['total_chunks']}"
            }
            formatted_results.append(result)
            
            # 원하는 개수만큼 수집되면 중단
            if len(formatted_results) >= k:
                break
                
        return formatted_results 