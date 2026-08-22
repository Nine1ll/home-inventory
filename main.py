from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

# DB관련 import
from database import engine, Base, get_db
import models
import schemas

# 앱 시작 시 모델대로 테이블 생성 (있으면 건너뜀)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Inventory API")

# 인증 구현 전까지 임시로 사용할 가구 ID
TEMP_HOUSEHOLD_ID = 1


@app.get("/")
def read_root():
    return {"message": "집 물류 관리 서비스에 오신 걸 환영합니다"}

# CREATE: 새 아이템 등록 
@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    # 3: 같은 가구+품목명+위치+유통기한이면 기존 배치 수량 증가
    existing = db.query(models.Item).filter(
        and_(
            models.Item.household_id == TEMP_HOUSEHOLD_ID,
            models.Item.name == item.name,
            models.Item.location_id == item.location_id,
            models.Item.expiry_date == item.expiry_date,
        )
    ).first()

    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return existing

    new_item = models.Item(
        household_id=TEMP_HOUSEHOLD_ID,
        name=item.name,
        quantity=item.quantity,
        location_id=item.location_id,
        barcode=item.barcode,
        expiry_date=item.expiry_date
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# READ All: 전체 아이템 조회
@app.get("/items", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).filter(
        models.Item.household_id == TEMP_HOUSEHOLD_ID
    ).all()


# READ One: 특정 아이템 조회
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_items(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return item


# DELETE: 아이템 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    db.delete(item)
    db.commit()
    return {"message": f"아이템 {item_id} 삭제 완료"}