# back/init_db.py
import json
import sqlite3

import os
import random

# 1. 현재 파일(init_db.py)이 있는 폴더 위치인 'backend/app'을 가져옵니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 한 단계 위로 올라가서('backend'), 'data' 폴더 안의 'localhub.db' 경로를 완성합니다.
DB_PATH = os.path.join(os.path.dirname(current_dir), "data", "localhub.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 2. places 테이블 생성 (어떤 타입인지 구분하는 'type' 컬럼 추가!)
# type: 'restaurant' (식당) 또는 'tour' (관광지)
cursor.execute("""
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id TEXT UNIQUE,
    title TEXT,
    address TEXT,
    image_url TEXT,
    map_x REAL,
    map_y REAL,
    type TEXT  
)
""")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id INTEGER,
        nickname TEXT NOT NULL,
        password TEXT NOT NULL,
        rating INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (place_id) REFERENCES places (id)
    )
    ''')
conn.commit()

# 3. 데이터를 넣는 헬퍼 함수 정의
def load_and_insert(file_name, place_type):
    json_file_path = os.path.join("jsonData", file_name)
    
    # 파일이 실제로 존재하는지 확인
    if not os.path.exists(json_file_path):
        print(f"⚠️ 파일을 찾을 수 없습니다: {json_file_path}")
        return

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    inserted_count = 0
    for item in data.get("items", []):
        content_id = item.get("contentid")
        title = item.get("title")
        address = item.get("addr1")
        image_url = item.get("firstimage")
        map_x = float(item.get("mapx")) if item.get("mapx") else None
        map_y = float(item.get("mapy")) if item.get("mapy") else None

        try:
            # 중복된 content_id가 들어오면 무시하고 새로 들어온 것만 저장
            cursor.execute("""
            INSERT OR IGNORE INTO places (content_id, title, address, image_url, map_x, map_y, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (content_id, title, address, image_url, map_x, map_y, place_type))
            
            # 실제로 삽입되었을 때만 개수 카운트 (중복 무시 제외)
            if cursor.rowcount > 0:
                inserted_count += 1
        except Exception as e:
            print(f"데이터 입력 중 오류 발생 ({title}): {e}")

    conn.commit()
    print(f"✅ {file_name}에서 {inserted_count}개의 {place_type} 데이터를 성공적으로 등록했습니다.")

# 4. 각각의 파일 실행하기
# (만약 실제 파일 이름이 다르다면 아래 파일명을 본인 파일명에 맞게 변경해주세요!)
load_and_insert("restaurant.json", "restaurant")
load_and_insert("tour.json", "tour")

def generate_dummy_reviews():
    # 1. 맛집 5개, 관광지 5개의 실제 DB ID를 가져옵니다.
    cursor.execute("SELECT id, title FROM places WHERE type='restaurant' LIMIT 5")
    restaurants = cursor.fetchall()

    cursor.execute("SELECT id, title FROM places WHERE type='tour' LIMIT 5")
    tours = cursor.fetchall()

    # 2. 랜덤으로 달아줄 리뷰 템플릿과 닉네임 목록
    review_templates = [
        ("정말 최고였어요! 다음에 또 오고 싶습니다.", 5),
        ("기대 이상이네요. 주변에도 추천할게요.", 5),
        ("전체적으로 무난하고 괜찮았습니다.", 4),
        ("가족들과 함께 갔는데 다들 만족했어요.", 4),
        ("생각보다 평범했어요. 한 번쯤 가볼 만합니다.", 3),
        ("조금 아쉬운 부분이 있었지만 나쁘지 않네요.", 3),
        ("개인적인 취향은 아니었어요. 아쉽습니다.", 2),
        ("SNS에서 본 거랑 좀 달라서 실망했어요.", 2)
    ]
    nicknames = ["지나가던행인", "프로리뷰어", "로컬주민", "여행조아", "솔직후기남", "동네주민", "방구석미식가"]

    target_places = restaurants + tours
    inserted_reviews = 0

    # 3. 10개의 장소에 각각 4~6개의 리뷰를 랜덤으로 작성
    for place_id, title in target_places:
        num_reviews = random.randint(4, 6) # 4개에서 6개 사이
        
        for _ in range(num_reviews):
            content, rating = random.choice(review_templates)
            nickname = random.choice(nicknames)
            password = "1234" # 테스트용 비밀번호 통일
            
            cursor.execute("""
            INSERT INTO reviews (place_id, nickname, password, rating, content)
            VALUES (?, ?, ?, ?, ?)
            """, (place_id, nickname, password, rating, content))
            
            inserted_reviews += 1

    conn.commit()
    print(f"🌟 추천 시스템용 맛집/관광지 10곳에 총 {inserted_reviews}개의 더미 리뷰를 등록했습니다!")

# 함수 실행
generate_dummy_reviews()

# 5. 연결 종료
conn.close()
print("\n🎉 모든 데이터 마이그레이션이 완료되었습니다!")