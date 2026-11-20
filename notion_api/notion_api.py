# Notion API Test

import os
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv("env.notion")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID") # 타겟 페이지들이 담긴 루트 페이지 id

# 임시 테스트용 target_date
target_date = "20261117"

# 노션 클라이언트 객체
notion = Client(auth=NOTION_API_KEY)

# 루트 페이지의 하위 페이지 조회
# response는 루트 페이지의 하위 페이지 목록
response = notion.blocks.children.list(block_id=NOTION_ROOT_PAGE_ID)

# 하위 페이지 목록 중 날짜가 target_date와 일치하는 페이지의 id와 제목을 저장
child_page_ids_pages = []
for child in response["results"]:
    print(child["id"], child["child_page"]["title"])
    child_page_ids_pages.append((child["id"], child["child_page"]["title"]))


# 하위 페이지 목록 중 날짜가 target_date와 일치하는 페이지의 id를 통해 내용 조회
for id, title in child_page_ids_pages:
    if target_date == title:
        data = notion.blocks.children.list(block_id=id)
        
        # raw_json을 따로 DB에 저장 필요
        # 임시로 DB가 아닌 작업 디렉토리에 저장
        with open(f"{title}_raw_json.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print("="*30)
            print(f"Saved_page_id: {id}")
            print(f"Saved {title}_raw_json.json")


#TODO: 내용 조회 후 자세한 구조 확인 필요