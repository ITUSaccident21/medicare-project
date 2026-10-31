from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user_models import (
    User, 
    PatientProfile, 
    UserRegisterRequest, 
    UserLoginRequest, 
    TokenResponse, 
    ProfileUpdateRequest, 
    ProfileResponse
)

router = APIRouter()
security_bearer = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    """Dependency trích xuất và xác thực User từ JWT Bearer Token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu token xác thực Bearer",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        phone_number: str = payload.get("sub")
        if phone_number is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không chứa thông tin định danh hợp lệ",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Đăng ký tài khoản mới và tự động tạo hồ sơ bệnh nhân rỗng."""
    # Kiểm tra số điện thoại đã tồn tại chưa
    existing_user = db.query(User).filter(User.phone_number == req.phone_number).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số điện thoại này đã được đăng ký trong hệ thống"
        )

    # Tạo User mới với mật khẩu băm bcrypt
    new_user = User(
        phone_number=req.phone_number,
        full_name=req.full_name,
        hashed_password=get_password_hash(req.password),
        is_active=True
    )
    db.add(new_user)
    db.flush()  # Nhận new_user.id

    # Tạo hồ sơ bệnh nhân mặc định
    profile = PatientProfile(
        user_id=new_user.id,
        age=30,
        gender="OTHER",
        allergies="",
        underlying_conditions="",
        medical_history=""
    )
    db.add(profile)
    db.commit()
    db.refresh(new_user)

    # Sinh JWT Token
    access_token = create_access_token(data={"sub": new_user.phone_number, "user_id": new_user.id})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        full_name=new_user.full_name,
        phone_number=new_user.phone_number
    )


@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Đăng nhập bằng số điện thoại và mật khẩu, trả về JWT Access Token."""
    user = db.query(User).filter(User.phone_number == req.phone_number).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Số điện thoại hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị tạm khóa"
        )

    access_token = create_access_token(data={"sub": user.phone_number, "user_id": user.id})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        full_name=user.full_name,
        phone_number=user.phone_number
    )


@router.get("/me", response_model=ProfileResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lấy thông tin tài khoản kèm hồ sơ bệnh nền và dị ứng của người dùng hiện tại."""
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
    if not profile:
        profile = PatientProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        age=profile.age,
        gender=profile.gender,
        is_pregnant=profile.is_pregnant,
        allergies=profile.allergies or "",
        underlying_conditions=profile.underlying_conditions or "",
        medical_history=profile.medical_history or "",
        updated_at=profile.updated_at
    )


@router.put("/me/profile", response_model=ProfileResponse)
def update_profile(
    req: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cập nhật hồ sơ bệnh nền, tiền sử dị ứng và thông tin sức khỏe cá nhân."""
    profile = db.query(PatientProfile).filter(PatientProfile.user_id == current_user.id).first()
    if not profile:
        profile = PatientProfile(user_id=current_user.id)
        db.add(profile)

    if req.age is not None:
        profile.age = req.age
    if req.gender is not None:
        profile.gender = req.gender
    if req.is_pregnant is not None:
        profile.is_pregnant = req.is_pregnant
    if req.allergies is not None:
        profile.allergies = req.allergies
    if req.underlying_conditions is not None:
        profile.underlying_conditions = req.underlying_conditions
    if req.medical_history is not None:
        profile.medical_history = req.medical_history

    db.commit()
    db.refresh(profile)

    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        age=profile.age,
        gender=profile.gender,
        is_pregnant=profile.is_pregnant,
        allergies=profile.allergies or "",
        underlying_conditions=profile.underlying_conditions or "",
        medical_history=profile.medical_history or "",
        updated_at=profile.updated_at
    )
