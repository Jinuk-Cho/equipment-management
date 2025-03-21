# 설비 관리 시스템

설비 고장 분석 및 관리를 위한 웹 기반 대시보드 시스템입니다.

## 주요 기능

1. **로그인 및 권한 관리**
   - ID/PW 로그인
   - Google 계정 연동
   - 사용자 권한 관리 (관리자, 리더, 일반 직원)

2. **실시간 대시보드**
   - 설비 상태 요약
   - 현재 고장 장비 리스트
   - 교체 부품 및 작업 내역
   - 시간별 오류 발생 트렌드
   - 구역별 장비 현황
   - 필터 & 검색 기능

3. **장비 상세 조회**
   - 장비별 상세 정보
   - 과거 오류 내역
   - 부품 교체 이력
   - 예방 점검 일정

4. **데이터 입력 (모바일 최적화)**
   - 작업 정보 입력
   - QR 코드 스캔 기능
   - 실시간 데이터 동기화

5. **보고서 및 통계**
   - 고장 유형 분석
   - 부품 소모 현황
   - 작업자별 통계
   - 다운타임 분석

6. **관리자 설정**
   - 사용자 관리
   - 설비 목록 관리
   - 오류 코드 관리
   - 부품 리스트 관리

## 설치 방법

1. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

2. Google Sheets API 설정:
   - Google Cloud Console에서 프로젝트 생성
   - Google Sheets API 활성화
   - 서비스 계정 생성 및 키 파일 다운로드
   - 키 파일을 `config/client_secrets.json`에 저장

3. 환경 변수 설정:
   - `.streamlit/secrets.toml` 파일 생성
   - Google Sheets 스프레드시트 ID 설정

## 실행 방법

```bash
streamlit run app.py
```

## 데이터 구조

구글 스프레드시트에 다음과 같은 시트들이 필요합니다:

1. 설비목록
2. 오류이력
3. 부품교체
4. 예방점검
5. 오류코드
6. 부품목록

## 기여 방법

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 