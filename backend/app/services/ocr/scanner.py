"""
OCR Scanner Service
Phụ trách: VT4 - Lê Thanh Phong & VT3 - Dương Phan Minh Trí
Trích xuất tên thuốc và hàm lượng từ hình ảnh đơn thuốc / vỏ hộp thuốc.
"""

def extract_drugs_from_image(image_bytes: bytes) -> list:
    """Bóc tách danh sách thuốc từ hình ảnh qua Gemini Vision."""
    # Stub OCR trả về danh mục nhận diện mẫu
    return [
        {"raw_name": "Decolgen Forte", "confidence": 0.95},
        {"raw_name": "Amlodipine 5mg", "confidence": 0.92}
    ]
