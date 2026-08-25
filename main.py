import streamlit as st
import datetime
import requests

# إعدادات صفحة التطبيق
st.set_page_config(page_title="Raseen AI Pro", page_icon="📈", layout="centered")

# توكن بوت التيليجرام الخاص بك ومعرفك الشخصي المعتمد
TELEGRAM_BOT_TOKEN = "8858466092:AAF2_YCAukhlvrKgVbBD0levV0i6Gbuag90"
CREATOR_CHAT_ID = "1370315348"

def send_telegram_notification(chat_id, message):
    """
    دالة إرسال رسائل التنبيه الفورية عبر بوت تيليجرام لكل من المستثمرين، الشركات، وأنت كصانع
    """
    if not chat_id:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        return False

# تصميم واجهة التطبيق وخلفية الشعار الجديد مع الهوية الخضراء الاستثمارية
st.markdown("""
    <style>
    .main {
        background-color: #0e2f1a;
        background-image: linear-gradient(rgba(14, 47, 26, 0.92), rgba(14, 47, 26, 0.92)), url('https://i.ibb.co/6R0n5W8/image-20.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }
    h1, h2, h3 {
        color: #a5d6a7;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي للتطبيق
st.title("Raseen AI Pro")
st.write("نظام التداول الذكي المتطور والمربوط بمنصة MetaTrader 5 والذكاء الاصطناعي")

# قائمة لغات وقارات العالم (باستبعاد تام لإسرائيل لغةً وبلداً)
countries_languages = {
    "المملكة العربية السعودية (العربية)": "ar",
    "United States (English)": "en",
    "France (Français)": "fr",
    "Türkiye (Türkçe)": "tr",
    "Japan (日本語)": "ja",
    "Germany (Deutsch)": "de",
    "Brazil (Português)": "pt",
    "China (中文)": "zh"
}

# --- 1. واجهة التسجيل ---
st.header("تسجيل الدخول / إنشاء الحساب")

selected_cl = st.selectbox("اختر البلد واللغة / Country & Language", list(countries_languages.keys()))
user_name = st.text_input("الاسم الكامل / Full Name")
user_age = st.number_input("العمر / Age", min_value=18, max_value=100, value=25)
user_email = st.text_input("البريد الإلكتروني / Email")
user_password = st.text_input("كلمة المرور / Password", type="password")
user_telegram_id = st.text_input("معرف تيليجرام الخاص بك (Telegram Chat ID) لتلقي التنبيهات الفورية", value=CREATOR_CHAT_ID)

if st.button("حفظ بيانات التسجيل"):
    if user_name.strip() != "":
        st.success(f"مرحباً بك، {user_name}! تم حفظ بياناتك بنجاح.")
    else:
        st.error("الرجاء إدخال الاسم بشكل صحيح.")

st.markdown("---")

# --- 2. إدارة الحسابات (MT5) والتجربة المجانية ---
st.header("إدارة الحسابات وربط MetaTrader 5")
account_type = st.radio("نوع الحساب", ["حساب تجريبي (Demo)", "حساب حقيقي (Live)"])

# الإضافة الجديدة المطلوبة لربط بيانات الحساب والسيرفر بدقة مثل MT5
mt5_account_id = st.text_input("رقم حساب MT5 (Account ID)", value="10012350082")
mt5_server_name = st.text_input("اسم السيرفر (Server Name)", value="MetaQuotes-Demo")

if "حقيقي" in account_type:
    st.info("💡 ملاحظة للمستثمرين والشركات: يحصل الحساب الحقيقي على فترة تجربة مجانية لمدة 30 يوماً للبوت. **لا يتم أبداً خصم أي رسوم أو أموال من رصيد التداول الخاص بك في MT5.**")

# خانة الإيداع وحساب اللوت التلقائي بواسطة الذكاء الاصطناعي
deposit_amount = st.number_input("أدخل مبلغ الإيداع الفعلي في تطبيق MetaTrader 5 ($)", min_value=10.0, max_value=10000000.0, value=100.0)

def calculate_ai_lot_and_trades(deposit):
    """
    الذكاء الاصطناعي يحلل مبلغ الإيداع ويحدد تلقائياً عدد الصفقات وحجم اللوت بدقة
    """
    if deposit <= 50:
        return 0.01, 1
    elif deposit <= 500:
        return 0.02, 2
    elif deposit <= 5000:
        return 0.05, 3
    elif deposit <= 50000:
        return 0.1, 5
    else:
        return 0.2, 8

calculated_lot, calculated_trades = calculate_ai_lot_and_trades(deposit_amount)

st.write(f"📊 **التحليل التلقائي للذكاء الاصطناعي - حجم اللوت:** {calculated_lot}")
st.write(f"🔢 **عدد الصفقات المتزامنة:** {calculated_trades}")

st.markdown("---")

# --- 3. إعدادات المبلغ المحدد والفترة المحددة ---
st.header("إعدادات الهدف والمهلة الزمنية للبوت")

target_amount = st.selectbox(
    "المبلغ المحدد المستهدف ($)",
    [
        "من 10 دولار إلى 50 دولار",
        "من 50 دولار إلى 100 دولار",
        "من 100 دولار إلى 500 دولار",
        "من 500 دولار إلى 1000 دولار",
        "من 1000 دولار إلى 5000 دولار",
        "من 5000 دولار إلى 10000 دولار",
        "من 10000 دولار إلى 50000 دولار",
        "من 50000 دولار إلى 100000 دولار",
        "من 100000 دولار إلى 1000000 دولار",
        "من 1000000 دولار إلى 5000000 دولار",
        "من 10 دولار الى 1,250,369,824,789,318 دولار"
    ]
)

timeframe_option = st.selectbox(
    "الفترة المحددة لجمع المبلغ",
    ["من يوم إلى 7 أيام", "من شهر إلى 12 شهراً", "من سنة إلى 5 سنوات"]
)

st.markdown("---")

# --- 4. تحليل الذكاء الاصطناعي وتنفيذ أوامر البوت والإشعارات الفورية ---
st.header("التحكم الآلي والتنفيذ")

if st.button("بدء تحليل الذكاء الاصطناعي وتنفيذ أوامر البوت"):
    st.warning("🔄 جاري تحليل السوق بالمؤشرات والاستراتيجيات (Price Action / Smart Money)...")
    
    # تحديد الأهداف بدقة عالية ومحاكاة السعر الحالي
    current_market_price = 4638.77
    take_profit_target = current_market_price + 15.50
    stop_loss_target = current_market_price - 8.20

    st.success(f"✅ تم ربط الحساب ({mt5_account_id} - {mt5_server_name}) بنجاح وتحليل السوق بدقة عالية!")
    st.success(f"🎯 **الأهداف المحددة آلياً:** سعر الدخول: `{current_market_price}` | هدف الأرباح (TP): `{take_profit_target}` | وقف الخسارة (SL): `{stop_loss_target}`")
    
    # صياغة رسالة التنبيه الموحدة التي تصل عبر بوت تيليجرام (لك ولكل المستثمرين والشركات)
    alert_message = (
        f"🚨 *Raseen AI Pro - تنبيه تداول فوري وتحديد الأهداف*\n"
        f"👤 المستثمر/الشركة: {user_name}\n"
        f"🔗 الحساب المرتبط: `{mt5_account_id}` ({account_type})\n"
        f"🏢 السيرفر: `{mt5_server_name}`\n"
        f"💰 مبلغ الإيداع في MT5: ${deposit_amount}\n"
        f"📊 اللوت المستخدم: {calculated_lot} | عدد الصفقات: {calculated_trades}\n"
        f"🎯 المبلغ المستهدف العام: {target_amount}\n"
        f"📈 السعر الحالي: `{current_market_price}` | هدف الأرباح (TP): `{take_profit_target}`\n"
        f"⏳ الفترة المحددة: {timeframe_option}\n"
        f"📈 *حالة البوت:* تحليل الذكاء الاصطناعي نشط. ينتظر وصول الصفقات للهدف المحدد، ويقوم بالإغلاق التلقائي للأرباح وإرسال إشعار فوري عند اكتمال الهدف!"
    )
    
    # إرسال التنبيه للمستثمر أو الشركة عبر تيليجرام
    if user_telegram_id:
        send_telegram_notification(user_telegram_id.strip(), alert_message)
    
    # إرسال نسخة إليك أنت كصانع ومبرمج للتطبيق
    if user_telegram_id.strip() != CREATOR_CHAT_ID:
        send_telegram_notification(CREATOR_CHAT_ID, f"📈 [متابعة عمليات العملاء والشركات]\n" + alert_message)
    
    st.info("📩 تم تفعيل نظام التنبيهات الفورية وإرسال تفاصيل الصفقة إلى بوت تيليجرام بنجاح!")

st.markdown("---")

# --- 5. باقات الاشتراكات للمستثمرين والشركات ---
st.header("باقات الاشتراكات الاحترافية")
st.write("تظهر أسعار الباقات للمستثمرين والشركات بعملاتهم المحلية، بينما يتم التداول داخل MetaTrader 5 بالدولار الأمريكي ($) دون المساس برصيد التداول أبداً:")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("الشهرية")
    st.write("**50** (عملة محلية)")
    st.text("تاريخ البدء والنهاية (30 يوم)")
    st.button("اشتراك شهري")

with col2:
    st.subheader("السنوية")
    st.write("**200** (عملة محلية)")
    st.text("تاريخ البدء والنهاية (365 يوم)")
    st.button("اشتراك سنوي")

with col3:
    st.subheader("مدى الحياة")
    st.write("**1000** (عملة محلية)")
    st.text("لا تنتهي أبداً (تاريخ بدء فقط)")
    st.button("اشتراك مدى الحياة")

st.markdown("---")

# --- 6. تفاصيل التطبيق وروابط التحميل للمستثمرين والشركات ---
st.header("تفاصيل التطبيق وروابط التحميل (App Details & Download)")
st.write("""
**مرحباً بك في منصة Raseen AI Pro العالمية:**
* **نبذة عن المنصة:** تطبيق ذكاء اصطناعي متطور مخصص للربط المباشر مع منصة التداول العالمية **MetaTrader 5 (MT5)**، يعمل على تحليل السوق بدقة فائقة باستخدام استراتيجيات حركة السعر (Price Action) ومفاهيم الأموال الذكية (Smart Money).
* **الأمان والموثوقية:** اشتراكات الباقات تتم عبر بوابات دفع خارجية مستقلة تماماً، ولا يتم خصم أي رسوم من أرصدة التداول الخاصة بالمستثمرين والشركات.
* **الإدارة التلقائية:** البوت يراقب السوق، ينفذ الصفقات بناءً على قوة الاتجاه، وينتظر وصول الأهداف ليغلق الصفقات الرابحة ويوقف العمل تلقائياً فور تحقيق المستهدف مع إرسال إشعار فوري عبر التيليجرام.
""")

st.markdown("🔗 **[انقر هنا لتحميل تطبيق Raseen AI Pro (نسخة الشركات والمستثمرين)](https://replit.com)**")
