from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

# ==============================================================================
# 1. SQLAlchemy ORM Models (CSDL Quan hệ)
# ==============================================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    # Quan hệ 1-1 với PatientProfile
    profile = relationship("PatientProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True, default=30)
    gender = Column(String(10), nullable=True, default="OTHER")
    is_pregnant = Column(Boolean, default=False)
    allergies = Column(Text, default="", nullable=True)  # VD: "Penicillin, Aspirin"
    underlying_conditions = Column(Text, default="", nullable=True)  # VD: "Cao huyết áp, Đái tháo đường"
    medical_history = Column(String(500), default="", nullable=True)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="profile")

# ==============================================================================
# 2. Pydantic Schemas (API Data Contracts)
# ==============================================================================

class UserRegisterRequest(BaseModel):
    phone_number: str = Field(..., min_length=9, max_length=15, description="Số điện thoại đăng ký")
    full_name: str = Field(..., min_length=2, max_length=100, description="Họ và tên")
    password: str = Field(..., min_length=6, description="Mật khẩu tối thiểu 6 ký tự")

class UserLoginRequest(BaseModel):
    phone_number: str = Field(..., description="Số điện thoại đăng nhập")
    password: str = Field(..., description="Mật khẩu")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    phone_number: str

class ProfileUpdateRequest(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = Field(None, pattern="^(MALE|FEMALE|OTHER)$")
    is_pregnant: Optional[bool] = False
    allergies: Optional[str] = Field(None, description="Danh sách dị ứng thuốc phân tách bằng dấu phẩy")
    underlying_conditions: Optional[str] = Field(None, description="Danh sách bệnh nền phân tách bằng dấu phẩy")
    medical_history: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone_number: str
    age: Optional[int] = None
    gender: Optional[str] = None
    is_pregnant: bool = False
    allergies: str = ""
    underlying_conditions: str = ""
    medical_history: str = ""
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
