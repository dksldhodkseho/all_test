# Notion API Test

import os
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv("env.notion")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID") # 타겟 페이지들이 담긴 루트 페이지 id

# 임시 테스트용 target_date 하드 코딩
# TODO: 프론트에서 요청이 오면 날짜 받아올 수 있도록 수정 or 매일 주기적 배치
target_date = "20261120"

# 노션 클라이언트 객체
notion = Client(auth=NOTION_API_KEY)

def get_notion_raw_json(page_id):
    """
    has_more = false가 될 떄까지 children.list를 반복 호출
    start_cursor=next_cursor를 통해 답변 이어줌
    """
    results = []
    start_cursor = None

    while True:
        kwargs = {'block_id': page_id}
        if start_cursor is not None:
            kwargs['start_cursor'] = start_cursor
        
        data = notion.blocks.children.list(**kwargs)
        results.extend(data['results'])

        if not data.get('has_more'):
            break
        start_cursor = data['next_cursor']

    return results

# 루트 페이지의 하위 페이지 조회
root_results = get_notion_raw_json(NOTION_ROOT_PAGE_ID)

# 하위 페이지 목록 중 날짜가 target_date와 일치하는 페이지의 id와 제목을 저장
child_page_ids_pages = []
for child in root_results:
    print(child['id'], child['child_page']['title'])
    child_page_ids_pages.append((child['id'], child['child_page']['title']))


# 하위 페이지 목록 중 날짜가 target_date와 일치하는 페이지의 id를 통해 내용 조회
for id, title in child_page_ids_pages:
    if target_date == title:
        page_results = get_notion_raw_json(id)
        
        # raw_json을 따로 DB에 저장 필요
        # 임시로 DB가 아닌 작업 디렉토리에 저장
        data = {
            'object': 'list',
            'results': page_results,
            'has_more': False,
            'next_cursor': None,
        }
        with open(f"{title}_raw_json.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("="*30)
        print(f'Saved_page_id: {id}')
        print(f'Saved {title}_raw_json.json')
        print(f'total_blocks: {len(page_results)}')
