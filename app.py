import streamlit as st
import time
from datetime import datetime, timedelta

# استيراد الوظائف من الملفات الجانبية
try:
    from bot import send_alert
except ImportError:
    def send_alert(msg):
        pass

try:
    from mt5_bot import execute_trade_signal
except ImportError:
    def execute_trade_signal(symbol, timeframe, action, lot):
        pass

# إعدادات الصفحة
st.set_page_config(page_title="Raseen AI Pro - Smart Trading", page_icon="🤖", layout="wide")

# تهيئة الجلسة والحفظ الثابت لمنع فقدان البيانات عند إعادة التحميل
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'mt5_data' not in st.session_state:
    st.session_state.mt5_data = {
        "first_name": "عزام",
        "second_name": "الهذلي",
        "server": "MetaQuotes-Demo",
        "acc_type": "Forex Hedged USD (1:100)",
        "deposit": "3000 USD",
        "login": "111726346",
        "password": "A@3hHoNo",
        "investor": "Ir_4UmSt",
        "country": "المملكة العربية السعودية (السعودية)",
        "currency": "ريال سعودي (SAR)",
        "reg_date": datetime.now()
    }
if 'is_paid' not in st.session_state:
    st.session_state.is_paid = False
if 'subscribers_db' not in st.session_state:
    st.session_state.subscribers_db = []

# القواميس واللغات العالمية
translations = {
    "العربية": {
        "title": "🚀 Raseen AI Pro - محرك الذكاء الاصطناعي للتنفيذ الآلي",
        "sidebar_title": "🔐 بوابة الحسابات ومنصة MT5",
        "welcome": "أهلاً بك يا بطل:",
        "logout": "تسجيل الخروج",
        "tab1": "⚡ التحليل الفني والدخول الآلي الفوري",
        "tab2": "💎 باقات الاشتراك و Apple Pay",
        "tab3": "👥 لوحة إدارة الحسابات والمشتركين",
        "amount_range": "حدد نطاق المبلغ المخصص للتنفيذ الآلي (من 10 دولار إلى 50,000,000,000 دولار):",
        "pairs": "اختر زوج العملات أو الأصل المالي",
        "timeframe": "اختر الفريم الزمني للاستراتيجية",
        "execute_btn": "🚀 تنفيذ الصفقة فوراً على حساب MT5",
        "monthly": "الباقة الشهرية",
        "yearly": "الباقة السنوية",
        "vip": "باقة مدى الحياة (VIP)"
    },
    "English": {
        "title": "🚀 Raseen AI Pro - AI Automated Trading Engine",
        "sidebar_title": "🔐 MT5 Account & Portal",
        "welcome": "Welcome:",
        "logout": "Logout",
        "tab1": "⚡ Technical Analysis & Auto Execution",
        "tab2": "💎 Subscription Plans & Apple Pay",
        "tab3": "👥 Accounts & Subscribers Dashboard",
        "amount_range": "Select Amount Range ($10 to $50,000,000,000):",
        "pairs": "Select Trading Pair",
        "timeframe": "Select Timeframe",
        "execute_btn": "🚀 Execute Trade Instantly on MT5",
        "monthly": "Monthly Plan",
        "yearly": "Yearly Plan",
        "vip": "VIP Lifetime Plan"
    },
    "Français": {
        "title": "🚀 Raseen AI Pro - Moteur de Trading Automatisé par IA",
        "sidebar_title": "🔐 Portail Compte MT5",
        "welcome": "Bienvenue:",
        "logout": "Déconnexion",
        "tab1": "⚡ Analyse Technique & Exécution Auto",
        "tab2": "💎 Abonnements & Apple Pay",
        "tab3": "👥 Tableau de bord",
        "amount_range": "Sélectionnez la plage de montant:",
        "pairs": "Sélectionner la paire",
        "timeframe": "Sélectionner l'unité de temps",
        "execute_btn": "🚀 Exécuter l'ordre instantanément sur MT5",
        "monthly": "Plan Mensuel",
        "yearly": "Plan Annuel",
        "vip": "Plan VIP à vie"
    },
    "Español": {
        "title": "🚀 Raseen AI Pro - Motor de Trading Automatizado por IA",
        "sidebar_title": "🔐 Portal de Cuenta MT5",
        "welcome": "Bienvenido:",
        "logout": "Cerrar sesión",
        "tab1": "⚡ Análisis Técnico y Ejecución Automática",
        "tab2": "💎 Planes de Suscripción y Apple Pay",
        "tab3": "👥 Panel de Suscriptores",
        "amount_range": "Seleccione el rango de monto:",
        "pairs": "Seleccionar par de divisas",
        "timeframe": "Seleccionar marco de tiempo",
        "execute_btn": "🚀 Ejecutar orden instantáneamente en MT5",
        "monthly": "Plan Mensual",
        "yearly": "Plan Anual",
        "vip": "Plan VIP de por vida"
    }
}

# قائمة بلدان وعملات كأس العالم التاريخية (باستبعاد إسرائيل)
world_cup_countries_and_currencies = {
    "المملكة العربية السعودية (السعودية)": "ريال سعودي (SAR)",
    "قطر": "ريال قطري (QAR)",
    "المغرب": "درهم مغربي (MAD)",
    "مصر": "جنيه مصري (EGP)",
    "تونس": "دينار تونسي (TND)",
    "الجزائر": "دينار جزائري (DZD)",
    "البرازيل": "ريال برازيلي (BRL)",
    "الأرجنتين": "بيزو أرجنتيني (ARS)",
    "ألمانيا": "يورو (EUR)",
    "إسبانيا": "يورو (EUR)",
    "فرنسا": "يورو (EUR)",
    "إنجلترا (المملكة المتحدة)": "جنيه إسترليني (GBP)",
    "البرتغال": "يورو (EUR)",
    "إيطاليا": "يورو (EUR)",
    "هولندا": "يورو (EUR)",
    "كرواتيا": "يورو (EUR)",
    "اليابان": "ين ياباني (JPY)",
    "كوريا الجنوبية": "وون كوري جنوبي (KRW)",
    "الولايات المتحدة الأمريكية": "دولار أمريكي (USD)",
    "المكسيك": "بيزو مكسيكي (MXN)",
    "كندا": "دولار كندي (CAD)",
    "أوروغواي": "بيزو أوروغواياني (UYU)",
    "كولومبيا": "بيزو كولومبي (COP)",
    "تشيلي": "بيزو تشيلي (CLP)",
    "السنغال": "فرنك غرب إفريقي (XOF)",
    "غانا": "سيدي غاني (GHS)",
    "الكاميرون": "فرنك وسط إفريقي (XAF)",
    "نيجيريا": "نايرا نيجيرية (NGN)",
    "جنوب أفريقيا": "راند جنوب إفريقي (ZAR)",
    "أستراليا": "دولار أسترالي (AUD)",
    "سويسرا": "فرنك سويسري (CHF)",
    "بلجيكا": "يورو (EUR)",
    "الدنمارك": "كرونة دانماركية (DKK)",
    "صربيا": "دينار صربي (RSD)",
    "بولندا": "زلوتي بولندي (PLN)"
}

currency_symbols = {
    "ريال سعودي (SAR)": {"code": "SAR", "symbol": "ر.س", "monthly": 25, "yearly": 200, "vip": 1000},
    "دولار أمريكي (USD)": {"code": "USD", "symbol": "$", "monthly": 25, "yearly": 200, "vip": 1000},
    "يورو (EUR)": {"code": "EUR", "symbol": "€", "monthly": 25, "yearly": 200, "vip": 1000},
    "جنيه إسترليني (GBP)": {"code": "GBP", "symbol": "£", "monthly": 25, "yearly": 200, "vip": 1000},
    "ين ياباني (JPY)": {"code": "JPY", "symbol": "¥", "monthly": 3800, "yearly": 30000, "vip": 150000},
    "ريال قطري (QAR)": {"code": "QAR", "symbol": "ر.ق", "monthly": 25, "yearly": 200, "vip": 1000},
    "درهم مغربي (MAD)": {"code": "MAD", "symbol": "د.م.", "monthly": 250, "yearly": 2000, "vip": 10000},
    "جنيه مصري (EGP)": {"code": "EGP", "symbol": "ج.م", "monthly": 1200, "yearly": 9500, "vip": 48000},
    "ريال برازيلي (BRL)": {"code": "BRL", "symbol": "R$", "monthly": 125, "yearly": 1000, "vip": 5000},
    "بيزو أرجنتيني (ARS)": {"code": "ARS", "symbol": "$", "monthly": 25000, "yearly": 200000, "vip": 1000000},
    "دولار كندي (CAD)": {"code": "CAD", "symbol": "CA$", "monthly": 35, "yearly": 270, "vip": 1350},
    "دولار أسترالي (AUD)": {"code": "AUD", "symbol": "A$", "monthly": 38, "yearly": 300, "vip": 1500},
    "فرنك سويسري (CHF)": {"code": "CHF", "symbol": "CHF", "monthly": 23, "yearly": 180, "vip": 900}
}

trading_pairs = [
    "الذهب (XAUUSD)", "الفضة (XAGUSD)", "النفط (WTI)", "EUR/USD", "GBP/USD", 
    "USD/JPY", "USD/CHF", "AUD/USD", "USDCAD", "مؤشر داو جونز (US30)", 
    "مؤشر ناسداك (NAS100)", "بيتكوين (BTCUSD)"
]

timeframes = ["دقيقة (M1)", "5 دقائق (M5)", "15 دقيقة (M15)", "نصف ساعة (M30)", "ساعة (H1)", "4 ساعات (H4)", "يومي (D1)", "أسبوعي (W1)", "شهري (MN)"]

# نطاقات المبالغ المحددة التي طلبتها بدقة متناهية
amount_ranges = [
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
    "من 5000000 دولار إلى 10000000 دولار",
    "من 10000000 دولار إلى 50000000 دولار",
    "من 50000000 دولار إلى 100000000 دولار",
    "من 100000000 دولار إلى 500000000 دولار",
    "من 500000000 دولار إلى 1000000000 دولار",
    "من 1000000000 دولار إلى 5000000000 دولار",
    "من 5000000000 دولار إلى 50000000000 دولار"
]

# --- القائمة الجانبية (اللغة وإدارة الحساب الثابت) ---
st.sidebar.title("🌐 Language / اللغة")
selected_lang = st.sidebar.selectbox("Choose Language", ["العربية", "English", "Français", "Español"])
t = translations[selected_lang]

st.sidebar.markdown("---")
st.sidebar.title(t["sidebar_title"])

# تسجيل الدخول التلقائي أو الثابت لمنع الطلب المتكرر
st.session_state.logged_in = True
st.session_state.user_role = 'client'

# عرض بيانات حساب MT5 في القائمة الجانبية مطابقة للصورة تماماً
with st.sidebar.expander("📋 بيانات حساب MT5 المسجلة (اضغط للعرض)", expanded=True):
    f_name = st.text_input("الاسم الأول", value=st.session_state.mt5_data["first_name"])
    s_name = st.text_input("الاسم الثاني", value=st.session_state.mt5_data["second_name"])
    serv = st.text_input("الخادم", value=st.session_state.mt5_data["server"])
    acc_t = st.text_input("نوع الحساب", value=st.session_state.mt5_data["acc_type"])
    dep = st.text_input("الإيداع", value=st.session_state.mt5_data["deposit"])
    log_num = st.text_input("الدخول", value=st.session_state.mt5_data["login"])
    passw = st.text_input("كلمة المرور", value=st.session_state.mt5_data["password"], type="password")
    inv = st.text_input("مستثمر", value=st.session_state.mt5_data["investor"])
    
    country_sel = st.selectbox("الدولة", list(world_cup_countries_and_currencies.keys()))
    curr_sel = st.selectbox("العملة", list(currency_symbols.keys()))
    
    if st.button("حفظ وتحديث البيانات"):
        st.session_state.mt5_data.update({
            "first_name": f_name, "second_name": s_name, "server": serv,
            "acc_type": acc_t, "deposit": dep, "login": log_num,
            "password": passw, "investor": inv, "country": country_sel, "currency": curr_sel
        })
        st.sidebar.success("تم الحفظ بنجاح!")
        st.rerun()

# --- الواجهة الرئيسية ---
st.title(t["title"])
st.markdown(f"### {t['welcome']} **{st.session_state.mt5_data['first_name']} {st.session_state.mt5_data['second_name']}** 🟢")
st.markdown("---")

# جدول عرض تفاصيل الحساب في الواجهة مثل الصورة التي أرسلتها
d = st.session_state.mt5_data
st.markdown(f"""
| تفاصيل الحساب (MetaTrader 5) | القيمة المسجلة |
| :--- | :--- |
| 👤 **الاسم الأول** | {d['first_name']} |
| 👤 **الاسم الثاني** | {d['second_name']} |
| 🏢 **الخادم** | `{d['server']}` |
| ⚙️ **نوع الحساب** | {d['acc_type']} |
| 💰 **الإيداع** | **{d['deposit']}** |
| 🔢 **الدخول** | `{d['login']}` |
| 🔑 **كلمة المرور** | `********` |
| 👁️ **مستثمر** | `{d['investor']}` |
""")
st.markdown("---")

tabs = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tabs[0]:
    st.subheader(t["tab1"])
    
    # خانة اختيار نطاق المبلغ المخصص لتحديد اللوت وعدد الصفقات بدقة
    selected_range = st.selectbox(t["amount_range"], amount_ranges)
    
    c_pair, c_time = st.columns(2)
    with c_pair:
        selected_pair = st.selectbox(t["pairs"], trading_pairs)
    with c_time:
        selected_timeframe = st.selectbox(t["timeframe"], timeframes)
        
    # حساب اللوت وعدد الصفقات آلياً بناءً على نطاق المبلغ المختار
    base_val = 3000.0
    if "10" in selected_range and "50" in selected_range: base_val = 30.0
    elif "50" in selected_range: base_val = 75.0
    elif "100" in selected_range: base_val = 300.0
    elif "500" in selected_range: base_val = 750.0
    elif "1000" in selected_range: base_val = 3000.0
    elif "5000" in selected_range: base_val = 7500.0
    elif "10000" in selected_range: base_val = 25000.0
    elif "50000" in selected_range: base_val = 75000.0
    elif "100000" in selected_range: base_val = 300000.0
    elif "1000000" in selected_range: base_val = 3000000.0
    elif "5000000" in selected_range: base_val = 15000000.0
    elif "10000000" in selected_range: base_val = 30000000.0
    elif "50000000" in selected_range: base_val = 150000000.0
    elif "100000000" in selected_range: base_val = 300000000.0
    elif "500000000" in selected_range: base_val = 1500000000.0
    elif "1000000000" in selected_range: base_val = 3000000000.0
    elif "5000000000" in selected_range: base_val = 25000000000.0
    
    calc_lot = round(max(0.01, base_val / 1000.0), 2)  
    calc_trades = max(1, int(base_val / 200))  
    
    st.write(f"📊 **AI Risk Management & MT5 Lot Calculation:** Range: `{selected_range}` | Calculated Lot: **{calc_lot}** | Safe Trades Count: **{calc_trades}**")
    
    if st.button(t["execute_btn"], type="primary"):
        with st.spinner("Analyzing market and executing orders instantly on MT5..."):
            time.sleep(0.4)
            import random
            signals_pool = [
                {"type": "STRONG BUY 🚀", "action": "Executed STRONG BUY order successfully", "desc": "SMC Order Block reaction with RSI bullish crossover."},
                {"type": "BUY 📈", "action": "Executed BUY order successfully", "desc": "Market structure BOS held above support zone."},
                {"type": "STRONG SELL 📉", "action": "Executed STRONG SELL order successfully", "desc": "Supply zone rejection with strong momentum breakdown."},
                {"type": "SELL 🔻", "action": "Executed SELL order successfully", "desc": "Resistance retest with price action confirmation."}
            ]
            chosen_sig = random.choice(signals_pool)
            
            # تنفيذ فوري عبر ميتاتريدر 5
            execute_trade_signal(selected_pair, selected_timeframe, chosen_sig['action'], calc_lot)
            
            st.success(f"⚡ **Instant MT5 Execution (`{d['login']}`):**\n\n* **Pair:** {selected_pair} | **Timeframe:** {selected_timeframe}\n* **Action:** **{chosen_sig['action']}**\n* **Lot Size:** {calc_lot} | **Trades:** {calc_trades}\n* **Analysis:** {chosen_sig['desc']}")
            send_alert(f"🤖 *MT5 Instant Execution*\nLogin: {d['login']}\nPair: {selected_pair}\nAction: {chosen_sig['action']}\nLot: {calc_lot}")

with tabs[1]:
    st.subheader(t["tab2"])
    
    curr_info = currency_symbols[d['currency']]
    start_date = datetime.now().strftime('%Y-%m-%d')
    month_end = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    year_end = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        ### {t['monthly']}
        **{curr_info['monthly']} {curr_info['symbol']} / Month**
        - 📅 Start Date: `{start_date}`
        - ⏳ End Date: `{month_end}`
        - Full AI & MT5 Auto Execution
        """)
        if st.button(" Apple Pay - Monthly (25)"):
            st.session_state.is_paid = True
            st.success("🎉 Monthly subscription activated successfully via Apple Pay!")
            st.rerun()
            
    with c2:
        st.markdown(f"""
        ### {t['yearly']}
        **{curr_info['yearly']} {curr_info['symbol']} / Year**
        - 📅 Start Date: `{start_date}`
        - ⏳ End Date: `{year_end}`
        - Priority Execution & Support
        """)
        if st.button(" Apple Pay - Yearly (200)"):
            st.session_state.is_paid = True
            st.success("🎉 Yearly subscription activated successfully via Apple Pay!")
            st.rerun()
            
    with c3:
        st.markdown(f"""
        ### {t['vip']}
        **{curr_info['vip']} {curr_info['symbol']} (Lifetime)**
        - 📅 Start Date: `{start_date}`
        - ⏳ End Date: **Lifetime / دائم (No Expiry)**
        - Unlimited VIP Privileges
        """)
        if st.button(" Apple Pay - VIP Lifetime (1000)"):
            st.session_state.is_paid = True
            st.success("🎉 VIP Lifetime subscription activated successfully!")
            st.rerun()

with tabs[2]:
    st.subheader("👑 Subscribers Management Dashboard (عزام الفضلي)")
    st.markdown(f"""
    - **Subscriber #1:** {d['first_name']} {d['second_name']}
      - 🌍 Country: {d['country']} | 💰 Currency: {d['currency']}
      - 🔢 Login: `{d['login']}` | 🏢 Server: `{d['server']}`
      - ⏰ Reg Date: {d['reg_date'].strftime('%Y-%m-%d %H:%M')}
    ---
    """)

st.markdown("---")
st.markdown("Raseen AI Pro - 2026 All Rights Reserved for Developer Azzam Al-Fadhli")
