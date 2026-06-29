import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

class PricePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def predict_next_price(self, df: pd.DataFrame) -> float:
        """
        دریافت دیتافریم قیمت‌ها و پیش‌بینی قیمت بعدی
        df باید شامل ستون‌های 'price' و 'timestamp' باشد
        """
        if df.empty or len(df) < 3:
            return None  # برای پیش‌بینی حداقل به 3 نقطه داده نیاز داریم

        # تبدیل زمان به اعداد (Timestamp) برای پردازش ریاضی
        X = np.array(df['timestamp'].map(pd.Timestamp.to_julian_date)).reshape(-1, 1)
        y = df['price'].values

        # آموزش مدل روی داده‌های موجود
        self.model.fit(X, y)

        # پیش‌بینی برای "زمان حال" یا گام زمانی بعدی
        next_timestamp = np.array([[X[-1][0] + 1]]) # فرض می‌کنیم گام بعدی یک واحد زمانی است
        prediction = self.model.predict(next_timestamp)

        return float(prediction[0])

    def get_trend_direction(self, df: pd.DataFrame) -> str:
        """تشخیص اینکه روند صعودی است یا نزولی"""
        if len(df) < 2:
            return "unknown"
        
        recent_avg = df['price'].tail(3).mean()
        older_avg = df['price'].head(3).mean()

        if recent_avg > older_avg:
            return "upward"  # صعودی
        elif recent_avg < older_avg:
            return "downward" # نزولی
        else:
            return "stable"   # ثابت