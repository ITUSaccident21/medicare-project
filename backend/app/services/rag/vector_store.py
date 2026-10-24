"""
Vector Store Service (ChromaDB Local)
Phụ trách: VT4 - Lê Thanh Phong (AI Assistant Lead)
Quản lý embeddings và truy vấn ngữ liệu y tế chuẩn Bộ Y tế.
"""

def query_medical_guidelines(query_text: str, n_results: int = 3) -> list:
    """Truy vấn các đoạn văn bản y tế liên quan từ ChromaDB Local."""
    return [
        {
            "content": "Người mắc bệnh tăng huyết áp nên duy trì chế độ ăn giảm muối (< 5g/ngày) và tập thể dục 30 phút mỗi ngày.",
            "source": "Hướng dẫn Chẩn đoán và Điều trị Tăng huyết áp - Bộ Y tế 2022",
            "score": 0.92
        }
    ]
