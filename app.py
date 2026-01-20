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
# 🎨 CSS واجهة المنصة (Streamlit UI)
# هذا الجزء يحافظ على تصميم واجهة التطبيق التي تحبها (أزرق وذهبي)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    /* === إعدادات عامة === */
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* إخفاء عناصر Streamlit الافتراضية */
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* === الهيدر الرئيسي (Hero Section) === */
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

    /* الخط الذهبي المتوهج */
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        box-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700;
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }

    .main-title {
        font-size: 52px; font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    .sub-title { color: #e0e0e0; font-size: 18px; letter-spacing: 2px; font-weight: 500; opacity: 0.9; }
    @keyframes titleGlow { from { filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.3)); } to { filter: drop-shadow(0 0 25px rgba(255, 215, 0, 0.6)); } }

    /* === عنوان القسم === */
    .section-header { text-align: center; margin: 30px 20px; color: #FFD700; font-size: 1.4rem; font-weight: bold; text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3); }

    /* === أزرار الاختيار (Radio Buttons) === */
    div[role="radiogroup"] {
        display: flex !important; flex-direction: row-reverse !important; justify-content: center !important;
        gap: 15px !important; flex-wrap: wrap !important; background: rgba(0, 0, 0, 0.3) !important;
        padding: 20px !important; border-radius: 15px !important; margin: 0 20px 30px 20px !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
    }
    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95)) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important; padding: 15px 25px !important;
        border-radius: 12px !important; cursor: pointer !important; text-align: center !important;
        flex: 1 !important; min-width: 160px !important; max-width: 220px !important;
        color: white !important; font-weight: 600 !important; transition: all 0.4s !important;
    }
    div[role="radiogroup"] label:hover {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 31, 63, 0.95)) !important;
        border-color: #FFD700 !important; transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 215, 0, 0.2) !important;
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(184, 134, 11, 0.15)) !important;
        border-color: #FFD700 !important; box-shadow: 0 0 25px rgba(255, 215, 0, 0.3) !important;
    }

    /* === بطاقات الإدخال === */
    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px; padding: 30px; margin: 10px; border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3); transition: all 0.4s ease;
    }
    .input-card:hover { transform: translateY(-5px); border-color: rgba(255, 215, 0, 0.4); box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4); }
    .input-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid rgba(255, 215, 0, 0.2); }
    .input-icon { width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #FFD700, #B8860B); border-radius: 12px; font-size: 1.5rem; }
    .input-title { color: #FFD700; font-size: 1.2rem; font-weight: 700; }
    .input-subtitle { color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-top: 5px; }

    /* === حقول النص والملفات === */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important; border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px !important; color: white !important; font-family: 'Tajawal', sans-serif !important;
        font-size: 1rem !important; padding: 20px !important; text-align: right !important; direction: rtl !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important; outline: none !important; }
    [data-testid="stFileUploader"] { background: rgba(0, 0, 0, 0.3) !important; border: 2px dashed rgba(255, 215, 0, 0.3) !important; border-radius: 15px !important; padding: 25px !important; }
    [data-testid="stFileUploader"]:hover { border-color: #FFD700 !important; background: rgba(255, 215, 0, 0.05) !important; }
    [data-testid="stFileUploader"] button { background: linear-gradient(135deg, #FFD700, #B8860B) !important; color: #001f3f !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; padding: 10px 20px !important; }

    /* === زر المعالجة === */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 50%, #FFD700 100%) !important; background-size: 200% auto !important;
        color: #001f3f !important; font-family: 'Tajawal', sans-serif !important; font-weight: 900 !important;
        font-size: 1.3rem !important; border-radius: 15px !important; width: 100% !important; padding: 18px 40px !important;
        border: none !important; box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4) !important; transition: all 0.4s !important;
        animation: buttonPulse 2s infinite !important;
    }
    @keyframes buttonPulse { 0%, 100% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4); } 50% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.6); } }
    .stButton > button:hover { transform: translateY(-3px) scale(1.02) !important; box-shadow: 0 15px 40px rgba(218, 165, 32, 0.5) !important; background-position: right center !important; }

    /* === شريط التقدم والنجاح === */
    .progress-box { background: rgba(0, 31, 63, 0.9); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 15px; padding: 30px; margin: 20px; text-align: center; }
    .progress-bar-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 12px; overflow: hidden; margin: 20px 0; }
    .progress-bar-fill { height: 100%; background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700); background-size: 200% 100%; border-radius: 10px; animation: progressShine 1.5s infinite linear; transition: width 0.3s ease; }
    @keyframes progressShine { 0% { background-position: 200% center; } 100% { background-position: -200% center; } }
    .success-banner { background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1)); border: 2px solid #22c55e; border-radius: 15px; padding: 20px 30px; text-align: center; margin: 20px; animation: successPop 0.5s ease; }
    @keyframes successPop { 0% { transform: scale(0.9); opacity: 0; } 50% { transform: scale(1.02); } 100% { transform: scale(1); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب الكاملة (Templates) - 5 أنماط كاملة ومحدثة
# ---------------------------------------------------------

# 1. القالب الرسمي (Official Report) - تصميم الطباعة الكلاسيكي الحديث
STYLE_OFFICIAL_FULL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700&display=swap');
    :root { --navy: #001f3f; --gold: #c5a059; --paper: #ffffff; --text: #333; --border: #ddd; }
    
    body { font-family: 'Tajawal', sans-serif; background: #525659; color: var(--text); padding: 40px 0; direction: rtl; margin: 0; }
    .container { 
        max-width: 21cm; min-height: 29.7cm; margin: 0 auto; background: var(--paper); padding: 2.5cm; 
        box-shadow: 0 0 20px rgba(0,0,0,0.1); position: relative; 
    }
    
    /* Header */
    header { border-bottom: 3px double var(--navy); padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end; }
    .header-right h1 { color: var(--navy); font-size: 24pt; margin: 0; font-family: 'Amiri', serif; }
    .header-right h2 { color: var(--gold); font-size: 14pt; margin: 5px 0 0; font-weight: normal; }
    .header-left { text-align: left; font-size: 10pt; color: #666; line-height: 1.5; }
    
    /* Content */
    .report-meta { background: #f9f9f9; padding: 15px; border-right: 4px solid var(--navy); margin-bottom: 30px; font-size: 11pt; }
    h1.doc-title { text-align: center; font-size: 20pt; text-decoration: underline; margin: 40px 0; color: #000; }
    
    .section-title { font-size: 16pt; color: var(--navy); border-bottom: 1px solid var(--gold); padding-bottom: 5px; margin-top: 30px; margin-bottom: 15px; font-family: 'Amiri', serif; font-weight: bold; }
    p { font-size: 12pt; line-height: 1.6; text-align: justify; margin-bottom: 15px; }
    
    /* Metrics Grid */
    .metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 30px 0; }
    .metric-box { border: 1px solid var(--border); padding: 15px; text-align: center; background: #fff; }
    .metric-val { font-size: 18pt; font-weight: bold; color: var(--navy); display: block; margin-bottom: 5px; }
    .metric-lbl { font-size: 10pt; color: #555; }
    
    /* Chart Section */
    .chart-container { 
        width: 100%; height: 350px; margin: 30px 0; padding: 10px; 
        border: 1px solid #eee; background: #fff; page-break-inside: avoid; 
    }
    
    /* Tables */
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 11pt; }
    th { background: var(--navy); color: white; padding: 10px; border: 1px solid var(--navy); }
    td { border: 1px solid var(--border); padding: 8px; text-align: center; }
    tr:nth-child(even) { background: #f4f4f4; }
    
    /* Signature */
    .signature-block { margin-top: 80px; display: flex; justify-content: space-between; page-break-inside: avoid; }
    .sign-box { text-align: center; width: 200px; }
    .sign-title { font-weight: bold; margin-bottom: 50px; font-size: 12pt; }
    .sign-line { border-top: 1px solid #000; width: 100%; display: block; }
    
    @media print { 
        body { background: white; padding: 0; } 
        .container { box-shadow: none; margin: 0; width: 100%; max-width: 100%; padding: 0; }
        .chart-container { break-inside: avoid; }
    }
</style>
"""

# 2. القالب الرقمي (Digital Dashboard) - تصميم الشاشات المظلم
STYLE_DIGITAL_FULL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    :root { --bg-dark: #1a1a2e; --card-dark: #16213e; --accent: #0f3460; --highlight: #e94560; --text: #e0e0e0; --success: #00d2d3; }
    
    body { font-family: 'Cairo', sans-serif; background: var(--bg-dark); color: var(--text); margin: 0; padding: 20px; direction: rtl; }
    .dashboard-container { max-width: 1600px; margin: 0 auto; display: grid; gap: 20px; grid-template-columns: repeat(12, 1fr); }
    
    /* Top Header */
    .dash-header { grid-column: 1 / -1; background: var(--card-dark); padding: 20px; border-radius: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--highlight); }
    .dash-header h1 { margin: 0; font-size: 1.8rem; background: linear-gradient(to right, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .live-badge { background: rgba(233, 69, 96, 0.2); color: var(--highlight); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; border: 1px solid var(--highlight); animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
    
    /* KPI Cards */
    .kpi-section { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    .kpi-card { background: var(--card-dark); padding: 25px; border-radius: 15px; position: relative; overflow: hidden; transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .kpi-card:hover { transform: translateY(-5px); background: #1f2b4d; }
    .kpi-card::before { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px; background: var(--success); }
    .kpi-val { font-size: 2.5rem; font-weight: 700; color: #fff; margin: 10px 0; }
    .kpi-title { font-size: 0.9rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Main Chart Area */
    .main-chart-panel { grid-column: span 8; background: var(--card-dark); padding: 20px; border-radius: 15px; height: 400px; position: relative; }
    @media (max-width: 1000px) { .main-chart-panel { grid-column: 1 / -1; } }
    .panel-title { font-size: 1.2rem; margin-bottom: 15px; color: #fff; border-left: 3px solid var(--accent); padding-left: 10px; }
    .chart-box { width: 100%; height: 320px; }
    
    /* Side Panel */
    .side-panel { grid-column: span 4; background: var(--card-dark); padding: 20px; border-radius: 15px; display: flex; flex-direction: column; gap: 15px; }
    @media (max-width: 1000px) { .side-panel { grid-column: 1 / -1; } }
    .list-item { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; }
    .list-item span { font-weight: bold; color: var(--success); }
    
    /* Tables */
    .data-table-panel { grid-column: 1 / -1; background: var(--card-dark); padding: 20px; border-radius: 15px; }
    table { width: 100%; border-collapse: collapse; color: #ddd; }
    th { text-align: right; padding: 15px; border-bottom: 1px solid #333; color: #888; }
    td { padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }
    tr:hover td { background: rgba(255,255,255,0.02); }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }
</style>
"""

# 3. القالب التحليلي (Analytical Report) - تصميم أكاديمي وعميق
STYLE_ANALYTICAL_FULL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');
    :root { --primary: #2c3e50; --secondary: #3498db; --bg: #ecf0f1; --white: #fff; }
    
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); color: #333; padding: 30px; direction: rtl; }
    .research-paper { max-width: 1100px; margin: 0 auto; background: var(--white); padding: 60px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); border-top: 10px solid var(--primary); }
    
    /* Title Section */
    .paper-header { text-align: center; margin-bottom: 60px; border-bottom: 1px solid #eee; padding-bottom: 30px; }
    .paper-header h1 { font-size: 2.5rem; color: var(--primary); margin-bottom: 10px; }
    .paper-meta { color: #7f8c8d; font-style: italic; }
    
    /* Abstract Box */
    .abstract-box { background: #f8f9fa; padding: 30px; border-right: 5px solid var(--secondary); margin-bottom: 40px; font-size: 1.1rem; line-height: 1.8; color: #555; }
    .abstract-title { font-weight: bold; text-transform: uppercase; color: var(--secondary); display: block; margin-bottom: 10px; font-size: 0.9rem; }
    
    /* Stats Hierarchy */
    .hierarchy-grid { display: flex; gap: 20px; justify-content: space-around; margin: 40px 0; background: #fff; padding: 20px; border: 1px solid #eee; border-radius: 8px; }
    .node { text-align: center; }
    .node-val { font-size: 2rem; font-weight: bold; color: var(--primary); display: block; }
    .node-lbl { font-size: 0.9rem; color: #7f8c8d; }
    
    /* Content Columns */
    .content-cols { column-count: 2; column-gap: 40px; text-align: justify; margin-bottom: 40px; }
    @media (max-width: 800px) { .content-cols { column-count: 1; } }
    p { margin-bottom: 20px; line-height: 1.7; font-size: 1rem; }
    
    /* Charts embedded in text */
    .figure-box { break-inside: avoid; background: #fff; border: 1px solid #eee; padding: 15px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .figure-caption { text-align: center; font-size: 0.9rem; color: #777; margin-top: 10px; font-style: italic; }
    .chart-wrapper { width: 100%; height: 300px; }
    
    /* Analysis Lists */
    ul.analysis-list { list-style: none; padding: 0; }
    ul.analysis-list li { margin-bottom: 15px; padding-right: 20px; position: relative; }
    ul.analysis-list li::before { content: '■'; color: var(--secondary); position: absolute; right: 0; top: 0; font-size: 1.2rem; line-height: 1.5rem; }
</style>
"""

# 4. قالب العرض التقديمي (Presentation Slides) - تصميم شرائح Reveal.js
STYLE_PRESENTATION_FULL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    body { margin: 0; padding: 0; overflow-x: hidden; background: #000; font-family: 'Tajawal', sans-serif; direction: rtl; }
    
    /* Slide Container */
    .slides-wrapper { scroll-snap-type: y mandatory; overflow-y: scroll; height: 100vh; scroll-behavior: smooth; }
    
    /* Individual Slide */
    .slide {
        height: 100vh; width: 100%; scroll-snap-align: start;
        display: flex; flex-direction: column; padding: 40px 80px; box-sizing: border-box;
        position: relative; background: radial-gradient(circle at center, #002b49 0%, #001a2c 100%);
        color: white; border-bottom: 4px solid #c5a059;
    }
    
    /* Cover Slide */
    .slide.cover { justify-content: center; align-items: center; text-align: center; background: linear-gradient(135deg, #001f3f 0%, #000 100%); }
    .cover-content { border: 2px solid #c5a059; padding: 60px 100px; background: rgba(0,0,0,0.4); backdrop-filter: blur(5px); }
    .cover h1 { font-size: 4.5rem; color: #c5a059; text-shadow: 0 10px 30px rgba(0,0,0,0.5); margin: 0 0 20px 0; }
    .cover h2 { font-size: 2rem; color: #fff; font-weight: 300; margin: 0; }
    
    /* Content Slide Structure */
    .slide-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 40px; height: 10%; }
    .slide-title { font-size: 2.5rem; color: #c5a059; font-weight: 800; }
    .slide-logo { font-size: 1.2rem; opacity: 0.7; }
    
    .slide-body { display: flex; height: 80%; gap: 60px; align-items: center; }
    .text-column { flex: 1; font-size: 1.6rem; line-height: 1.6; }
    .visual-column { flex: 1; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.03); border-radius: 20px; padding: 20px; }
    
    /* Chart in Slide */
    .slide-chart-box { width: 100%; height: 100%; min-height: 400px; }
    
    /* Bullet Points */
    ul { list-style: none; padding: 0; }
    li { margin-bottom: 30px; position: relative; padding-right: 40px; opacity: 0; animation: slideIn 0.5s forwards; }
    li:nth-child(1) { animation-delay: 0.2s; }
    li:nth-child(2) { animation-delay: 0.4s; }
    li:nth-child(3) { animation-delay: 0.6s; }
    @keyframes slideIn { from { transform: translateX(-20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    li::before { content: '➤'; color: #c5a059; position: absolute; right: 0; }
    
    /* Navigation Hint */
    .nav-hint { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: rgba(255,255,255,0.3); animation: bounce 2s infinite; }
    @keyframes bounce { 0%, 20%, 50%, 80%, 100% {transform: translateY(0) translateX(-50%);} 40% {transform: translateY(-10px) translateX(-50%);} 60% {transform: translateY(-5px) translateX(-50%);} }
</style>
"""

# 5. القالب التنفيذي (Executive Summary) - ملخص الصفحة الواحدة
STYLE_EXECUTIVE_FULL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap');
    :root { --dark: #111; --accent: #FFD700; --gray: #f4f4f4; }
    
    body { font-family: 'Tajawal', sans-serif; background: #fff; color: #222; margin: 0; padding: 40px; direction: rtl; }
    .exec-wrapper { max-width: 900px; margin: 0 auto; border: 1px solid #e0e0e0; padding: 50px; box-shadow: 0 15px 50px rgba(0,0,0,0.05); }
    
    /* Header */
    .exec-header { display: flex; justify-content: space-between; border-bottom: 5px solid var(--dark); padding-bottom: 30px; margin-bottom: 40px; }
    .main-head h1 { font-size: 3.5rem; font-weight: 800; margin: 0; line-height: 1; letter-spacing: -1px; }
    .sub-head { text-align: left; display: flex; flex-direction: column; justify-content: flex-end; }
    .date-badge { background: var(--dark); color: var(--accent); padding: 5px 15px; font-weight: bold; display: inline-block; text-align: center; }
    
    /* Key Takeaway (Big Yellow Box) */
    .takeaway-box { background: #fff9c4; border-right: 6px solid var(--accent); padding: 25px; font-size: 1.4rem; font-weight: 500; color: #444; margin-bottom: 40px; line-height: 1.6; }
    
    /* Metrics Row */
    .metrics-row { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 40px; background: var(--gray); padding: 30px; border-radius: 12px; }
    .m-item { text-align: center; flex: 1; border-left: 1px solid #ddd; }
    .m-item:last-child { border-left: none; }
    .m-val { font-size: 3rem; font-weight: 800; color: var(--dark); display: block; line-height: 1; }
    .m-lbl { font-size: 0.9rem; text-transform: uppercase; color: #666; margin-top: 10px; display: block; }
    
    /* Split Layout: Chart + List */
    .split-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }
    .chart-area { height: 350px; background: #fff; border: 1px solid #eee; padding: 10px; }
    .action-list h3 { border-bottom: 2px solid var(--accent); padding-bottom: 10px; margin-top: 0; }
    .action-item { margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px dotted #ccc; display: flex; gap: 10px; }
    .action-icon { color: var(--accent); font-weight: bold; }
    
    /* Footer */
    .exec-footer { margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px; text-align: center; font-size: 0.8rem; color: #999; }
</style>
"""

# ---------------------------------------------------------
# 🛠️ دوال المساعدة (Helpers)
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
    return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ واجهة التطبيق الرئيسية
# ---------------------------------------------------------

# الهيدر
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

# عنوان اختيار النمط
st.markdown('<div class="section-header">🎨 اختر نمط الإخراج المطلوب</div>', unsafe_allow_html=True)

# أزرار الاختيار (تمت استعادتها)
report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي (شرائح)", "✨ ملخص تنفيذي"),
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

# ---------------------------------------------------------
# 🚀 منطق المعالجة الرئيسي (The Core Engine)
# ---------------------------------------------------------
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. يرجى إضافته في Secrets.")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            full_text += f"\n\n[FILE_CONTENT]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            # تحديد المتغيرات بناءً على اختيار المستخدم
            target_css = ""
            prompt_instruction = ""
            chart_script_instruction = ""
            html_wrapper_class = ""
            
            # 1. إعدادات الكتاب الرسمي
            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL_FULL
                html_wrapper_class = "container"
                prompt_instruction = """
                **Style: Official Government Report.**
                - **Tone:** Formal, authoritative, precise.
                - **Structure:**
                  - `<header>`: Contains `<div class="header-right"><h1>Title</h1><h2>Subtitle</h2></div>` and `<div class="header-left">Date/Ref No</div>`.
                  - `<div class="report-meta">`: Brief executive context.
                  - `<div class="metric-grid">`: 3 to 6 `<div class="metric-box"><span class="metric-val">X</span><span class="metric-lbl">Y</span></div>`.
                  - `<div class="chart-container"><canvas id="reportChart"></canvas></div>`.
                  - Content Sections: Use `<h3 class="section-title">` for headings and `<p>` for text.
                  - `<table>`: Standard data table.
                  - `<div class="signature-block">`: Signatures at bottom.
                """
                chart_script_instruction = """
                new Chart(document.getElementById('reportChart'), {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ label: 'Data', data: values, backgroundColor: '#001f3f' }] },
                    options: { responsive: true, maintainAspectRatio: false }
                });
                """

            # 2. إعدادات الداشبورد الرقمي
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL_FULL
                html_wrapper_class = "dashboard-container"
                prompt_instruction = """
                **Style: Modern Dark Dashboard.**
                - **Tone:** Technical, concise, data-driven.
                - **Structure:**
                  - `<div class="dash-header"><h1>Title</h1><div class="live-badge">LIVE ANALYTICS</div></div>`.
                  - `<div class="kpi-section">`: Multiple `<div class="kpi-card"><div class="kpi-val">X</div><div class="kpi-title">Y</div></div>`.
                  - `<div class="main-chart-panel"><div class="panel-title">Overview</div><div class="chart-box"><canvas id="dashChart"></canvas></div></div>`.
                  - `<div class="side-panel">`: List of top items `<div class="list-item">Text <span>Val</span></div>`.
                  - `<div class="data-table-panel">`: Detailed table.
                """
                chart_script_instruction = """
                new Chart(document.getElementById('dashChart'), {
                    type: 'line',
                    data: { labels: labels, datasets: [{ label: 'Trend', data: values, borderColor: '#e94560', backgroundColor: 'rgba(233, 69, 96, 0.2)', fill: true, tension: 0.4 }] },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { grid: { color: 'rgba(255,255,255,0.1)' } }, x: { grid: { color: 'rgba(255,255,255,0.1)' } } }, plugins: { legend: { labels: { color: '#fff' } } } }
                });
                """

            # 3. إعدادات التحليل العميق
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL_FULL
                html_wrapper_class = "research-paper"
                prompt_instruction = """
                **Style: Deep Research/Analytical Paper.**
                - **Tone:** Academic, detailed, objective.
                - **Structure:**
                  - `<div class="paper-header"><h1>Title</h1><div class="paper-meta">Author | Date</div></div>`.
                  - `<div class="abstract-box"><span class="abstract-title">Abstract</span>Text...</div>`.
                  - `<div class="hierarchy-grid">`: Tree nodes `<div class="node"><span class="node-val">X</span><span class="node-lbl">Y</span></div>`.
                  - `<div class="content-cols">`: Detailed text analysis.
                  - `<div class="figure-box"><div class="chart-wrapper"><canvas id="analysisChart"></canvas></div><div class="figure-caption">Fig 1. Data Distribution</div></div>`.
                  - `<ul class="analysis-list">`: Detailed findings.
                """
                chart_script_instruction = """
                new Chart(document.getElementById('analysisChart'), {
                    type: 'mixed',
                    data: { labels: labels, datasets: [{ type: 'bar', label: 'Volume', data: values, backgroundColor: '#3498db' }, { type: 'line', label: 'Trend', data: values2, borderColor: '#2c3e50' }] },
                    options: { responsive: true, maintainAspectRatio: false }
                });
                """

            # 4. إعدادات العرض التقديمي
            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION_FULL
                html_wrapper_class = "slides-wrapper"
                prompt_instruction = """
                **Style: Interactive Presentation Slides (Reveal.js style).**
                - **Structure (Output multiple slides inside wrapper):**
                  - Slide 1: `<div class="slide cover"><div class="cover-content"><h1>Title</h1><h2>Subtitle</h2></div><div class="nav-hint">Scroll Down</div></div>`.
                  - Slide 2: `<div class="slide"><div class="slide-header"><div class="slide-title">Overview</div></div><div class="slide-body"><div class="text-column"><ul><li>Point 1</li><li>Point 2</li></ul></div><div class="visual-column"><div class="slide-chart-box"><canvas id="slideChart"></canvas></div></div></div></div>`.
                  - Slide 3: `<div class="slide">...Recommendations/Closing...</div>`.
                """
                chart_script_instruction = """
                new Chart(document.getElementById('slideChart'), {
                    type: 'doughnut',
                    data: { labels: labels, datasets: [{ data: values, backgroundColor: ['#c5a059', '#001f3f', '#fff', '#888'] }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { color: '#fff', font: { size: 16 } } } } }
                });
                """

            # 5. إعدادات الملخص التنفيذي
            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE_FULL
                html_wrapper_class = "exec-wrapper"
                prompt_instruction = """
                **Style: One-Page Executive Summary.**
                - **Tone:** Brief, high-impact, direct.
                - **Structure:**
                  - `<div class="exec-header"><div class="main-head"><h1>Title</h1></div><div class="sub-head"><span class="date-badge">CONFIDENTIAL</span></div></div>`.
                  - `<div class="takeaway-box">The main conclusion sentence...</div>`.
                  - `<div class="metrics-row">`: `<div class="m-item"><span class="m-val">X</span><span class="m-lbl">Y</span></div>` (3-4 items).
                  - `<div class="split-layout">`:
                    - `<div class="chart-area"><canvas id="execChart"></canvas></div>`.
                    - `<div class="action-list"><h3>Action Items</h3><div class="action-item"><span class="action-icon">➤</span>Text</div>...</div>`.
                """
                chart_script_instruction = """
                new Chart(document.getElementById('execChart'), {
                    type: 'bar',
                    indexAxis: 'y',
                    data: { labels: labels, datasets: [{ label: 'Impact', data: values, backgroundColor: '#FFD700' }] },
                    options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y' }
                });
                """

            # 🛑 الـ Prompt الموحد القوي (The Master Prompt)
            prompt = f"""
            You are an expert Data Analyst & Full-Stack Developer.
            **Objective:** Convert the provided text data into a FULL HTML Report based on the specific style requested.
            
            **Input Data:**
            {full_text}
            
            **INSTRUCTIONS:**
            1. **Content Processing:** Read the input thoroughly. Extract key metrics, dates, names, and strategic insights.
            2. **HTML Structure:** Generate the HTML Body contents based on the following style guide:
               {prompt_instruction}
            3. **INTERACTIVITY (Chart.js Injection):**
               - You MUST identify the most relevant dataset for visualization (e.g., Voting numbers, Budget, Progress).
               - Generate two Javascript arrays: `labels` (categories) and `values` (numbers).
               - AT THE VERY END of your response (after the HTML), add a `<script>` block.
               - Inside the script, define: `const labels = [...]; const values = [...];` based on your analysis.
               - Then, insert exactly this chart configuration code:
               {chart_script_instruction}
            
            **Output Constraints:**
            - Return ONLY valid HTML code to be placed inside the `<body>`.
            - Do NOT include `<html>`, `<head>`, or `<style>` tags (I have already injected them).
            - Do NOT use markdown blocks (```html).
            - Language: Arabic (Professional).
            """

            # شريط التقدم التفاعلي
            progress_placeholder = st.empty()
            steps = [
                "جاري قراءة وتحليل البيانات...",
                f"تطبيق القالب المختار: {report_type}...",
                "استخراج البيانات الرقمية للرسوم البيانية...",
                "توليد كود التقرير النهائي..."
            ]
            
            for i, step in enumerate(steps):
                p = (i + 1) * 25
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 10px;">⚡</div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {p}%;"></div></div>
                    <div style="color:white; font-size:1.1rem;">{step}</div>
                </div>''', unsafe_allow_html=True)
                time.sleep(0.5)
            
            # توليد المحتوى
            response = model.generate_content(prompt)
            html_body = clean_html_response(response.text)
            
            # تجميع الملف النهائي (حقن المكتبات + CSS + Body)
            final_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Report Output</title>
                <script src="[https://cdn.jsdelivr.net/npm/chart.js](https://cdn.jsdelivr.net/npm/chart.js)"></script>
                <link href="[https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css)" rel="stylesheet">
                {target_css}
            </head>
            <body>
                <div class="{html_wrapper_class}">
                    {html_body}
                </div>
                <div style="position:fixed; bottom:20px; left:20px; z-index:999;">
                    <button onclick="window.print()" style="background:#001f3f; color:white; border:none; padding:15px; border-radius:50%; cursor:pointer; box-shadow:0 5px 15px rgba(0,0,0,0.3); width:60px; height:60px; font-size:24px;">
                        <i class="fas fa-print"></i>
                    </button>
                </div>
            </body>
            </html>
            """
            
            progress_placeholder.empty()

            # عرض النتيجة
            st.markdown(f'''
            <div class="success-banner">
                <span style="font-size: 1.4rem;">✅ تم إنشاء التقرير بنجاح!</span><br>
                <span style="opacity:0.8">النمط: {report_type} | الحالة: تفاعلي</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.components.v1.html(final_html, height=900, scrolling=True)

            # زر التحميل
            st.download_button(
                label="📥 تحميل التقرير (HTML تفاعلي)",
                data=final_html,
                file_name=f"Report_{report_type.replace(' ', '_')}.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")

# ---------------------------------------------------------
# الفوتر (Footer)
# ---------------------------------------------------------
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
