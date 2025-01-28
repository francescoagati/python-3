"""
Progetto FastAPI monofile con SQLite, SQLAlchemy e Pydantic
"""

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Configurazione database SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

# Setup database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelli SQLAlchemy
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String)

# create has many relationship
class DbDocumentUser(Base):
    __tablename__ = "document_user"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    
class DbDocument(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user = relationship("DBUser", secondary="document_user", back_populates="documents")
    



# Crea le tabelle (solo per sviluppo)
Base.metadata.create_all(bind=engine)

# Schemi Pydantic
class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Funzioni CRUD
def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = DBUser(
        email=user.email,
        full_name=user.full_name,
        password=user.password  # Da hasare in produzione!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Configurazione FastAPI
app = FastAPI()
router = APIRouter()

# Middleware CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dipendenze
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint
@router.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

app.include_router(router, prefix="/api")

# Endpoint root
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Se eseguito direttamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)