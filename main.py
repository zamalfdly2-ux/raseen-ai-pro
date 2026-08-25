import time
import requests
import numpy as np

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

ACCOUNTS = {
    "Demo": {
        "server": "MetaQuotes-Demo",
        "login": 10012369762,
        "password": "JxOnC@7p",
        "active": True
    }
}

TARGET_ASSETS = {
    "Gold": {
        "symbol": "XAUUSD", 
        "lots": [0.01, 0.02, 0.03, 0.05], 
        "sl_pips": 300, 
        "tp_pips": 600
    }
}

TELEGRAM_CONFIG = {
    "bot_token": "YOUR_BOT_TOKEN_HERE",
    "chat_id": "YOUR_CHAT_ID_HERE",
    "enabled": False
}

def send_telegram_alert(message):
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

def execute_multi_orders_with_risk():
    print("=" * 60)
    print("Raseen AI Pro - Bot Started")
    print("=" * 60)
    
    if not MT5_AVAILABLE:
        print("MetaTrader5 library is not available.")
        return

    for acc_name, acc_info in ACCOUNTS.items():
        if not acc_info["active"]:
            continue
            
        print(f"Connecting to account: {acc_info['login']}")
        if not mt5.initialize(login=acc_info["login"], password=acc_info["password"], server=acc_info["server"]):
            print(f"Connection failed: {mt5.last_error()}")
            continue
            
        print("Connected successfully. Analyzing and executing...")
                
        for asset_key, asset_val in TARGET_ASSETS.items():
            symbol = asset_val["symbol"]
            symbol_info = mt5.symbol_info(symbol)
            
            if symbol_info is None or not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    print(f"Failed to select symbol {symbol}")
                    continue
                    
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                print("Failed to get market tick data")
                continue
                
            point = symbol_info.point
            
            for lot in asset_val["lots"]:
                price = tick.ask
                sl = price - (asset_val["sl_pips"] * point)
                tp = price + (asset_val["tp_pips"] * point)
                
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_BUY,
                    "price": price,
                    "sl": sl,
                    "tp": tp,
                    "deviation": 20,
                    "magic": 202608,
                    "comment": "Raseen AI Pro Grid",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_FOK,
                }
                
                result = mt5.order_send(request)
                timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
                
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    msg = f"Raseen AI Pro Executed: {symbol} | Lot: {lot} | Price: {price} | Time: {timestamp_str}"
                    print(msg)
                    send_telegram_alert(msg)
                else:
                    print(f"Order failed for lot {lot}. Error code: {result.retcode}")
                
                time.sleep(0.3)
            
        mt5.shutdown()
        print("Session closed.")

if __name__ == "__main__":
    execute_multi_orders_with_risk()
