# 설비 관리 시스템 / Hệ thống quản lý thiết bị

한국어와 베트남어를 지원하는 설비 관리 시스템입니다. 이 시스템은 제조 환경에서 설비의 상태, 고장 내역, 부품 교체 이력 등을 관리하고 모니터링하는 데 사용됩니다.

## 주요 기능

- **대시보드**: 설비 상태, 고장 유형, 부품 교체 현황 등을 한눈에 확인
- **설비 상세**: 각 설비별 상세 정보와 고장 이력, 부품 교체 이력 조회
- **데이터 입력**: 설비 고장 및 부품 교체 데이터 입력
- **보고서**: 다양한 통계 보고서 생성 및 조회
- **관리자 설정**: 사용자, 설비, 오류 코드, 부품 관리
- **계획 관리**: 설비 점검 및 유지보수 계획 수립과 실행 관리
- **알림 시스템**: 고장 발생 및 유지보수 일정 알림

## 기술 스택

- **Frontend/Backend**: Streamlit
- **데이터 처리**: Pandas
- **시각화**: Plotly
- **다국어 지원**: 한국어, 베트남어

## 실행 방법

1. 필요한 패키지 설치:
   ```
   pip install -r requirements.txt
   ```

2. 애플리케이션 실행:
   ```
   streamlit run app.py
   ```

## 개발자

이 애플리케이션은 한국-베트남 협력 프로젝트의 일환으로 개발되었습니다.

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

### Frontend 구조
- `app.py`: 메인 애플리케이션
- `components/`: 각 기능별 컴포넌트
  - `dashboard.py`: 대시보드
  - `equipment_detail.py`: 설비 상세 정보
  - `data_input.py`: 데이터 입력
  - `reports.py`: 보고서
  - `admin.py`: 관리자 설정
  - `plan_management.py`: 계획 관리
  - `notification.py`: 알림 관리
  - `common/`: 공통 컴포넌트
    - `header.py`: 헤더 컴포넌트
    - `sidebar.py`: 사이드바 컴포넌트
    - `footer.py`: 푸터 컴포넌트

### Backend 구조
- `services/`: 비즈니스 로직
  - `auth_service.py`: 인증 관련 서비스
  - `equipment_service.py`: 설비 관련 서비스
  - `plan_service.py`: 계획 관련 서비스
  - `notification_service.py`: 알림 관련 서비스
- `utils/`: 유틸리티 함수
  - `database.py`: 데이터베이스 연결 및 쿼리
  - `logger.py`: 로깅 유틸리티
  - `validators.py`: 입력 검증

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

6. maintenance_plans (유지보수 계획)
   - id
   - plan_code (계획코드)
   - equipment_number (설비번호)
   - plan_type (계획유형)
   - start_date (시작일)
   - end_date (종료일)
   - status (상태)
   - created_by (생성자)
   - updated_at (수정일시)

7. plan_details (계획 상세)
   - id
   - plan_code (계획코드)
   - task_description (작업설명)
   - assigned_worker (담당자)
   - estimated_time (예상시간)
   - completion_status (완료상태)

8. notifications (알림)
   - id
   - notification_type (알림유형)
   - target_user (대상사용자)
   - message (메시지)
   - created_at (생성시간)
   - read_status (읽음상태)

## API 엔드포인트

### 설비 관련
- GET /api/equipment - 설비 목록 조회
- GET /api/equipment/{id} - 설비 상세 조회
- POST /api/equipment - 설비 등록
- PUT /api/equipment/{id} - 설비 정보 수정
- DELETE /api/equipment/{id} - 설비 삭제

### 계획 관련
- GET /api/plans - 계획 목록 조회
- POST /api/plans - 계획 등록
- PUT /api/plans/{id} - 계획 수정
- DELETE /api/plans/{id} - 계획 삭제
- PUT /api/plans/{id}/status - 계획 상태 변경

### 알림 관련
- GET /api/notifications - 알림 목록 조회
- PUT /api/notifications/{id}/read - 알림 읽음 처리
- DELETE /api/notifications/{id} - 알림 삭제

## 상태 코드

### 설비 상태
- NORMAL: 정상 가동
- WARNING: 주의 필요
- ERROR: 고장
- MAINTENANCE: 유지보수 중
- STOPPED: 가동 중지

### 계획 상태
- DRAFT: 초안
- SCHEDULED: 예정됨
- IN_PROGRESS: 진행 중
- COMPLETED: 완료
- CANCELLED: 취소됨
- SUSPENDED: 일시 중지

## 에러 처리

### 공통 에러 코드
- E001: 인증 오류
- E002: 권한 없음
- E003: 잘못된 요청
- E004: 리소스 없음
- E005: 서버 오류

## 라이선스

MIT License 