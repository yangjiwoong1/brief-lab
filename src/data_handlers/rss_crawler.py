import feedparser
from bs4 import BeautifulSoup
import requests
import random
from typing import List, Dict
from datetime import datetime
import time

class YonhapNewsCrawler:
    def __init__(self):
        self.rss_urls = [
            "https://www.yna.co.kr/rss/news.xml", # 최신 기사
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        } # 봇의 접근을 차단하는 경우가 있기 때문에 HTTP 헤더에 User-Agent 추가

    def _get_article_content(self, url: str) -> str:
        """
        RSS에는 본문 내용이 없기 때문에 기사 URL에서 본문 내용을 추출합니다.
        본문 URL로 HTTP 요청을 보내고, 본문 내용을 추출합니다.

        return:
            - 본문 내용(각 단락을 줄바꿈으로 연결)
            - 빈 문자열 (예외 발생 시)
        """
        try:
            response = requests.get(url, headers=self.headers) # HTML 페이지 요청
            response.raise_for_status() # 요청 실패 시 예외 발생
            soup = BeautifulSoup(response.text, 'html.parser') # BeautifulSoup 객체로 파싱
            
            # 연합뉴스 본문 컨텐츠 영역
            article_div = soup.select_one('div.story-news')  # story-news 클래스를 가진 div 선택
            if article_div:
                # 본문 단락들 (p 태그들)
                paragraphs = article_div.find_all('p', recursive=False)  # recursive=False로 직계 p 태그만 선택
                # 각 단락의 텍스트를 리스트로 모으고 줄바꿈으로 연결
                content = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
                # 저작권 관련 텍스트와 송고 시간 제거
                content = content.split('<저작권자')[0].strip()
                return content
            return ""
        except Exception as e:
            print(f"기사 내용 추출 실패 ({url}): {str(e)}")
            return ""

    def fetch_news(self) -> List[Dict]:
        """
        RSS 피드에서 뉴스 기사를 수집합니다.
        """
        all_entries = []
        
        for url in self.rss_urls:
            feed = feedparser.parse(url)
            
            for entry in feed.entries:
                # 저작권 고지문 건너뛰기
                if '[알림]' in entry.title or '저작권' in entry.title:
                    continue
                    
                # RSS 피드의 요약 정보
                soup = BeautifulSoup(entry.description, 'html.parser')
                summary = soup.get_text()
                
                # 실제 기사 본문 가져오기
                full_content = self._get_article_content(entry.link)
                
                if full_content:  # 본문이 성공적으로 추출된 경우만 저장
                    news_item = {
                        'title': entry.title.replace('<![CDATA[', '').replace(']]>', ''),  # CDATA 태그 제거
                        'summary': summary,
                        'content': full_content,
                        'link': entry.link,
                        'published': entry.published,
                        'author': entry.get('dc_creator', ''),  # 작성자 정보 추가
                        'image_url': entry.get('media_content', [{}])[0].get('url', ''),  # 이미지 URL 추가
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    all_entries.append(news_item)
                    # 다음 반복 전에 0~1초 사이로 랜덤하게 딜레이를 주어 서버 부하를 줄임
                    time.sleep(random.uniform(0,1))
        
        return all_entries

if __name__ == "__main__":
    crawler = YonhapNewsCrawler()
    news_items = crawler.fetch_news()
    print(f"수집된 뉴스 기사 수: {len(news_items)}")
    if news_items:
        print("\n첫 번째 기사 샘플:")
        print(f"제목: {news_items[0]['title']}")
        print(f"작성자: {news_items[0]['author']}")
        print(f"발행일: {news_items[0]['published']}")
        print(f"요약: {news_items[0]['summary'][:200]}...")
        print(f"본문:\n{news_items[0]['content'][:500]}...") 