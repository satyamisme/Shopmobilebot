from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association tables
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    telegram_id = Column(Integer, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    roles = relationship("Role", secondary=user_roles, back_populates="users")

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(String)
    
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    imei = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    ram = Column(String)
    storage = Column(String)
    network = Column(String)
    price = Column(Float, nullable=False)
    condition = Column(String)
    status = Column(String, default='in_stock')
    shop_id = Column(Integer, ForeignKey('shops.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    shop = relationship("Shop", back_populates="products")

class Shop(Base):
    __tablename__ = 'shops'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="shop")