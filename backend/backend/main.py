from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # swap later with postgres

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

# ===== DATABASE MODELS =====
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user = Column(String)
    items = Column(String)
    vendor = Column(String)
    price = Column(Integer)
    status = Column(String)

Base.metadata.create_all(bind=engine)

# ===== DEPENDENCY =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== ENDPOINTS =====
@app.post("/order")
def create_order(data: dict, db=Depends(get_db)):
    order = Order(
        user=data["user"],
        items=str(data["items"]),
        vendor=data["vendor"],
        price=data["price"],
        status="processing"
    )
    db.add(order)
    db.commit()
    return {"success": True}

@app.get("/orders")
def get_orders(db=Depends(get_db)):
    return db.query(Order).all()
