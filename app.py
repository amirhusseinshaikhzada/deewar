import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

# وارد کردن ماژول‌های خودت (نام‌ها را دقیقاً مطابق فایل خودت تنظیم کن)
from scraper.deewar_engine import DeewarScraper
from database.db_manager import DatabaseManager
from analyzer.price_analyzer import PriceAnalyzer
from ai.predictor import PricePredictor
from ai.consultant import AIConsultant

# ۱. تنظیمات اولیه
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# ۲. مقداردهی ابزارها
db = DatabaseManager()
scraper = DeewarScraper()
analyzer = PriceAnalyzer()
predictor = PricePredictor()
consultant = AIConsultant()

# --- BOT LOGIC (Handlers) ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🚀 *ربات تحلی بازار دیوار (نسخه Flask)*\n\n"
        "من آماده هستم! فقط نام کالا و شهر را بفرست.\n"
        "مثال: `iPhone 13 Tehran`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_search(message):
    chat_id = message.chat.id
    try:
        user_input = message.text.strip()
        parts = user_input.split()
        
        if len(parts) < 2:
            bot.reply_to(message, "❌ فرمت اشتباه است. مثال: `iPhone 13 Tehran`", parse_mode="Markdown")
            return

        keyword = " ".join(parts[:-1])
        city = parts[-1]

        bot.send_message(chat_id, f"🔍 در حال جستجو و تحلیل `{keyword}` در `{city}`...")

        # گام ۱: اسکرپینگ
        new_prices = scraper.scrape_prices(city, keyword)
        if not new_prices:
            bot.reply_to(message, "❌ داده‌ای پیدا نشد.")
            return

        # گام ۲: ذخیره در دیتابیس
        for price in new_prices:
            db.add_price_entry(keyword, city, price)

        # گام ۳: استخراج داده‌ها برای تحلیل
        df = db.get_prices_for_item(keyword)
        if df.empty:
            bot.reply_to(message, "❌ دیتابیس خالی است.")
            return

        # گام ۴: استفاده از ماژول Analyzer شما (Stats + Visualizer)
        # فرض بر این است که متد get_stats در کلاس شما وجود دارد
        stats = analyzer.get_stats(df) 
        
        # گام ۵: پیش‌بینی و مشاوره
        predicted_val = predictor.predict_next_price(df)
        trend = predictor.get_trend_direction(df)
        
        avg_str = f"{stats['avg']:,.0f} تومان"
        min_str = f"{stats['min']:,.0f} تومان"
        max_str = f"{stats['max']:,.0f} تومان"
        pred_str = f"{market_data['predicted']:,.0f} تومان"

        # حالا متن نهایی را می‌سازیم
        # نکته: از {{ }} استفاده می‌کنیم تا پایتون آن‌ها را به عنوان متن معمولی در نظر بگیرد
        response_msg = (
            f"📊 *گزارش تحلیل نهایی:*\n\n"
            f"📦 کالا: `{keyword}`\n"
            f"💰 میانگین: `{avg_str}`\n"
            f"📉 کمترین: `{min_str}`\n"
            f"📈 بیشترین: `{max_str}`\n"
            f"🔮 پیش‌بینی: `{pred_str}`\n"
            f"📈 روند: `{trend.upper()}`\n\n"
            f"🤖 *مشاوره:* \n_{advice}_"
        )
        # ارسال تصویر نمودار در ابتدا، سپس متن
        with open(chart_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=response_msg, parse_mode="Markdown")

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "💥 خایی در پردازش رخ داد.")

# --- FLASK ROUTES ---

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    """این مسیر، پیام‌های تلگرام را دریافت و به ربات پاس می‌دهد"""
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Bot is Alive! 🚀"

# --- RUN SERVER ---

if __name__ == "__main__":
    # د حالت Flask، ما از polling استفاده نمی‌کنیم
    # فقط سرور را اجرا می‌کنیم
    app.run(port=5000)