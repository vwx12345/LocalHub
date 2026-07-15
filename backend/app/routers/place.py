# app/routers/place.py
from fastapi import APIRouter, Query
import sqlite3
from app.core.config import settings

router = APIRouter(
    prefix="/api",
    tags=["places"]
)



@router.get("/places")
def get_places(type: str = Query(None, description="filter by 'restaurant' or 'tour'")):
    # 디버깅용: 서버 터미널에 현재 읽으려는 DB 실제 경로를 찍어줍니다.
    DB_PATH = settings.database_url.replace("sqlite:///","")
    print(f"🔍 [DB 접근 경로]: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # ⭐️ 프론트에서 넘어오는 type 파라미터 조건 처리
        if type:
            cursor.execute("SELECT * FROM places WHERE type = ?", (type,))
        else:
            cursor.execute("SELECT * FROM places")
            
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "content_id": row["content_id"],
                "title": row["title"],
                "address": row["address"],
                "image_url": row["image_url"],
                "map_x": row["map_x"],
                "map_y": row["map_y"],
                "type": row["type"]
            })
            
        return result

    except sqlite3.OperationalError as e:
        # ⚠️ 만약 테이블이 없거나 DB 에러가 나면 터미널에 상세 내역을 출력합니다.
        print(f"❌ SQLite 에러 발생: {e}")
        return {"error": str(e)}
        
    finally:
        conn.close()