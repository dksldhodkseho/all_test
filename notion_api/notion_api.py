# Notion API Test

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv("env.notion")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID")

target_date = "20261117"

# 노션 클라이언트 객체
notion = Client(auth=NOTION_API_KEY)

# 루트 페이지의 하위 페이지 조회
# response는 루트 페이지의 하위 페이지 목록
response = notion.blocks.children.list(block_id=NOTION_ROOT_PAGE_ID)

# 하위 페이지 목록 중 날짜가 target_date와 일치하는 페이지의 id와 제목을 저장
child_page_ids_pages = []
for child in response["results"]:
    child_page_ids_pages.append((child["id"], child["child_page"]["title"]))

# 하위 페이지 목록 중 날짜가 target_date와 일치하는 페이지의 id를 통해 내용 조회
for id, title in child_page_ids_pages:
    if target_date == title:
        print(notion.blocks.children.list(block_id=id))