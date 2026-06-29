# این فایل باعث می‌شود کلاس‌های داخل پوشه آنالیز 
# به راحتی از بیرون قابل دسترسی باشند.

from analyzer.price_analyzer import PriceAnalyzer , MarketAnalyzer

# با این کار، وقتی در فایل اصلی می‌گویی:
# from analyzer import MarketAnalyzer
# مستقیماً به کلاس دسترسی داری و نیازی نیست آدرس طولانی بدهی.