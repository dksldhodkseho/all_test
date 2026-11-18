# Notion API Test

## 가상 환경 및 필요 라이브러리 설치
conda activate notion-api-test
pip install requirements.txt

## Notion Client
response = notion.blocks.children.list(clock_id=NOTION_ROOT_PAGE_ID)

### 하위 페이지 조회
최상위 루트 페이지에서 하위 페이지의 id, title 조회 가능

### 페이지 내용
페이지 내용 확인 가능

### 사용 방법
1. env에 저장된 root 페이지 id를 통해 하위 페이지들의 id, title을 tuple로 저장
2. 튜플에서 하위 페이지의 제목과 target_date가 일치하면 하위 페이지의 id를 통해 내용 조회
3. block['type']에서 Content Text Type, block[block['type']['rich_text']]에서 본문 내용 확인 가능

### Content Text Type
1. heading_1
    1번 제목 (markdown #)
2. heading_2
    2번 제목 (markdown ##)
3. heading_3
    3번 제목 (markdown ###)
4. heading_4
    4번 제목 (markdown ####)
5. paragraph
    일반 본문
6. number_list_item
    번호 목록 (1,2,3,4... 번호 매긴 리스트)
7. bulleted_list_item
    글머리 목록 (markdown -)
