# 설비 관리 시스템

설비의 상태를 모니터링하고 관리하는 웹 기반 시스템입니다.

## 주요 기능

- 실시간 설비 상태 모니터링
- 설비 고장 이력 관리
- 부품 교체 이력 관리
- 통계 및 보고서 생성
- 관리자 설정

## 시스템 요구사항

- Python 3.8 이상
- Streamlit
- Supabase

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/Jinuk-Cho/equipment-management.git
cd equipment-management
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 Supabase 연결 정보를 입력:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 실행 방법

```bash
streamlit run app.py
```

웹 브라우저에서 자동으로 애플리케이션이 열립니다. (기본 주소: http://localhost:8501)

## 로그인 정보

- 아이디: admin
- 비밀번호: admin

## 세션 관리

- 로그인 세션 유지 시간: 12시간
- 브라우저 새로고침 후에도 세션 유지
- 세션 만료 시 자동 로그아웃

## 주요 구성 요소

- `app.py`: 메인 애플리케이션
- `components/`: 각 기능별 컴포넌트
  - `dashboard.py`: 대시보드
  - `equipment_detail.py`: 설비 상세 정보
  - `data_input.py`: 데이터 입력
  - `reports.py`: 보고서
  - `admin.py`: 관리자 설정

## 데이터베이스 구조

### 테이블 구조

1. equipment_list (설비 목록)
   - id
   - equipment_number (설비번호)
   - building (건물)
   - equipment_type (설비유형)
   - status (상태)

2. error_history (고장 이력)
   - id
   - timestamp (발생시간)
   - equipment_number (설비번호)
   - error_code (에러코드)
   - error_detail (에러상세)
   - repair_time (수리시간)
   - repair_method (수리방법)
   - worker (작업자)
   - supervisor (관리자)

3. parts_replacement (부품 교체)
   - id
   - timestamp (교체시간)
   - equipment_number (설비번호)
   - part_code (부품코드)
   - worker (작업자)
   - supervisor (관리자)

4. error_codes (에러 코드)
   - id
   - error_code (에러코드)
   - description (설명)
   - error_type (에러유형)

5. parts_list (부품 목록)
   - id
   - part_code (부품코드)
   - part_name (부품명)
   - stock (재고)

## 라이선스

MIT License 