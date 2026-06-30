from sqlalchemy import create_engine, text # اضافه کردن text برای اجرای دستورات SQL
import pandas as pd
import os

class DatabaseManager:
    def __init__(self, db_url=os.getenv("DATABASE_URL")):
        self.engine = create_engine(db_url)
        self._create_table()

    def _create_table(self):
        """ایجاد جدول در صورت عدم وجود"""
        query = """
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY,
            keyword TEXT,
            city TEXT,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()

    def add_price_entry(self, keyword, city, price):
        """ذخیره قیمت جدید"""
        query = "INSERT INTO prices (keyword, city, price) VALUES (:keyword, :city, :price)"
        with self.engine.connect() as connection:
            connection.execute(text(query), {"keyword": keyword, "city": city, "price": price})
            connection.commit()

    def get_prices_for_item(self, keyword) -> pd.DataFrame:
        """دریافت تمام قیمت‌های یک کالا به صورت دیتافریم"""
        query = f"SELECT * FROM prices WHERE keyword = '{keyword}' ORDER BY timestamp ASC"
        return pd.read_sql(query, self.engine)
