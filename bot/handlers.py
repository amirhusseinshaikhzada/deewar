from scraper.deewar_engine import DeewarScraper
from analyzer.price_analyzer import PriceAnalyzer
from telebot import types
from bot import messages

# ما این شیء را در app.py تعریف می‌کنیم و اینجا استفاده می‌کنیم
# اما برای ساختار کد، فرض می‌کنیم bot_instance از بیرون پاس داده می‌شود

def register_handlers(bot):
    """ثبت تمام هندلرها در ربات"""
    
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """دستور /start"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # لیست شهرها (در آینده از config خوانده می‌شود)
        cities = ["Tehran", "Isfahan", "Mashhad", "Tabriz", "Shiraz"]
        
        buttons = [
            types.InlineKeyboardButton(text=city, callback_data=f"city_{city}") 
            for city in cities
        ]
        markup.add(*buttons)
        
        bot.reply_to(message, messages.START_MESSAGE, reply_markup=markup, parse_mode='Markdown')

    @bot.callback_query_handler(func=lambda call: call.data.startswith('city_'))
    def callback_city(call):
        """هندلر دکمه‌های انتخاب شهر"""
        selected_city = call.data.split("_")[1]
        
        # ذخیره شهر در حافظه موقت (در پروژه‌های بزرگ از Redis استفاده می‌شود)
        # فعلاً از set_user_properties یا ذخیره در دیتابیس استفاده خواهیم کرد
        # برای سادگی فعلاً در یک دیکشنری در حافظه (Memory) نگه می‌داریم
        # (این بخش در مرحله دیتابیس اصلاح می‌شود)
        
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📍 شما شهر **{selected_city}** را انتخاب کردید.\n\n{messages.CITY_SELECTION_PROMPT}",
            parse_mode='Markdown'
        )
        
        # ذخیره موقت شهر در context کاربر (استفاده از کاربر برای مرحله بعد)
        # نکته: در telebot ساده، ما باید خودمان مدیریت وضعیت (State) را انجام دهیم
        bot.set_chat_action(call.message.chat.id, 'typing')

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        """هندلر پیام‌های متنی (نام محصول)"""
        # اینجا باید چک کنیم آیا کاربر شهر را انتخاب کرده یا نه
        # فعلاً یک پاسخ نمایشی می‌دهیم
        bot.reply_to(message, messages.SEARCHING_MESSAGE)
        DeewarScraper()
        PriceAnalyzer()
        bot.reply_to(message , messages.RESULT_MESSAGE_TEMPLATE)
        
        # در مراحل بعد:
        # 1. Scraper را صدا می‌زنیم
        # 2. Analyzer را صدا می‌زنیم
        # 3. نتیجه را به کاربر برمی‌گردانیم
