"""
Mock AI Service - Sandbox Offline Mode
Phụ trách: VT4 - Lê Thanh Phong & VT2 - Nguyễn Bảo Trọng
Cho phép kiểm thử tự động, chạy offline không cần API Key và không tốn tiền quota.
"""

class MockAIService:
    @staticmethod
    def generate_chat_response(question: str) -> dict:
        return {
            "answer": f"[SANDBOX MOCK] Khuyến nghị dinh dưỡng cho câu hỏi: '{question}'. Hãy duy trì chế độ ăn nhạt và uống đủ nước.",
            "source": "Hướng dẫn Dinh dưỡng Bộ Y tế (Mock Sandbox)",
            "disclaimer": "Thông tin chỉ mang tính tham khảo trong môi trường kiểm thử."
        }

    @staticmethod
    def generate_ddi_explanation(alerts: list, patient_age: int) -> dict:
        if not alerts:
            return {
                "source_engine": "MOCK_AI_SANDBOX",
                "content_markdown": "Hệ thống không ghi nhận tương tác nguy hiểm giữa các thuốc đã chọn.",
                "disclaimer": "Khuyến nghị mang tính tham khảo."
            }
        
        lines = [f"### [SANDBOX MOCK] Lời khuyên y tế (Bệnh nhân {patient_age} tuổi):\n"]
        for alert in alerts:
            lines.append(f"- Cảnh báo: {alert.get('mechanism', 'Tương tác đối kháng')}")
        lines.append("\nVui lòng hỏi ý kiến bác sĩ trước khi đổi thuốc.")
        
        return {
            "source_engine": "MOCK_AI_SANDBOX",
            "content_markdown": "\n".join(lines),
            "disclaimer": "Thông tin mang tính chất tham khảo trong môi trường kiểm thử."
        }
