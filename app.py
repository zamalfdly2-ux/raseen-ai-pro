import streamlit as st
import time
import requests
from datetime import datetime, timedelta

# إعدادات الصفحة
st.set_page_config(
    page_title="Raseen AI Pro - Smart Trading & Bot System",
    page_icon="🤖",
    layout="wide"
)

# بيانات تيليجرام الخاصة بك
TELEGRAM_BOT_TOKEN = "8858466092:AAF2_YCAukhlvrKgVbBD0levV0i6Gbuag90"
TELEGRAM_CHAT_ID = "1370315348"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
    except:
        pass

# تهيئة حالة الجلسة
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'subscription_status' not in st.session_state:
    st.session_state.subscription_status = "تجريبي (متاح لمدة 15 يوم)"
if 'live_trades' not in st.session_state:
    st.session_state.live_trades = []

st.title("🚀 Raseen AI Pro - ربط تحليل الذكاء الاصطناعي بتنفيذ البوت الآلي")
st.markdown("---")

# الدول واللغات (بدون إسرائيل)
countries_list = [
    "المملكة العربية السعودية", "المملكة المتحدة", "الولايات المتحدة الأمريكية", 
    "البرازيل", "الأرجنتين", "فرنسا", "ألمانيا", "إسبانيا", "إيطاليا", 
    "البرتغال", "المغرب", "اليابان", "كوريا الجنوبية", "مصر", "قطر", 
    "الإمارات العربية المتحدة", "المكسيك", "كندا", "أستراليا"
]
languages_list = ["العربية", "English", "Español", "Français", "Deutsch", "Italiano", "Português", "日本語"]

st.sidebar.header("🌐 إعدادات المنصة")
selected_country = st.sidebar.selectbox("اختر الدولة", countries_list)
selected_lang = st.sidebar.selectbox("اختر اللغة", languages_list)

st.sidebar.markdown("---")
st.sidebar.header("🔐 بيانات الحساب (MT5)")
account_mode = st.sidebar.selectbox("نوع الحساب", ["حساب تجريبي (Demo)", "حقيقي (Live)"])
acc_number = st.sidebar.text_input("رقم الحساب", value="10012369762")
acc_pass = st.sidebar.text_input("كلمة المرور", type="password")

if st.sidebar.button("ربط الحساب"):
    if acc_number:
        st.sidebar.success(f"تم ربط الحساب ({acc_number}) بنجاح!")

# الأقسام الرئيسية
tab1, tab2, tab3, tab4 = st.tabs(["⚡ صفقات وتنفيذ الذكاء الاصطناعي", "🤖 تشغيل البوت والتحكم", "📊 شارت وتحليل السوق", "💎 باقات الاشتراك"])

with tab1:
    st.subheader("⚡ نظام التنفيذ الفعلي لإشارات الذكاء الاصطناعي (AI to Bot Execution)")
    st.write("يقوم الذكاء الاصطناعي بتحليل السوق وإرسال الأمر للبوت (شراء/بيع بناءً على قوة الحركة).")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Balance (الرصيد)", "$5,000.00")
    col_m2.metric("Equity (السيولة)", "$5,450.00", "+$450")
    col_m3.metric("Margin (الهامش)", "$120.50")
    col_m4.metric("Free Margin (المتاح)", "$5,329.50", "🟢")
    
    st.markdown("---")
    
    # زر فحص السوق وتنفيذ الأمر تلقائياً
    if st.button("🔍 فحص السوق بالذكاء الاصطناعي وتنفيذ الأمر الآن", type="primary"):
        with st.spinner("جاري تحليل الشارت (Smart Money & Price Action)..."):
            time.sleep(1.5)
            
            # محاكاة قرار الذكاء الاصطناعي (طلوع قوي، نزول قوي، إلخ)
            import random
            signals = [
                {"signal": "طلوع قوي 🚀", "action": "شراء (BUY)", "price": "4029.50", "target": "4100.00", "profit": "+$320.00"},
                {"signal": "نزول قوي 📉", "action": "بيع (SELL)", "price": "4028.10", "target": "3950.00", "profit": "+$290.50"},
                {"signal": "طلوع عادي 📈", "action": "شراء (BUY)", "price": "4029.00", "target": "4060.00", "profit": "+$150.00"},
                {"signal": "نزول عادي 🔻", "action": "بيع (SELL)", "price": "4028.50", "target": "4000.00", "profit": "+$110.00"}
            ]
            chosen = random.choice(signals)
            
            st.success(f"🤖 **إشارة الذكاء الاصطناعي:** {chosen['signal']}")
            st.info(f"⚙️ **البوت ينفذ الأمر:** تم تنفيذ أمر **{chosen['action']}** على الذهب (XAUUSD) بنجاح!")
            
            # إضافة الصفقة للجدول وتنبيه تيليجرام
            st.session_state.live_trades.insert(0, chosen)
            send_telegram_alert(f"🤖 *تنبيه تنفيذ صفقة*\nالذكاء الاصطناعي رصد: {chosen['signal']}\nالبوت نفذ: *{chosen['action']}*\nالسعر: {chosen['price']}")

    st.markdown("### سجل الصفقات المنفذة تلقائياً:")
    if st.session_state.live_trades:
        for t in st.session_state.live_trades:
            st.write(f"🔹 الإشارة: **{t['signal']}** | التنفيذ: **{t['action']}** | السعر: {t['price']} | الهدف: {t['target']} | الربح: **{t['profit']}**")
    else:
        st.info("لم يتم تنفيذ صفقات بعد. اضغط على زر الفحص لتشغيل الذكاء الاصطناعي والبوت.")

with tab2:
    st.subheader("🤖 مركز تشغيل وإيقاف بوت التداول الآلي")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("🟢 تشغيل البوت والذكاء الاصطناعي (24/7)"):
            st.session_state.bot_running = True
            st.success("تم تشغيل البوت على السحابة ليتلقى أوامر الذكاء الاصطناعي وينفذها مباشرة!")
            send_telegram_alert("🟢 *تشغيل النظام*\nتم تشغيل بوت Raseen AI Pro لاستقبال إشارات الذكاء الاصطناعي وتنفيدها.")
    with c_btn2:
        if st.button("🔴 إيقاف البوت"):
            st.session_state.bot_running = False
            st.warning("تم إيقاف البوت مؤقتاً.")
            send_telegram_alert("🔴 *إيقاف النظام*\nتم إيقاف بوت Raseen AI Pro مؤقتاً.")
            
    if st.session_state.bot_running:
        st.success("حالة الخادم: Server is online 🟢 (البوت يترجم إشارات الذكاء الاصطناعي وينفذها لحظياً)")
    else:
        st.error("حالة الخادم: Server is offline 🔴")

with tab3:
    st.subheader("📊 تحليل السوق الفوري (SMC & Price Action)")
    asset = st.selectbox("اختر الأصل", ["الذهب (XAUUSD)", "EUR/USD", "مؤشر DAX (GER30)"])
    st.write("الذكاء الاصطناعي يراقب مستويات السيولة ونقاط الـ Order Blocks لاستخراج إشارات (طلوع قوي/عادي - نزول قوي/عادي).")

with tab4:
    st.subheader("💎 باقات الاشتراك للمستثمرين والشركات العالمية")
    st.write("فترة التجربة للحسابات الحقيقية (15 يوماً)، وبعدها تفعيل الباقات:")
    c1, c2, c3 = st.columns(3)
    c1.markdown("### الباقة الشهرية\n**25 ريال / شهرياً**")
    c2.markdown("### الباقة السنوية\n**200 ريال / سنوياً**")
    c3.markdown("### مدى الحياة (VIP)\n**1000 ريال (دائم)**")

st.markdown("---")
st.markdown("Raseen AI Pro - 2026 جميع الحقوق محفوظة")
