from fastapi import FastAPI

app = FastAPI(title="Home Inventory API")

@app.get("/")
def read_root():
    return {"message": "집 물류 관리 서비스에 오신 걸 환영합니다"}
