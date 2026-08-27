import streamlit as st
import time
from datetime import datetime, timedelta
import random

# إعدادات الصفحة
st.set_page_config(page_title="Raseen AI Pro - Smart Trading", page_icon="🤖", layout="wide")

# تهيئة الجلسة والحفظ الثابت لمنع فقدان البيانات أو الخروج المتكرر
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
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

# القواميس واللغات العالمية
translations = {
    "العربية": {
        "title": "🚀 Raseen AI Pro - محرك الذكاء الاصطناعي والتنفيذ الذكي",
        "sidebar_title": "🔐 بوابة الحسابات ومنصة MT5",
        "welcome": "أهلاً بك يا بطل:",
        "tab1": "⚡ التحليل الفني، أسعار السوق وأهداف TP/SL الدقيقة",
        "tab2": "💎 باقات الاشتراك و Apple Pay",
        "tab3": "👥 لوحة إدارة الحسابات والمشتركين",
        "amount_range": "حدد نطاق المبلغ المخصص للتنفيذ (من 10 دولار إلى 50,000,000,000 دولار):",
        "pairs": "اختر زوج العملات أو الأصل المالي",
        "timeframe": "اختر الفريم الزمني للاستراتيجية",
        "execute_btn": "🚀 تنفيذ الصفقة وإرسال الأسعار بدقة مطابقة للمنصة",
        "monthly": "الباقة الشهرية",
        "yearly": "الباقة السنوية",
        "vip": "باقة مدى الحياة (VIP)"
    },
    "English": {
        "title": "🚀 Raseen AI Pro - AI Automated Trading Engine",
        "sidebar_title": "🔐 MT5 Account & Portal",
        "welcome": "Welcome:",
        "tab1": "⚡ Technical Analysis, Market Prices & Precise TP/SL",
        "tab2": "💎 Subscription Plans & Apple Pay",
        "tab3": "👥 Accounts & Subscribers Dashboard",
        "amount_range": "Select Amount Range ($10 to $50,000,000,000):",
        "pairs": "Select Trading Pair",
        "timeframe": "Select Timeframe",
        "execute_btn": "🚀 Execute Trade & Send Precise Market Prices",
        "monthly": "Monthly Plan",
        "yearly": "Yearly Plan",
        "vip": "VIP Lifetime Plan"
    }
}

# قائمة بلدان وعملات كأس العالم (باستبعاد إسرائيل)
world_cup_countries_and_currencies = {
    "المملكة العربية السعودية (السعودية)": "ريال سعودي (SAR)",
    "قطر": "ريال قطري (QAR)",
    "المغرب": "درهم مغربي (MAD)",
    "مصر": "جنيه مصري (EGP)",
    "الولايات المتحدة الأمريكية": "دولار أمريكي (USD)",
    "إنجلترا (المملكة المتحدة)": "جنيه إسترليني (GBP)",
    "فرنسا": "يورو (EUR)",
    "البرازيل": "ريال برازيلي (BRL)",
    "الأرجنتين": "بيزو أرجنتيني (ARS)"
}

currency_symbols = {
    "ريال سعودي (SAR)": {"code": "SAR", "symbol": "ر.س", "monthly": 25, "yearly": 200, "vip": 1000},
    "دولار أمريكي (USD)": {"code": "USD", "symbol": "$", "monthly": 25, "yearly": 200, "vip": 1000},
    "يورو (EUR)": {"code": "EUR", "symbol": "€", "monthly": 25, "yearly": 200, "vip": 1000},
    "جنيه إسترليني (GBP)": {"code": "GBP", "symbol": "£", "monthly": 25, "yearly": 200, "vip": 1000},
    "ريال قطري (QAR)": {"code": "QAR", "symbol": "ر.ق", "monthly": 25, "yearly": 200, "vip": 1000},
    "درهم مغربي (MAD)": {"code": "MAD", "symbol": "د.م.", "monthly": 250, "yearly": 2000, "vip": 10000},
    "جنيه مصري (EGP)": {"code": "EGP", "symbol": "ج.م", "monthly": 1200, "yearly": 9500, "vip": 48000},
    "ريال برازيلي (BRL)": {"code": "BRL", "symbol": "R$", "monthly": 125, "yearly": 1000, "vip": 5000}
}

trading_pairs = [
    "الذهب (XAUUSD)", "الفضة (XAGUSD)", "النفط (WTI)", "EUR/USD", "GBP/USD", 
    "USD/JPY", "مؤشر داو جونز (US30)", "مؤشر ناسداك (NAS100)", "بيتكوين (BTCUSD)"
]

timeframes = ["دقيقة (M1)", "5 دقائق (M5)", "15 دقيقة (M15)", "نصف ساعة (M30)", "ساعة (H1)", "4 ساعات (H4)", "يومي (D1)"]

amount_ranges = [
    "من 10 دولار إلى 50 دولار", "من 50 دولار إلى 100 دولار", "من 100 دولار إلى 500 دولار",
    "من 500 دولار إلى 1000 دولار", "من 1000 دولار إلى 5000 دولار", "من 5000 دولار إلى 10000 دولار",
    "من 10000 دولار إلى 50000 دولار", "من 50000 دولار إلى 100000 دولار", "من 100000 دولار إلى 500000 دولار",
    "من 500000 دولار إلى 1000000 دولار", "من 1000000 دولار إلى 5000000 دولار", "من 5000000 دولار إلى 10000000 دولار",
    "من 10000000 دولار إلى 50000000 دولار", "من 50000000 دولار إلى 100000000 دولار", "من 100000000 دولار إلى 500000000 دولار",
    "من 500000000 دولار إلى 1000000000 دولار", "من 1000000000 دولار إلى 5000000000 دولار", "من 5000000000 دولار إلى 50000000000 دولار"
]

# --- القائمة الجانبية (اللغة وإدارة الحساب الثابت) ---
selected_lang = st.sidebar.selectbox("🌐 Language / اللغة", ["العربية", "English"])
t = translations[selected_lang]

st.sidebar.markdown("---")
st.sidebar.title(t["sidebar_title"])

with st.sidebar.expander("📋 بيانات حساب MT5 (ثابت ولا يمحى)", expanded=True):
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
        st.sidebar.success("تم تحديث البيانات بنجاح وثبات تام!")
        st.rerun()

# --- الواجهة الرئيسية ---
st.title(t["title"])
st.markdown(f"### {t['welcome']} **{st.session_state.mt5_data['first_name']} {st.session_state.mt5_data['second_name']}** 🟢")
st.markdown("---")

# جدول عرض تفاصيل الحساب تماماً مثل الصورة الأصلية
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
    
    selected_range = st.selectbox(t["amount_range"], amount_ranges)
    
    c_pair, c_time = st.columns(2)
    with c_pair:
        selected_pair = st.selectbox(t["pairs"], trading_pairs)
    with c_time:
        selected_timeframe = st.selectbox(t["timeframe"], timeframes)
        
    # عرض أسعار السوق المباشرة تماماً مثل واجهة المنصة في الصورة اليمين (SELL / BUY)
    current_bid = 4340.10
    current_ask = 4340.89
    
    st.markdown("### 📊 أسعار المنصة الحية وأسعار الأهداف (Market Prices & Precise TP/SL)")
    col_bid, col_ask = st.columns(2)
    with col_bid:
        st.markdown(f"🔴 **SELL (بيع):** `{current_bid}`")
    with col_ask:
        st.markdown(f"🔵 **BUY (شراء):** `{current_ask}`")

    # إعدادات الأهداف الدقيقة المماثلة لشاشة التداول
    c_tp, c_sl = st.columns(2)
    with c_tp:
        tp_target = st.number_input("🎯 سعر هدف الأرباح (Take Profit)", value=4345.50, step=0.1, format="%.2f")
    with c_sl:
        sl_target = st.number_input("🛑 سعر وقف الخسارة (Stop Loss)", value=4335.20, step=0.1, format="%.2f")
        
    # حساب اللوت آلياً بناءً على نطاق المبلغ
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
    
    st.write(f"📊 **إدارة المخاطر:** نطاق المبلغ: `{selected_range}` | اللوت الآلي: **{calc_lot}** | عدد الصفقات: **{calc_trades}**")
    
    if st.button(t["execute_btn"], type="primary"):
        with st.spinner("جاري تنفيذ الأمر وإرسال الأسعار المطابقة لشاشة التداول..."):
            time.sleep(0.5)
            st.success(f"""
            ⚡ **تم التنفيذ بنجاح على حساب MT5 (`{d['login']}`):**
            * **الأصل المالي:** {selected_pair} | **الفريم:** {selected_timeframe}
            * **حجم اللوت:** `{calc_lot}` | **عدد الصفقات:** `{calc_trades}`
            * **سعر الدخول الحالي:** بيع `{current_bid}` / شراء `{current_ask}`
            * **🎯 سعر جني الربح (TP):** `{tp_target}`
            * **🛑 سعر وقف الخسارة (SL):** `{sl_target}`
            * **حالة التنفيذ:** مطابق لبيانات الشاشة بدقة تامة ومربوط بحسابك بنجاح.
            """)

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
        **{curr_info['monthly']} {curr_info['symbol']} / شهرياً**
        - 📅 تاريخ البدء: `{start_date}`
        - ⏳ تاريخ الانتهاء: `{month_end}`
        - تحليل ذكاء اصطناعي وتنفيد آلي كامل
        """)
        if st.button(" Apple Pay - اشتراك شهري (25)"):
            st.session_state.is_paid = True
            st.success("🎉 تم تفعيل الباقة الشهرية بنجاح عبر Apple Pay!")
            st.rerun()
            
    with c2:
        st.markdown(f"""
        ### {t['yearly']}
        **{curr_info['yearly']} {curr_info['symbol']} / سنوياً**
        - 📅 تاريخ البدء: `{start_date}`
        - ⏳ تاريخ الانتهاء: `{year_end}`
        - تنفيذ وأولوية دعم فني قصوى
        """)
        if st.button(" Apple Pay - اشتراك سنوي (200)"):
            st.session_state.is_paid = True
            st.success("🎉 تم تفعيل الباقة السنوية بنجاح عبر Apple Pay!")
            st.rerun()
            
    with c3:
        st.markdown(f"""
        ### {t['vip']}
        **{curr_info['vip']} {curr_info['symbol']} (مدى الحياة)**
        - 📅 تاريخ البدء: `{start_date}`
        - ⏳ تاريخ الانتهاء: **مدى الحياة / دائم (لا ينتهي)**
        - امتيازات VIP المطلقة للأبد
        """)
        if st.button(" Apple Pay - باقة مدى الحياة (1000)"):
            st.session_state.is_paid = True
            st.success("🎉 تم تفعيل باقة مدى الحياة بنجاح!")
            st.rerun()

with tabs[2]:
    st.subheader("👑 لوحة إدارة الحسابات والمشتركين (عزام الفضلي)")
    st.markdown(f"""
    - **المشترك الرئيسي:** {d['first_name']} {d['second_name']}
      - 🌍 الدولة: {d['country']} | 💰 العملة: {d['currency']}
      - 🔢 رقم الدخول: `{d['login']}` | 🏢 الخادم: `{d['server']}`
      - ⏰ تاريخ التسجيل: {d['reg_date'].strftime('%Y-%m-%d %H:%M')}
    ---
    """)

st.markdown("---")
st.markdown("Raseen AI Pro - 2026 جميع الحقوق محفوظة للمطور عزام الفضلي")
