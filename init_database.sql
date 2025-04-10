-- 시퀀스 및 확장 기능 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    department VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- 설비 테이블
CREATE TABLE IF NOT EXISTS equipment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_number VARCHAR(50) UNIQUE NOT NULL,
    serial_number VARCHAR(50),
    equipment_type VARCHAR(100) NOT NULL,
    building VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT '정상',
    installation_date DATE DEFAULT NOW()
);

-- 오류 코드 테이블
CREATE TABLE IF NOT EXISTS error_codes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    error_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    error_type VARCHAR(50) NOT NULL
);

-- 부품 테이블
CREATE TABLE IF NOT EXISTS parts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    part_code VARCHAR(20) UNIQUE NOT NULL,
    part_name VARCHAR(100) NOT NULL,
    stock INTEGER DEFAULT 0
);

-- 고장 이력 테이블
CREATE TABLE IF NOT EXISTS error_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id UUID REFERENCES equipment(id),
    error_code_id UUID REFERENCES error_codes(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    equipment_number VARCHAR(50),
    serial_number VARCHAR(50),
    repair_time INTEGER NOT NULL,
    repair_method TEXT,
    worker_id UUID REFERENCES users(id),
    supervisor_id UUID REFERENCES users(id),
    worker VARCHAR(100),
    supervisor VARCHAR(100),
    error_code VARCHAR(20),
    error_detail TEXT,
    image_paths TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 부품 교체 이력 테이블
CREATE TABLE IF NOT EXISTS parts_replacement (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id UUID REFERENCES equipment(id),
    part_id UUID REFERENCES parts(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    equipment_number VARCHAR(50),
    serial_number VARCHAR(50),
    worker_id UUID REFERENCES users(id),
    supervisor_id UUID REFERENCES users(id),
    worker VARCHAR(100),
    supervisor VARCHAR(100),
    part_code VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

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

-- 시리얼 번호 매핑 테이블
CREATE TABLE IF NOT EXISTS equipment_serials (
    id SERIAL PRIMARY KEY,
    equipment_number INTEGER UNIQUE NOT NULL,
    serial_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 시리얼 번호 데이터 추가 (최초 50개)
INSERT INTO equipment_serials (equipment_number, serial_number) VALUES
(1, '800-001'), (2, '800-002'), (3, '800-003'), (4, '800-004'), (5, '800-005'),
(6, '800-006'), (7, '800-007'), (8, '800-008'), (9, '800-009'), (10, '800-010'),
(11, '800-011'), (12, '800-012'), (13, '800-013'), (14, '800-014'), (15, '800-015'),
(16, '800-016'), (17, '800-017'), (18, '800-018'), (19, '800-019'), (20, '800-020'),
(21, '800-021'), (22, '800-022'), (23, '800-023'), (24, '800-024'), (25, '800-025'),
(26, '800-026'), (27, '800-027'), (28, '800-028'), (29, '800-029'), (30, '800-030'),
(31, '800-031'), (32, '800-032'), (33, '800-033'), (34, '800-034'), (35, '800-035'),
(36, '800-036'), (37, '800-037'), (38, '800-038'), (39, '800-039'), (40, '800-040'),
(41, '800-041'), (42, '800-042'), (43, '800-043'), (44, '800-044'), (45, '800-045'),
(46, '800-046'), (47, '800-047'), (48, '800-048'), (49, '800-049'), (50, '800-050')
ON CONFLICT (equipment_number) DO UPDATE
SET serial_number = EXCLUDED.serial_number;

-- 모든 테이블에 RLS 활성화
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE equipment ENABLE ROW LEVEL SECURITY;
ALTER TABLE error_codes ENABLE ROW LEVEL SECURITY;
ALTER TABLE parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE error_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE parts_replacement ENABLE ROW LEVEL SECURITY;
ALTER TABLE equipment_stops ENABLE ROW LEVEL SECURITY;
ALTER TABLE equipment_serials ENABLE ROW LEVEL SECURITY;

-- 관리자는 모든 테이블에 대한 모든 권한 부여
CREATE POLICY admin_all_users ON users FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY admin_all_equipment ON equipment FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY admin_all_error_codes ON error_codes FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY admin_all_parts ON parts FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY admin_all_error_history ON error_history FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY admin_all_parts_replacement ON parts_replacement FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY admin_all_equipment_stops ON equipment_stops FOR ALL TO authenticated USING (
    auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

CREATE POLICY "Public equipment_serials access" ON equipment_serials FOR SELECT USING (true);
CREATE POLICY "Authenticated users can insert equipment_serials" ON equipment_serials FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Users can update their own equipment_serials" ON equipment_serials FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admins can delete equipment_serials" ON equipment_serials FOR DELETE USING (auth.role() = 'authenticated' AND (SELECT role FROM users WHERE id = auth.uid()) = 'admin');

-- 일반 사용자 정책 설정
CREATE POLICY read_all_equipment ON equipment FOR SELECT TO authenticated USING (true);
CREATE POLICY read_all_error_codes ON error_codes FOR SELECT TO authenticated USING (true);
CREATE POLICY read_all_parts ON parts FOR SELECT TO authenticated USING (true);

-- 사용자는 자신의 프로필만 볼 수 있음
CREATE POLICY read_own_user_profile ON users FOR SELECT TO authenticated USING (
    auth.uid() = id OR auth.uid() IN (SELECT id FROM users WHERE role = 'admin')
);

-- 사용자는 자신의 프로필만 수정할 수 있음
CREATE POLICY update_own_user_profile ON users FOR UPDATE TO authenticated USING (
    auth.uid() = id
);

-- 오류 이력 및 부품 교체 이력 읽기 정책
CREATE POLICY read_all_error_history ON error_history FOR SELECT TO authenticated USING (true);
CREATE POLICY read_all_parts_replacement ON parts_replacement FOR SELECT TO authenticated USING (true);
CREATE POLICY read_all_equipment_stops ON equipment_stops FOR SELECT TO authenticated USING (true);

-- 오류 이력 및 부품 교체 이력 생성 정책
CREATE POLICY insert_error_history ON error_history FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY insert_parts_replacement ON parts_replacement FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY insert_equipment_stops ON equipment_stops FOR INSERT TO authenticated WITH CHECK (true);

-- 부품 교체시 재고 자동 감소 트리거
CREATE OR REPLACE FUNCTION decrease_part_stock()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE parts
  SET stock = stock - 1
  WHERE id = NEW.part_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 트리거 생성
DROP TRIGGER IF EXISTS after_parts_replacement_insert ON parts_replacement;
CREATE TRIGGER after_parts_replacement_insert
AFTER INSERT ON parts_replacement
FOR EACH ROW EXECUTE FUNCTION decrease_part_stock();

-- 관리자 계정 생성
INSERT INTO users (id, email, name, role, created_at)
VALUES (
    '00000000-0000-0000-0000-000000000000',
    'admin@example.com',
    '관리자',
    'admin',
    NOW()
) ON CONFLICT (id) DO NOTHING;

-- 샘플 데이터 생성
-- 설비 데이터
INSERT INTO equipment (equipment_number, serial_number, equipment_type, building, status) VALUES
('EQ001', '800-001', '프레스', 'A동', '정상'),
('EQ002', '800-002', '컨베이어', 'A동', '점검중'),
('EQ003', '800-003', '로봇', 'B동', '정상'),
('EQ004', '800-004', '프레스', 'B동', '고장'),
('EQ005', '800-005', '컨베이어', 'C동', '정상')
ON CONFLICT (equipment_number) DO NOTHING;

-- 오류 코드 데이터
INSERT INTO error_codes (error_code, description, error_type) VALUES
('E001', '모터 과열', '모터'),
('E002', '센서 고장', '센서'),
('E003', '전원 문제', '전기'),
('E004', '제어기 오류', '제어'),
('E005', '기계적 고장', '기계')
ON CONFLICT (error_code) DO NOTHING;

-- 부품 데이터
INSERT INTO parts (part_code, part_name, stock) VALUES
('P001', '모터', 10),
('P002', '센서', 15),
('P003', '전원 모듈', 8),
('P004', '제어기', 5),
('P005', '베어링', 20)
ON CONFLICT (part_code) DO NOTHING;

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_equipment_serials_equipment_number ON equipment_serials(equipment_number);
CREATE INDEX IF NOT EXISTS idx_equipment_serials_serial_number ON equipment_serials(serial_number); 