-- 설비 정지 이력 테이블
CREATE TABLE IF NOT EXISTS equipment_stops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id UUID REFERENCES equipment(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    equipment_number VARCHAR(50),
    serial_number VARCHAR(50),
    stop_reason VARCHAR(100) NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER NOT NULL,
    details TEXT,
    worker VARCHAR(100),
    supervisor VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 활성화
ALTER TABLE equipment_stops ENABLE ROW LEVEL SECURITY;

-- 관리자 정책 - 모든 작업 허용
CREATE POLICY admin_all_equipment_stops ON equipment_stops FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

-- 일반 사용자 정책 - 읽기 허용
CREATE POLICY read_all_equipment_stops ON equipment_stops FOR SELECT TO authenticated USING (true);

-- 일반 사용자 정책 - 데이터 추가 허용
CREATE POLICY insert_equipment_stops ON equipment_stops FOR INSERT TO authenticated WITH CHECK (true);
