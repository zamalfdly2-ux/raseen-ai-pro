import time
import requests
import MetaTrader5 as mt5

# --- إعدادات الحسابات (التجريبي والحقيقي) ---
ACCOUNTS = {
    "demo": {
        "server": "MetaQuotes-Demo",
        "login": 10012369762,
        "password": "JxOnC@7p"
    },
    "real": {
        "server": "YOUR_BROKER_REAL_SERVER",  # استبدله باسم سيرفر الشركة الحقيقي
        "login": 123456789,                    # استبدله برقم حسابك الحقيقي
        "password": "YOUR_REAL_PASSWORD"       # استبدله بكلمة مرور الحقيقي
    }
}

# ⚡ اختر وضع التشغيل هنا: اكتب "demo" للتجريبي أو "real" للحقيقي
MODE = "demo" 

# --- إعدادات تيليجرام ---
TELEGRAM_CONFIG = {
    "bot_token": "8858466092:AAF2_YCAukhlvrKgVbBD0levV0i6Gbuag90",
    "chat_id": "1370315348",
    "enabled": True
}

# --- إعدادات الاستراتيجية والأصول (الذهب) ---
SYMBOL = "XAUUSD"
LOT_SEQUENCE = [0.01, 0.02, 0.03, 0.05]  # الصفقات المتسلسلة
SL_PIPS = 300  # وقف الخسارة
TP_PIPS = 600  # جني الأرباح

def send_telegram_alert(message):
    """إرسال إشعار فوري إلى تيليجرام"""
    if not TELEGRAM_CONFIG["enabled"]:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CONFIG["chat_id"],
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Telegram Error: {e}")

def initialize_mt5():
    acc = ACCOUNTS[MODE]
    print(f"🔄 جاري الاتصال بمنصة MetaTrader 5 ({MODE.upper()} Account)...")
    
    if not mt5.initialize(login=acc["login"], 
                          password=acc["password"], 
                          server=acc["server"]):
        print(f"فشل الاتصال، الكود: {mt5.last_error()}")
        return False
        
    print(f"✅ تم الاتصال بنجاح بـحساب الـ {MODE.upper()}.")
    return True

def analyze_and_execute():
    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        print(f"⚠️ الأصل {SYMBOL} غير متوفر.")
        return

    if not symbol_info.visible:
        if not mt5.symbol_select(SYMBOL, True):
            print(f"⚠️ تعذر تفعيل الأصل {SYMBOL}.")
            return

    tick = mt5.symbol_info_tick(SYMBOL)
    if tick is None:
        print("⚠️ تعذر جلب بيانات السعر الحالية.")
        return

    point = symbol_info.point
    price = tick.bid
    
    print(f"📊 تحليل السوق لـ {SYMBOL} | السعر الحالي: {price} [حساب: {MODE.upper()}]")
    print("🚀 جاري تنفيذ صفقات الحزمة المتسلسلة...")

    for lot in LOT_SEQUENCE:
        sl = price - (SL_PIPS * point)
        tp = price + (TP_PIPS * point)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": tick.ask,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 20260825,
            "comment": f"Raseen AI Pro ({MODE})",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            msg = (
                f"🤖 *Raseen AI Pro - تنبيه صفقة جديدة*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🏷️ النوع: `{MODE.upper()}`\n"
                f"📌 الأصل: `{SYMBOL}`\n"
                f"⚡ الإجراء: *BUY (شراء)*\n"
                f"📦 حجم اللوت: `{lot}`\n"
                f"💰 سعر الدخول: `{tick.ask}`\n"
                f"⏱️ الوقت: `{timestamp_str}`\n"
                f"💬 الحالة: *تم التنفيذ بنجاح*"
            )
            print(f"🔵 [تم التنفيذ] صفقة شراء | لوت: {lot} | بسعر: {tick.ask}")
            send_telegram_alert(msg)
        else:
            print(f"❌ [فشل التنفيذ] للوت {lot}، الكود: {result.retcode}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    if initialize_mt5():
        try:
            while True:
                print("\n--- 🔍 فحص إشارات السوق الجديدة ---")
                analyze_and_execute()
                print("⏳ الانتظار للفحص القادم (خلال 60 ثانية)...")
                time.sleep(60)
        except KeyboardInterrupt:
            print("🛑 تم إيقاف البوت بواسطة المستخدم.")
            mt5.shutdown()
