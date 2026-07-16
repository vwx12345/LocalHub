from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import (
    CommentCreate,
    CommentDelete,
    CommentItemResponse,
    CommentResponse,
    CommentUpdate,
)


router = APIRouter(tags=["comments"])


def get_comment_or_404(
    comment_id: int,
    db: Session,
) -> Comment:
    comment = db.get(Comment, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다.",
        )

    return comment


def verify_comment_password(
    comment: Comment,
    password: str,
) -> None:
    if comment.password != password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )


def to_comment_response(
    comment: Comment,
) -> CommentItemResponse:
    return CommentItemResponse.model_validate(comment)


@router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentResponse],
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
) -> list[CommentResponse]:
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc(), Comment.id.asc())
    )

    comments = list(db.scalars(statement).all())

    parent_comments: list[Comment] = []
    replies_by_parent: dict[int, list[Comment]] = {}

    for comment in comments:
        if comment.parent_id is None:
            parent_comments.append(comment)
            continue

        replies_by_parent.setdefault(
            comment.parent_id,
            [],
        ).append(comment)

    result: list[CommentResponse] = []

    for parent in parent_comments:
        parent_data = to_comment_response(parent)

        replies = [
            to_comment_response(reply)
            for reply in replies_by_parent.get(parent.id, [])
        ]

        result.append(
            CommentResponse(
                **parent_data.model_dump(),
                replies=replies,
            )
        )

    return result


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    post_id: int,
    request: CommentCreate,
    db: Session = Depends(get_db),
) -> Comment:
    post = db.get(Post, post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    if request.parent_id is not None:
        parent_comment = db.get(
            Comment,
            request.parent_id,
        )

        if (
            parent_comment is None
            or parent_comment.post_id != post_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="부모 댓글을 찾을 수 없습니다.",
            )

        # 대댓글에 다시 답글을 작성하는 것을 차단
        if parent_comment.parent_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="대댓글에는 답글을 작성할 수 없습니다.",
            )

    comment = Comment(
        post_id=post_id,
        parent_id=request.parent_id,
        content=request.content,
        password=request.password,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.put(
    "/comments/{comment_id}",
    response_model=CommentItemResponse,
)
def update_comment(
    comment_id: int,
    request: CommentUpdate,
    db: Session = Depends(get_db),
) -> Comment:
    comment = get_comment_or_404(
        comment_id=comment_id,
        db=db,
    )

    verify_comment_password(
        comment=comment,
        password=request.password,
    )

    comment.content = request.content

    db.commit()
    db.refresh(comment)

    return comment


@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(
    comment_id: int,
    request: CommentDelete,
    db: Session = Depends(get_db),
) -> Response:
    comment = get_comment_or_404(
        comment_id=comment_id,
        db=db,
    )

    verify_comment_password(
        comment=comment,
        password=request.password,
    )

    # 부모 댓글을 삭제하면 직속 대댓글도 함께 삭제
    if comment.parent_id is None:
        db.execute(
            delete(Comment).where(
                Comment.parent_id == comment.id
            )
        )

    db.delete(comment)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )