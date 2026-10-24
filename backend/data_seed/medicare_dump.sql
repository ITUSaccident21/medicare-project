-- ==============================================================================
-- Bản sao lưu dữ liệu CSDL MediCare (Offline Backup Dump)
-- Dùng để phục hồi dữ liệu chạy offline trên localhost:5432 khi demo
-- ==============================================================================

-- 1. Bảng hoạt chất chuẩn
INSERT INTO active_ingredients (id, inn_name, atc_code, drug_class) VALUES
(1, 'Paracetamol', 'N02BE01', 'Giảm đau, hạ sốt'),
(2, 'Ibuprofen', 'M01AE01', 'Kháng viêm không steroid (NSAID)'),
(3, 'Aspirin', 'B01AC06', 'Chống kết tập tiểu cầu, NSAID'),
(4, 'Amlodipine', 'C08CA01', 'Chẹn kênh canxi (Hạ áp)'),
(5, 'Phenylephrine', 'R01AA04', 'Co mạch, chống sung huyết mũi')
ON CONFLICT (id) DO NOTHING;

-- 2. Bảng biệt dược
INSERT INTO brand_names (id, brand_name, dosage_form) VALUES
(1, 'Panadol Extra', 'Viên nén'),
(2, 'Decolgen Forte', 'Viên nén'),
(3, 'Amlor 5mg', 'Viên nang')
ON CONFLICT (id) DO NOTHING;

-- 3. Bảng quy tắc tương tác (Aspirin < Ibuprofen)
INSERT INTO drug_drug_interactions (ingredient_a_id, ingredient_b_id, severity, mechanism, clinical_management) VALUES
(2, 3, 'RED', 'Tăng nguy cơ xuất huyết tiêu hóa và loét dạ dày', 'Tránh phối hợp đồng thời. Tham khảo ý kiến bác sĩ.')
ON CONFLICT (ingredient_a_id, ingredient_b_id) DO NOTHING;
