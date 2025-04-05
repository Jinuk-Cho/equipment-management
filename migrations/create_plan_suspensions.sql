-- plan_suspensions 테이블 생성
CREATE TABLE IF NOT EXISTS public.plan_suspensions (
    id SERIAL PRIMARY KEY,
    equipment_number VARCHAR(50) NOT NULL,
    plan_id VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- '설비 PM' 또는 '모델 변경'
    start_date DATE NOT NULL,
    estimated_end_date DATE,
    end_date DATE,
    reason TEXT,
    responsible_person VARCHAR(100),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    building VARCHAR(50), -- A동, B동 등 건물 정보
    model_from VARCHAR(100), -- 모델 변경 시 기존 모델
    model_to VARCHAR(100), -- 모델 변경 시 신규 모델
    process_name VARCHAR(100), -- 공정명
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_plan_suspensions_equipment_number ON public.plan_suspensions(equipment_number);
CREATE INDEX IF NOT EXISTS idx_plan_suspensions_status ON public.plan_suspensions(status);
CREATE INDEX IF NOT EXISTS idx_plan_suspensions_type ON public.plan_suspensions(type);

-- 설명 추가
COMMENT ON TABLE public.plan_suspensions IS '설비 정지 계획 정보 테이블';
COMMENT ON COLUMN public.plan_suspensions.id IS '고유 식별자';
COMMENT ON COLUMN public.plan_suspensions.equipment_number IS '설비 번호';
COMMENT ON COLUMN public.plan_suspensions.plan_id IS '계획 식별자';
COMMENT ON COLUMN public.plan_suspensions.type IS '정지 유형 (설비 PM 또는 모델 변경)';
COMMENT ON COLUMN public.plan_suspensions.start_date IS '정지 시작일';
COMMENT ON COLUMN public.plan_suspensions.estimated_end_date IS '예상 종료일';
COMMENT ON COLUMN public.plan_suspensions.end_date IS '실제 종료일 (종료되지 않은 경우 NULL)';
COMMENT ON COLUMN public.plan_suspensions.reason IS '정지 사유';
COMMENT ON COLUMN public.plan_suspensions.responsible_person IS '담당자';
COMMENT ON COLUMN public.plan_suspensions.status IS '상태 (ACTIVE, COMPLETED 등)';
COMMENT ON COLUMN public.plan_suspensions.building IS '건물 정보 (A동, B동 등)';
COMMENT ON COLUMN public.plan_suspensions.model_from IS '모델 변경 시 기존 모델';
COMMENT ON COLUMN public.plan_suspensions.model_to IS '모델 변경 시 신규 모델';
COMMENT ON COLUMN public.plan_suspensions.process_name IS '공정명';
COMMENT ON COLUMN public.plan_suspensions.created_at IS '생성 일시';
COMMENT ON COLUMN public.plan_suspensions.updated_at IS '수정 일시';

-- 갱신 트리거 추가
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_plan_suspensions_updated_at
BEFORE UPDATE ON public.plan_suspensions
FOR EACH ROW
EXECUTE FUNCTION update_modified_column(); 