# API로 데이터를 주고 받을 때는 모양이 달라야함 

from pydantic import BaseModel, Field
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