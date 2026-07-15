# app/routers/place.py
from fastapi import APIRouter, Query
import sqlite3
from app.core.config import settings

router = APIRouter(
    prefix="/api",
    tags=["places"]
)

@router.get("/places")
def get_places(
    type: str = Query(None), 
    keyword: str = Query(None) # ⭐️ 검색어 파라미터 추가
):
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 1. 기본 뼈대가 되는 SQL 쿼리문
        sql = "SELECT * FROM places WHERE 1=1"
        params = []
        
        # 2. 카테고리(type)가 선택되었다면 조건 추가
        if type:
            sql += " AND type = ?"
            params.append(type)
            
        # 3. ⭐️ 검색어(keyword)가 입력되었다면 이름(title) 또는 주소(address)에서 검색
        if keyword:
            sql += " AND (title LIKE ? OR address LIKE ?)"
            # 포함하는 단어를 찾기 위해 양옆에 %를 붙여줍니다. (예: "%칼국수%")
            params.append(f"%{keyword}%")
            params.append(f"%{keyword}%")
            
        cursor.execute(sql, params)
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
    except Exception as e:
        print(f"❌ DB 조회 실패: {e}")
        return {"error": str(e)}
    finally:
        conn.close()