from fastapi import APIRouter, Query, HTTPException
import sqlite3
from app.core.config import settings
from pydantic import BaseModel  # ⭐️ 리뷰 데이터 검증을 위해 추가

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

# ⭐️ 리뷰 수정 시 넘어오는 데이터 양식 (비밀번호 확인 + 수정할 별점/내용)
class ReviewUpdate(BaseModel):
    password: str
    rating: int
    content: str

# ⭐️ 리뷰 삭제 시 넘어오는 데이터 양식 (비밀번호 확인만 필요)
class ReviewDelete(BaseModel):
    password: str


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

# ⭐️ 4. 리뷰 수정 API (비밀번호가 일치할 때만 수정 허용)
@router.put("/reviews/{review_id}")
def update_review(review_id: int, review: ReviewUpdate):
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password FROM reviews WHERE id = ?", (review_id,))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        if row["password"] != review.password:
            raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

        cursor.execute(
            "UPDATE reviews SET rating = ?, content = ? WHERE id = ?",
            (review.rating, review.content, review_id)
        )
        conn.commit()
        return {"message": "리뷰가 수정되었습니다."}
    except HTTPException:
        # 위에서 던진 404 / 401은 그대로 응답으로 전달
        raise
    except Exception as e:
        print(f"❌ 리뷰 수정 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ⭐️ 5. 리뷰 삭제 API (비밀번호가 일치할 때만 삭제 허용)
@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, review: ReviewDelete):
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password FROM reviews WHERE id = ?", (review_id,))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        if row["password"] != review.password:
            raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
        return {"message": "리뷰가 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 리뷰 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ==========================================
# 👇 6. 새로 추가된 랭킹 조회 API 👇
# ==========================================
@router.get("/ranking")
def get_place_ranking(type: str = Query("restaurant")):
    """
    type에 따라 'restaurant' 또는 'tour'의 랭킹 TOP 5를 반환합니다.
    (평점 높은 순 -> 리뷰 많은 순)
    """
    db_path = settings.database_url.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        query = """
        SELECT 
            p.id, 
            p.content_id,
            p.title, 
            p.address, 
            p.image_url, 
            p.map_x,
            p.map_y,
            p.type,
            COUNT(r.id) AS review_count,
            ROUND(AVG(r.rating), 1) AS avg_rating
        FROM places p
        JOIN reviews r ON p.id = r.place_id
        WHERE p.type = ?
        GROUP BY p.id
        ORDER BY avg_rating DESC, review_count DESC
        LIMIT 5
        """
        
        cursor.execute(query, (type,))
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"❌ 랭킹 조회 실패: {e}")
        return {"error": str(e)}
    finally:
        conn.close()