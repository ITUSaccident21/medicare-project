"""
Medical Prompts & Safety Guardrails
Phụ trách: VT4 - Lê Thanh Phong (AI Assistant Lead)
"""

SYSTEM_RAG_PROMPT = """Bạn là Trợ lý Sức khỏe AI MediCare.
Nhiệm vụ của bạn là giải đáp thắc mắc của người bệnh dựa CHÍNH XÁC trên các tài liệu y khoa được cung cấp.
Nếu thông tin không có trong tài liệu, hãy thành thật trả lời là không có cơ sở xác thực.
Luôn luôn kèm theo câu khuyến cáo người bệnh tham vấn bác sĩ trực tiếp."""

TRIAGE_RED_FLAGS = [
    "đau thắt ngực",
    "khó thở dữ dội",
    "nôn ra máu",
    "mất ý thức",
    "liệt nửa người"
]

def check_emergency_triage(text: str) -> bool:
    """Kiểm tra xem câu hỏi có chứa triệu chứng cấp cứu nguy kịch không."""
    lowered = text.lower()
    return any(flag in lowered for flag in TRIAGE_RED_FLAGS)
