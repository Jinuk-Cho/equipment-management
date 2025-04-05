CREATE TABLE plan_suspensions (
    id SERIAL PRIMARY KEY,
    plan_code VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (plan_code) REFERENCES maintenance_plans(plan_code)
);

CREATE INDEX idx_plan_suspensions_plan_code ON plan_suspensions(plan_code);
CREATE INDEX idx_plan_suspensions_dates ON plan_suspensions(start_date, end_date); 