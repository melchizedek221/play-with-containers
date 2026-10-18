import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

# Création de l'URL de connexion
DATABASE_URL = os.getenv('BILLING_DB_URI')

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création d'une session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de la base pour les modèles déclaratifs
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    number_of_items = Column(Integer)
    total_amount = Column(Float)

# Création des tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_order(db, user_id: str, number_of_items: int, total_amount: float):
    new_order = Order(user_id=user_id, number_of_items=number_of_items, total_amount=total_amount)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order