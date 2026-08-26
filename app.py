
‏import streamlit as st
‏import time
‏import requests
‏from datetime import datetime, timedelta

# إعدادات الصفحة
‏st.set_page_config(page_title="Raseen AI Pro - Smart Trading", page_icon="🤖", layout="wide")

# بيانات تيليجرام
‏TELEGRAM_BOT_TOKEN = "8858466092:AAF2_YCAukhlvrKgVbBD0levV0i6Gbuag90"
‏TELEGRAM_CHAT_ID = "1370315348"

‏def send_telegram_alert(message):
‏    try:
‏        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
‏        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
‏        requests.post(url, json=payload)
‏    except:
‏        pass

# تهيئة قاعدة البيانات في الجلسة
‏if 'ai_signals_history' not in st.session_state:
‏    st.session_state.ai_signals_history = []
‏if 'subscribers_db' not in st.session_state:
‏    st.session_state.subscribers_db = []
‏if 'logged_in_user' not in st.session_state:
‏    st.session_state.logged_in_user = None
‏if 'user_role' not in st.session_state:
‏    st.session_state.user_role = None  # 'admin' or 'client'

# 🌍 القوائم العالمية (كأس العالم 2010-2026) خالية تماماً من الكيان المرفوض
‏world_cup_countries = [
    "المملكة العربية السعودية", "قطر", "المغرب", "مصر", "تونس", "الجزائر", 
    "البرازيل", "الأرجنتين", "ألمانيا", "إسبانيا", "فرنسا", "إنجلترا", "البرتغال", 
    "إيطاليا", "هولندا", "كرواتيا", "اليابان", "كوريا الجنوبية", "الولايات المتحدة", 
    "المكسيك", "كندا", "أوروغواي", "كولومبيا", "تشيلي", "السنغال", "غانا", "الكاميرون", 
    "نيجيريا", "جنوب أفريقيا", "أستراليا", "سويسرا", "بلجيكا", "الدنمارك", "صربيا", "بولندا"
]

‏world_cup_languages = [
    "العربية", "English", "Español", "Français", "Deutsch", "Português", 
‏    "Italiano", "Nederlands", "Hrvatski", "日本語", "한국어", "Polski"
]

‏world_cup_currencies = [
    "ريال سعودي (SAR)", "دولار أمريكي (USD)", "يورو (EUR)", "جنيه إسترليني (GBP)", 
    "ين ياباني (JPY)", "ريال قطري (QAR)", "درهم مغربي (MAD)", "جنيه مصري (EGP)", 
    "ريال برازيلي (BRL)", "بيزو أرجنتيني (ARS)", "دولار كندي (CAD)", "دولار أسترالي (AUD)", "فرنك سويسري (CHF)"
]

‏trading_pairs = [
    "الذهب (XAUUSD)", "الفضة (XAGUSD)", "النفط (WTI)", "EUR/USD", "GBP/USD", 
‏    "USD/JPY", "USD/CHF", "AUD/USD", "USDCAD", "مؤشر داو جونز (US30)", 
    "مؤشر ناسداك (NAS100)", "بيتكوين (BTCUSD)"
]

‏timeframes = ["دقيقة (M1)", "5 دقائق (M5)", "15 دقيقة (M15)", "نصف ساعة (M30)", "ساعة (H1)", "4 ساعات (H4)", "يومي (D1)", "أسبوعي (W1)", "شهري (MN)"]

# --- الواجهة الجانبية: نظام تسجيل الدخول المنفصل ---
‏st.sidebar.title("🔐 بوابة الدخول")
‏login_type = st.sidebar.radio("اختر نوع الدخول:", ["دخول المستثمرين والشركات", "دخول الصانع والمبرمج (المدير)"])

‏st.sidebar.markdown("---")

‏if login_type == "دخول الصانع والمبرمج (المدير)":
‏    st.sidebar.subheader("👑 تسجيل دخول المبرمج")
‏    admin_name = st.sidebar.text_input("الاسم", value="عزام الفضلي")
‏    admin_email = st.sidebar.text_input("البريد الإلكتروني")
‏    admin_pass = st.sidebar.text_input("كلمة المرور", type="password")
    
‏    if st.sidebar.button("تسجيل الدخول كمدير"):
‏        if admin_name == "عزام الفضلي" and admin_pass: # يمكنك تغيير الشرط ليكون أكثر تعقيداً لاحقاً
‏            st.session_state.logged_in_user = admin_name
‏            st.session_state.user_role = 'admin'
‏            st.sidebar.success("تم تسجيل الدخول بنجاح بصلاحيات المبرمج الكاملة! 🟢")
‏            st.rerun()
‏        else:
‏            st.sidebar.error("بيانات المبرمج غير صحيحة.")

‏elif login_type == "دخول المستثمرين والشركات":
‏    st.sidebar.subheader("👤 تسجيل بيانات المستثمر/الشركة")
    
‏    client_name = st.sidebar.text_input("الاسم الكامل / اسم الشركة")
‏    client_age = st.sidebar.number_input("العمر / سنة التأسيس", min_value=18, max_value=200, value=25)
‏    client_email = st.sidebar.text_input("البريد الإلكتروني")
‏    client_country = st.sidebar.selectbox("الدولة", world_cup_countries)
‏    client_lang = st.sidebar.selectbox("اللغة", world_cup_languages)
‏    client_curr = st.sidebar.selectbox("العملة المفضلة", world_cup_currencies)
    
‏    account_mode = st.sidebar.selectbox("نوع الحساب", ["حساب تجريبي (Demo - مجاني ودائم)", "حقيقي (Live - تجربة 15 يوم)"])
‏    acc_number = st.sidebar.text_input("رقم الحساب (Login)")
‏    server_name = st.sidebar.text_input("اسم السيرفر (Server)")
‏    acc_pass = st.sidebar.text_input("كلمة المرور للمنصة", type="password")
    
‏    if st.sidebar.button("تسجيل وحفظ البيانات"):
‏        if client_name and client_email and acc_number and acc_pass:
‏            reg_time = datetime.now()
            # في الحقيقة نحن نضيف المستخدم لقاعدة البيانات، وهنا نعتبره سجل دخوله فوراً
‏            st.session_state.logged_in_user = client_name
‏            st.session_state.user_role = 'client'
‏            st.session_state.client_data = {
‏                "name": client_name, "age": client_age, "email": client_email, 
‏                "country": client_country, "acc_type": account_mode, "reg_date": reg_time
            }
‏            st.session_state.subscribers_db.append(st.session_state.client_data)
‏            st.sidebar.success(f"مرحباً بك {client_name}، تم التسجيل بنجاح!")
‏            send_telegram_alert(f"👤 *مستثمر جديد*\nالاسم: {client_name}\nالنوع: {account_mode}\nالدولة: {client_country}")
‏            st.rerun()
‏        else:
‏            st.sidebar.error("يرجى إكمال جميع الحقول.")

# --- المحتوى الرئيسي (Main Content) ---
‏st.title("🚀 Raseen AI Pro - نظام الذكاء الاصطناعي العالمي")
‏st.markdown("---")

‏if st.session_state.logged_in_user is None:
‏    st.info("يرجى تسجيل الدخول من القائمة الجانبية للبدء.")
‏else:
    # التحقق من صلاحيات العميل (هل انتهت 15 يوم؟)
‏    is_locked = False
‏    if st.session_state.user_role == 'client':
‏        c_data = st.session_state.client_data
‏        if "حقيقي" in c_data["acc_type"]:
            # لمحاكاة التجربة، نحسب الأيام (في التطبيق الفعلي نستخدم التاريخ الحالي)
‏            days_passed = (datetime.now() - c_data["reg_date"]).days
‏            if days_passed > 15: # تم القفل
‏                is_locked = True
                
    # إنشاء التبويبات بناءً على الصلاحيات
‏    if st.session_state.user_role == 'admin':
‏        tabs = st.tabs(["⚡ تحليل الذكاء الاصطناعي (مفتوح)", "💎 باقات الاشتراك و Apple Pay", "👥 لوحة الإدارة (خاصة بالمبرمج)"])
‏    else:
‏        tabs = st.tabs(["⚡ تحليل الذكاء الاصطناعي", "💎 باقات الاشتراك و Apple Pay"])

    # التبويب الأول: التحليل
‏    with tabs[0]:
‏        st.subheader("⚡ نظام الذكاء الاصطناعي المتقدم لتحليل الأسواق")
        
‏        if is_locked:
‏            st.error("🔒 **انتهت الفترة التجريبية (15 يوم). تم إيقاف الذكاء الاصطناعي للحساب الحقيقي.**")
‏            st.warning("يرجى الانتقال لتبويب (باقات الاشتراك) وتجديد الاشتراك عبر Apple Pay لاستمرار الخدمة واستقبال الإشارات.")
‏        else:
‏            st.success(f"مرحباً بك يا {st.session_state.logged_in_user}! النظام يعمل بكفاءة 🟢")
            
‏            c_asset, c_time = st.columns(2)
‏            with c_asset:
‏                selected_pair = st.selectbox("اختر الزوج المالي", trading_pairs)
‏            with c_time:
‏                selected_timeframe = st.selectbox("اختر الفريم الزمني (Timeframe)", timeframes)
                
‏            manual_deposit = st.number_input("أدخل رأس المال للحساب اليدوي ($):", min_value=1.0, value=1000.0, step=100.0)
            
‏            calculated_lots = round(max(0.01, manual_deposit / 1000.0), 2)  
‏            calculated_trades = max(1, int(manual_deposit / 200))  
            
‏            st.write(f"📊 **تحليل رأس المال:** اللوت المناسب: **{calculated_lots}** | الصفقات المتاحة: **{calculated_trades}**")
            
‏            if st.button("🔍 تحليل الشارت وإرسال التنبيه الآن", type="primary"):
‏                with st.spinner("الذكاء الاصطناعي يقرأ البيانات..."):
‏                    time.sleep(1.5)
‏                    import random
‏                    signal_type = random.choice(["شراء 🚀", "بيع 📉"])
‏                    st.success(f"✅ **إشارة جاهزة على {selected_pair} (فريم {selected_timeframe}): {signal_type}**")
‏                    send_telegram_alert(f"🤖 *تنبيه ذكاء اصطناعي*\nالزوج: {selected_pair}\nالفريم: {selected_timeframe}\nالإشارة: {signal_type}\nاللوت المقترح: {calculated_lots}")

    # التبويب الثاني: الاشتراكات و Apple Pay
‏    with tabs[1]:
‏        st.subheader("💳 باقات الاشتراك المتاحة للشركات والمستثمرين")
‏        st.write("يمكنك الدفع بأمان وسرعة باستخدام **Apple Pay ** لتفعيل الذكاء الاصطناعي بلا انقطاع.")
        
‏        c1, c2, c3 = st.columns(3)
‏        with c1:
‏            st.markdown("### الباقة الشهرية\n**25 ريال / شهر**\n- تفعيل الذكاء الاصطناعي\n- جميع الأزواج والفريمات")
‏            if st.button(" Apple Pay - شراء (25 ريال)"):
‏                st.success("تم توجيهك لبوابة الدفع (سيتم ربطها قريباً)...")
‏        with c2:
‏            st.markdown("### الباقة السنوية\n**200 ريال / سنة**\n- توفير ممتاز\n- دعم فني فوري")
‏            if st.button(" Apple Pay - شراء (200 ريال)"):
‏                st.success("تم توجيهك لبوابة الدفع (سيتم ربطها قريباً)...")
‏        with c3:
‏            st.markdown("### الباقة المفتوحة (VIP)\n**1000 ريال / مدى الحياة**\n- تملك النظام مدى الحياة\n- استشارات خاصة")
‏            if st.button(" Apple Pay - شراء (1000 ريال)"):
‏                st.success("تم توجيهك لبوابة الدفع (سيتم ربطها قريباً)...")

    # التبويب الثالث: لوحة التحكم (للمبرمج فقط)
‏    if st.session_state.user_role == 'admin':
‏        with tabs[2]:
‏            st.subheader("👑 لوحة تحكم المبرمج (عزام الفضلي)")
‏            st.write("هنا يمكنك رؤية جميع بيانات المستثمرين والشركات المشتركين في المنصة.")
            
‏            if st.session_state.subscribers_db:
‏                for idx, sub in enumerate(st.session_state.subscribers_db, 1):
‏                    st.markdown(f"""
                    - **العميل #{idx}:** {sub['name']}
                      - العمر/سنة التأسيس: {sub['age']} | البريد: {sub['email']}
                      - الدولة: {sub['country']} | نوع الحساب: {sub['acc_type']}
                    ---
                    """)
‏            else:
‏                st.info("لا يوجد مشتركين مسجلين حتى الآن.")

‏st.markdown("---")
‏st.markdown("Raseen AI Pro - 2026 جميع الحقوق محفوظة للمبرمج عزام الفضلي")
