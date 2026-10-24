# Tài Liệu Thiết Kế Kỹ Thuật (SDD) - Module M4: Động Cơ Kiểm Tra Tương Tác Thuốc & Cảnh Báo Dược Lý

* **Mã module:** M4 (Clinical Drug Interaction & Pharmacology Alert Engine)
* **Dự án:** MediCare - Hệ thống Hỗ trợ Thăm khám & Sổ tay Y tế Thông minh
* **Tác giả:** Nhóm MediCare (Dương Phan Minh Trí, Trương Huệ Trí, Nguyễn Bảo Trọng, Lê Thanh Phong)
* **Phiên bản:** Draft v1.1 (Đã chuẩn hóa sau phản biện Stage 7 Critic Review)
* **Ngày cập nhật:** 2026-10-25

---

## Phần 1: Bối Cảnh, Mục Tiêu & Ranh Giới Phạm Vi (Context & Scope)

### 1.1. Bối cảnh & Vấn đề Kỹ thuật
Bệnh nhân điều trị đa bệnh lý mạn tính thường xuyên đối mặt với nguy cơ tương tác thuốc nguy hiểm (Polypharmacy). Các giải pháp hiện nay thường mắc phải 2 thái cực:
1. Chỉ hiển thị bảng đối chiếu dược thư khô khan, chứa nhiều thuật ngữ học thuật mà người bệnh không hiểu được mức độ nguy hiểm thực tế đối với cơ thể mình.
2. Lạm dụng LLM lớn để phán đoán tương tác tự do, dẫn đến ảo giác (Hallucination), độ trễ cao và nghẽn hệ thống khi kiểm thử hoặc tải cao.

Module M4 giải quyết triệt để vấn đề này bằng kiến trúc **Hybrid "Rule-First, LLM-Second"** kết hợp chiến lược **Phân tầng Đa mô hình (Multi-Model Tiering)** để đảm bảo độ chính xác y khoa tuyệt đối và thời gian phản hồi tức thì.

### 1.2. Chiến lược Phân tầng Đa Mô Hình (Multi-Model Architecture)
Nhằm tránh việc tập trung toàn bộ tải xử lý vào một mô hình duy nhất (single point of failure / compute bottleneck) gây nghẽn hệ thống và làm bộ kiểm thử kéo dài, kiến trúc M4 phân tách thành 3 tầng runtime và 1 công cụ ETL ngoại tuyến:

| Tầng (Tier) | Mô hình / Công nghệ đảm nhiệm | Vai trò & Mục đích sử dụng | Độ trễ (SLA) |
| :--- | :--- | :--- | :--- |
| **Tier 0 (Lõi Xác thực)** | **Deterministic SQL Query (PostgreSQL)** | Đóng vai trò là nguồn chân lý duy nhất (Single Source of Truth - SSOT) cho toàn bộ logic đối soát tương tác Thuốc–Thuốc (DDI), Thuốc–Bệnh (DCI) và Trùng hoạt chất. | **< 15ms** |
| **Tier 1 (Suy luận Nhanh Online)** | **Gemini 1.5 Flash / Flash-8B** | Nhận kết quả xác thực từ Tier 0 và hồ sơ bệnh nhân đã khử nhận dạng để định dạng khuyến nghị y khoa tiếng Việt dễ hiểu trên giao diện Web. | **~500ms – 800ms** |
| **Tier 2 (Kiểm thử & Offline Mock)** | **Template-Based Fallback Engine (`USE_MOCK_AI=True`)** | Dùng trong `pytest`, CI GitHub Actions và chế độ offline dự phòng. Sinh lời khuyên tức thì từ template mẫu có sẵn trong DB. | **< 5ms** |
| **ETL Tooling (Tiền xử lý Ngoại tuyến)** | **Gemini 1.5 Pro / GPT-4o (Batch Run)** | Công cụ tiền xử lý dữ liệu ngoại tuyến, chỉ chạy 1 lần duy nhất lúc seed dữ liệu (dịch và chuẩn hóa 350 cặp tương tác từ DDInter sang tiếng Việt). **Tuyệt đối không gọi lúc runtime.** | **Ngoại tuyến** |

### 1.3. Mục tiêu Cụ thể (Goals)
1. **Phát hiện Trùng lặp Hoạt chất (Duplicate Therapy):** Tự động phát hiện trường hợp đơn thuốc chứa nhiều biệt dược có chung hoạt chất (nguy cơ quá liều vô ý) trước khi chạy ma trận tương tác.
2. **Đối soát Tổ hợp DDI/DCI cấp độ Hoạt chất:** Tự động phân rã biệt dược thành các hoạt chất thành phần (hỗ trợ thuốc đa hoạt chất) và truy vấn ma trận tương tác.
3. **Phân cấp Cảnh báo 4 Mức độ (Risk Hierarchy):**
   - **ĐỎ (RED - Major / Chống chỉ định tuyệt đối):** Nguy cơ tử vong, xuất huyết nặng hoặc tổn thương vĩnh viễn. Khóa giao diện yêu cầu xác nhận.
   - **VÀNG (YELLOW - Moderate / Thận trọng):** Giảm hiệu lực thuốc, cần uống cách xa nhau hoặc điều chỉnh liều.
   - **XANH (GREEN - Minor / Tương thích):** Toàn bộ các thuốc trong danh mục kiểm tra đều tương thích an toàn.
   - **XÁM (UNKNOWN_RISK / Chưa kiểm chứng):** Đơn thuốc có chứa thuốc nằm ngoài CSDL 100 hoạt chất đã kiểm duyệt (ngoài MVP), không có cảnh báo RED nhưng không thể xác nhận an toàn tuyệt đối.
4. **Tối ưu hóa Thời gian Thực thi Kiểm thử Tự động (Execution Latency Optimization):** 100% các bài test logic và API test chạy qua Tier 0 và Tier 2 với `USE_MOCK_AI=True`, đảm bảo toàn bộ test suite `pytest` hoàn thành trong **dưới 3 giây**.

### 1.4. Ranh giới Ngoài Phạm Vi (Non-Goals cho MVP)
- Không tính toán nồng độ dược động học chi tiết theo chỉ số thanh thải Creatinine thực tế hoặc mg/kg thể trọng.
- Không tự ý kê đơn thuốc thay thế hoặc chỉnh sửa liều lượng của bác sĩ.
- Không dùng LLM để suy đoán tương tác cho các thuốc nằm ngoài CSDL 100 hoạt chất đã kiểm duyệt.

---

## Phần 2: Kiến Trúc Hệ Thống, Thiết Kế CSDL 3NF & Đặc Tả API Contracts

### 2.1. Kiến Trúc Luồng Dữ Liệu Đồng Bộ Tối Ưu (Synchronous Fast REST Flow)

Trong phạm vi bản MVP, hệ thống thực thi theo một chu trình HTTP REST đồng bộ duy nhất (`POST /api/v1/ddi/check`) với cam kết SLA tổng thể dưới 1 giây: Tier 0 hoàn tất đối soát y khoa trong < 15ms, Tier 1 bổ sung khuyến nghị trong 500–800ms (nếu vượt quá ngưỡng 1.5s, hệ thống tự động fallback về template tĩnh có sẵn). Kiến trúc Streaming/SSE được ghi nhận là định hướng mở rộng cho giai đoạn Post-MVP:

```mermaid
sequenceDiagram
    autonumber
    actor User as Bệnh nhân (Web Client)
    participant UI as React Frontend
    participant API as FastAPI Gateway (M4 Router)
    participant DB as PostgreSQL (Supabase 3NF)
    participant LLM as Gemini 1.5 Flash (Tier 1)
    participant Mock as Fallback Engine (Tier 2)

    User->>UI: Nhập danh sách thuốc (Autocomplete / Tủ thuốc / OCR)
    UI->>API: POST /api/v1/ddi/check (payload danh sách thuốc & profile)
    
    rect rgb(240, 248, 255)
        note over API,DB: Giai đoạn 1: Core Verification Engine (Tier 0 - Single Batch CTE)
        API->>DB: Truy vấn Single SQL CTE (Bung Brand, Kiểm tra Trùng hoạt chất, DDI, DCI)
        DB-->>API: Trả về kết quả đối soát y khoa xác thực (< 15ms)
    end

    alt Đơn thuốc an toàn tuyệt đối (Không có cảnh báo RED / YELLOW)
        API->>Mock: Sinh thông điệp tương thích mặc định
        Mock-->>API: Trả về thông báo an toàn tức thì (< 1ms)
    else Kiểm thử / Offline mode (USE_MOCK_AI=True)
        API->>Mock: Nạp kết quả đối soát vào template tĩnh từ DB
        Mock-->>API: Trả về khuyến cáo định dạng trước (< 5ms)
    else Runtime có cảnh báo cần diễn giải (USE_MOCK_AI=False)
        API->>LLM: Gửi prompt đóng đã khử nhận dạng (PHI-Filtered Payload)
        alt Gemini phản hồi thành công (< 800ms)
            LLM-->>API: Trả về lời giải thích cá nhân hóa
        else Timeout (> 1.5s) hoặc Lỗi API
            API->>Mock: Tự động fallback về template tĩnh trong DB
            Mock-->>API: Trả về khuyến cáo an toàn dự phòng
        end
    end

    API-->>UI: Trả về JSON tổng hợp (summary, alerts, personalized_advice)
    UI-->>User: Hiển thị bảng cảnh báo giao thông (Đỏ khóa màn hình / Vàng accordion / Xám ngoài MVP)
```

---

### 2.2. Thiết Kế Cơ Sở Dữ Liệu Quan Hệ Chuẩn 3NF (PostgreSQL)

Mô hình dữ liệu giải quyết bài toán thuốc đa hoạt chất, kiểm tra trùng hoạt chất và quan hệ tương tác dược lực học có hướng:

```
┌────────────────────────┐       ┌────────────────────────┐
│  active_ingredients    │       │      brand_names       │
├────────────────────────┤       ├────────────────────────┤
│ id (PK)                │       │ id (PK)                │
│ inn_name (VARCHAR)     │       │ brand_name (VARCHAR)   │
│ atc_code (VARCHAR)     │       │ manufacturer (VARCHAR) │
│ drug_class (VARCHAR)   │       └───────────┬────────────┘
└───────────┬────────────┘                   │ 1
            │ 1                              │
            │          ┌──────────────────┐  │
            └─────────<│ drug_ingredients │>-┘ N
                     N ├──────────────────┤
                       │ brand_id (FK)    │
                       │ ingredient_id(FK)│
                       │ strength (MG/ML) │
                       └──────────────────┘
```

#### Chi tiết các bảng CSDL:

1. **Bảng `active_ingredients` (Danh mục Hoạt chất Chuẩn):**
   - `id`: SERIAL PRIMARY KEY
   - `inn_name`: VARCHAR(255) NOT NULL UNIQUE (Tên quốc tế INN: Paracetamol, Ibuprofen, Amlodipine...)
   - `atc_code`: VARCHAR(10) (Mã phân loại ATC)
   - `drug_class`: VARCHAR(100) (Nhóm dược lý: NSAID, CCB, ACEi, Kháng sinh...)

2. **Bảng `brand_names` (Biệt dược Thương mại tại Việt Nam):**
   - `id`: SERIAL PRIMARY KEY
   - `brand_name`: VARCHAR(255) NOT NULL (Panadol Extra, Decolgen Forte, Augmentin 1g...)
   - `registration_number`: VARCHAR(50) (Số đăng ký lưu hành)
   - `dosage_form`: VARCHAR(50) (Viên nén, viên sủi, dung dịch...)

3. **Bảng `drug_ingredients` (Bảng liên kết N-N: Biệt dược - Hoạt chất):**
   - `brand_id`: INT REFERENCES `brand_names(id)` ON DELETE CASCADE
   - `ingredient_id`: INT REFERENCES `active_ingredients(id)` ON DELETE RESTRICT
   - `strength`: VARCHAR(50) (Hàm lượng: 500mg, 10mg...)
   - `PRIMARY KEY (brand_id, ingredient_id)`

4. **Bảng `conditions` (Danh mục Bệnh nền & Trạng thái Sinh lý):**
   - `id`: SERIAL PRIMARY KEY
   - `icd10_code`: VARCHAR(10) NOT NULL UNIQUE (I10 - Tăng huyết áp, K25 - Loét dạ dày, O09 - Thai kỳ...)
   - `condition_name`: VARCHAR(255) NOT NULL

5. **Bảng `drug_drug_interactions` (Quy tắc Tương tác Thuốc - Thuốc):**
   - `id`: SERIAL PRIMARY KEY
   - `ingredient_a_id`: INT REFERENCES `active_ingredients(id)`
   - `ingredient_b_id`: INT REFERENCES `active_ingredients(id)`
   - `precipitant_ingredient_id`: INT REFERENCES `active_ingredients(id)` (Thuốc tác nhân gây biến đổi)
   - `object_ingredient_id`: INT REFERENCES `active_ingredients(id)` (Thuốc chịu ảnh hưởng)
   - `severity`: VARCHAR(10) NOT NULL CHECK (`severity` IN ('RED', 'YELLOW', 'GREEN'))
   - `mechanism`: TEXT NOT NULL (Cơ chế dược lý)
   - `clinical_management`: TEXT NOT NULL (Khuyến cáo xử trí y khoa mẫu cho fallback)
   - `CHECK (ingredient_a_id < ingredient_b_id)` kèm `UNIQUE (ingredient_a_id, ingredient_b_id)`

6. **Bảng `drug_condition_interactions` (Quy tắc Tương tác Thuốc - Bệnh nền / Thai kỳ):**
   - `id`: SERIAL PRIMARY KEY
   - `ingredient_id`: INT REFERENCES `active_ingredients(id)`
   - `condition_id`: INT REFERENCES `conditions(id)`
   - `severity`: VARCHAR(10) NOT NULL CHECK (`severity` IN ('RED', 'YELLOW'))
   - `contraindication_type`: VARCHAR(20) CHECK (`contraindication_type` IN ('ABSOLUTE', 'RELATIVE'))
   - `clinical_advice`: TEXT NOT NULL
   - `UNIQUE (ingredient_id, condition_id)`

---

### 2.3. Đặc Tả Giao Tiếp API Contract (Pydantic v2 Schemas)

#### Mã nguồn khai báo Pydantic Models chuẩn (`app/models/ddi_schemas.py`):

```python
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class RiskLevelEnum(str, Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    UNKNOWN_RISK = "UNKNOWN_RISK"

class InputSourceEnum(str, Enum):
    MANUAL_INPUT = "MANUAL_INPUT"
    CABINET_F2 = "CABINET_F2"
    OCR_M1 = "OCR_M1"

class DrugInputItem(BaseModel):
    brand_id: Optional[int] = Field(None, description="ID biệt dược trong CSDL (nếu chọn từ danh mục)")
    ingredient_id: Optional[int] = Field(None, description="ID hoạt chất gốc (nếu nhập theo tên generic)")
    raw_name: str = Field(..., min_length=1, description="Tên thuốc hiển thị hoặc trích xuất từ OCR")
    source: InputSourceEnum = Field(InputSourceEnum.MANUAL_INPUT, description="Nguồn trích xuất thuốc")

class PatientProfileInput(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Tuổi bệnh nhân")
    gender: str = Field(..., pattern="^(MALE|FEMALE|OTHER)$", description="Giới tính")
    condition_ids: List[int] = Field(default_factory=list, description="Danh sách ID bệnh nền (bảng conditions)")
    is_pregnant: bool = Field(False, description="Cờ đánh dấu phụ nữ đang mang thai")

class CheckInteractionRequest(BaseModel):
    drugs: List[DrugInputItem] = Field(..., min_length=1, description="Danh sách thuốc cần đối soát")
    patient_profile: PatientProfileInput = Field(..., description="Hồ sơ bệnh nền của người bệnh")

class OutOfScopeDrugItem(BaseModel):
    raw_name: str
    message: str

class DDIAlertItem(BaseModel):
    severity: RiskLevelEnum
    drug_a: str = Field(..., description="Tên biệt dược/hoạt chất A")
    drug_b: str = Field(..., description="Tên biệt dược/hoạt chất B")
    precipitant_drug: Optional[str] = Field(None, description="Thuốc tác nhân gây tương tác")
    object_drug: Optional[str] = Field(None, description="Thuốc bị ảnh hưởng nồng độ/dược lực")
    mechanism: str
    clinical_management: str

class DCIAlertItem(BaseModel):
    severity: RiskLevelEnum
    drug: str
    condition: str
    contraindication_type: str = Field(..., description="ABSOLUTE hoặc RELATIVE")
    clinical_advice: str

class DuplicateTherapyAlertItem(BaseModel):
    severity: RiskLevelEnum = RiskLevelEnum.RED
    ingredient_name: str
    involved_drugs: List[str]
    warning_message: str

class SummaryStatus(BaseModel):
    overall_risk_level: RiskLevelEnum
    total_drugs_analyzed: int
    total_ingredients_resolved: int
    out_of_scope_drugs: List[OutOfScopeDrugItem] = Field(default_factory=list)

class PersonalizedAdvice(BaseModel):
    source_engine: str = Field(..., description="GEMINI_1.5_FLASH hoặc FALLBACK_TEMPLATE_ENGINE")
    content_markdown: str
    disclaimer: str

class CheckInteractionResponse(BaseModel):
    summary: SummaryStatus
    duplicate_therapy_alerts: List[DuplicateTherapyAlertItem] = Field(default_factory=list)
    ddi_alerts: List[DDIAlertItem] = Field(default_factory=list)
    dci_alerts: List[DCIAlertItem] = Field(default_factory=list)
    personalized_advice: PersonalizedAdvice
```

#### HTTP Status Codes:
- `200 OK`: Đối soát thành công (bao gồm cả khi có cảnh báo RED hoặc thuốc out-of-scope).
- `400 Bad Request`: Payload sai quy cách (mảng `drugs` rỗng).
- `422 Unprocessable Entity`: Dữ liệu không thỏa mãn validation (tuổi âm, chuỗi rỗng).
- `500 Internal Server Error`: Lỗi kết nối CSDL PostgreSQL Supabase.

---

## Phần 3: Chi Tiết Thuật Toán Đối Soát Tổ Hợp SQL & Prompt Guardrail LLM

### 3.1. Thuật Toán Đối Soát Tổ Hợp SQL (Single Batch CTE Engine)

Quy trình đối soát được gom thành 1 câu truy vấn CTE duy nhất trên PostgreSQL nhằm triệt tiêu độ trễ mạng qua lại:

```
[Danh sách Thuốc đầu vào] 
          │
          ▼
Bước 1: Phân rã Hoạt chất & Ánh xạ Ngược (Resolver & Reverse-Map)
          │  - Ánh xạ brand_id / ingredient_id -> Danh sách ingredient_ids
          │  - Lưu bảng ánh xạ trong RAM: ingredient_to_brand_map[ing_id] = [brand_names]
          │  - Lọc ra các thuốc không có trong DB -> out_of_scope_drugs
          ▼
Bước 1.1: Quét Trùng Lặp Hoạt Chất (Duplicate Therapy Scan) - O(N)
          │  - Đếm tần suất: count(ingredient_id) trong đơn
          │  - Nếu count >= 2 từ các biệt dược khác nhau:
          │    -> Kích hoạt cảnh báo RED: "DUPLICATE_THERAPY_OVERDOSE"
          ▼
Bước 2: Sinh Tập Cặp Chuẩn Hóa Đối Xứng (Symmetric Pair Generation)
          │  - Tập hoạt chất duy nhất: Set S = {id_1, ..., id_k}
          │  - Tạo tổ hợp C(k, 2) cặp (a, b) với điều kiện bất biến: a < b
          ▼
Bước 3: Truy Vấn Batch SQL Duy Nhất (Single CTE Batch Execution)
          │  - SELECT * FROM drug_drug_interactions WHERE (ingredient_a_id, ingredient_b_id) IN (...)
          │  - UNION ALL / JOIN kiểm tra drug_condition_interactions
          ▼
Bước 4: Đánh Giá Mức Độ Nguy Cơ Tối Đa (Max Severity Triage)
             Nếu có cảnh báo RED hoặc DUPLICATE_THERAPY: overall_risk_level = RED;
             Ngược lại nếu có cảnh báo YELLOW: overall_risk_level = YELLOW;
             Ngược lại nếu len(out_of_scope_drugs) > 0: overall_risk_level = UNKNOWN_RISK;
             Ngược lại: overall_risk_level = GREEN.
```

---

### 3.2. Cấu Trúc Prompt Đóng, Bảo Mật Dữ Liệu (PHI Filter) & LLM Guardrail

#### Cơ chế Khử Nhận Dạng Dữ Liệu Y Tế (PHI Sanitization Filter):
Trước khi gửi payload tới Gemini 1.5 Flash, hệ thống thực hiện khử bỏ toàn bộ dữ liệu định danh:
- Không gửi họ tên, số điện thoại, CCCD hay mã bệnh án.
- Tuổi được chuẩn hóa theo nhóm nguy cơ: ví dụ "Bệnh nhân cao tuổi (65 tuổi)".
- Bệnh nền chỉ gửi tên nhóm bệnh chuẩn ICD-10 (ví dụ: "Tăng huyết áp vô căn", "Loét dạ dày tá tràng").

#### System Prompt & Template:
```text
VAI TRÒ VÀ NGUYÊN TẮC HOẠT ĐỘNG:
Bạn là Trợ lý Dược lý Lâm sàng MediCare. Nhiệm vụ duy nhất của bạn là biên dịch và giải thích các cảnh báo tương tác thuốc đã được xác thực từ CSDL Y tế thành lời khuyên an toàn, chuẩn mực cho người bệnh.

RÀNG BUỘC CỐT TỬ (STRICT GUARDRAILS):
1. KHÔNG ĐƯỢC TỰ Ý THÊM TƯƠNG TÁC MỚI: Bạn TUYỆT ĐỐI KHÔNG ĐƯỢC suy đoán hoặc nêu thêm bất kỳ cặp tương tác thuốc hay bệnh nền nào khác ngoài danh sách được cung cấp trong [DỮ LIỆU ĐỐI SOÁT XÁC THỰC].
2. KHÔNG THAY ĐỔI MỨC ĐỘ NGUY CƠ: Nếu dữ liệu là RED, giải thích theo mức nguy hiểm cao / cần ngừng hoặc hỏi ngay ý kiến bác sĩ. Nếu dữ liệu là YELLOW, giải thích theo hướng cần uống cách giờ hoặc theo dõi triệu chứng.
3. VĂN PHONG CHUẨN MỰC, LỊCH THIỆP: Sử dụng đại từ xưng hô phù hợp với độ tuổi của bệnh nhân (bác/cô/chú/anh/chị). Trình bày rõ ràng, ân cần nhưng nghiêm cẩn, không dùng trợ từ suồng sã.
4. KHUYẾN CÁO PHÁP LÝ BẮT BUỘC: Luôn kết thúc bằng việc nhắc nhở người bệnh tham vấn bác sĩ hoặc dược sĩ chuyên khoa trước khi thay đổi liệu trình dùng thuốc.

DỮ LIỆU ĐẦU VÀO:
- Hồ sơ bệnh nhân: Nhóm tuổi: {{age_group}}, Giới tính: {{gender}}, Bệnh nền: {{conditions}}
- Dữ liệu đối soát xác thực từ CSDL:
{{sql_interactions_json}}

HÃY XUẤT RA NỘI DUNG LỜI KHUYÊN (Định dạng Markdown):
```

---

### 3.3. Cơ Chế Template-Based Fallback Engine (Tier 2)

Động cơ dự phòng đảm bảo tính sẵn sàng cao và hỗ trợ kiểm thử tức thì:

1. **Kích hoạt tự động khi:**
   - Cờ môi trường `USE_MOCK_AI=True` (chế độ kiểm thử `pytest` hoặc CI/CD).
   - Đơn thuốc an toàn tuyệt đối (`GREEN`) -> kích hoạt Short-Circuit trả về thông điệp mặc định.
   - Hoặc Gemini API ném lỗi ngoại lệ (HTTP 429, 504, ConnectionError, Timeout > 1.5s).

2. **Thuật toán sinh văn bản mẫu tĩnh hoàn chỉnh:**
   ```python
   def generate_fallback_advice(
       duplicate_alerts: list,
       ddi_alerts: list,
       dci_alerts: list
   ) -> str:
       if not duplicate_alerts and not ddi_alerts and not dci_alerts:
           return "Hệ thống không ghi nhận tương tác nguy hiểm giữa các thuốc đã được đối soát trong danh mục."
       
       lines = ["### Cảnh báo an toàn dược phẩm quan trọng:\n"]
       
       for dup in duplicate_alerts:
           lines.append(f"- 🚨 **CẢNH BÁO TRÙNG HOẠT CHẤT ({dup.ingredient_name})**: {dup.warning_message}")
           
       for ddi in ddi_alerts:
           icon = "🚨 [NGUY CƠ CAO]" if ddi.severity == "RED" else "⚠️ [LƯU Ý]"
           lines.append(f"- {icon} **{ddi.drug_a} ✕ {ddi.drug_b}**: {ddi.clinical_management}")
           
       for dci in dci_alerts:
           icon = "🚨 [CHỐNG CHỈ ĐỊNH]" if dci.severity == "RED" else "⚠️ [THẬN TRỌNG]"
           lines.append(f"- {icon} **{dci.drug} với {dci.condition}**: {dci.clinical_advice}")
       
       lines.append("\n*Lưu ý: Thông tin trên được trích xuất từ Dược thư Y tế. Vui lòng tham vấn bác sĩ điều trị trước khi sử dụng.*")
       return "\n".join(lines)
   ```
   - **Tốc độ thực thi:** **$< 1\text{ms}$**, an toàn tuyệt đối và bảo đảm 100% test `pytest` chạy xanh ngay lập tức.

---

## Phần 4: Quản Lý Rủi Ro, Kế Hoạch Kiểm Thử (Pytest) & Triển Khai

### 4.1. Ma Trận Quản Lý Rủi Ro & Chiến Lược Giảm Thiểu

| Rủi ro Kỹ thuật / Nghiệp vụ | Mức độ | Khả năng xảy ra | Chiến lược Giảm thiểu & Phòng vệ |
| :--- | :---: | :---: | :--- |
| **1. Ngộ nhận an toàn đối với thuốc ngoài danh mục (Out-of-Scope Fallacy)** | **Rất Cao** | Cao | Gán nhãn `overall_risk_level = "UNKNOWN_RISK"`; UI hiển thị thẻ viền xám đứt đoạn thông báo rõ: *"Chưa có dữ liệu kiểm tra cho thuốc này (ngoài MVP)"*. |
| **2. Bỏ sót quá liều do trùng hoạt chất (Duplicate Therapy)** | **Rất Cao** | Cao | Bổ sung Bước 1.1 quét tần suất hoạt chất trước khi khử trùng lặp; kích hoạt cảnh báo mức RED ngay khi phát hiện $count \ge 2$. |
| **3. Bỏ sót chống chỉ định thai kỳ (`is_pregnant`)** | **Rất Cao** | Trung bình | Backend tự động ánh xạ cờ `is_pregnant=True` sang mã ICD-10 `'O09'` trong bảng `conditions`, đưa vào tập `condition_ids` đối soát DCI. |
| **4. AI Hallucination (LLM tự bịa tương tác mới)** | **Cao** | Trung bình | Áp dụng Closed-Domain Prompt và bộ lọc PHI: LLM chỉ nhận JSON kết quả đã xác thực từ CSDL, nghiêm cấm bổ sung tương tác ngoài danh sách được cung cấp. |
| **5. Nghẽn mạng / Quota Rate Limit ngày báo cáo Demo** | **Cao** | Trung bình | Tự động Fallback sang Template Engine tĩnh khi API timeout > 1.5s hoặc lỗi mạng; chuẩn bị sẵn file seed SQL chạy offline trên `localhost:5432`. |
| **6. Bộ kiểm thử chạy chậm làm nghẽn CI/CD** | **Trung bình** | Cao | 100% các ca kiểm thử trong `pytest` chạy với cờ `USE_MOCK_AI=True` (Tier 0 & Tier 2) và test DB in-memory, hoàn toàn không gọi API ra internet, bảo đảm test suite chạy xong dưới 2 giây. |

---

### 4.2. Kế Hoạch Kiểm Thử Toàn Diện (Pytest Test Suite)

#### 4.2.1. Thiết Kế Môi Trường Kiểm Thử CSDL Cục Bộ (`backend/tests/conftest.py`)
Để đảm bảo toàn bộ bộ test chạy độc lập, offline và hoàn tất trong dưới 2 giây trên GitHub Actions:
- Sử dụng SQLite in-memory (`sqlite:///:memory:`) với cấu hình tương thích hoặc PostgreSQL container cục bộ.
- Fixture `db_session` tự động nạp schema và 30 hoạt chất/thuốc mẫu (seed fixture), bọc mỗi test case trong một Transaction và tự động `rollback` sau khi hoàn thành test để dữ liệu giữa các bài test luôn cô lập.
- Fixture `client` (FastAPI `TestClient`) tiêm đè `get_db` dependency sang session test.

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    # Nạp dữ liệu seed cơ bản cho test (Decolgen, Panadol, Aspirin, Ibuprofen, ICD-10 O09, K25)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

#### 4.2.2. Danh Mục Ca Kiểm Thử Động Cơ Logic (`backend/tests/test_ddi_engine.py`):

1. **`test_detect_duplicate_therapy_overdose`:**
   - *Mục tiêu:* Kiểm tra việc phát hiện bệnh nhân uống cùng lúc 2 biệt dược chứa chung hoạt chất (*Decolgen Forte* và *Panadol Extra* đều có *Paracetamol*).
   - *Kỳ vọng:* Kích hoạt cảnh báo mức `RED`, trường `ingredient_name = "Paracetamol"`.

2. **`test_resolve_combination_drug_success`:**
   - *Mục tiêu:* Phân rã biệt dược *Decolgen Forte* thành đúng 3 hoạt chất con: Paracetamol (500mg), Phenylephrine (10mg), Chlorpheniramine (2mg).
   - *Kỳ vọng:* Trả về mảng 3 ID hoạt chất chính xác từ bảng `drug_ingredients`.

3. **`test_ddi_symmetric_query_invariance`:**
   - *Mục tiêu:* Kiểm tra tính bất biến đối xứng. Cặp (Aspirin, Ibuprofen) hay (Ibuprofen, Aspirin) đều cùng tìm ra đúng 1 quy tắc tương tác mức ĐỎ duy nhất.
   - *Kỳ vọng:* Số lượng cảnh báo trả về là 1, `severity = "RED"`.

4. **`test_dci_disease_contraindication`:**
   - *Mục tiêu:* Kiểm tra tương tác thuốc–bệnh nền giữa hoạt chất *Ibuprofen* và bệnh nền *Loét dạ dày tá tràng (K25)*.
   - *Kỳ vọng:* `contraindication_type = "ABSOLUTE"`, `severity = "RED"`.

5. **`test_dci_pregnancy_contraindication_auto_mapping`:**
   - *Mục tiêu:* Người dùng truyền `is_pregnant=True` và thuốc chống chỉ định thai kỳ (*Enalapril* hoặc *Ibuprofen* trong 3 tháng cuối).
   - *Kỳ vọng:* Backend tự động map mã ICD-10 `'O09'` vào tập `condition_ids`, kích hoạt cảnh báo `RED` chống chỉ định thai kỳ.

6. **`test_out_of_scope_isolation_and_unknown_risk`:**
   - *Mục tiêu:* Người dùng truyền vào một loại thuốc bổ không có trong CSDL (`brand_id = null`, `raw_name = "Thuốc khớp gia truyền"`).
   - *Kỳ vọng:* Thuốc nằm riêng trong mảng `out_of_scope_drugs`, `overall_risk_level = "UNKNOWN_RISK"`.

7. **`test_llm_fallback_on_timeout_or_mock`:**
   - *Mục tiêu:* Kiểm tra cơ chế tự động chuyển sang văn bản mẫu tĩnh khi `USE_MOCK_AI=True` hoặc mô phỏng Gemini API timeout.
   - *Kỳ vọng:* API trả về mã 200, trường `source_engine = "FALLBACK_TEMPLATE_ENGINE"`, nội dung format chính xác không ném lỗi cú pháp.

8. **`test_execution_performance_under_100ms`:**
   - *Mục tiêu:* Đánh giá thời gian phản hồi của Tầng 0 (SQL Engine) với đơn thuốc gồm 6 biệt dược (~28 cặp kiểm tra).
   - *Đánh dấu:* `@pytest.mark.performance`.
   - *Kỳ vọng:* Thời gian thực thi đo đạc $< 30\text{ms}$ trên local, $< 100\text{ms}$ trên CI.

#### 4.2.3. Danh Mục Ca Kiểm Thử Tích Hợp API Gateway (`backend/tests/test_ddi_api.py`):
1. **`test_api_ddi_check_success_200`:** Gửi payload chuẩn, xác nhận HTTP status 200 và response body khớp hoàn toàn với schema Pydantic `CheckInteractionResponse`.
2. **`test_api_ddi_check_empty_drugs_validation_422`:** Gửi mảng `drugs=[]`, xác nhận FastAPI validation chặn lại và trả về HTTP 422 Unprocessable Entity.
3. **`test_api_ddi_check_database_error_500`:** Giả lập lỗi ngắt kết nối database, xác nhận exception handler trả về HTTP 500 với thông điệp an toàn.

---

### 4.3. Kế Hoạch Triển Khai & Lệnh CLI Thực Thi (Sprint Execution)

#### 4.3.1. Các Lệnh CLI Khởi Tạo Cơ Sở Dữ Liệu & Nạp Dữ Liệu Mẫu:
```bash
# 1. Chuyển vào thư mục backend
cd backend

# 2. Chạy migration schema CSDL (Supabase Cloud hoặc Postgres local)
alembic upgrade head

# 3. Nạp 100 hoạt chất, 350 biệt dược và ma trận tương tác chuẩn
python -m backend.data_seed.seed_m4_interactions

# 4. Chạy toàn bộ test suite (chế độ mock an toàn < 2s)
pytest tests/ -v
```

#### 4.3.2. Phân Công Nhiệm Vụ Thành Viên (RACI Matrix):

| Thành viên | Trách nhiệm chính trong Module M4 | File thành phẩm bàn giao cụ thể |
| :--- | :--- | :--- |
| **Trương Huệ Trí** *(PO & Data Lead)* | Thiết kế Schema CSDL Supabase 3NF và biên tập script nạp dữ liệu DDI/DCI. | `backend/data_seed/seed_m4_interactions.py`<br>`backend/data_seed/medicare_dump.sql` |
| **Dương Phan Minh Trí** *(Frontend Lead & DDI Logic)* | Lập trình logic truy vấn SQL Batch tại Backend và xây dựng giao diện Tra cứu an toàn M4 trên React. | `backend/app/routers/m4_ddi.py`<br>`frontend/src/features/ddi/MedicineInteractionChecker.tsx` |
| **Nguyễn Bảo Trọng** *(DevOps & QA Lead)* | Xây dựng bộ test case `pytest`, cấu hình CI GitHub Actions và tối ưu hóa index truy vấn CSDL. | `backend/tests/conftest.py`<br>`backend/tests/test_ddi_engine.py`<br>`backend/tests/test_ddi_api.py` |
| **Lê Thanh Phong** *(AI Assistant Lead)* | Thiết kế Prompt Guardrail cho Gemini 1.5 Flash và hoàn thiện thuật toán Fallback Template Engine. | `backend/app/services/ddi_llm_service.py`<br>`backend/app/models/ddi_schemas.py` |

---

### 4.4. Phương Án Phòng Vệ Ngày Báo Cáo (Offline Resilience)

Để đảm bảo buổi báo cáo trước hội đồng không bị phụ thuộc vào chất lượng mạng Wi-Fi tại trường:
1. Toàn bộ CSDL Supabase được trích xuất sẵn một bản sao lưu cục bộ `backend/data_seed/medicare_dump.sql`.
2. Khi không có mạng, chỉ cần đổi biến môi trường trong file `backend/.env`:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/medicare_local
   USE_MOCK_AI=True
   GEMINI_API_KEY=dummy_offline_key
   GEMINI_TIMEOUT_SECONDS=1.5
   ```
3. Hệ thống chuyển đổi ngay lập tức sang chế độ Offline: toàn bộ logic SQL chạy trên máy cục bộ với tốc độ $2\text{ms}$, lời khuyên được sinh tức thì từ Template Engine tĩnh, đảm bảo buổi demo mượt mà 100%.
