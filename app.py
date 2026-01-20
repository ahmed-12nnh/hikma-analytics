import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = None

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 🎨 CSS المحسن - (نفس تصميمك الأصلي 100%)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    /* إعدادات عامة */
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* إخفاء عناصر Streamlit */
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* ===== الهيدر الرئيسي ===== */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 20px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 
            0 0 40px rgba(0, 31, 63, 0.8),
            inset 0 0 30px rgba(0, 0, 0, 0.5),
            0 0 15px rgba(255, 215, 0, 0.1);
        position: relative;
        overflow: hidden;
        animation: fadeIn 1s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* الخط الذهبي العلوي المتوهج */
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        box-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }

    /* العنوان الرئيسي */
    .main-title {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        text-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.3)); }
        to { filter: drop-shadow(0 0 25px rgba(255, 215, 0, 0.6)); }
    }

    /* العنوان الفرعي */
    .sub-title {
        color: #e0e0e0;
        font-size: 18px;
        letter-spacing: 2px;
        font-weight: 500;
        opacity: 0.9;
    }

    /* ===== عنوان القسم ===== */
    .section-header {
        text-align: center;
        margin: 30px 20px;
        color: #FFD700;
        font-size: 1.4rem;
        font-weight: bold;
        text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
    }

    /* ===== أزرار الاختيار ===== */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row-reverse !important;
        justify-content: center !important;
        gap: 15px !important;
        flex-wrap: wrap !important;
        background: rgba(0, 0, 0, 0.3) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 0 20px 30px 20px !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95)) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        padding: 15px 25px !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-align: center !important;
        flex: 1 !important;
        min-width: 160px !important;
        max-width: 220px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    div[role="radiogroup"] label::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.15), transparent) !important;
        transition: left 0.5s ease !important;
    }
    
    div[role="radiogroup"] label:hover::before {
        left: 100% !important;
    }

    div[role="radiogroup"] label:hover {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 31, 63, 0.95)) !important;
        border-color: #FFD700 !important;
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            0 0 20px rgba(255, 215, 0, 0.2) !important;
    }
    
    div[role="radiogroup"] label[data-checked="true"],
    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(184, 134, 11, 0.15)) !important;
        border-color: #FFD700 !important;
        box-shadow: 
            0 0 25px rgba(255, 215, 0, 0.3),
            inset 0 0 20px rgba(255, 215, 0, 0.1) !important;
    }

    /* ===== بطاقات الإدخال ===== */
    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 10px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
    }
    
    .input-card:hover {
        border-color: rgba(255, 215, 0, 0.4);
        transform: translateY(-5px);
        box-shadow: 
            0 15px 50px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(255, 215, 0, 0.1);
    }

    .input-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .input-icon {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #FFD700, #B8860B);
        border-radius: 12px;
        font-size: 1.5rem;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
    }

    .input-title {
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: 700;
    }

    .input-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* ===== حقل النص ===== */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1rem !important;
        padding: 20px !important;
        text-align: right !important;
        direction: rtl !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }

    /* ===== رفع الملفات ===== */
    [data-testid="stFileUploader"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px dashed rgba(255, 215, 0, 0.3) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #FFD700 !important;
        background: rgba(255, 215, 0, 0.05) !important;
    }
    
    [data-testid="stFileUploader"] section {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #FFD700, #B8860B) !important;
        color: #001f3f !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4) !important;
    }

    /* ===== زر المعالجة الرئيسي ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 50%, #FFD700 100%) !important;
        background-size: 200% auto !important;
        color: #001f3f !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        border-radius: 15px !important;
        width: 100% !important;
        padding: 18px 40px !important;
        border: none !important;
        box-shadow: 
            0 8px 30px rgba(218, 165, 32, 0.4),
            0 0 0 0 rgba(255, 215, 0, 0.5) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        animation: buttonPulse 2s infinite !important;
    }
    
    @keyframes buttonPulse {
        0%, 100% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4), 0 0 0 0 rgba(255, 215, 0, 0.4); }
        50% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.6), 0 0 0 10px rgba(255, 215, 0, 0); }
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 15px 40px rgba(218, 165, 32, 0.5),
            0 0 30px rgba(255, 215, 0, 0.3) !important;
        background-position: right center !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    /* ===== التنبيهات ===== */
    .stAlert {
        background: rgba(0, 31, 63, 0.9) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.5) !important;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.15) !important;
        border: 1px solid rgba(255, 193, 7, 0.5) !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.15) !important;
        border: 1px solid rgba(220, 53, 69, 0.5) !important;
    }

    /* ===== زر التحميل ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 15px 40px !important;
        border-radius: 12px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(99, 102, 241, 0.5) !important;
    }

    /* ===== شريط النجاح ===== */
    .success-banner {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 20px 30px;
        text-align: center;
        margin: 20px;
        animation: successPop 0.5s ease;
    }
    
    @keyframes successPop {
        0% { transform: scale(0.9); opacity: 0; }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-banner span {
        color: #22c55e;
        font-size: 1.2rem;
        font-weight: 700;
    }

    /* ===== إخفاء التسميات ===== */
    .stTextArea > label,
    .stFileUploader > label,
    .stRadio > label {
        display: none !important;
    }

    /* ===== المعاينة ===== */
    iframe {
        border-radius: 15px !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important;
    }

    /* ===== شريط التقدم ===== */
    .progress-box {
        background: rgba(0, 31, 63, 0.9);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 30px;
        margin: 20px;
        text-align: center;
    }
    
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% 100%;
        border-radius: 10px;
        animation: progressShine 1.5s infinite linear;
        transition: width 0.3s ease;
    }
    
    @keyframes progressShine {
        0% { background-position: 200% center; }
        100% { background-position: -200% center; }
    }
    
    .progress-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        margin-top: 10px;
    }

    /* ===== الاستجابة ===== */
    @media (max-width: 768px) {
        .main-title { font-size: 36px; }
        .sub-title { font-size: 14px; }
        .hero-section { padding: 30px 20px; margin: 10px; }
        div[role="radiogroup"] label { min-width: 130px !important; padding: 12px 15px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب المطورة (تفاعلية + CSS حديث)
# ---------------------------------------------------------

# 1. القالب الرسمي المطور (Official)
STYLE_OFFICIAL_MODERN = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
    :root { --navy: #001f3f; --gold: #c5a059; --paper: #ffffff; --text: #333; }
    body { font-family: 'Tajawal', sans-serif; background: #f4f4f4; color: var(--text); padding: 40px; margin: 0; direction: rtl; }
    .container { max-width: 1000px; margin: 0 auto; background: var(--paper); padding: 60px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-radius: 8px; position: relative; }
    
    /* ترويسة الكتاب الرسمي */
    header { border-bottom: 3px solid var(--navy); padding-bottom: 30px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: center; }
    .header-right { text-align: right; }
    .header-left { text-align: left; opacity: 0.8; font-size: 0.9rem; }
    header h1 { color: var(--navy); font-size: 2.2rem; margin: 0; font-weight: 800; }
    header h2 { color: var(--gold); font-size: 1.2rem; margin: 5px 0 0; }
    
    /* البطاقات الرسمية */
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }
    .metric-box { border: 1px solid #eee; padding: 20px; border-right: 4px solid var(--navy); background: #fcfcfc; transition: 0.3s; }
    .metric-box:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .metric-val { font-size: 1.8rem; font-weight: bold; color: var(--navy); display: block; }
    .metric-lbl { font-size: 0.9rem; color: #666; }

    /* الجداول */
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.95rem; }
    th { background: var(--navy); color: white; padding: 12px; text-align: center; }
    td { border: 1px solid #ddd; padding: 10px; text-align: center; }
    tr:nth-child(even) { background: #f9f9f9; }

    /* الرسم البياني */
    .chart-section { margin: 40px 0; border: 1px solid #eee; padding: 20px; border-radius: 8px; page-break-inside: avoid; background: #fff; }
    .chart-container { height: 350px; }
    
    /* التوقيع */
    .signature { margin-top: 80px; display: flex; justify-content: space-between; page-break-inside: avoid; }
    .sign-box { text-align: center; width: 200px; }
    .sign-line { border-top: 1px solid #333; margin-top: 40px; }
    
    @media print { body { background: white; padding: 0; } .container { box-shadow: none; margin: 0; width: 100%; max-width: 100%; } }
</style>
"""

# 2. القالب الرقمي المطور (Digital Dashboard)
STYLE_DIGITAL_MODERN = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    :root { --bg-dark: #1a1a2e; --card-dark: #16213e; --accent: #0f3460; --highlight: #e94560; --text-light: #e0e0e0; }
    body { font-family: 'Cairo', sans-serif; background: var(--bg-dark); color: var(--text-light); margin: 0; padding: 20px; direction: rtl; }
    .container { max-width: 1400px; margin: 0 auto; }
    
    /* الهيدر الرقمي */
    .dash-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; background: var(--card-dark); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); }
    .dash-header h1 { margin: 0; background: linear-gradient(90deg, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .status-badge { background: rgba(46, 204, 113, 0.2); color: #2ecc71; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; border: 1px solid #2ecc71; }

    /* شبكة البطاقات */
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 30px; }
    .kpi-card { background: var(--card-dark); padding: 25px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); position: relative; overflow: hidden; transition: transform 0.3s; }
    .kpi-card:hover { transform: translateY(-5px); background: #1a2644; }
    .kpi-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--highlight); }
    .kpi-value { font-size: 2.5rem; font-weight: bold; margin: 10px 0; }
    .kpi-label { color: #888; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }

    /* المحتوى والرسوم */
    .layout-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
    .panel { background: var(--card-dark); border-radius: 15px; padding: 25px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05); }
    .chart-container { position: relative; height: 350px; width: 100%; }
    
    /* الجداول المظلمة */
    table { width: 100%; border-collapse: collapse; }
    th { text-align: right; color: #888; padding: 15px; border-bottom: 1px solid #333; }
    td { padding: 15px; border-bottom: 1px solid #222; }
    tr:hover { background: rgba(255,255,255,0.02); }
</style>
"""

# 3. القالب التحليلي المطور (Analytical)
STYLE_ANALYTICAL_MODERN = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    :root { --blue: #0056b3; --light-blue: #eef5ff; --grey: #f8f9fa; }
    body { font-family: 'Cairo', sans-serif; background: #fff; color: #333; padding: 40px; direction: rtl; }
    .report-container { max-width: 1100px; margin: 0 auto; }
    
    .section-title { font-size: 1.8rem; color: var(--blue); margin-bottom: 20px; display: flex; align-items: center; gap: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    .stats-row { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
    .stat-block { flex: 1; background: var(--light-blue); padding: 20px; border-radius: 8px; border: 1px solid #d0e3ff; min-width: 200px; text-align: center; }
    .stat-block .num { font-size: 2rem; font-weight: 900; color: var(--blue); display: block; }
    
    .viz-container { background: white; border: 1px solid #eee; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border-radius: 10px; margin: 20px 0; height: 350px; }
    
    table { width: 100%; border: 1px solid #ddd; border-collapse: collapse; margin-top: 20px; }
    th { background: #0056b3; color: white; padding: 10px; }
    td { border: 1px solid #ddd; padding: 10px; text-align: center; }
</style>
"""

# 4. قالب العرض التقديمي المطور (Slides)
STYLE_PRESENTATION_MODERN = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    body { margin: 0; padding: 0; overflow-x: hidden; background: #000; font-family: 'Tajawal', sans-serif; direction: rtl; }
    .slide-container { scroll-snap-type: y mandatory; overflow-y: scroll; height: 100vh; scroll-behavior: smooth; }
    
    .slide {
        height: 100vh; width: 100vw; scroll-snap-align: start;
        display: flex; flex-direction: column; padding: 40px 80px; box-sizing: border-box;
        position: relative; background: radial-gradient(circle at center, #002b49 0%, #001a2c 100%);
        color: white; border-bottom: 2px solid #c5a059;
    }
    
    .slide.cover { justify-content: center; align-items: center; text-align: center; }
    .cover h1 { font-size: 4rem; color: #c5a059; text-shadow: 0 5px 20px rgba(0,0,0,0.5); margin: 0; }
    .cover h2 { font-size: 2rem; color: #fff; opacity: 0.9; font-weight: 300; }
    
    .slide-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 40px; }
    .slide-title { font-size: 2.5rem; color: #c5a059; font-weight: bold; }
    
    .content-split { display: flex; gap: 50px; height: 70%; }
    .text-side { flex: 1; font-size: 1.5rem; line-height: 1.8; overflow-y: auto; }
    .viz-side { flex: 1; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; }
    .slide-chart { width: 100%; height: 100%; min-height: 300px; }
    
    ul { list-style: none; padding: 0; }
    li { margin-bottom: 20px; position: relative; padding-right: 30px; }
    li::before { content: '➤'; color: #c5a059; position: absolute; right: 0; }
</style>
"""

# 5. الملخص التنفيذي المطور (Executive)
STYLE_EXECUTIVE_MODERN = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap');
    body { font-family: 'Tajawal', sans-serif; background: #fff; color: #222; margin: 0; padding: 40px; direction: rtl; }
    .exec-container { max-width: 900px; margin: 0 auto; border: 1px solid #eee; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.08); }
    
    .exec-header { border-bottom: 4px solid #000; padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; }
    .brand { font-size: 0.9rem; text-transform: uppercase; color: #666; letter-spacing: 2px; }
    h1 { font-size: 3rem; margin: 10px 0; font-weight: 900; line-height: 1; }
    
    .summary-lead { font-size: 1.3rem; font-weight: 500; color: #444; margin-bottom: 40px; border-right: 5px solid #FFD700; padding-right: 25px; background: #fafafa; padding: 20px; }
    
    .big-numbers { display: flex; justify-content: space-between; margin: 40px 0; background: #002b49; color: white; padding: 30px; border-radius: 10px; }
    .bn-item { text-align: center; flex: 1; border-left: 1px solid rgba(255,255,255,0.2); }
    .bn-item:last-child { border-left: none; }
    .bn-val { font-size: 2.5rem; font-weight: bold; color: #FFD700; display: block; }
    
    .chart-zone { margin: 40px 0; height: 350px; }
    .key-points { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
    .kp-card { background: #f9f9f9; padding: 20px; border-radius: 8px; border-top: 3px solid #002b49; }
</style>
"""

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    text_content = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            text_content = df.to_string()
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text_content = stringio.read()
    except Exception as e:
        return f"خطأ في قراءة الملف: {e}"
    return text_content

def clean_html_response(text):
    text = text.replace("```html", "").replace("```", "")
    return text.strip()

def get_working_model():
    """دالة احتياطية ترجع الموديل الافتراضي، المعالجة الحقيقية للخطأ في الدالة الرئيسية"""
    return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ بناء الواجهة
# ---------------------------------------------------------

# الهيدر الرئيسي
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

# عنوان اختيار النمط
st.markdown('<div class="section-header">🎨 اختر نمط الإخراج المطلوب</div>', unsafe_allow_html=True)

# أزرار الاختيار
report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي (PPT)", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# منطقة الإدخال
col_input, col_upload = st.columns([2, 1])

with col_input:
    st.markdown('''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📝</div>
            <div>
                <div class="input-title">البيانات / الملاحظات</div>
                <div class="input-subtitle">أدخل النص أو الصق محتوى التقرير هنا</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...", label_visibility="collapsed")

with col_upload:
    st.markdown('''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📎</div>
            <div>
                <div class="input-title">رفع الملفات</div>
                <div class="input-subtitle">PDF, XLSX, TXT - حتى 200MB</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    if uploaded_file:
        st.success(f"✅ تم إرفاق: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

# زر المعالجة
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. يرجى إضافته في Secrets.")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            full_text += f"\n\n[محتوى الملف]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            
            # === الحل الذكي لمشكلة الموديل (Fallback Logic) ===
            try:
                # المحاولة الأولى: الموديل السريع
                model = genai.GenerativeModel("gemini-1.5-flash")
                # اختبار بسيط للتأكد من الاتصال
                # response = model.generate_content("test") 
            except:
                # في حال الفشل، الانتقال للموديل المستقر
                model = genai.GenerativeModel("gemini-pro")

            target_css = ""
            prompt_instruction = ""
            file_label = "Report"
            
            # اختيار القالب والتعليمات بناءً على اختيار المستخدم
            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL_MODERN
                file_label = "Official_Report"
                prompt_instruction = """
                **Style:** Official Government Report.
                - Use `<header>` with `<h1>` and `<h2>`.
                - Use `<div class="metric-grid">` with 3-4 `<div class="metric-box">`.
                - Use `<div class="chart-section"><div class="chart-container"><canvas id="mainChart"></canvas></div></div>`.
                - Use standard HTML tables and sections.
                - **MANDATORY:** End with a `<script>` tag that renders a Bar Chart using Chart.js on canvas 'mainChart'.
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL_MODERN
                file_label = "Digital_Dashboard"
                prompt_instruction = """
                **Style:** Modern Dark Dashboard.
                - Use `<div class="dash-header">`.
                - Use `<div class="kpi-grid">` with `<div class="kpi-card">`.
                - Use `<div class="layout-grid">` containing `<div class="panel"><div class="chart-container"><canvas id="dashChart"></canvas></div></div>`.
                - **MANDATORY:** End with a `<script>` tag that renders a Line Chart using Chart.js on canvas 'dashChart' with neon colors.
                """

            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL_MODERN
                file_label = "Deep_Analysis"
                prompt_instruction = """
                **Style:** Deep Analytical Report.
                - Use `<div class="stats-row">`.
                - Use `<div class="viz-container"><canvas id="analysisChart"></canvas></div>`.
                - Detailed text analysis.
                - **MANDATORY:** End with a `<script>` tag that renders a Mixed Chart using Chart.js on canvas 'analysisChart'.
                """

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION_MODERN
                file_label = "Presentation_Slides"
                prompt_instruction = """
                **Style:** Interactive Slides.
                - Output multiple `<div class="slide">`.
                - Slide 1: Cover.
                - Slide 2: `<div class="content-split"><div class="viz-side"><canvas id="slideChart1"></canvas></div>...</div>`.
                - **MANDATORY:** End with a `<script>` tag that renders a Doughnut Chart using Chart.js on canvas 'slideChart1'.
                """

            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE_MODERN
                file_label = "Executive_Summary"
                prompt_instruction = """
                **Style:** Executive Summary.
                - Use `<div class="exec-header">`.
                - Use `<div class="big-numbers">`.
                - Use `<div class="chart-zone"><canvas id="execChart"></canvas></div>`.
                - **MANDATORY:** End with a `<script>` tag that renders a Horizontal Bar Chart using Chart.js on canvas 'execChart'.
                """

            # بناء الـ Prompt
            prompt = f"""
            You are an expert Data Analyst & Developer.
            **Objective:** Create a FULL, DETAILED HTML report body based on the input.
            
            **CRITICAL INSTRUCTIONS:**
            1. **Process Content:** Be exhaustive. Don't summarize too much.
            2. **Format:** Output ONLY valid HTML code (inside <body> tags). Do not include <html>, <head>, or <body> tags.
            3. **Design:** Follow these specific design rules:
            {prompt_instruction}
            
            **INPUT DATA:**
            {full_text}
            
            **LANGUAGE:** Arabic (Professional).
            **IMPORTANT:** You MUST include the <script> block for Chart.js at the very end. Make sure the chart data reflects the numbers in the text.
            """

            # شريط التقدم
            progress_placeholder = st.empty()
            
            for i in range(0, 101, 10):
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🤖</div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {i}%;"></div>
                    </div>
                    <div class="progress-text">جاري تحليل البيانات وتوليد التقرير التفاعلي... {i}%</div>
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(0.1)
            
            # محاولة التوليد (مع معالجة الأخطاء الداخلية للموديل)
            try:
                response = model.generate_content(prompt)
                html_body = clean_html_response(response.text)
            except Exception as e:
                # إذا فشل الموديل الأول أثناء التوليد، نجرب الموديل الثاني (gemini-pro)
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)
                html_body = clean_html_response(response.text)
            
            progress_placeholder.empty()
            
            # تجميع الملف النهائي
            final_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>تقرير {file_label}</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
                {target_css}
            </head>
            <body>
                <div class="{ 'presentation-container' if 'عرض تقديمي' in report_type else 'container' }">
                    {html_body}
                </div>
                {SCRIPT_PRESENTATION if 'عرض تقديمي' in report_type else ''}
            </body>
            </html>
            """

            st.markdown('''
            <div class="success-banner">
                <span>✅ تم إنشاء التقرير بنجاح!</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.components.v1.html(final_html, height=850, scrolling=True)

            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=final_html,
                file_name=f"{file_label}.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")
            st.warning("قد يكون السبب ضعف الاتصال أو مشكلة في مفتاح API.")

# الفوتر
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''
<div style="
    background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
    border-radius: 15px;
    padding: 30px 20px;
    margin: 20px;
    border: 1px solid rgba(255, 215, 0, 0.3);
    text-align: center;
    box-shadow: 0 -5px 30px rgba(0, 0, 0, 0.3);
">
    <div style="
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 0 auto 20px auto;
        border-radius: 2px;
    "></div>
    <p style="
        color: #FFD700;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
        font-family: 'Tajawal', sans-serif;
    ">الجهاز المركزي للجودة الشاملة</p>
    <p style="
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 15px;
        font-family: 'Tajawal', sans-serif;
    ">وحدة التخطيط الاستراتيجي والتطوير</p>
    <div style="
        width: 100px;
        height: 1px;
        background: rgba(255, 215, 0, 0.3);
        margin: 15px auto;
    "></div>
    <p style="
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
        font-family: 'Tajawal', sans-serif;
    ">جميع الحقوق محفوظة © 2026</p>
</div>
''', unsafe_allow_html=True)
