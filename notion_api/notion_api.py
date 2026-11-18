# Notion API Test

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv("env.notion")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_ROOT_PAGE_ID = os.getenv("NOTION_ROOT_PAGE_ID")

target_date = "20261117"

notion = Client(auth=NOTION_API_KEY)

response = notion.blocks.children.list(block_id=NOTION_ROOT_PAGE_ID)

child_page_ids_pages = []
for child in response["results"]:
    child_page_ids_pages.append((child["id"], child["child_page"]["title"]))

for id, title in child_page_ids_pages:
    if target_date == title:
        print(notion.blocks.children.list(block_id=id))