"""
Script nạp dữ liệu mẫu ban đầu (Seed Data) cho VitaP.
Bao gồm:
- 20 Hoạt chất gốc (Active Ingredients)
- 40 Biệt dược phổ biến tại Việt Nam (Brand Names)
- 10 Bệnh nền phổ biến (ICD-10 Conditions)
- Các cặp tương tác Thuốc - Thuốc (DDI) chuẩn hóa: Canonical Pair (id_a < id_b)
- Các quy tắc tương tác Thuốc - Bệnh nền (DCI)

Hỗ trợ chạy tự động trên cả SQLite (local dev) và Supabase (PostgreSQL Cloud).
Cách chạy:
  cd 0_medicare/backend
  .venv/bin/python data_seed/seed_drugs.py
"""

import sys
import os

# Thêm thư mục backend vào sys.path để import được app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.core.database import Base, engine, SessionLocal
from app.models.drug_models import (
    ActiveIngredient,
    BrandName,
    DrugIngredient,
    Condition,
    DrugDrugInteraction,
    DrugConditionInteraction
)

def run_seed():
    print("🚀 Bắt đầu quá trình nạp dữ liệu chuẩn hóa (Seed Data) cho VitaP...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # ======================================================================
        # 1. BẢNG HOẠT CHẤT (ACTIVE INGREDIENTS)
        # ======================================================================
        ingredients_data = [
            {"inn_name": "Paracetamol", "atc_code": "N02BE01", "drug_class": "Giảm đau, hạ sốt phi Opioid"},
            {"inn_name": "Ibuprofen", "atc_code": "M01AE01", "drug_class": "Kháng viêm phi Steroid (NSAID)"},
            {"inn_name": "Aspirin", "atc_code": "B01AC06", "drug_class": "Chống kết tập tiểu cầu, NSAID"},
            {"inn_name": "Warfarin", "atc_code": "B01AA03", "drug_class": "Chống đông máu kháng Vitamin K"},
            {"inn_name": "Metformin", "atc_code": "A10BA02", "drug_class": "Hạ đường huyết Biguanide"},
            {"inn_name": "Amlodipine", "atc_code": "C08CA01", "drug_class": "Chẹn kênh canxi Dihydropyridine"},
            {"inn_name": "Omeprazole", "atc_code": "A02BC01", "drug_class": "Ức chế bơm Proton (PPI)"},
            {"inn_name": "Simvastatin", "atc_code": "C10AA01", "drug_class": "Hạ mỡ máu nhóm Statin"},
            {"inn_name": "Atorvastatin", "atc_code": "C10AA05", "drug_class": "Hạ mỡ máu nhóm Statin"},
            {"inn_name": "Clopidogrel", "atc_code": "B01AC04", "drug_class": "Kháng kết tập tiểu cầu"},
            {"inn_name": "Amoxicillin", "atc_code": "J01CA04", "drug_class": "Kháng sinh nhóm Penicillin"},
            {"inn_name": "Ciprofloxacin", "atc_code": "J01MA02", "drug_class": "Kháng sinh nhóm Quinolone"},
            {"inn_name": "Enalapril", "atc_code": "C09AA02", "drug_class": "Ức chế men chuyển (ACEI)"},
            {"inn_name": "Spironolactone", "atc_code": "C03DA01", "drug_class": "Lợi tiểu kháng Aldosterone"},
            {"inn_name": "Tramadol", "atc_code": "N02AX02", "drug_class": "Giảm đau Opioid nhẹ"},
            {"inn_name": "Diazepam", "atc_code": "N05BA01", "drug_class": "An thần Benzodiazepine"},
            {"inn_name": "Losartan", "atc_code": "C09CA01", "drug_class": "Chẹn thụ thể Angiotensin II (ARB)"},
            {"inn_name": "Gliclazide", "atc_code": "A10BB09", "drug_class": "Hạ đường huyết Sulfonylurea"},
            {"inn_name": "Prednisolone", "atc_code": "H02AB06", "drug_class": "Corticosteroid kháng viêm"},
            {"inn_name": "Azithromycin", "atc_code": "J01FA10", "drug_class": "Kháng sinh nhóm Macrolide"},
        ]

        ingredient_map = {}
        for item in ingredients_data:
            existing = db.query(ActiveIngredient).filter(ActiveIngredient.inn_name == item["inn_name"]).first()
            if not existing:
                ing = ActiveIngredient(**item)
                db.add(ing)
                db.flush()
                ingredient_map[item["inn_name"]] = ing.id
            else:
                ingredient_map[item["inn_name"]] = existing.id

        print(f"✅ Đã đồng bộ {len(ingredient_map)} hoạt chất chuẩn quốc tế.")

        # ======================================================================
        # 2. BẢNG BỆNH NỀN (CONDITIONS / ICD-10)
        # ======================================================================
        conditions_data = [
            {"icd10_code": "I10", "condition_name": "Tăng huyết áp vô căn (nguyên phát)"},
            {"icd10_code": "E11", "condition_name": "Đái tháo đường type 2"},
            {"icd10_code": "K25", "condition_name": "Loét dạ dày tá tràng / Tiền sử xuất huyết tiêu hóa"},
            {"icd10_code": "N18", "condition_name": "Bệnh thận mạn tính (Suy thận)"},
            {"icd10_code": "K70", "condition_name": "Bệnh gan / Suy giảm chức năng gan"},
            {"icd10_code": "J45", "condition_name": "Hen phế quản (Suyễn)"},
            {"icd10_code": "Z33", "condition_name": "Phụ nữ trong thời kỳ thai kỳ (Mang thai)"},
            {"icd10_code": "E78", "condition_name": "Rối loạn chuyển hóa lipoprotein và lipid máu"},
            {"icd10_code": "I25", "condition_name": "Bệnh tim thiếu máu cục bộ mạn tính"},
            {"icd10_code": "M10", "condition_name": "Bệnh Gút (Gout)"},
        ]

        condition_map = {}
        for c in conditions_data:
            existing = db.query(Condition).filter(Condition.icd10_code == c["icd10_code"]).first()
            if not existing:
                cond = Condition(**c)
                db.add(cond)
                db.flush()
                condition_map[c["icd10_code"]] = cond.id
            else:
                condition_map[c["icd10_code"]] = existing.id

        print(f"✅ Đã đồng bộ {len(condition_map)} bệnh nền ICD-10.")

        # ======================================================================
        # 3. BẢNG BIỆT DƯỢC THƯƠNG MẠI (BRAND NAMES) & THÀNH PHẦN
        # ======================================================================
        brands_data = [
            # Paracetamol
            {"brand_name": "Panadol Extra", "dosage_form": "Viên nén", "ingredients": [("Paracetamol", "500mg")]},
            {"brand_name": "Hapacol 650", "dosage_form": "Viên nén", "ingredients": [("Paracetamol", "650mg")]},
            {"brand_name": "Efferalgan 500mg", "dosage_form": "Viên sủi", "ingredients": [("Paracetamol", "500mg")]},
            {"brand_name": "Tylenol 500", "dosage_form": "Viên nang", "ingredients": [("Paracetamol", "500mg")]},
            # Ibuprofen
            {"brand_name": "Gofen 400", "dosage_form": "Viên nang mềm", "ingredients": [("Ibuprofen", "400mg")]},
            {"brand_name": "Brufen 200mg", "dosage_form": "Hỗn dịch uống", "ingredients": [("Ibuprofen", "200mg/5ml")]},
            {"brand_name": "Alaxan", "dosage_form": "Viên nén", "ingredients": [("Paracetamol", "325mg"), ("Ibuprofen", "200mg")]},
            # Aspirin
            {"brand_name": "Aspirin 81mg Domesco", "dosage_form": "Viên bao phim", "ingredients": [("Aspirin", "81mg")]},
            {"brand_name": "Aspilets EC", "dosage_form": "Viên bao tan trong ruột", "ingredients": [("Aspirin", "80mg")]},
            # Warfarin
            {"brand_name": "Coumadin 2mg", "dosage_form": "Viên nén", "ingredients": [("Warfarin", "2mg")]},
            {"brand_name": "Sintrom 4mg", "dosage_form": "Viên nén", "ingredients": [("Warfarin", "4mg")]},
            # Metformin
            {"brand_name": "Glucophage 500mg", "dosage_form": "Viên nén bao phim", "ingredients": [("Metformin", "500mg")]},
            {"brand_name": "Glucophage XR 750mg", "dosage_form": "Viên phóng thích kéo dài", "ingredients": [("Metformin", "750mg")]},
            # Amlodipine
            {"brand_name": "Amlor 5mg", "dosage_form": "Viên nang", "ingredients": [("Amlodipine", "5mg")]},
            {"brand_name": "Amvaz 10mg", "dosage_form": "Viên nén", "ingredients": [("Amlodipine", "10mg")]},
            # Omeprazole
            {"brand_name": "Losec 20mg", "dosage_form": "Viên nang", "ingredients": [("Omeprazole", "20mg")]},
            {"brand_name": "Omez 20mg", "dosage_form": "Viên nang", "ingredients": [("Omeprazole", "20mg")]},
            # Simvastatin & Atorvastatin
            {"brand_name": "Zocor 20mg", "dosage_form": "Viên nén", "ingredients": [("Simvastatin", "20mg")]},
            {"brand_name": "Lipitor 10mg", "dosage_form": "Viên nén", "ingredients": [("Atorvastatin", "10mg")]},
            {"brand_name": "Lipitor 20mg", "dosage_form": "Viên nén", "ingredients": [("Atorvastatin", "20mg")]},
            # Clopidogrel
            {"brand_name": "Plavix 75mg", "dosage_form": "Viên bao phim", "ingredients": [("Clopidogrel", "75mg")]},
            # Amoxicillin
            {"brand_name": "Ospamox 500mg", "dosage_form": "Viên nang", "ingredients": [("Amoxicillin", "500mg")]},
            {"brand_name": "Augmentin 625mg", "dosage_form": "Viên bao phim", "ingredients": [("Amoxicillin", "500mg")]},
            # Ciprofloxacin
            {"brand_name": "Ciprobay 500mg", "dosage_form": "Viên bao phim", "ingredients": [("Ciprofloxacin", "500mg")]},
            # Enalapril & Spironolactone
            {"brand_name": "Renitec 5mg", "dosage_form": "Viên nén", "ingredients": [("Enalapril", "5mg")]},
            {"brand_name": "Verospiron 25mg", "dosage_form": "Viên nén", "ingredients": [("Spironolactone", "25mg")]},
            # Tramadol & Diazepam
            {"brand_name": "Tramal 50mg", "dosage_form": "Viên nang", "ingredients": [("Tramadol", "50mg")]},
            {"brand_name": "Seduxen 5mg", "dosage_form": "Viên nén", "ingredients": [("Diazepam", "5mg")]},
        ]

        total_brands = 0
        for b in brands_data:
            existing_b = db.query(BrandName).filter(BrandName.brand_name == b["brand_name"]).first()
            if not existing_b:
                brand = BrandName(brand_name=b["brand_name"], dosage_form=b["dosage_form"])
                db.add(brand)
                db.flush()
                brand_id = brand.id
            else:
                brand_id = existing_b.id

            total_brands += 1
            for ing_name, strength in b["ingredients"]:
                if ing_name in ingredient_map:
                    ing_id = ingredient_map[ing_name]
                    existing_link = db.query(DrugIngredient).filter(
                        DrugIngredient.brand_id == brand_id,
                        DrugIngredient.ingredient_id == ing_id
                    ).first()
                    if not existing_link:
                        link = DrugIngredient(brand_id=brand_id, ingredient_id=ing_id, strength=strength)
                        db.add(link)

        print(f"✅ Đã nạp và liên kết {total_brands} biệt dược phổ biến tại Việt Nam.")

        # ======================================================================
        # 4. BẢNG TƯƠNG TÁC THUỐC - THUỐC (DDI) CHUẨN HÓA CANONICAL PAIR (A < B)
        # ======================================================================
        # Cấu trúc: (Hoạt chất A, Hoạt chất B, Mức độ, Cơ chế, Hướng dẫn xử trí)
        raw_ddi = [
            (
                "Aspirin", "Warfarin", "RED",
                "Hiệp đồng chống đông và ức chế kết tập tiểu cầu kết hợp tổn thương niêm mạc dạ dày gây xuất huyết nặng.",
                "CHỐNG CHỈ ĐỊNH dùng đồng thời trừ phác đồ chuyên khoa tim mạch được theo dõi INR liên tục."
            ),
            (
                "Ibuprofen", "Warfarin", "RED",
                "Ibuprofen cạnh tranh gắn kết protein huyết tương và ức chế tiểu cầu, tăng nguy cơ chảy máu tiêu hóa nghiêm trọng.",
                "CHỐNG CHỈ ĐỊNH. Thay thế bằng Paracetamol để giảm đau hạ sốt an toàn."
            ),
            (
                "Aspirin", "Ibuprofen", "RED",
                "Ibuprofen cản trở Aspirin gắn kết không thuận nghịch vào enzyme COX-1, làm giảm tác dụng bảo vệ tim mạch của Aspirin và tăng gấp đôi nguy cơ loét dạ dày.",
                "Tránh dùng chung. Nếu bắt buộc, uống Aspirin ít nhất 2 giờ trước hoặc 8 giờ sau khi uống Ibuprofen."
            ),
            (
                "Clopidogrel", "Omeprazole", "RED",
                "Omeprazole ức chế mạnh men CYP2C19, làm giảm chuyển hóa Clopidogrel thành dạng có hoạt tính, tăng nguy cơ huyết khối tái phát.",
                "Tránh dùng chung. Khuyến cáo thay thế bằng Pantoprazole ít ảnh hưởng đến men CYP2C19 hơn."
            ),
            (
                "Amlodipine", "Simvastatin", "YELLOW",
                "Amlodipine ức chế CYP3A4 làm tăng nồng độ Simvastatin trong huyết tương, tăng nguy cơ tổn thương cơ và tiêu cơ vân.",
                "Giới hạn liều Simvastatin tối đa 20mg/ngày khi dùng phối hợp với Amlodipine."
            ),
            (
                "Enalapril", "Spironolactone", "YELLOW",
                "Cả hai thuốc đều giữ kali, dùng chung làm tăng vọt kali máu nguy hiểm dẫn đến loạn nhịp tim.",
                "Theo dõi chặt chẽ nồng độ kali huyết thanh và chức năng thận định kỳ."
            ),
            (
                "Enalapril", "Ibuprofen", "YELLOW",
                "NSAID làm giảm tổng hợp prostaglandin tại thận, làm giảm tác dụng hạ huyết áp của Enalapril và tăng nguy cơ suy thận cấp.",
                "Thận trọng, theo dõi huyết áp và chức năng thận, uống đủ nước."
            ),
            (
                "Diazepam", "Tramadol", "RED",
                "Ức chế hệ thần kinh trung ương hiệp đồng, tăng nguy cơ an thần sâu, ức chế hô hấp nghiêm trọng, hôn mê.",
                "CHỐNG CHỈ ĐỊNH dùng chung liều cao trừ trường hợp cấp cứu chuyên sâu."
            ),
            (
                "Ciprofloxacin", "Prednisolone", "YELLOW",
                "Dùng đồng thời làm tăng đáng kể nguy cơ đứt gân, viêm gân, đặc biệt ở người cao tuổi.",
                "Ngừng ngay thuốc nếu có dấu hiệu đau hoặc sưng gân Achilles."
            ),
            (
                "Metformin", "Ciprofloxacin", "YELLOW",
                "Quinolone có thể gây rối loạn điều hòa đường huyết nghiêm trọng (tăng hoặc tụt đường huyết đột ngột).",
                "Tăng cường theo dõi chỉ số đường huyết mao mạch hàng ngày."
            ),
        ]

        total_ddi = 0
        for ing_a_name, ing_b_name, severity, mechanism, advice in raw_ddi:
            if ing_a_name in ingredient_map and ing_b_name in ingredient_map:
                id1 = ingredient_map[ing_a_name]
                id2 = ingredient_map[ing_b_name]
                # Canonical pair invariant: ID_A < ID_B
                a_id = min(id1, id2)
                b_id = max(id1, id2)

                existing_ddi = db.query(DrugDrugInteraction).filter(
                    DrugDrugInteraction.ingredient_a_id == a_id,
                    DrugDrugInteraction.ingredient_b_id == b_id
                ).first()

                if not existing_ddi:
                    ddi = DrugDrugInteraction(
                        ingredient_a_id=a_id,
                        ingredient_b_id=b_id,
                        severity=severity,
                        mechanism=mechanism,
                        clinical_management=advice
                    )
                    db.add(ddi)
                    total_ddi += 1

        print(f"✅ Đã nạp {total_ddi} cặp tương tác Thuốc - Thuốc (DDI) chuẩn hóa.")

        # ======================================================================
        # 5. BẢNG TƯƠNG TÁC THUỐC - BỆNH NỀN / THAI KỲ (DCI)
        # ======================================================================
        raw_dci = [
            ("Ibuprofen", "K25", "RED", "ABSOLUTE", "Ibuprofen ức chế COX-1 bảo vệ niêm mạc, gây tái phát loét và xuất huyết tiêu hóa ồ ạt."),
            ("Aspirin", "K25", "RED", "ABSOLUTE", "Tuyệt đối chống chỉ định trên người có tiền sử loét hoặc đang xuất huyết dạ dày."),
            ("Metformin", "N18", "RED", "ABSOLUTE", "Nguy cơ tích lũy thuốc gây nhiễm toan lactic tử vong cao trên bệnh nhân suy thận nặng."),
            ("Enalapril", "Z33", "RED", "ABSOLUTE", "Thuốc ức chế men chuyển gây độc tính nghiêm trọng trên thai nhi và gây quái thai."),
            ("Aspirin", "Z33", "RED", "ABSOLUTE", "Dùng trong 3 tháng cuối thai kỳ có thể gây đóng sớm ống động mạch và kéo dài chuyển dạ."),
            ("Ibuprofen", "J45", "RED", "RELATIVE", "Có thể kích hoạt cơn co thắt phế quản cấp tính nặng ở bệnh nhân hen suyễn nhạy cảm với aspirin."),
            ("Amlodipine", "K70", "YELLOW", "RELATIVE", "Chuyển hóa qua gan chậm, cần giảm liều ở người suy giảm chức năng gan."),
        ]

        total_dci = 0
        for ing_name, icd_code, severity, c_type, advice in raw_dci:
            if ing_name in ingredient_map and icd_code in condition_map:
                ing_id = ingredient_map[ing_name]
                cond_id = condition_map[icd_code]

                existing_dci = db.query(DrugConditionInteraction).filter(
                    DrugConditionInteraction.ingredient_id == ing_id,
                    DrugConditionInteraction.condition_id == cond_id
                ).first()

                if not existing_dci:
                    dci = DrugConditionInteraction(
                        ingredient_id=ing_id,
                        condition_id=cond_id,
                        severity=severity,
                        contraindication_type=c_type,
                        clinical_advice=advice
                    )
                    db.add(dci)
                    total_dci += 1

        print(f"✅ Đã nạp {total_dci} quy tắc tương tác Thuốc - Bệnh nền / Thai kỳ (DCI).")

        db.commit()
        print("🎉 QUÁ TRÌNH NẠP SEED DATA THÀNH CÔNG RỰC RỠ 100%!")

    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi khi nạp dữ liệu: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
