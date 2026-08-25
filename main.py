==========================================
‏# Raseen AI Pro - Complete Execution & Risk Bot
# ==========================================

‏import time
‏import requests
‏import numpy as np

‏try:
‏    import MetaTrader5 as mt5
‏    MT5_AVAILABLE = True
‏except ImportError:
‏    MT5_AVAILABLE = False

# --- 1. إعدادات حسابات التداول (تجريبي وحقيقي) ---
‏ACCOUNTS = {
‏    "Demo": {
‏        "server": "MetaQuotes-Demo",
‏        "login": 10012369762,
‏        "password": "JxOnC@7p",
‏        "active": True
    },
‏    "Real": {
‏        "server": "YOUR_REAL_SERVER",
‏        "login": 00000000,
‏        "password": "YOUR_REAL_PASSWORD",
‏        "active": False
    }
}

# --- 2. الأصول المستهدفة مع إعدادات إدارة المخاطر (صفقات متسلسلة وأرباح زرقاء) ---
‏TARGET_ASSETS = {
‏    "Gold": {
‏        "symbol": "XAUUSD", 
‏        "lots": [0.01, 0.02, 0.03, 0.05], 
‏        "sl_pips": 300, 
‏        "tp_pips": 600
    }
}

# --- 3. إعدادات تيليجرام للإشعارات الفورية ---
‏TELEGRAM_CONFIG = {
‏    "bot_token": "YOUR_BOT_TOKEN_HERE",
‏    "chat_id": "YOUR_CHAT_ID_HERE",
‏    "enabled": False  # ضعها True عند إضافة التوكن الخاص بك
}

‏def send_telegram_alert(message):
    """إرسال إشعار تفصيلي بوقت التنفيذ وتأكيد وصول الصفقة للتيليجرام"""
‏    if not TELEGRAM_CONFIG["enabled"]:
‏        return
‏    url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"
‏    payload = {
‏        "chat_id": TELEGRAM_CONFIG["chat_id"],
‏        "text": message,
‏        "parse_mode": "Markdown"
    }
‏    try:
‏        requests.post(url, json=payload, timeout=5)
‏    except Exception as e:
‏        print(f"Telegram Error: {e}")

# --- 4. دالة التنفيذ المتسلسل مع مستويات الأمان (SL & TP) ---
‏def execute_multi_orders_with_risk():
‏    print("=" * 60)
‏    print("🚀 بدء تشغيل روبوت التداول الذكي: Raseen AI Pro")
‏    print("=" * 60)
    
‏    if not MT5_AVAILABLE:
‏        print("⚠️ مكتبة MetaTrader5 غير مثبتة. يرجى تثبيتها عبر: pip install MetaTrader5")
‏        return

‏    for acc_name, acc_info in ACCOUNTS.items():
‏        if not acc_info["active"]:
‏            continue
            
‏        print(f"\n💼 الاتصال بالحساب ({acc_name}): {acc_info['login']}")
‏        if not mt5.initialize(login=acc_info["login"], password=acc_info["password"], server=acc_info["server"]):
‏            print(f"❌ فشل الاتصال: {mt5.last_error()}")
‏            continue
            
‏        print("✅ تم الاتصال بنجاح بالمنصة، جاري تحليل السوق وتنفيذ الصفقات...")
                
‏        for asset_key, asset_val in TARGET_ASSETS.items():
‏            symbol = asset_val["symbol"]
‏            symbol_info = mt5.symbol_info(symbol)
            
‏            if symbol_info is None or not symbol_info.visible:
‏                if not mt5.symbol_select(symbol, True):
‏                    print(f"❌ فشل تفعيل الرمز {symbol}")
‏                    continue
                    
‏            tick = mt5.symbol_info_tick(symbol)
‏            if tick is None:
‏                print("❌ فشل جلب أسعار السوق الحالية")
‏                continue
                
‏            point = symbol_info.point
            
            # حلقة لتنفيذ صفقات متعددة ومتسلسلة (تظهر أرباحها باللون الأزرق على الآيفون)
‏            for lot in asset_val["lots"]:
‏                price = tick.ask
‏                sl = price - (asset_val["sl_pips"] * point)
‏                tp = price + (asset_val["tp_pips"] * point)
                
‏                request = {
‏                    "action": mt5.TRADE_ACTION_DEAL,
‏                    "symbol": symbol,
‏                    "volume": lot,
‏                    "type": mt5.ORDER_TYPE_BUY,
‏                    "price": price,
‏                    "sl": sl,
‏                    "tp": tp,
‏                    "deviation": 20,
‏                    "magic": 202608,
‏                    "comment": "Raseen AI Pro Grid",
‏                    "type_time": mt5.ORDER_TIME_GTC,
‏                    "type_filling": mt5.ORDER_FILLING_FOK,
                }
                
‏                execution_start_time = time.time()
‏                result = mt5.order_send(request)
‏                execution_duration = round(time.time() - execution_start_time, 3)
‏                timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
                
‏                if result.retcode == mt5.TRADE_RETCODE_DONE:
‏                    msg = (
‏                        f"🤖 *Raseen AI Pro - تقرير التنفيذ الآلي*\n"
‏                        f"━━━━━━━━━━━━━━━━━━━━━━\n"
‏                        f"🏢 الحساب: `{acc_name}` ({acc_info['login']})\n"
‏                        f"📌 الأصل: `{symbol}`\n"
‏                        f"⚡ الإجراء: *BUY (شراء)*\n"
‏                        f"📦 اللوت: `{lot}`\n"
‏                        f"🛑 وقف الخسارة (SL): `{sl}`\n"
‏                        f"🎯 جني الأرباح (TP): `{tp}`\n"
‏                        f"⏱️ وقت التنفيذ: `{timestamp_str}` (استغرق {execution_duration} ثانية)\n"
‏                        f"💬 الحالة: *تم تنفيذ الصفقة بنجاح*"
                    )
‏                    print(msg)
‏                    print("-" * 50)
‏                    send_telegram_alert(msg)
‏                else:
‏                    print(f"⚠️ خطأ في تنفيذ اللوت {lot}. كود الخطأ: {result.retcode}")
                
‏                time.sleep(0.3)
            
‏        mt5.shutdown()
‏        print("🔒 تم إغلاق جلسة الاتصال بلطف.")

‏if __name__ == "__main__":
‏    execute_multi_orders_with_risk()
