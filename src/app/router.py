# app/router.py
from fastapi import APIRouter, HTTPException
from src.data_handlers.build_vectordb import main
import traceback

router = APIRouter()

@router.post("/build-vectordb")
def build_vectordb():
    """
    뉴스 기사 수집 및 벡터 저장소 구축
    """
    try:
        main()
        return {"message": "벡터 DB 생성 완료"}
    except Exception as e:
        # 전체 스택 트레이스 터미널 출력
        traceback.print_exc()
        # 문제 생긴 state 덤프
        print("Failed input state:", state)
        raise HTTPException(status_code=500, detail=str(e))
