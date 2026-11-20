# Notion API Test

## 가상 환경 및 필요 라이브러리 설치
```bash
conda activate notion-api-test
pip install -r requirements.txt
```

## Notion Client
```python
response = notion.blocks.children.list(block_id=NOTION_ROOT_PAGE_ID)
```

### 하위 페이지 조회
최상위 루트 페이지에서 하위 페이지의 id, title 조회 가능

### 페이지 내용
페이지 내용 확인 가능

### 사용 방법
1. env에 저장된 root 페이지 id를 통해 하위 페이지들의 id, title을 tuple로 저장
2. 튜플에서 하위 페이지의 제목과 target_date가 일치하면 하위 페이지의 id를 통해 내용 조회
3. `result['type']`에서 Content Text Type, `result[result['type']]['rich_text']`에서 본문 내용 확인 가능

### Content Text Type
1. `heading_1` — 1번 제목 (markdown `#`)
2. `heading_2` — 2번 제목 (markdown `##`)
3. `heading_3` — 3번 제목 (markdown `###`)
4. `heading_4` — 4번 제목 (markdown `####`)
5. `paragraph` — 일반 본문
6. `numbered_list_item` — 번호 목록 (1,2,3,4... 번호 매긴 리스트)
7. `bulleted_list_item` — 글머리 목록 (markdown `-`)

## Client 객체 자세한 명세
### 저장되는 raw_json
확인해야 하는 Key
1. `results`: 페이지의 실제 content와 content에 대한 meta_data가 담겨 있음
2. `has_more`: 아직 안받은 결과가 있다면 true, 보통 results가 100개가 넘어가면 잘려서 출력됨.
3. `next_cursor`: `has_more`가 true일 때 같은 API를 다시 날리기 위한 값
   ```python
   start_cursor=next_cursor
   ```

has_more가 true이면 자동으로 이어 받지 않으므로, next_cursor를 start_cursor로 넘겨 같은 API를 직접 다시 호출해야 한다.
보통 100개 단위로 잘리므로, has_more가 false가 될 때까지 반복 호출이 테스트가 필요하다.

### results 구조
| key | type | description | note |
| --- | --- | --- | --- |
| object | string | 객체의 종류 | 보통 block |
| id | string | 해당 블록의 uuid | |
| parent | dictionary | 부모에 대한 metadata | ex. type, page_id |
| created_time | string | 생성 시각 | |
| last_edited_time | string | 마지막 수정 시각 | |
| created_by | dictionary | 생성자의 metadata | ex. user_id |
| last_edited_by | dictionary | 마지막 수정자의 metadata | ex. user_id |
| has_children | boolean | 하위에 블록이 또 있는지 여부 | true라면 별도 children 조회 필요 |
| in_trash | boolean | 휴지통에 있는지 여부 | 일정 기간 soft_delete?? |
| type | string | 블록 종류 | heading_2 같은 것인지 단순 텍스트인지 구분하기 위함 |
| (type의 value값) | dictionary | 실제 본문이 담겨 있는 딕셔너리 | 아래 별도 후술 |
| archived | boolean | 아카이브 여부 | in_trash와 비슷하게 쓰임 |

#### 본문 content
result의 type의 value값을 key값으로 사용
ex) `result['type']`이 `heading_2`라면 `'heading_2': {...}` 형태로 나옴

실제 텍스트는 아래처럼 확인 가능
```python
result[result['type']]['rich_text'][i]['text']['content']
# 또는 읽기용
result[result['type']]['rich_text'][i]['plain_text']
```