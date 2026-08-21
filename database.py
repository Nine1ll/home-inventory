from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite 데이터베이스 파일 경로. 프로젝트 폴더에 home_inventory.db 생성
SQLALCHEMY_DATABASE_URL = "sqlite:///./home_inventory.db"


# 엔진: DB와 실제 연결 경로
# check_same_thread=False는 SQLite를 FastAPI와 쓸 때 필요한 옵션
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 세션: DB에 뭔가 읽고 쓸 때 쓰는 작업 단위
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: 모든 모델 클래스가 상속할 부모. 이걸 상속하면 DB 테이블이 됨
Base = declarative_base()