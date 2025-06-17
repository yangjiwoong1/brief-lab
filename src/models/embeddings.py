from typing import List
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud import aiplatform
from dotenv import load_dotenv
import os

# 프로젝트 루트에 .env 파일 생성 후 환경변수 설정
# GOOGLE_CLOUD_PROJECT=프로젝트 ID
# GOOGLE_APPLICATION_CREDENTIALS=서비스 계정 키 경로(json)
# VERTEX_AI_LOCATION=리전

load_dotenv()

class NewsEmbeddings:
    def __init__(self, project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT"), location: str = os.getenv("VERTEX_AI_LOCATION")):
        """
        Vertex AI 임베딩 모델 초기화
        """
        aiplatform.init(project=project_id, location=location)
        self.embeddings = VertexAIEmbeddings(
            model_name="text-multilingual-embedding-002"
        )
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        텍스트 리스트를 임베딩 벡터로 변환
        """
        return self.embeddings.embed_documents(texts)

    def create_query_embedding(self, text: str) -> List[float]:
        """
        검색 쿼리 텍스트를 임베딩 벡터로 변환
        """
        return self.embeddings.embed_query(text) 