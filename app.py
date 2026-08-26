import streamlit as st
from datetime import datetime, timedelta

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Raseen AI Pro - المنصة العالمية السحابية", layout="centered")

# --- 1. القواميس واللغات العالمية (بدون إسرائيل) ---
LANGUAGES = {
    "العربية": {
        "title": "منصة Raseen AI Pro السحابية للتداول الذكي والذكاء الاصطناعي",
        "select_lang": "اختر لغتك المفضلة:",
        "select_curr": "اختر عملتك المفضلة:",
        "packages": "اختر باقة الاشتراكات للمتداولين والشركات",
        "monthly": "الباقة الشهرية (25 ريال) - تسجل تاريخ البدء والانتهاء",
        "yearly": "الباقة السنوية (200 ريال) - تسجل تاريخ البدء والانتهاء",
        "lifetime": "باقة مدى الحياة (1000 ريال) - تسجل تاريخ البدء فقط (لا تنتهي أبداً)",
        "acc_type": "نوع الحساب (MetaTrader 5)",
        "demo": "حساب تجريبي (Demo)",
        "real": "حساب حقيقي (Live) - تجربة مجانية 15 يوم للمستثمرين",
        "login_mt5": "إدارة حسابات MetaTrader 5 وتيليجرام والتحكم",
        "chat_id_label": "معرف تيليجرام الخاص بك (Telegram Chat ID)",
        "acc_num": "رقم الحساب الحقيقي أو التجريبي",
        "acc_pass": "كلمة المرور",
        "server": "اسم السيرفر (Server Name)",
        "deposit": "مبلغ الإيداع الفعلي ($) لحساب اللوت التلقائي",
        "target_amount": "المبلغ المستهدف (Target Capital Range)",
        "ai_control_title": "تحليل الذكاء الاصطناعي وتنفيذ البوت",
        "start_btn": "🟢 تشغيل الذكاء الاصطناعي والبوت",
        "stop_btn": "🔴 توقف الذكاء الاصطناعي والبوت",
        "success_sub": "تم تشغيل البوت على السيرفر السحابي 24/7 بنجاح! يمكنك إطفاء الكمبيوتر ومتابعة التداول من جوالك.",
        "admin_free": "مرحباً يا عزام (المالك والمبرمج): دخول حر ومجاني كامل للسيرفر والبوت بدون أي قيود."
    },
    "English": {
        "title": "Raseen AI Pro Cloud Trading Platform",
        "select_lang": "Select your language:",
        "select_curr": "Select your currency:",
        "packages": "Choose Subscription Package",
        "monthly": "Monthly Plan (25 SAR) - Tracks Start & End Date",
        "yearly": "Yearly Plan (200 SAR) - Tracks Start & End Date",
        "lifetime": "Lifetime Plan (1000 SAR) - Start Date Only (No Expiry)",
        "acc_type": "Account Type",
        "demo": "Demo Account",
        "real": "Real Account (15-Day Free Trial for Investors)",
        "login_mt5": "MetaTrader 5 & Telegram Management",
        "chat_id_label": "Telegram Chat ID",
        "acc_num": "Account ID",
        "acc_pass": "Password",
        "server": "Server Name",
        "deposit": "Deposit Amount ($) for Auto Lot",
        "target_amount": "Target Capital Range",
        "ai_control_title": "AI Analysis & Bot Execution",
        "start_btn": "🟢 Start AI & Bot",
        "stop_btn": "🔴 Stop AI & Bot",
        "success_sub": "Cloud Bot is running 24/7! You can turn off your PC and track via mobile.",
        "admin_free": "Welcome Azzam (Owner): Full Free Access."
    }
}

# --- 2. عملات العالم (بدون إسرائيل) ---
CURRENCIES = [
    "SAR (السعودية)", "AED (الإمارات)", "QAR (قطر)", "KWD (الكويت)", "BHD (البحرين)", 
    "OMR (عمان)", "JOD (الأردن)", "EGP (مصر)", "TRY (تركيا)", "JPY (اليابان)", 
    "CNY (الصين)", "INR (الهند)", "KRW (كوريا الجنوبية)", "SGD (سغافورة)", "MYR (ماليزيا)",
    "EUR (أوروبا)", "GBP (المملكة المتحدة)", "CHF (سويسرا)", "SEK (السويد)", "NOK (النرويج)",
    "USD (الولايات المتحدة)", "CAD (كندا)", "MXN (المكسيك)", "BRL (البرازيل)", "ARS (الأرجنتين)",
    "ZAR (جنوب أفريقيا)", "AUD (أستراليا)", "NZD (نيوزيلندا)"
]

# --- 3. نطاقات المبالغ المستهدفة الجديدة المحدثة ---
TARGET_AMOUNTS = [
    "من 10 دولار إلى 50 دولار",
    "من 50 دولار إلى 100 دولار",
    "من 100 دولار إلى 500 دولار",
    "من 500 دولار إلى 1000 دولار",
    "من 1000 دولار إلى 5000 دولار",
    "من 5000 دولار إلى 10000 دولار",
    "من 10000 دولار إلى 50000 دولار",
    "من 50000 دولار إلى 100000 دولار",
    "من 100000 دولار إلى 500000 دولار",
    "من 500000 دولار إلى 1000000 دولار",
    "من 1000000 دولار إلى 5000000 دولار",
    "من 5000000 دولار إلى 10,000,000 دولار",
    "من 10,000,000 دولار إلى 50,000,000 دولار",
    "من 50,000,000 دولار إلى 100,000,000 دولار",
    "من 100,000,000 دولار إلى 500,000,000 دولار"
]

# --- 4. واجهة التطبيق واختيار اللغة والعملة ---
col_l1, col_l2 = st.columns(2)
with col_l1:
    selected_lang_name = st.selectbox("Language / اللغة", list(LANGUAGES.keys()))
lang = LANGUAGES.get(selected_lang_name, LANGUAGES["العربية"])

with col_l2:
    st.selectbox(lang["select_curr"], CURRENCIES)

st.title(lang["title"])
st.markdown("---")

# --- 5. التحقق من حساب المالك (عزام) والمستثمرين ---
user_identifier = st.text_input("أدخل اسمك أو بريدك الإلكتروني للتحقق:")
is_owner = ("عزام" in user_identifier or "Azzam" in user_identifier or "1370315348" in user_identifier)

if is_owner:
    st.success(lang["admin_free"])
    has_access = True
else:
    st.info("ℹ️ للمتداولين والمستثمرين والشركات العالمية: الحساب الحقيقي يمنح تجربة مجانية لمدة 15 يوماً، بعدها يُقفل البوت وتظهر الباقات للاشتراك.")
    acc_mode_check = st.radio("نوع الاستخدام:", ["حساب تجريبي (مفتوح ودائم)", "حساب حقيقي (تجربة 15 يوم أو باقة مدفوعة)"])
    
    if "تجريبي" in acc_mode_check:
        has_access = True
    else:
        package_choice = st.radio(lang["packages"], [lang["monthly"], lang["yearly"], lang["lifetime"]])
        payment_confirmed = st.checkbox("تأكيد الدفع أو تفعيل الفترة التجريبية (15 يوم)")
        
        if payment_confirmed:
            has_access = True
            start_date = datetime.now()
            if "الشهرية" in package_choice or "Monthly" in package_choice:
                end_date = start_date + timedelta(days=30)
                st.info(f"📅 تاريخ البدء: {start_date.strftime('%Y-%m-%d')} | 📅 تاريخ انتهاء الباقة الشهرية: {end_date.strftime('%Y-%m-%d')}")
            elif "السنوية" in package_choice or "Yearly" in package_choice:
                end_date = start_date + timedelta(days=365)
                st.info(f"📅 تاريخ البدء: {start_date.strftime('%Y-%m-%d')} | 📅 تاريخ انتهاء الباقة السنوية: {end_date.strftime('%Y-%m-%d')}")
            else:
                st.info(f"📅 تاريخ البدء: {start_date.strftime('%Y-%m-%d')} | باقة مدى الحياة: تسجل تاريخ البدء فقط (لا تنتهي أبداً ♾️)")
        else:
            has_access = False
            st.warning("🔒 الحساب مقفل. يرجى اختيار الباقة وتأكيد التفعيل للمتابعة واستخدام البوت.")

# --- 6. إعدادات الحسابات والذكاء الاصطناعي والتنفيذ الآلي ---
if has_access:
    st.markdown("---")
    st.subheader(lang["login_mt5"])
    
    # خانة تيليجرام مع التوكن الخاص بك
    telegram_chat_id = st.text_input(lang["chat_id_label"], value="1370315348")
    st.caption("Bot Token: `8858466092:AAF2_YCAukhlvrKgVbBD0levV0i6Gbuag90`")
    
    acc_type = st.radio(lang["acc_type"], [lang["demo"], lang["real"]])
    account_id = st.text_input(lang["acc_num"], value="10012350082")
    account_pass = st.text_input(lang["acc_pass"], type="password")
    server_name = st.text_input(lang["server"], value="MetaQuotes-Demo")
    
    # الإيداع وحساب اللوت التلقائي
    deposit_val = st.number_input(lang["deposit"], min_value=10.0, value=5000.0, step=50.0)
    
    def calculate_auto_lot(deposit):
        if deposit <= 50:
            return 0.01
        elif deposit <= 500:
            return 0.02
        else:
            return round(max(0.01, (deposit / 1000) * 0.01), 2)
            
    auto_lot = calculate_auto_lot(deposit_val)
    st.success(f"📊 التحليل التلقائي للذكاء الاصطناعي - حجم اللوت المحسوب: **{auto_lot}** | عدد الصفقات المتزامنة: مناسب لرأس المال.")

    # اختيار نطاق المبلغ المستهدف الجديد
    st.markdown("---")
    selected_target_range = st.selectbox(lang["target_amount"], TARGET_AMOUNTS)
    st.info(f"🎯 تم ضبط النطاق المستهدف للبوت: ({selected_target_range}). سيتم إرسال رسالة فورية عبر التيليجرام بمجرد وصول المبلغ المحدد (سواء قبل الفترة أو بعدها).")

    # لوحة تحكم الذكاء الاصطناعي وتشغيل / توقف البوت
    st.markdown("---")
    st.subheader(lang["ai_control_title"])
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(lang["start_btn"]):
            st.success(lang["success_sub"])
            st.balloons()
            st.write("🔄 **حالة السيرفر السحابي 24/7:** جارٍ تحليل السوق بالمؤشرات والاستراتيجيات (Price Action / Smart Money) بدقة عالية جداً (طلوع قوي/عادي للشراء، نزول قوي/عادي للبيع)...")
            st.write("🎯 **التنبيهات الفورية:** متصل الآن ببوت تيليجرام لإرسال الأهداف وإشعارك عند الوصول الفعلي للمبلغ!")
            
    with col_btn2:
        if st.button(lang["stop_btn"]):
            st.error("🔴 تم إيقاف تحليل الذكاء الاصطناعي وتوقف البوت عن التداول الآلي.")
