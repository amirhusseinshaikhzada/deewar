import openai
import os

class AIConsultant:
    def __init__(self):
        # در صورت داشتن API Key، این بخش فعال می‌شود
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        else:
            self.api_key = None

    def ask_advice(self, user_query: str, market_data: dict) -> str:
        """
        ارسال داده‌های بازار به هوش مصنوعی برای دریافت مشاوره انسانی
        market_data: شامل اطلاعاتی مثل میانگین قیمت، روند و پیش‌بینی است
        """
        
        # اگر API Key نداشتیم، یک پاسخ هوشمند بر اساس قوانین (Rule-based) می‌دهیم
        if not self.api_key:
            return self._fallback_advice(user_query, market_data)

        # اگر API Key داشتیم، از قدرت GPT استفاده می‌کنیم
        prompt = f"""
        تو یک مشاور هوشمند بازار دیوار هستی. 
        داده‌های بازار فعلی: {market_data}
        سوال کاربر: {user_query}
        لطفاً با لحنی دوستانه و حرفه‌ای به کاربر پاسخ بده و بگو آیا الان زمان مناسبی برای خرید است یا خیر.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a helpful market expert."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ خطایی در ارتباط با مشاور هوشمند رخ داد: {e}"

    def _fallback_advice(self, query: str, data: dict) -> str:
        """پاسخ جایگزین زمانی که هوش مصنوعی متصل نیست"""
        trend = data.get("trend", "نامشخص")
        prediction = data.get("prediction", "نامشخص")
        
        if trend == "upward":
            return f"🧐 تحلیل سیستم: روند بازار صعودی است  قیمت احتمالی بعدی حدود {prediction:,.0f} تومان پیش‌بینی می‌شود. پیشنهاد می‌شود زودتر خرید کنید!"
        elif trend == "downward":
            return f"📉 تحلی سیستم: روند بازار نزولی است. قیمت‌ها در حال کاهش است. پیشنهاد می‌شود کمی صبر کنید تا قیمت‌ها پایین‌تر بیاید."
        else:
            return "⚖️ تحلیل سیستم: بازار در حالت پایدار است. خرید یا فروش در این لحظه ریسک زیادی ندارد."