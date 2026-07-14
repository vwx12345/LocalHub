#!/usr/bin/env bash

set -euo pipefail

echo "[1/7] 실행 위치 확인"

if [ ! -f "localhub/package.json" ]; then
  echo "오류: localhub/package.json을 찾을 수 없습니다."
  echo "LocalHub/frontend 폴더에서 실행하세요."
  exit 1
fi

echo "[2/7] 기존 프론트 환경변수 임시 보관"

if [ -f ".env" ]; then
  mv .env ../frontend_env_backup
fi

echo "[3/7] 잘못 생성된 외부 npm 파일 제거"

rm -rf node_modules
rm -f package.json package-lock.json

echo "[4/7] 내부 프로젝트의 불필요한 node_modules 제거"

rm -rf localhub/node_modules

echo "[5/7] localhub 프로젝트를 frontend 루트로 이동"

shopt -s dotglob nullglob

for item in localhub/*; do
  mv "$item" .
done

shopt -u dotglob nullglob

rmdir localhub

echo "[6/7] 환경변수 복원"

if [ -f "../frontend_env_backup" ]; then
  mv ../frontend_env_backup .env
fi

if [ ! -f ".env.example" ] && [ -f ".env" ]; then
  cp .env .env.example
fi

echo "[7/7] 패키지 설치 및 프로젝트 검사"

npm install
npm install axios
npm run lint
npm run build

echo
echo "프론트엔드 정리가 완료되었습니다."
echo "개발 서버를 실행합니다."
echo

npm run dev
