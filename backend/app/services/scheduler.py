"""
Background Scheduler Service
Phụ trách: VT2 - Nguyễn Bảo Trọng (DevOps & Backend Lead)
Dịch vụ chạy ngầm lập lịch thông báo và nhắc giờ uống thuốc cho người bệnh.
"""

def init_scheduler():
    """Khởi tạo background job scheduler (APScheduler)."""
    print("⏰ [SCHEDULER] Background medication reminder service initialized.")

def send_pill_reminder(user_id: int, drug_name: str, dose_time: str):
    """Gửi thông báo nhắc giờ uống thuốc."""
    print(f"🔔 [REMINDER] Nhắc nhở uống thuốc cho User {user_id}: {drug_name} vào lúc {dose_time}")
