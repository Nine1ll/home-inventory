from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    ForeignKey, func
)
from sqlalchemy.orm import relationship
from database import Base


class Household(Base):
    __tablename__ = 'households'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    invite_code = Column(String, unique=True, index=True)

    # Relation: 이 가구에 속한 것들
    users = relationship("User", back_populates="household")
    locations = relationship("Location", back_populates="household")
    items = relationship("Item", back_populates="household")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)  # §1 평문 저장 금지 - 이름으로 강제

    household = relationship("Household", back_populates="users")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("locations.id"), nullable=True)  # §2 자기참조 트리
    name = Column(String, nullable=False)
    pos_x = Column(Float, nullable=True)  # 3차 2D맵용 - 지금은 null
    pos_y = Column(Float, nullable=True)

    household = relationship("Household", back_populates="locations")

    # 자기참조: 부모-자식 위치 관계
    children = relationship("Location", backref="parent", remote_side=[id])
    items = relationship("Item", back_populates="location")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    barcode = Column(String, nullable=True, index=True)  # 3 자체 상품 사전
    quantity = Column(Integer, nullable=False, default=1)
    expiry_date = Column(Date, nullable=True)  # 3 배치 구분 기준

    household = relationship("Household", back_populates="items")
    location = relationship("Location", back_populates="items")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)      # 누가
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)       # 무엇을
    action = Column(String, nullable=False)          # 넣기/꺼내기 등 무슨 동작
    quantity_delta = Column(Integer, nullable=False)  # 변화량 (+2, -1 등)
    created_at = Column(DateTime, server_default=func.now())  # 언제 (6)