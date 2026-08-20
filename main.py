from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Home Inventory API")

# 데이터 모델: 재고 아이템 하나의 형태를 정의
class Item(BaseModel):
    name: str
    quantity: int
    category: str

# 임시 저장소 (메모리), 서버 끄면 사라짐 (나중에 DB로 교체)
inventory: dict[int, Item] = {}
next_id = 1


@app.get("/")
def read_root():
    return {"message": "집 물류 관리 서비스에 오신 걸 환영합니다"}

# CREATE: 새 아이템 등록 
@app.post("/items")
def create_item(item: Item):
    global next_id
    item_id = next_id
    inventory[item_id] = item
    next_id +=1 
    return {'id': item_id, 'item': item}

# READ All: 전체 아이템 조회
@app.get("/items")
def get_items():
    return inventory

# READ One: 특정 아이템 조회
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return inventory[item_id]

# UPDATE: 기존 아이템 수정 
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    inventory[item_id] = item
    return {'id': item_id, 'item': item}

# DELETE: 아이템 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    del inventory[item_id]
    return {"message": f"아이템 {item_id} 삭제 완료"}