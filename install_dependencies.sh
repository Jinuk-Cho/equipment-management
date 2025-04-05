#!/bin/bash

# 기존 가상환경 제거 (있는 경우)
rm -rf venv/

# 새 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# pip 업그레이드
pip install --upgrade pip

# 기존 패키지 제거
pip uninstall -y supabase supabase-py postgrest httpx

# requirements.txt 설치
pip install -r requirements.txt

# 설치된 패키지 확인
pip freeze 

# app.py 파일을 스테이징
git add app.py

# 변경사항 커밋
git commit -m "fix: remove duplicate initialization and rendering code

- Remove duplicate language initialization
- Remove duplicate component initialization
- Remove duplicate menu rendering code
- Fix indentation warnings"

# 원격 저장소에 푸시
git push origin main 