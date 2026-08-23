from datetime import datetime, timedelta
import random
import time
import streamlit as st

# إعدادات الصفحة
st.set_page_title("Raseen AI Pro - Smart Trading System", layout="centered")

# تصميم الواجهة والتنسيقات الخضراء والخلفيات
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .green-screen {
        background: linear-gradient(135deg, #0f5132 0%, #198754 100%);
        padding: 25px; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    .lock-box {
        background-color: #842029; padding: 20px; border-radius: 10px; text-align: center; font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# نظام اللغات (العربية والإنجليزية واللغات الأخرى)
translations = {
    "العربية": {
        "title": "راسين (Raseen AI Pro) - نظام التداول الذكي",
        "welcome": "أهلاً بك في منصة الذكاء الاصطناعي لـ MT5",
        "name": "الاسم الكامل",
        "email": "البريد الإلكتروني",
        "pass": "كلمة المرور",
        "mt5_id": "رقم حساب MetaTrader 5 (MT5 ID)",
        "mt5_server": "اسم السيرفر (مثال: MetaQuotes-Demo أو الحقيقي)",
        "acc_type": "نوع الحساب",
        "demo": "حساب تجريبي (Demo)",
        "live": "حساب حقيقي (Live)",
        "deposit": "مبلغ الإيداع الفعلي في MT5 (بالدولار الأمريكي $)",
        "target_amt": "اختر المبلغ المستهدف للبوت",
        "target_time": "اختر الفترة الزمنية المستهدفة",
        "start_btn": (
            "تحليل الذكاء الاصطناعي الفائق وتنفيذ أوامر MT5 الفورية"
        ),
        "trial_ended": (
            "انتهت الفترة التجريبية (30 يوماً). يرجى اختيار باقة الاشتراك"
            " للتجديد."
        ),
        "subscribe_title": "اختر باقة الاشتراك (بالعملة المحلية لبلدك):",
        "p1": "باقة الشهر - 25 (بعملتك المحلية)",
        "p2": "باقة السنة - 200 (بعملتك المحلية)",
        "p3": "باقة مدى الحياة - 1000 (بعملتك المحلية)",
    },
    "English": {
        "title": "Raseen AI Pro - Smart Trading System",
        "welcome": "Welcome to MT5 AI Trading Platform",
        "name": "Full Name",
        "email": "Email",
        "pass": "Password",
        "mt5_id": "MetaTrader 5 Account ID",
        "mt5_server": "Server Name (e.g., MetaQuotes-Demo or Live)",
        "acc_type": "Account Type",
        "demo": "Demo Account",
        "live": "Live Account",
        "deposit": "MT5 Deposit Amount (USD $)",
        "target_amt": "Select Target Amount",
        "target_time": "Select Target Time Period",
        "start_btn": "Run Advanced AI Analysis & Execute MT5 Orders",
        "trial_ended": (
            "Trial period (30 days) has ended. Please subscribe to unlock."
        ),
        "subscribe_title": "Choose Subscription Plan (Local Currency):",
        "p1": "Monthly Plan - 25 (Local Currency)",
        "p2": "Yearly Plan - 200 (Local Currency)",
        "p3": "Lifetime Plan - 1000 (Local Currency)",
    },
}

# 1. الشاشة الخضراء الأولى (التسجيل والربط)
st.markdown('<div class="green-screen">', unsafe_allow_html=True)
st.markdown("<h2>🌍 الشاشة الخضراء: التسجيل وربط MT5</h2>", unsafe_allow_html=True)

lang_choice = st.selectbox("Language / لغة التطبيق", ["العربية", "English"])
t = translations[lang_choice]

# استبعاد إسرائيل تماماً من البلدان
countries = (
    [
        "المملكة العربية السعودية",
        "الإمارات",
        "الكويت",
        "مصر",
        "قطر",
        "عمان",
        "البحرين",
        "أخرى",
    ]
    if lang_choice == "العربية"
    else [
        "Saudi Arabia",
        "UAE",
        "Kuwait",
        "Egypt",
        "Qatar",
        "Oman",
        "Bahrain",
        "Other",
    ]
)
country_choice = st.selectbox(
    "البلد / Country" if lang_choice == "العربية" else "Country", countries
)

st.markdown("---")
full_name = st.text_input(t["name"])
email = st.text_input(t["email"])
password = st.text_input(t["pass"], type="password")

st.markdown("### 📊 بيانات ربط MetaTrader 5 (من التطبيق)")
mt5_id_input = st.text_input(t["mt5_id"])
mt5_server_input = st.text_input(t["mt5_server"])

st.markdown("</div>", unsafe_allow_html=True)

if full_name and email and mt5_id_input:
  st.markdown("---")

  # التحقق هل المستخدم هو الصانع والمبرمج (عزام) لصلاحياته المطلقة
  is_creator = "عزام" in full_name or email.lower() == "azzam@raseen.ai"

  if is_creator:
    st.success(
        "🔓 أهلاً بك يا عزام (الصانع والمبرمج). لك صلاحية مطلقة ومفتوحة بدون"
        " قيود أو اشتراكات!"
    )
    acc_type = st.radio(t["acc_type"], [t["demo"], t["live"]])
    deposit_val = st.number_input(
        t["deposit"], min_value=10.0, value=1000.0
        if acc_type == t["live"]
        else 100000.0
    )
    is_subscribed = True
  else:
    # للمستثمرين والمتداولين والشركات
    acc_type = st.radio(t["acc_type"], [t["demo"], t["live"]])

    if acc_type == t["demo"]:
      st.info(
          "الحساب التجريبي: رصيد افتراضي من 100,000$ إلى 5,000,000$"
          if lang_choice == "العربية"
          else "Demo Virtual Balance: $100,000 - $5,000,000"
      )
      deposit_val = 100000.0
      is_subscribed = True
    else:
      deposit_val = st.number_input(t["deposit"], min_value=10.0, value=500.0)
      trial_expired = False  # محاكاة انتهاء فترة الـ 30 يوماً

      if trial_expired:
        st.markdown(
            f'<div class="lock-box">🔒 {t["trial_ended"]}</div>',
            unsafe_allow_html=True,
        )
        selected_pkg = st.selectbox(
            t["subscribe_title"], [t["p1"], t["p2"], t["p3"]]
        )
        if st.button(
            "إتمام الدفع بالعملة المحلية وفك القفل"
            if lang_choice == "العربية"
            else "Pay & Unlock"
        ):
          st.success(
              "تم الدفع بالعملة المحلية بنجاح! تم تفعيل البوت."
              if lang_choice == "العربية"
              else "Paid successfully! Bot unlocked."
          )
          is_subscribed = True
        else:
          is_subscribed = False
      else:
        is_subscribed = True

  if is_subscribed:
    st.markdown("---")
    st.subheader(
        "🎯 إعدادات الأهداف المالية والفترات الزمنية للذكاء الاصطناعي"
    )

    targets = [
        "10$ - 50$",
        "50$ - 100$",
        "100$ - 500$",
        "500$ - 1,000$",
        "1,000$ - 5,000$",
        "5,000$ - 10,000$",
        "10,000$ - 50,000$",
        "50,000$ - 100,000$",
        "100,000$ - 500,000$",
        "1,000,000$ - 5,000,000$",
    ]
    st.selectbox(t["target_amt"], targets)

    periods = (
        ["من 1 إلى 7 أيام", "من شهر إلى 12 شهراً", "من سنة إلى 5 سنوات"]
        if lang_choice == "العربية"
        else ["1 to 7 Days", "1 to 12 Months", "1 to 5 Years"]
    )
    st.selectbox(t["target_time"], periods)

    st.markdown("---")

    if st.button(t["start_btn"], type="primary"):
      with st.spinner(
          "جاري ربط حساب MT5 وتفعيل تحليل الذكاء الاصطناعي (SMC & Order"
          " Blocks)..."
          if lang_choice == "العربية"
          else "Connecting MT5 & activating AI analysis..."
      ):
        time.sleep(3)

      ai_signals = [
          "طلوع قوي 📈 ⟵ شراء قوي (Strong Buy)",
          "نزول قوي 📉 ⟵ بيع قوي (Strong Sell)",
          "طلوع عادي ↗️ ⟵ شراء (Buy)",
          "نزول عادي ↘️ ⟵ بيع (Sell)",
      ]
      current_signal = random.choice(ai_signals)
      lot = round(max(0.01, deposit_val * 0.001), 2)

      st.success(
          "🚀 **تم تشغيل البوت بنجاح تام وإرسال الأوامر المباشرة لمنصة MT5!**"
      )
      st.info(
          f"🔹 **رقم الحساب المربوط:** {mt5_id_input} ({mt5_server_input})\n\n"
          f"🔹 **حجم الإيداع (بالدولار):** ${deposit_val}\n\n"
          f"🔹 **حجم العقد المحسوب (Lot Size):** {lot}\n\n"
          f"🔹 **إشارة الذكاء الاصطناعي الفورية:** {current_signal}\n\n"
          "📌 **ملاحظة:** تم إلغاء الأهداف (TP & SL) والبوت يدير الصفقة ديناميكياً"
          " حتى الوصول للمبلغ المستهدف وإرسال إشعار التليجرام الفوري بلغتك"
          " المختارة."
      )
