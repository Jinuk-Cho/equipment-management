# 설비 관리 시스템 (Equipment Management System)

## 소개
이 시스템은 제조업체에서 설비 관리, 고장 추적, 부품 교체 및 보고서 생성을 위한 웹 기반 애플리케이션입니다.
Streamlit을 기반으로 구축되었으며, 다국어 지원(한국어/베트남어)을 제공합니다.

## 주요 기능
- 대시보드: 설비 상태, 고장, 부품 교체 현황 요약
- 설비 상태 모니터링: 실시간 설비 상태 및 상세 정보 제공
- 데이터 입력: 고장, 부품 교체, 모델 변경, 설비 정지 데이터 입력
- 보고서: 설비 통계, 고장 분석, 부품 소모 현황 등 다양한 보고서
- 계획 관리: 설비 점검 및 정비 계획 관리
- 관리자 설정: 사용자, 설비, 오류 코드 관리

## 기술 스택
- Frontend: Streamlit
- Backend: Python
- 데이터베이스: Supabase
- 차트: Plotly

## 설치 및 실행 방법
```bash
# 저장소 클론
git clone https://github.com/your-username/equipment-management.git
cd equipment-management

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 패키지 설치
pip install -r requirements.txt

# 애플리케이션 실행
streamlit run app.py
```

## 시스템 구조
시스템은 모듈식 구조로 설계되어 있으며, 각 기능은 별도의 컴포넌트로 구현되어 있습니다.

### 컴포넌트 구조
- `app.py`: 메인 애플리케이션
- `components/`: 각 기능별 컴포넌트
  - `dashboard.py`: 대시보드 컴포넌트
  - `equipment_detail.py`: 설비 상세 정보 컴포넌트
  - `data_input.py`: 데이터 입력 컴포넌트
  - `reports.py`: 보고서 컴포넌트
  - `admin.py`: 관리자 설정 컴포넌트
  - `plan_management.py`: 계획 관리 컴포넌트
  - `plan_suspension.py`: 계획 정지 관리 컴포넌트
  - `equipment_status_detail.py`: 설비 상태 상세 컴포넌트
  - `language.py`: 다국어 지원 모듈
- `utils/`: 유틸리티 기능
  - `supabase_client.py`: Supabase 연동 클라이언트
- `services/`: 비즈니스 로직
  - `plan_service.py`: 계획 관리 서비스

## 컴포넌트 사용 방법

### 컴포넌트 초기화
모든 컴포넌트는 언어 파라미터를 받도록 설계되어 있습니다. 컴포넌트 초기화 시 언어 코드를 전달하여 다국어 지원을 활성화할 수 있습니다.

```python
# 컴포넌트 초기화 방법
dashboard_component = DashboardComponent(lang='kr')  # 한국어
equipment_detail_component = EquipmentDetailComponent(lang='vn')  # 베트남어
```

### 언어 설정
시스템은 다음 두 가지 방법으로 언어를 설정할 수 있습니다:

1. 컴포넌트 초기화 시 언어 지정 (위 예시 참조)
2. 세션 상태를 통한 전역 언어 설정
```python
# 세션 상태로 언어 설정
st.session_state.current_lang = 'kr'  # 한국어
st.session_state.current_lang = 'vn'  # 베트남어
```

## 개발 모드
개발 중에는 개발 모드를 활성화하여 자동 로그인 기능을 사용할 수 있습니다.
```python
# app.py에서 개발 모드 설정
DEV_MODE = True  # 자동 로그인 활성화
```

## 호환성 이슈 방지 사항

### 1. 컴포넌트 초기화 시 언어 파라미터 전달
모든 컴포넌트는 언어 파라미터를 받도록 설계되어 있으며, 초기화 시 언어 코드를 제공해야 합니다.
```python
# 올바른 방법
component = ComponentClass(lang='kr')

# 잘못된 방법 (타입 오류 발생 가능)
component = ComponentClass()
```

### 2. 이미지 처리 시 RGBA 형식 처리
이미지를 처리할 때 RGBA 형식을 RGB로 변환하는 코드가 구현되어 있습니다. 이미지 업로드 시 다양한 형식을 지원합니다.

### 3. 언어 설정 일관성 유지
세션 상태와 컴포넌트 언어 설정이 일관되게 유지되도록 해야 합니다. 언어 변경 시 모든 컴포넌트에 반영되도록 구현되어 있습니다.

### 4. datetime 관련 호환성
날짜 및 시간 입력 시 `st.datetime_input` 대신 `st.date_input`과 `st.time_input`을 분리하여 사용하는 것이 호환성을 높입니다.

## 라이센스
이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요. 