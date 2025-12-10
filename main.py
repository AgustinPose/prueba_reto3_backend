from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import User
from pydantic import BaseModel


app = FastAPI()

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Dependencia para obtener DB en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "FastAPI + PostgreSQL funcionando! CRACK"}


class UserCreate(BaseModel):
    nombre: str


@app.post("/users")
def crear_usuario(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(nombre=payload.nombre)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()
