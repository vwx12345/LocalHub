# app/routers/place.py
from fastapi import APIRouter, Query
import sqlite3
from app.core.config import settings
from pydantic import BaseModel # ⭐️ 리뷰 데이터 검증을 위해 추가

router = APIRouter(
    prefix="/api",
    tags=["places"]
)

# ⭐️ 프론트에서 넘어올 리뷰 데이터 양식 (이름, 비번, 별점, 내용)
class ReviewCreate(BaseModel):
    place_id: int
    nickname: str
    password: str
    rating: int
    content: str

# 1. 통합 검색이 포함된 장소 조회 API
@router.get("/places")
def get_places(
    type: str = Query(None), 
    keyword: str = Query(None)
):
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        sql = "SELECT * FROM places WHERE 1=1"
        params = []
        
        if type:
            sql += " AND type = ?"
            params.append(type)
            
        if keyword:
            sql += " AND (title LIKE ? OR address LIKE ?)"
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

# ⭐️ 2. 특정 장소의 리뷰 목록 조회 API
@router.get("/places/{place_id}/reviews")
def get_reviews(place_id: int):
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 최신 리뷰가 맨 위로 오도록 내림차순(DESC) 정렬
        cursor.execute("SELECT id, nickname, rating, content, created_at FROM reviews WHERE place_id = ? ORDER BY id DESC", (place_id,))
        rows = cursor.fetchall()
        # 보안을 위해 password는 제외하고 프론트로 넘깁니다.
        return [dict(row) for row in rows] 
    except Exception as e:
        print(f"❌ 리뷰 조회 실패: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

# ⭐️ 3. 새로운 리뷰 등록 API
@router.post("/reviews")
def create_review(review: ReviewCreate):
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO reviews (place_id, nickname, password, rating, content) VALUES (?, ?, ?, ?, ?)",
            (review.place_id, review.nickname, review.password, review.rating, review.content)
        )
        conn.commit()
        return {"message": "리뷰가 성공적으로 등록되었습니다."}
    except Exception as e:
        print(f"❌ 리뷰 등록 실패: {e}")
        return {"error": str(e)}
    finally:
        conn.close()