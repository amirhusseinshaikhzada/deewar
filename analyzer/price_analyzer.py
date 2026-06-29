import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# --- کلاس محاسبات (کد خودت با اصلاحات کوچک) ---
class MarketAnalyzer:
    def __init__(self, data_frame: pd.DataFrame):
        self.df = data_frame

    def get_stats(self) -> dict:
        """محاسبه تمام آمارهایی که app.py نیاز دارد"""
        if self.df.empty:
            return {'avg': 0, 'min': 0, 'max': 0}
        
        return {
            'avg': self.df['price'].mean(),
            'min': self.df['price'].min(),
            'max': self.df['price'].max()
        }

    def analyze_trend(self) -> str:
        if len(self.df) < 2:
            return "ثابت"
        
        first_price = self.df['price'].iloc[0]
        last_price = self.df['price'].iloc[-1]
        
        # جلوگیری از تقسیم بر صفر
        if first_price == 0: return "ثابت"
        
        change_percent = ((last_price - first_price) / first_price) * 100
        
        if change_percent > 0.5:
            return "صعودی �"
        elif change_percent < -0.5:
            return "نزولی 📉"
        else:
            return "ثابت ↔️"

# --- کلاس رسم نمودار (کد خودت با اصلاحات کوچک) ---
class ChartVisualizer:
    def __init__(self, chart_dir: str = "charts"):
        self.chart_dir = chart_dir
        if not os.path.exists(self.chart_dir):
            os.makedirs(self.chart_dir)

    def create_price_chart(self, df: pd.DataFrame, city_name: str, product_name: str) -> str:
        if df.empty:
            return None

        # برای نمایش درست فونت فارسی در نمودار (در صورت نیاز به نصب کتابخانه arabic_reshaper)
        # فعلاً از حالت پیش‌فرض استفاده می‌کنیم
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))

        # رسم نمودار
        ax.plot(df['timestamp'], df['price'], color='#00ff00', linewidth=2, marker='o', markersize=4)
        
        ax.set_title(f"Price Trend: {product_name} in {city_name}", fontsize=15, color='white', pad=20)
        ax.set_xlabel("Time", fontsize=12, color='lightgray')
        ax.set_ylabel("Price (Tomans)", fontsize=12, color='lightgray')
        ax.grid(True, linestyle='--', alpha=0.3)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{city_name}_{product_name}_{timestamp_str}.png".replace(" ", "_")
        file_path = os.path.join(self.chart_dir, file_name)
        
        plt.savefig(file_path)
        plt.close(fig)
        
        return file_path

# --- کلاس اصلی که app.py آن را صدا می‌زند (The Bridge) ---
class PriceAnalyzer:
    """
    این کلاس نقش واسط را بازی می‌کند تا app.py نیازی به مدیریت دو کلاس جداگانه نداشته باشد.
    """
    def __init__(self):
        self.visualizer = ChartVisualizer()

    def get_stats(self, df: pd.DataFrame) -> dict:
        analyzer = MarketAnalyzer(df)
        stats = analyzer.get_stats()
        # اضافه کردن روند به دیکشنری stats برای راحتی در app.py
        stats['trend'] = analyzer.analyze_trend()
        return stats

    def generate_plot(self, df: pd.DataFrame, product_name: str) -> str:
        # استخراج شهر از دیتابیس یا استفاده از مقدار پیش‌فرض
        # در اینجا فرض می‌کنیم شهر را از ستون‌های دیتافریم می‌گیریم یا یک مقدار ثابت می‌گذاریم
        city = "Unknown"
        if 'city' in df.columns:
            city = df['city'].iloc[-1]
            
        return self.visualizer.create_price_chart(df, city, product_name)