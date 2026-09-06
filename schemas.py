# API로 데이터를 주고 받을 때는 모양이 달라야함 

from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime

# ---------- Item ----------
# 입력용: 사용자가 물건 등록할 때 보내는 형태
class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    quantity: int = Field(ge=1) # 등록은 최소 1개
    location_id: int
    barcode: str | None = None
    expiry_date: date | None = None


# 출력용: API가 응답으로 돌려주는 형태 (DB가 만든 id, created_at 포함)
class ItemResponse(BaseModel):
    id: int
    household_id: int
    location_id: int
    name: str
    barcode: str | None
    quantity: int
    expiry_date: date | None
    created_at: datetime

    # SQLAlchemy 객체를 Pydantic이 읽을 수 있게 해주는 설정
    model_config = {"from_attributes": True}



# ------ Auth ------
class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    household_name: str = Field(min_length=1)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    househlod_id: int
    model_config = {"from_attributes": True}

# ---------- Location ----------
class LocationCreate(BaseModel):
    name: str = Field(min_length=1)
    parent_id: int | None = None   # 최상위면 None

class LocationResponse(BaseModel):
    id: int
    household_id: int
    parent_id: int | None
    name: str
    path: str | None = None   # "주방 > 김치냉장고 > 2번 칸" (조회 시 계산)
    model_config = {"from_attributes": True}

# ---------- 꺼내기 ----------
class ItemConsume(BaseModel):
    quantity: int = Field(ge=1)