import MetaTrader5 as mt5

# 1. الاتصال ببرنامج MetaTrader 5 الأساسي
if not mt5.initialize():
    print("فشل الاتصال ببرنامج MT5، تأكد أنه مفتوح.")
    mt5.shutdown()

# 2. تسجيل الدخول باستخدام معلومات حسابك الفعلي
account_id = 10012369762  # رقم حسابك
account_password = "اكتب_كلمة_المرور_هنا"  # كلمة مرور حسابك
server_name = "MetaQuotes-Demo"  # اسم السيرفر

authorized = mt5.login(account_id, password=account_password, server=server_name)

if authorized:
    print(f"تم تسجيل الدخول بنجاح على الحساب: {account_id} 🟢")
    
    # جلب معلومات الحساب للتأكد (الرصيد والسيولة)
    account_info = mt5.account_info()
    if account_info != None:
        print(f"رصيد الحساب (Balance): {account_info.balance}")
        print(f"السيولة (Equity): {account_info.equity}")
else:
    print(f"فشل تسجيل الدخول، رمز الخطأ: {mt5.last_error()}")
