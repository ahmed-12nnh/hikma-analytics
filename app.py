import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح في Secrets.")
    st.stop()

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة والتصميم الحديث (Modern UI - Enhanced)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide")

# CSS متطور جداً - تحسينات: ألوان أكثر حداثة، استجابة كاملة، تأثيرات إبداعية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
    
    /* إعدادات الخط والاتجاه الرئيسية - تحسين: خط عالمي (Inter) للمظهر الحديث */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
        direction: rtl;
        color: #e0e0e0;
    }

    /* إخفاء القائمة الجانبية والهيدر الافتراضي */
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* ========================================= */
    /* 🦅 تصميم الهيدر الفخم (محسن: أكثر تفاعلية واستجابة) */
    /* ========================================= */
    .hero-section {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.9));
        border-radius: 25px;
        padding: 50px 30px;
        text-align: center;
        margin-bottom: 40px;
        border: 2px solid rgba(138, 43, 226, 0.4); /* لمسة إبداعية: حدود بنفسجية */
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), inset 0 0 30px rgba(138, 43, 226, 0.1);
        position: relative;
        overflow: hidden;
        animation: slideIn 1.2s ease-out;
    }

    /* تأثير إبداعي: خطوط متحركة في الأعلى */
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 8px;
        background: linear-gradient(90deg, transparent, #8a2be2, #ffd700, transparent);
        box-shadow: 0 0 20px #8a2be2;
        animation: shimmer 2s infinite;
    }

    .main-title {
        font-size: clamp(40px, 5vw, 60px); /* استجابة: يتكيف مع الشاشة */
        font-weight: 900;
        background: linear-gradient(to right, #ffd700, #8a2be2, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-shadow: 0px 5px 15px rgba(0,0,0,0.7);
    }

    .sub-title {
        color: #c0c0c0;
        font-size: clamp(16px, 2vw, 20px);
        letter-spacing: 1px;
        font-weight: 500;
    }

    /* ========================================= */
    /* تحسينات على الأزرار والحقول */
    /* ========================================= */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row-reverse;
        justify-content: center;
        gap: 20px;
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(138, 43, 226, 0.2);
        backdrop-filter: blur(10px); /* تأثير زجاجي إبداعي */
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(138, 43, 226, 0.1));
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px 25px;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.4s ease;
        text-align: center;
        flex: 1;
        color: white !important;
        font-weight: 600;
        font-size: 16px;
    }

    div[role="radiogroup"] label:hover {
        background: linear-gradient(135deg, #8a2be2, #ffd700);
        border-color: #ffd700;
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 10px 25px rgba(138, 43, 226, 0.5);
    }

    /* حقول الإدخال - محسنة للاستجابة */
    .stTextArea textarea, .stFileUploader {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(138, 43, 226, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        text-align: right;
        font-size: 16px;
        transition: border-color 0.3s;
    }
    .stTextArea textarea:focus, .stFileUploader:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }
    
    /* زر التشغيل - محسن بتأثيرات إبداعية */
    .stButton button {
        background: linear-gradient(90deg, #8a2be2, #ffd700, #00d4ff);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 18px;
        border-radius: 20px;
        width: 100%;
        padding: 18px;
        border: none;
        box-shadow: 0 5px 20px rgba(138, 43, 226, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    .stButton button:hover::before { left: 100%; }
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.7);
    }

    /* أنيميشن جديدة */
    @keyframes slideIn {
        0% { opacity: 0; transform: translateY(-30px) scale(0.9); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    /* تنسيق العناوين المخصصة - محسن */
    .custom-header {
        text-align: right !important;
        color: #ffd700;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 15px;
        border-right: 5px solid #8a2be2;
        padding-right: 15px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }

    /* قسم النتائج - جديد: بطاقات قابلة للطي للتنظيم */
    .results-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        margin-top: 30px;
        border: 1px solid rgba(138, 43, 226, 0.2);
        backdrop-filter: blur(10px);
    }
    .results-section h3 {
        color: #ffd700;
        text-align: center;
        margin-bottom: 20px;
    }

    /* استجابة للشاشات الصغيرة */
    @media (max-width: 768px) {
        .hero-section { padding: 30px 20px; }
        div[role="radiogroup"] { flex-direction: column; gap: 10px; }
        .main-title { font-size: 40px; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب (CSS Styles) - محسنة لتتناسب مع التصميم الجديد
# ---------------------------------------------------------
STYLE_OFFICIAL = """
<style>
    :root { --navy-blue: #001f3f; --gold: #FFD700; --light-gold: #FFEB84; --white: #ffffff; --gray: #f4f4f4; --dark-gray: #333; }
    body { font-family: 'Inter', sans-serif; background-color: var(--gray); color: var(--dark-gray); line-height: 1.6; direction: rtl; text-align: right; }
    .container { max-width: 1200px; margin: 20px auto; padding: 20px; display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
    header { background-color: var(--navy-blue); color: var(--gold); padding: 20px 0; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); grid-column: 1 / -1; margin-bottom: 20px; border-radius: 8px; }
    header h1 { margin: 0; font-size: 2.5em; font-weight: 700; }
    header h2 { margin: 10px 0 0; font-size: 1.5em; color: var(--light-gold); }
    .card { background-color: var(--white); border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); padding: 25px; display: flex; flex-direction: column; }
    .card h3 { color: var(--navy-blue); font-size: 1.8em; margin-top: 0; border-bottom: 2px solid var(--gold); padding-bottom: 10px; }
    .card table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.95em; }
    .card table th { background-color: var(--navy-blue); color: var(--light-gold); padding: 12px; border: 1px solid #ddd; }
    .card table td { border: 1px solid #ddd; padding: 12px; }
    .card ul { list-style: none; padding: 0; }
    .card ul li { padding: 10px 0; border-bottom: 1px dashed #eee; display: flex; justify-content: space-between; }
    .card ul li span.value { font-weight: 700; color: var(--gold); font-size: 1.1em; }
    .card.full-width { grid-column: 1 / -1; }
    footer { grid-column: 1 / -1; text-align: center; margin-top: 40px; padding: 20px; color: #666; font-size: 0.9em; border-top: 2px solid var(--navy-blue); }
</style>
"""

STYLE_DIGITAL = """
<style>
    body { font-family: 'Inter', sans-serif; line-height: 1.7; background-color: #f4f7f9; color: #333; direction: rtl; }
    .container { max-width: 1200px; margin: 20px auto; padding: 25px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07); }
    header { text-align: center; padding-bottom: 20px; margin-bottom: 30px; border-bottom: 3px solid #0056b3; }
    h1 { color: #0056b3; font-size: 2.4em; font-weight: 700; }
    h2 { color: #007bff; font-size: 2em; border-bottom: 2px solid #f0f0f0; margin-bottom: 20px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    thead th { background-color: #007bff; color: white; padding: 14px; }
    td { padding: 14px; border: 1px solid #e0e0e0; text-align: center; }
    .card { background-color: #fdfdfd; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; margin-top: 20px; box-shadow: 0 3px 8px rgba(0,0,0,0.05); }
    ul li { position: relative; padding-right: 35px; margin-bottom: 12px; }
    ul li::before { content: '•'; position: absolute; right: 0; color: #007bff; font-size: 1.8em; line-height: 1; }
    .goal { background-color: #e6f7ff; border: 1px solid #b3e0ff; padding: 18px; border-radius: 8px; text-align: center; margin-top: 20px; font-weight: bold; }
    footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-style: italic; color: #777; }
</style>
"""
STYLE_ANALYTICAL = """
<style>
    body { font-family: 'Inter', sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.7; direction: rtl; }
    .container { max-width: 1100px; margin: 20px auto; padding: 20px; }
    header { background-color: #004a99; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0, 74, 153, 0.2); }
    .report-section { background-color: #fff; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.07); margin-bottom: 25px; padding: 25px; }
    .report-section h2 { color: #004a99; border-bottom: 3px solid #0056b3; padding-bottom: 10px; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
    .stat-card { background-color: #eef5ff; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #d0e3ff; }
    .stat-card .value { font-size: 2.2rem; font-weight: 700; color: #004a99; }
    .pyramid-grid {
