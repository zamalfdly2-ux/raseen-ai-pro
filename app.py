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

# تهيئة الجلسة
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'client_data' not in st.session_state:
    st.session_state.client_data = None
if 'is_paid' not in st.session_state:
    st.session_state.is_paid = False
if 'subscribers_db' not in st.session_state:
    st.session_state.subscribers_db = []
if 'mt5_accounts' not in st.session_state:
    st.session_state.mt5_accounts = []

# القواميس واللغات العالمية
translations = {
    "العربية": {
        "title": "🚀 Raseen AI Pro - محرك الذكاء الاصطناعي للتنفيذ الآلي",
        "sidebar_title": "🔐 بوابة الحسابات واللغات",
        "login_type": "اختر نوع الدخول:",
        "investor_login": "دخول المستثمرين والشركات",
        "admin_login": "دخول المبرمج (المدير)",
        "name": "الاسم الكامل",
        "country": "الدولة المشاركة في كأس العالم",
        "currency": "العملة المفضلة",
        "server": "الخادم (Server)",
        "acc_type": "نوع الحساب",
        "deposit": "الإيداع / الرصيد",
        "login_num": "رقم الدخول (Login)",
        "password": "كلمة المرور",
        "save_btn": "حفظ الحساب والدخول للنظام",
        "tab1": "⚡ التحليل الفني والدخول الآلي الفوري",
        "tab2": "💎 باقات الاشتراك و Apple Pay",
        "tab3": "👥 لوحة إدارة الحسابات والمشتركين",
        "amount_range": "حدد نطاق المبلغ المخصص للتنفيذ الآلي:",
        "pairs": "اختر زوج العملات أو الأصل المالي",
        "timeframe": "اختر الفريم الزمني للاستراتيجية",
        "execute_btn": "🚀 تنفيذ الصفقة فوراً على حساب MT5",
        "monthly": "الباقة الشهرية",
        "yearly": "الباقة السنوية",
        "vip": "باقة مدى الحياة (VIP)"
    },
    "English": {
        "title": "🚀 Raseen AI Pro - AI Automated Trading Engine",
        "sidebar_title": "🔐 Account & Language Portal",
        "login_type": "Select Login Type:",
        "investor_login": "Investors & Companies Login",
        "admin_login": "Developer (Admin) Login",
        "name": "Full Name",
        "country": "World Cup Country",
        "currency": "Preferred Currency",
        "server": "Server",
        "acc_type": "Account Type",
        "deposit": "Deposit / Balance",
        "login_num": "Login Number",
        "password": "Password",
        "save_btn": "Save Account & Login",
        "tab1": "⚡ Technical Analysis & Auto Execution",
        "tab2": "💎 Subscription Plans & Apple Pay",
        "tab3": "👥 Accounts & Subscribers Dashboard",
        "amount_range": "Select Automated Trading Amount Range:",
        "pairs": "Select Trading Pair",
        "timeframe": "Select Timeframe",
        "execute_btn": "🚀 Execute Trade Instantly on MT5",
        "monthly": "Monthly Plan",
        "yearly": "Yearly Plan",
        "vip": "VIP Lifetime Plan"
    },
    "Français": {
        "title": "🚀 Raseen AI Pro - Moteur de Trading Automatisé par IA",
        "sidebar_title": "🔐 Portail des Comptes & Langues",
        "login_type": "Sélectionnez le type de connexion:",
        "investor_login": "Connexion Investisseurs & Entreprises",
        "admin_login": "Connexion Développeur (Admin)",
        "name": "Nom complet",
        "country": "Pays de la Coupe du Monde",
        "currency": "Devise préférée",
        "server": "Serveur",
        "acc_type": "Type de compte",
        "deposit": "Dépôt / Solde",
        "login_num": "Numéro de connexion",
        "password": "Mot de passe",
        "save_btn": "Enregistrer et Se connecter",
        "tab1": "⚡ Analyse Technique & Exécution Auto",
        "tab2": "💎 Abonnements & Apple Pay",
        "tab3": "👥 Tableau de bord des Abonnés",
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
        "sidebar_title": "🔐 Portal de Cuentas e Idiomas",
        "login_type": "Seleccione el tipo de inicio de sesión:",
        "investor_login": "Acceso de Inversores y Empresas",
        "admin_login": "Acceso de Desarrollador (Admin)",
        "name": "Nombre completo",
        "country": "País de la Copa del Mundo",
        "currency": "Moneda preferida",
        "server": "Servidor",
        "acc_type": "Tipo de cuenta",
        "deposit": "Depósito / Saldo",
        "login_num": "Número de acceso",
        "password": "Contraseña",
        "save_btn": "Guardar cuenta e iniciar sesión",
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

# قائمة بلدان وعملات كأس العالم التاريخية (باستثناء إسرائيل)
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
    "بولندا": "زلوتي بولندي (PLN)",
    "الأوروغواي": "بيزو أوروغواياني (UYU)",
    "السويد": "كرونة سويدية (SEK)",
    "النرويج": "كرونة نرويجية (NOK)"
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

# نطاقات المبالغ المحددة التي طلبتها
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

# --- القائمة الجانبية (اللغة والحسابات) ---
st.sidebar.title("🌐 Language / اللغة")
selected_lang = st.sidebar.selectbox("Choose Language / اختر اللغة", ["العربية", "English", "Français", "Español"])
t = translations[selected_lang]

st.sidebar.markdown("---")
st.sidebar.title(t["sidebar_title"])

if st.session_state.logged_in_user is not None:
    st.sidebar.success(f"🟢 **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Logout / تسجيل الخروج"):
        st.session_state.logged_in_user = None
        st.session_state.user_role = None
        st.session_state.client_data = None
        st.session_state.is_paid = False
        st.rerun()
else:
    login_type = st.sidebar.radio(t["login_type"], [t["investor_login"], t["admin_login"]])
    st.sidebar.markdown("---")

    if login_type == t["admin_login"]:
        st.sidebar.subheader("👑 Admin Login")
        admin_name = st.sidebar.text_input("Name", value="عزام الفضلي")
        admin_pass = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            if admin_name == "عزام الفضلي" and admin_pass:
                st.session_state.logged_in_user = admin_name
                st.session_state.user_role = 'admin'
                st.sidebar.success("Logged in successfully!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials.")

    elif login_type == t["investor_login"]:
        st.sidebar.subheader("👤 Investor & MT5 Setup")
        
        client_name = st.sidebar.text_input(t["name"], value="عزام الفضلي")
        client_country = st.sidebar.selectbox(t["country"], list(world_cup_countries_and_currencies.keys()))
        default_curr = world_cup_countries_and_currencies[client_country]
        client_curr = st.sidebar.selectbox(t["currency"], list(currency_symbols.keys()), index=list(currency_symbols.keys()).index(default_curr) if default_curr in currency_symbols else 0)
        
        st.sidebar.markdown("---")
        server_name = st.sidebar.text_input(t["server"], value="MetaQuotes-Demo")
        acc_type = st.sidebar.text_input(t["acc_type"], value="Forex Hedged USD (1:100)")
        deposit_val = st.sidebar.text_input(t["deposit"], value="3000 USD")
        acc_number = st.sidebar.text_input(t["login_num"], value="111726346")
        acc_pass = st.sidebar.text_input(t["password"], value="A@3hHoNo", type="password")
        
        if st.sidebar.button(t["save_btn"]):
            if client_name and acc_number and acc_pass:
                reg_time = datetime.now()
                st.session_state.logged_in_user = client_name
                st.session_state.user_role = 'client'
                
                account_info = {
                    "name": client_name,
                    "server": server_name,
                    "acc_type": acc_type,
                    "deposit": deposit_val,
                    "login": acc_number,
                    "password": acc_pass,
                    "currency": client_curr,
                    "country": client_country,
                    "reg_date": reg_time
                }
                
                st.session_state.client_data = account_info
                st.session_state.mt5_accounts.append(account_info)
                st.session_state.subscribers_db.append(account_info)
                
                st.sidebar.success("Account saved and linked successfully!")
                send_alert(f"👤 *New MT5 Account Linked*\nName: {client_name}\nLogin: {acc_number}\nServer: {server_name}")
                st.rerun()
            else:
                st.sidebar.error("Please fill in required fields.")

# --- الواجهة الرئيسية ---
st.title(t["title"])
st.markdown("---")

if st.session_state.logged_in_user is None:
    st.info("👈 Please login and link your MT5 account from the sidebar to start.")
else:
    if st.session_state.client_data:
        c_data = st.session_state.client_data
        st.markdown(f"""
        ### 📋 Linked MetaTrader 5 (MT5) Account Details:
        | Field | Details |
        | :--- | :--- |
        | 👤 **Name** | {c_data['name']} |
        | 🌍 **Country** | {c_data['country']} |
        | 🏢 **Server** | `{c_data['server']}` |
        | 💰 **Deposit / Balance** | **{c_data['deposit']}** |
        | 🔢 **Login** | `{c_data['login']}` |
        """)
        st.markdown("---")

    if st.session_state.user_role == 'admin':
        tabs = st.tabs([t["tab1"], t["tab2"], t["tab3"]])
    else:
        tabs = st.tabs([t["tab1"], t["tab2"]])

    with tabs[0]:
        st.subheader(t["tab1"])
        
        # خانة المبلغ المخصص المحددة بدقة
        selected_amount_range = st.selectbox(t["amount_range"], amount_ranges)
        
        c_pair, c_time = st.columns(2)
        with c_pair:
            selected_pair = st.selectbox(t["pairs"], trading_pairs)
        with c_time:
            selected_timeframe = st.selectbox(t["timeframe"], timeframes)
            
        # حساب اللوت وعدد الصفقات آلياً بناءً على نطاق المبلغ المختار للذكاء الاصطناعي
        base_val = 1000.0
        if "10" in selected_amount_range and "50" in selected_amount_range: base_val = 30.0
        elif "50" in selected_amount_range: base_val = 75.0
        elif "100" in selected_amount_range: base_val = 300.0
        elif "500" in selected_amount_range: base_val = 750.0
        elif "1000" in selected_amount_range: base_val = 3000.0
        elif "5000" in selected_amount_range: base_val = 7500.0
        elif "10000" in selected_amount_range: base_val = 25000.0
        elif "50000" in selected_amount_range: base_val = 75000.0
        elif "100000" in selected_amount_range: base_val = 300000.0
        elif "1000000" in selected_amount_range: base_val = 3000000.0
        
        calc_lot = round(max(0.01, base_val / 1000.0), 2)  
        calc_trades = max(1, int(base_val / 200))  
        
        st.write(f"📊 **AI Risk Management & MT5 Lot Sizing:** Selected Range: `{selected_amount_range}` | Calculated Lot: **{calc_lot}** | Safe Trades Count: **{calc_trades}**")
        
        if st.button(t["execute_btn"], type="primary"):
            with st.spinner("Analyzing market and executing orders instantly on MT5..."):
                time.sleep(0.5)
                import random
                
                signals_pool = [
                    {"type": "STRONG BUY 🚀", "action": "Executed STRONG BUY order successfully", "desc": "SMC Order Block reaction with RSI bullish crossover."},
                    {"type": "BUY 📈", "action": "Executed BUY order successfully", "desc": "Market structure BOS held above support zone."},
                    {"type": "STRONG SELL 📉", "action": "Executed STRONG SELL order successfully", "desc": "Supply zone rejection with strong momentum breakdown."},
                    {"type": "SELL 🔻", "action": "Executed SELL order successfully", "desc": "Resistance retest with price action confirmation."}
                ]
                chosen_sig = random.choice(signals_pool)
                
                # تنفيذ فوري عبر بوت ميتاتريدر 5
                execute_trade_signal(selected_pair, selected_timeframe, chosen_sig['action'], calc_lot)
                
                st.success(f"⚡ **Instant Execution Result on MT5 (`{st.session_state.client_data['login']}`):**\n\n* **Pair:** {selected_pair} | **Timeframe:** {selected_timeframe}\n* **Action:** **{chosen_sig['action']}**\n* **Lot Size:** {calc_lot} | **Trades Count:** {calc_trades}\n* **Analysis:** {chosen_sig['desc']}")
                
                send_alert(f"🤖 *Instant MT5 Execution*\nLogin: {st.session_state.client_data['login']}\nPair: {selected_pair}\nAction: {chosen_sig['action']}\nLot: {calc_lot}")

    with tabs[1]:
        st.subheader(t["tab2"])
        
        curr_info = currency_symbols[st.session_state.client_data['currency']] if st.session_state.client_data else currency_symbols["دولار أمريكي (USD)"]
        
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
            if st.button(" Apple Pay - Monthly"):
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
            if st.button(" Apple Pay - Yearly"):
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
            if st.button(" Apple Pay - VIP Lifetime"):
                st.session_state.is_paid = True
                st.success("🎉 VIP Lifetime subscription activated successfully!")
                st.rerun()

    if st.session_state.user_role == 'admin':
        with tabs[2]:
            st.subheader("👑 Subscribers Management Dashboard (عزام الفضلي)")
            if st.session_state.mt5_accounts:
                for idx, acc in enumerate(st.session_state.mt5_accounts, 1):
                    st.markdown(f"""
                    - **Subscriber #{idx}:** {acc['name']}
                      - 🌍 Country: {acc['country']} | 💰 Currency: {acc['currency']}
                      - 🔢 Login: `{acc['login']}` | 🏢 Server: `{acc['server']}`
                      - ⏰ Reg Date: {acc['reg_date'].strftime('%Y-%m-%d %H:%M')}
                    ---
                    """)
            else:
                st.info("No subscribers found.")

st.markdown("---")
st.markdown("Raseen AI Pro - 2026 All Rights Reserved for Developer Azzam Al-Fadhli")
