import requests
from bs4 import BeautifulSoup
import time
import random

class DeewarScraper:
    def __init__(self):
        self.base_url = "https://deevaar.com" # آدرس پایه (در واقع ساختار URL دیوار)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def _build_url(self, city: str, keyword: str) -> str:
        """
        ساخت URL بر اساس ساختار دیوار. 
        نکته: دیوار از ساختار /{city}/{keyword} استفاده می‌کند.
        """
        # تبدیل نام شهر به فرمت URL (مثلاً تهران -> tehran)
        # در پروژه واقعی باید یک نگاشت (Mapping) کامل داشته باشیم
        city_slug = city.lower().replace(" ", "-")
        keyword_slug = keyword.lower().replace(" ", "-")
        
        # ساخت URL نهایی (مثال: https://deevaar.com/tehran/iphone-13)
        return f"https://deevaar.com/{city_slug}/{keyword_slug}"

    def scrape_prices(self, city: str, keyword: str):
        """
        جستجو و استخراج قیمت‌ها
        خروجی: لیستی از قیمت‌های پیدا شده (به صورت float)
        """
        target_url = self._build_url(city, keyword)
        print(f"🔍 در حال جستجو در: {target_url}")
        
        prices_found = []
        
        try:
            # ایجاد درخواست با وقفه تصادفی برای جلوگیری از بلاک شدن
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(target_url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ خطا در دسترسی به سایت: Status {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')

            # --- بخش استخراج (این بخش به شدت به تغییرات ساختار HTML دیوار وابسته است) ---
            # فرض می‌کنیم قیمت‌ها در تگ‌هایی با کلاس خاصی قرار دارند
            # در واقعیت باید با Inspect کردن دقیق پیدا شوند
            
            # مثال فرضی برای استخراج قیمت‌ها:
            # معمولاً قیمت‌ها در تگ‌هایی با کلاس‌هایی مثل 'price' یا 'text-bold' هستند
            price_elements = soup.find_all('div', class_='price-class-name') # نام کلاس واقعی را اینجا قرار می‌دهیم
            
            for el in price_elements:
                raw_price = el.get_text().strip()
                # پاکسازی متن (حذف تومان، کاما و غیره)
                clean_price = self._clean_price_text(raw_price)
                if clean_price:
                    prices_found.append(clean_price)

            # اگر چیزی پیدا نکرد، برای تست از یک داده فرضی استفاده می‌کنیم (در محیط توسعه)
            if not prices_found:
                print("⚠️ هیچ قیمتی یافت نشد. احتمالاً ساختار HTML تغییر کرده یا محصول موجود نیست.")
                # در دنیای واقعی اینجا باید خطا برگردانیم، اما برای تست:
                # return [15000000.0, 15500000.0, 14800000.0] 
            
            return prices_found

        except Exception as e:
            print(f"💥 خطا در عملیات اسکرپینگ: {e}")
            return []

    def _clean_price_text(self, text: str) -> float:
        """
        تبدیل متن قیمت (مثلاً '۱۵,۰۰۰,۰۰۰ تومان') به عدد float
        """
        try:
            # حذف کاراکترهای غیر عددی (حذف تومان، کاما، حروف فارسی و ...)
            import re
            # نگه داشتن فقط اعداد
            numeric_string = re.sub(r'[^\d]', '', text)
            return float(numeric_string) if numeric_string else None
        except:
            return None