# 목차

1. @Next.js / React / TypeScript  
2. @Laravel PHP  
3. @Nest.js Guidelines  
    - @Nest.js Backend App  
    - @Nest.js Developer Guidelines  
4. @Next.js 14, Supabase, TailwindCSS, TypeScript  
5. @Angular Guidelines  
6. @추가 가이드라인  
    - @Flutter  
    - @Vue.js / TypeScript Best Practices  
    - @React Native / Expo  

---

## 1. Next.js / React / TypeScript

### 핵심 원칙
- **간결한 코드**: 정확한 예제와 함께 기술적인 TypeScript 코드를 작성합니다.
- **함수형/선언형 패턴**: 클래스 사용을 피하고 함수형 패러다임을 활용합니다.
- **모듈화**: 코드 중복을 피하기 위해 반복보다는 모듈화를 선호합니다.
- **명확한 변수 명명**: `isLoading`, `hasError` 등 보조 동사를 포함한 설명적인 변수 이름 사용.
- **파일 구조**: 컴포넌트, 서브컴포넌트, 헬퍼 함수, 정적 콘텐츠, 타입 파일로 구성합니다.

### 명명 규칙
- 디렉터리 이름은 소문자와 대시(`-`)로 구성 (예: `components/auth-wizard`).
- 컴포넌트는 named export를 사용합니다.

### TypeScript 사용법
- 모든 코드에 TypeScript 사용. 인터페이스를 타입보다 선호합니다.
- enum 사용 대신 map을 활용합니다.
- 함수형 컴포넌트와 TypeScript 인터페이스를 사용합니다.

### 문법 및 포매팅
- 순수 함수에는 `function` 키워드를 사용합니다.
- 조건문에 불필요한 중괄호 사용을 피하고, 간결한 구문을 사용합니다.
- 선언형 JSX 사용을 권장합니다.

### UI 및 스타일링
- Shadcn UI, Radix, TailwindCSS를 사용하여 컴포넌트와 스타일을 구성합니다.
- 모바일 우선 접근 방식을 활용한 반응형 디자인 구현.

### 성능 최적화
- `use client`, `useEffect`, `setState`의 사용을 최소화하고, React Server Components(RSC)를 선호합니다.
- 클라이언트 컴포넌트는 Suspense와 fallback을 사용해 감쌉니다.
- 비핵심 컴포넌트는 동적 로딩으로 처리합니다.
- 이미지 최적화: WebP 포맷, 사이즈 데이터 제공, lazy loading 구현.

### 주요 관례
- URL 검색 파라미터 상태 관리를 위해 `nuqs` 사용.
- Web Vitals (LCP, CLS, FID) 최적화.
- 데이터 fetching 및 상태 관리를 위해 최소한의 `use client` 사용.

---

## 2. Laravel PHP

### 핵심 원칙
- **간결한 코드**: PHP 예제와 함께 명확하고 기술적인 답변 작성.
- **Laravel 11+ 베스트 프랙티스**: 최신 Laravel 컨벤션 준수.
- **객체 지향 및 SOLID 원칙**: 의존성 주입과 서비스 컨테이너 사용.
- **모듈화**: 코드 중복을 피하고, 모듈화된 구조 유지.

### PHP/Laravel 특징
- PHP 8.2+ 기능 사용 (예: 타입 선언, match 표현식).
- PSR-12 코딩 표준 준수 및 strict typing 사용.
- Laravel의 내장 헬퍼, Eloquent ORM, 쿼리 빌더 활용.
- 오류 처리 및 로깅, 유효성 검증 구현.
- Blade 템플릿 엔진을 사용한 뷰 구성.

---

## 3. Nest.js Guidelines

### Nest.js Backend App

#### 기술 스택
- **백엔드**: Node.js + Nest.js
- **데이터베이스**: MongoDB (Mongoose ODM 사용)
- **인증**: JSON Web Tokens (JWT), SIWE

#### 워크플로우 및 코딩 표준
- 의존성 관리는 pnpm 사용.
- 모든 코드는 TypeScript로 작성하며, 변수와 함수에 명확한 타입 지정.
- Barrel import 사용, 상대경로 사용 권장.
- 에러 핸들링과 입력 검증 구현.

#### 베스트 프랙티스
- RESTful API 베스트 프랙티스 준수.
- SOLID 원칙과 모듈화된 설계 적용.
- 로직은 서비스 내부에 구현하고, 컨트롤러는 간결하게 유지.

### Nest.js Developer Guidelines

- 생성자 주입(Constructor Injection)과 분리된 서비스 사용.
- 코드 중복 방지를 위한 모듈화와 디렉터리 네이밍(소문자와 대시 사용).
- 서비스는 DI(Dependency Injection)를 통해 구현하며, 컨트롤러는 담당 영역에 집중.

---

## 4. Next.js 14, Supabase, TailwindCSS, TypeScript

- 최신 Next.js 14, Supabase, TailwindCSS, TypeScript 사용.
- 컴포넌트 이름은 kebab-case 사용 (예: `my-component.tsx`).
- React Server Components와 SSR을 우선시.
- `use client`는 작은 컴포넌트에 한정.
- 데이터 페칭 컴포넌트에 로딩 및 에러 상태 추가.
- 오류 처리와 로깅 구현, 시맨틱 HTML 요소 사용.

---

## 5. Angular Guidelines

### 핵심 원칙
- Angular 및 TypeScript 예제를 명확하고 정밀하게 제공.
- 불변성과 순수 함수를 적용.
- 컴포넌트 조합을 통한 모듈화 강조.
- 의미 있는 변수 이름 사용 및 kebab-case 파일 네이밍 준수.
- Named export를 선호.

### Angular 및 TypeScript 사용법
- 인터페이스를 사용해 데이터 구조 정의.
- `any` 타입 사용 지양, 타입 시스템을 최대한 활용.
- 파일 구성: import, 정의, 구현 순서 유지.
- 템플릿 문자열, 옵셔널 체이닝, nullish 병합 활용.
- Standalone 컴포넌트와 Angular Signals 시스템 활용.
- 서비스는 `inject` 함수를 통해 DI 처리.

### 파일 네이밍 및 코드 스타일
- 컴포넌트, 서비스, 모듈, 디렉티브, 파이프, 테스트 파일은 모두 kebab-case로 작성.
- 작은따옴표, 2칸 들여쓰기, 불변성을 위해 `const` 사용.
- Angular의 내장 기능을 활용한 오류 처리, lazy loading, 접근성 고려.

---

## 6. 추가 가이드라인

### Flutter
- Dart와 Flutter를 사용하여 클린 아키텍처 구현.
- SOLID 원칙 및 디자인 패턴 적용.
- 함수형 프로그래밍 패턴 사용과 위젯 트리 최적화.
- `const` 생성자를 사용해 재빌드를 최소화.

### Vue.js / TypeScript Best Practices
- Vue.js와 TypeScript를 활용한 간결하고 유지보수 가능한 코드 작성.
- 함수형 및 선언형 패턴 적용, 클래스 사용 최소화.
- Vue Composition API의 `<script setup>` 사용.
- TailwindCSS, Headless UI 또는 Element Plus와 연동해 반응형 디자인 구현.

### React Native / Expo
- TypeScript 기반 함수형 컴포넌트와 Hooks 사용.
- 파일은 기능별로 조직화.
- 리스트 렌더링 최적화와 일관된 스타일링 적용.
- React Navigation 등으로 네비게이션 및 이미지 최적화.
- 모든 답변은 한국어로 작성됩니다.

---

## 결론

이 문서는 [dotcursorrules.com/rules](https://dotcursorrules.com/rules)에서 제공하는 RULES를 종합하여 CURSOR RULES 프로젝트에 활용할 수 있도록 작성된 예시입니다.

---

## Streamlit 다운로드 버튼 생성

```python
import streamlit as st

st.title("CURSOR RULES 다운로드")
st.write("아래 버튼을 클릭하면 전체 RULES 문서를 텍스트 파일로 다운로드할 수 있습니다.")
st.download_button(
    label="Download CURSOR RULES",
    data=rules_content,
    file_name="CURSOR_RULES.txt",
    mime="text/plain"
)
