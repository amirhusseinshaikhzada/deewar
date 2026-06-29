from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """جدول کاربران برای مدیریت وضعیت و شهر انتخاب شده"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True) # ID تلگرام
    username = Column(String, nullable=True)
    selected_city = Column(String, nullable=True) # آخرین شهری که انتخاب کرده
    created_at = Column(DateTime, default=datetime.now)

class Product(Base):
    """جدول محصولات برای دسته‌بندی قیمت‌ها"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) # نام محصول (مثلاً آیفون 13)
    city = Column(String, nullable=False) # شهر مربوط به این محصول
    
    # رابطه با تاریخچه قیمت‌ها
    prices = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    """جدول تاریخچه قیمت‌ها (ستون اصلی برای تحلیل نمودار)"""
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    
    product = relationship("Product", back_populates="prices")