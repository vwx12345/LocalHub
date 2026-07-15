# app/search.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# ⭐️ 우리가 방금 만든 routers/place.py의 router를 불러옵니다.
from routers import place

app = FastAPI()

# CORS 설정은 메인 파일에서 한 번만 해주면 하위 라우터에도 전부 적용됩니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⭐️ 핵심: 분리한 라우터를 메인 앱에 등록합니다.
app.include_router(place.router)


@app.get("/")
def read_root():
    return {"message": "대전/충청 커뮤니티 백엔드 서버가 정상 작동 중입니다!"}