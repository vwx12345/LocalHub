const BASE_URL = '/api/posts'

// 게시글 전체 또는 카테고리별 조회
export async function getPosts(category = '') {
  const queryString = category
    ? `?category=${encodeURIComponent(category)}`
    : ''

  const response = await fetch(`${BASE_URL}${queryString}`)

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '게시글 조회 실패')
  }

  return data
}

// 게시글 상세 조회
export async function getPost(postId) {
  const response = await fetch(`${BASE_URL}/${postId}`)

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '게시글 조회 실패')
  }

  return data
}

// 게시글 작성
export async function createPost(postData) {
  const response = await fetch(BASE_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '게시글 작성 실패')
  }

  return data
}

// 게시글 수정
export async function updatePost(postId, postData) {
  const response = await fetch(`${BASE_URL}/${postId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '게시글 수정 실패')
  }

  return data
}

// 게시글 삭제
export async function deletePost(postId, password) {
  const response = await fetch(`${BASE_URL}/${postId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      password,
    }),
  })

  if (!response.ok) {
    const data = await response.json()
    throw new Error(data.detail ?? '게시글 삭제 실패')
  }

  return true
}

// 댓글 조회
export async function getComments(postId) {
  const response = await fetch(`${BASE_URL}/${postId}/comments`)

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '댓글 조회 실패')
  }

  return data
}

// 댓글 작성
export async function createComment(postId, commentData) {
  const response = await fetch(`${BASE_URL}/${postId}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(commentData),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '댓글 작성 실패')
  }

  return data
}

// 댓글 수정
export async function updateComment(commentId, commentData) {
  const response = await fetch(`/api/comments/${commentId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(commentData),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '댓글 수정 실패')
  }

  return data
}

// 댓글 삭제
export async function deleteComment(commentId, password) {
  const response = await fetch(`/api/comments/${commentId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      password,
    }),
  })

  if (!response.ok) {
    const data = await response.json()
    throw new Error(data.detail ?? '댓글 삭제 실패')
  }

  return true
}
