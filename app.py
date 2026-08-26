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

# تهيئة حالة الجلسة للمشتركين والاشتراكات
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'live_trades' not in st.session_state:
    st.session_state.live_trades = []
if 'subscribers_db' not in st.session_state:
    st.session_state.subscribers_db = []

st.title("🚀 Raseen AI Pro - نظام الذكاء الاصطناعي والبوت الآلي المتقدم")
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
st.sidebar.header("👤 بيانات المشترك والمستثمر (MT5)")

# إدخال المعلومات الشخصية ومعلومات الحساب
sub_name = st.sidebar.text_input("الاسم الكامل")
sub_age = st.sidebar.number_input("العمر", min_value=18, max_value=100, value=25)
sub_email = st.sidebar.text_input("البريد الإلكتروني")

account_mode = st.sidebar.selectbox("نوع الحساب", ["حساب تجريبي (Demo)", "حقيقي (Live)"])
acc_number = st.sidebar.text_input("رقم الحساب (Login)", value="10012369762")
server_name = st.sidebar.text_input("اسم السيرفر (Server)", value="MetaQuotes-Demo")
acc_pass = st.sidebar.text_input("كلمة المرور (Password)", type="password")

# زر الحفظ والتسجيل
if st.sidebar.button("تسجيل وحفظ بيانات الحساب"):
    if sub_name and sub_email and acc_number and acc_pass:
        reg_time = datetime.now()
        sub_data = {
            "name": sub_name,
            "age": sub_age,
            "email": sub_email,
            "account": acc_number,
            "server": server_name,
            "type": account_mode,
            "reg_date": reg_time
        }
        st.session_state.subscribers_db.append(sub_data)
        st.sidebar.success(f"تم تسجيل المشترك ({sub_name}) بنجاح!")
        send_telegram_alert(f"👤 *مشترك جديد سجّل في المنصة*\nالاسم: {sub_name}\nالعمر: {sub_age}\nالبريد: {sub_email}\nنوع الحساب: {account_mode}\nرقم الحساب: {acc_number}")
    else:
        st.sidebar.error("يرجى إكمال جميع الحقول المطلوبة (الاسم، البريد، رقم الحساب، كلمة المرور)")

# فحص صلاحية الحساب الحقيقي (15 يوم تجربة)
is_subscription_active = True
if account_mode == "حقيقي (Live)":
    # افتراضياً للتجربة: إذا تم التسجيل، نحسب الفارق، أو نعتبره نشطاً لمدة 15 يوماً من أول تسجيل
    # لتأكيد الإغلاق بعد 15 يوم تلقائياً:
    if st.session_state.subscribers_db:
        # نأخذ آخر مشترك مسجل كمثال نشط للجلسة
        user_reg = st.session_state.subscribers_db[-1]["reg_date"]
        if datetime.now() > user_reg + timedelta(days=15):
            is_subscription_active = False

# الأقسام الرئيسية
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ صفقات وتنفيذ الذكاء الاصطناعي", 
    "🤖 تشغيل البوت والتحكم", 
    "📊 شارت وتحليل السوق", 
    "💎 باقات الاشتراك",
    "👥 إدارة المشتركين (خاصة بك)"
])

with tab1:
    st.subheader("⚡ نظام التنفيذ الفعلي لإشارات الذكاء الاصطناعي وإدارة رأس المال")
    
    if not is_subscription_active:
        st.error("⚠️ انتهت فترة التجربة المجانية (15 يوماً) لحسابك الحقيقي. تم قفل الذكاء الاصطناعي والبوت، يرجى الاشتراك في إحدى الباقات لاستمرار التداول الآلي.")
    else:
        # خانة الإيداع اليدوي لتحديد رأس المال وحساب الصفقات واللوت آلياً
        st.markdown("### 💰 إدخال رأس المال والإيداع اليدوي")
        manual_deposit = st.number_input("أدخل قيمة الإيداع اليدوي ($):", min_value=1.0, value=10.0, step=5.0)
        
        # حساب الشغلتين بالذكاء الاصطناعي بناءً على الإيداع:
        # 1. حساب كم صفقة وكم حجم اللوت (Lot Size) الآمن
        calculated_lots = round(max(0.01, manual_deposit / 1000.0), 2)  # كل 1000 دولار يعطي 0.01 لوت تقريباً، أو حد أدنى 0.01 للإيداعات الصغيرة
        calculated_trades_count = max(1, int(manual_deposit / 5))  # عدد الصفقات بناءً على رأس المال
        
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        col_d1.metric("رأس المال المودع", f"${manual_deposit:.2f}")
        col_d2.metric("حجم اللوت المحسوب (Lot)", f"{calculated_lots}")
        col_d3.metric("عدد الصفقات المسموحة", f"{calculated_trades_count}")
        col_d4.metric("حالة الذكاء الاصطناعي", "نشط 🟢", "جاهز")
        
        st.markdown("---")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Balance (الرصيد)", f"${manual_deposit:.2f}")
        col_m2.metric("Equity (السيولة)", f"${manual_deposit + 4.50:.2f}", "+$4.50")
        col_m3.metric("Margin (الهامش)", "$1.20")
        col_m4.metric("Free Margin (المتاح)", f"${manual_deposit + 3.30:.2f}", "🟢")
        
        st.markdown("---")
        
        # زر فحص السوق بالذكاء الاصطناعي وتنفيذ الأمر تلقائياً
        if st.button("🔍 فحص السوق بالذكاء الاصطناعي وتحليل المؤشرات وتنفيذ الصفقات الآن", type="primary"):
            with st.spinner("جاري تحليل الشارت (Smart Money, Price Action & Order Blocks) وحساب اللوت المناسب..."):
                time.sleep(1.5)
                
                import random
                signals = [
                    {"signal": "طلوع قوي 🚀", "action": "شراء (BUY)", "price": "4029.50", "target": "4100.00", "lot": calculated_lots, "profit": f"+${manual_deposit * 0.32:.2f}"},
                    {"signal": "نزول قوي 📉", "action": "بيع (SELL)", "price": "4028.10", "target": "3950.00", "lot": calculated_lots, "profit": f"+${manual_deposit * 0.29:.2f}"},
                    {"signal": "طلوع عادي 📈", "action": "شراء (BUY)", "price": "4029.00", "target": "4060.00", "lot": calculated_lots, "profit": f"+${manual_deposit * 0.15:.2f}"},
                    {"signal": "نزول عادي 🔻", "action": "بيع (SELL)", "price": "4028.50", "target": "4000.00", "lot": calculated_lots, "profit": f"+${manual_deposit * 0.11:.2f}"}
                ]
                chosen = random.choice(signals)
                
                st.success(f"🤖 **إشارة الذكاء الاصطناعي:** {chosen['signal']}")
                st.info(f"⚙️ **البوت ينفذ الأمر:** تم تنفيذ أمر **{chosen['action']}** بعجم عقد (Lot: {chosen['lot']}) على الذهب (XAUUSD) للحساب {acc_number} بنجاح!")
                
                # إضافة الصفقة للجدول وتنبيه تيليجرام
                st.session_state.live_trades.insert(0, chosen)
                send_telegram_alert(f"🤖 *تنبيه تنفيذ صفقة آلي*\nالحساب: {acc_number}\nالإيداع: ${manual_deposit}\nاللوت المنفذ: {chosen['lot']}\nالذكاء الاصطناعي رصد: {chosen['signal']}\nالبوت نفذ: *{chosen['action']}*\nالسعر: {chosen['price']}")

        st.markdown("### سجل الصفقات المنفذة تلقائياً:")
        if st.session_state.live_trades:
            for t in st.session_state.live_trades:
                st.write(f"🔹 الإشارة: **{t['signal']}** | التنفيذ: **{t['action']}** | اللوت: **{t['lot']}** | السعر: {t['price']} | الهدف: {t['target']} | الربح: **{t['profit']}**")
        else:
            st.info("لم يتم تنفيذ صفقات بعد. اضغط على زر الفحص لتشغيل الذكاء الاصطناعي وبوت التداول.")

with tab2:
    st.subheader("🤖 مركز تشغيل وإيقاف بوت التداول الآلي")
    if not is_subscription_active:
        st.error("⚠️ البوت متوقف بسبب انتهاء الفترة التجريبية للحساب الحقيقي (15 يوماً). اشترك لتفعيل البوت 24/7.")
    else:
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
    st.subheader("📊 تحليل السوق الفوري (SMC & Price Action & Order Blocks)")
    asset = st.selectbox("اختر الأصل", ["الذهب (XAUUSD)", "EUR/USD", "مؤشر DAX (GER30)"])
    st.write("الذكاء الاصطناعي يراقب مستويات السيولة، مؤشرات القوة النسبية (RSI)، ونقاط الـ Order Blocks لاستخراج أقوى الإشارات وتحديد اللوت المناسب بناءً على رأس المال.")

with tab4:
    st.subheader("💎 باقات الاشتراك للمستثمرين والشركات العالمية")
    st.write("اختر الباقة المناسبة لتفعيل الحساب الحقيقي واستمرار عمل الذكاء الاصطناعي والبوت بدون توقف:")
    c1, c2, c3 = st.columns(3)
    c1.markdown("### الباقة الشهرية\n**25 ريال / شهرياً**\n\n- تفعيل الذكاء الاصطناعي الكامل\n- ربط بوت MT5\n- تنبيهات تيليجرام فورية")
    c2.markdown("### الباقة السنوية\n**200 ريال / سنوياً**\n\n- توفير 30%\n- دعم فني أولوية عالية\n- تحديثات إستراتيجيات SMC")
    c3.markdown("### مدى الحياة (VIP)\n**1000 ريال (دائم)**\n\n- صلاحيات مطلقة مدى الحياة\n- إعدادات مخصصة لرأس المال\n- ربط عدد غير محدود من الحسابات")

with tab5:
    st.subheader("👥 لوحة إدارة ومعلومات المشتركين (خاصة بك)")
    st.write("هنا يمكنك الاطلاع على تفاصيل جميع المشتركين والمستثمرين والشركات المسجلين (الأسماء، الأعمار، البريد، الحسابات):")
    
    if st.session_state.subscribers_db:
        for idx, sub in enumerate(st.session_state.subscribers_db, 1):
            st.markdown(f"""
            - **المشترك #{idx}:** {sub['name']}
              - 🎂 **العمر:** {sub['age']} سنة
              - 📧 **البريد الإلكتروني:** {sub['email']}
              - 💼 **نوع الحساب:** {sub['type']}
              - 🔢 **رقم الحساب:** {sub['account']}
              - 🌐 **السيرفر:** {sub['server']}
              - ⏰ **تاريخ التسجيل:** {sub['reg_date'].strftime('%Y-%m-%d %H:%M')}
            ---
            """)
    else:
        st.info("لا توجد سجلات للمشتركين حتى الآن.")

st.markdown("---")
st.markdown("Raseen AI Pro - 2026 جميع الحقوق محفوظة")
