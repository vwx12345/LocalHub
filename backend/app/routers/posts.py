
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.post import (
    PostCreate,
    PostDelete,
    PostResponse,
    PostUpdate,
)


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


PostCategory = Literal[
    "restaurant",
    "tour",
    "free",
]


@router.get(
    "",
    response_model=list[PostResponse],
)
def get_posts(
    category: PostCategory | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Post]:
    statement = select(Post)

    # category가 전달되면 해당 게시판의 글만 조회
    if category is not None:
        statement = statement.where(
            Post.category == category,
        )

    statement = statement.order_by(
        Post.id.desc(),
    )

    posts = db.scalars(statement).all()

    return list(posts)


@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
) -> Post:
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    post.views += 1

    db.commit()
    db.refresh(post)

    return post


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    request: PostCreate,
    db: Session = Depends(get_db),
) -> Post:
    post = Post(
        category=request.category,

        # 추가: 선택한 맛집 또는 관광지 번호 저장
        place_id=request.place_id,

        title=request.title,
        content=request.content,
        password=request.password,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put(
    "/{post_id}",
    response_model=PostResponse,
)
def update_post(
    post_id: int,
    request: PostUpdate,
    db: Session = Depends(get_db),
) -> Post:
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    if post.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )

    post.category = request.category

    # 추가: 연결된 맛집 또는 관광지 번호 수정
    post.place_id = request.place_id

    post.title = request.title
    post.content = request.content

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    post_id: int,
    request: PostDelete,
    db: Session = Depends(get_db),
) -> Response:
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    if post.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )

    # 해당 게시글의 일반 댓글과 대댓글을 모두 삭제
    db.execute(
        delete(Comment).where(
            Comment.post_id == post_id,
        )
    )

    # 게시글 삭제
    db.delete(post)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
