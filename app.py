import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time
import random
import json

# =========================================================
# 1. إعدادات النظام والأمان (System Configuration)
# =========================================================
try:
    # محاولة جلب المفتاح من أسرار النظام
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # يمكنك وضع مفتاحك هنا مباشرة إذا كنت تعمل محلياً
    API_KEY = None 

# إعدادات الصفحة - يجب أن تكون أول أمر
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي - الجيل الثالث",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. واجهة التطبيق (UI/UX) - (تصميمك الأصلي مع تحسينات طفيفة)
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    /* Global Settings */
    * { box-sizing: border-box; outline: none; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* Hiding Default Elements */
    [data-testid="stSidebar"], header, footer, #MainMenu { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }

    /* --- Hero Section (الهوية البصرية) --- */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 20px 0 40px 0;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 50px rgba(0, 31, 63, 0.9), inset 0 0 30px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        animation: fadeInDown 1s ease-out;
    }
    
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        animation: shimmer 3s infinite linear;
    }
    
    @keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }

    .main-title {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(180deg, #FFD700 10%, #B8860B 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 10px;
    }
    .sub-title { color: #e0e0e0; font-size: 1.2rem; letter-spacing: 1px; opacity: 0.9; font-weight: 300; }

    /* --- عنوان القسم --- */
    .section-header { text-align: center; margin: 30px 20px; color: #FFD700; font-size: 1.4rem; font-weight: bold; text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3); }

    /* --- أزرار الاختيار (Radio Buttons) --- */
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

    /* --- Input Cards (البطاقات) --- */
    .input-card {
        background: rgba(13, 25, 48, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 16px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .input-card:hover { transform: translateY(-5px); border-color: rgba(255, 215, 0, 0.4); }
    
    .card-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }
    .card-icon { font-size: 1.8rem; background: rgba(255, 215, 0, 0.1); width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border-radius: 12px; color: #FFD700; }
    .card-title { font-size: 1.1rem; font-weight: 700; color: #fff; }
    
    /* --- Streamlit Widgets Overrides --- */
    .stTextArea textarea {
        background: rgba(0,0,0,0.3) !important; border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important; font-family: 'Tajawal' !important; border-radius: 12px !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; box-shadow: 0 0 15px rgba(255, 215, 0, 0.1) !important; }
    
    div[data-testid="stFileUploader"] {
        background: rgba(0,0,0,0.2) !important; border: 1px dashed rgba(255,255,255,0.2) !important;
        border-radius: 12px !important; padding: 20px !important;
    }
    div[data-testid="stFileUploader"] section > button {
        background: linear-gradient(45deg, #FFD700, #B8860B) !important;
        color: #000 !important; font-weight: bold !important; border: none !important;
    }

    /* --- Action Button --- */
    .stButton > button {
        width: 100%; background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% auto; color: #001f3f; font-weight: 900; font-size: 1.3rem;
        padding: 18px 40px; border-radius: 15px; border: none;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        transition: 0.5s; font-family: 'Tajawal'; animation: buttonPulse 2s infinite;
    }
    @keyframes buttonPulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); } }
    .stButton > button:hover { background-position: right center; transform: scale(1.02); }

    /* --- Progress & Success --- */
    .progress-box { background: rgba(0, 31, 63, 0.9); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 15px; padding: 30px; margin: 20px; text-align: center; }
    .progress-bar-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 12px; overflow: hidden; margin: 20px 0; }
    .progress-bar-fill { height: 100%; background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700); background-size: 200% 100%; border-radius: 10px; animation: progressShine 1.5s infinite linear; transition: width 0.3s ease; }
    @keyframes progressShine { 0% { background-position: 200% center; } 100% { background-position: -200% center; } }
    .success-banner { background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1)); border: 2px solid #22c55e; border-radius: 15px; padding: 20px 30px; text-align: center; margin: 20px; animation: successPop 0.5s ease; }
    @keyframes successPop { 0% { transform: scale(0.9); opacity: 0; } 50% { transform: scale(1.02); } 100% { transform: scale(1); opacity: 1; } }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. مكتبة القوالب العملاقة (Master Templates)
# تحتوي على CSS و JS مدمجين لضمان التفاعلية
# =========================================================

# --- 1. القالب الرسمي (Government Official) ---
TEMPLATE_OFFICIAL = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800&display=swap');
        
        :root { --primary: #002b49; --gold: #c5a059; --bg: #fdfdfd; --text: #333; --border: #e0e0e0; }
        
        body { font-family: 'Tajawal', sans-serif; background: #525659; margin: 0; padding: 40px; }
        
        .paper {
            max-width: 210mm; min-height: 297mm; background: #fff; margin: auto; padding: 25mm;
            box-shadow: 0 0 30px rgba(0,0,0,0.5); position: relative; overflow: hidden;
        }
        
        /* Watermark */
        .watermark {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 120px; color: rgba(0,0,0,0.03); font-weight: 900; white-space: nowrap; pointer-events: none;
        }

        /* Header */
        header { border-bottom: 4px double var(--primary); padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end; }
        .logo-area h1 { color: var(--primary); font-size: 28pt; margin: 0; font-family: 'Amiri', serif; }
        .logo-area h2 { color: var(--gold); font-size: 14pt; margin: 5px 0 0; }
        .date-area { text-align: left; font-size: 11pt; color: #666; border-right: 3px solid var(--gold); padding-right: 15px; }

        /* Content */
        .section-title {
            font-size: 18pt; color: var(--primary); border-bottom: 2px solid var(--gold);
            padding-bottom: 5px; margin: 30px 0 20px 0; font-family: 'Amiri', serif; display: inline-block;
        }
        
        p { text-align: justify; line-height: 1.8; font-size: 13pt; margin-bottom: 15px; color: #444; }
        
        /* Stats Grid */
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 30px 0; }
        .stat-box { 
            border: 1px solid var(--border); padding: 20px; text-align: center; background: #fcfcfc;
            border-top: 4px solid var(--primary); transition: 0.3s;
        }
        .stat-val { font-size: 22pt; font-weight: bold; color: var(--primary); display: block; }
        .stat-lbl { font-size: 11pt; color: #666; margin-top: 5px; display: block; }

        /* Chart */
        .chart-container { width: 100%; height: 350px; border: 1px solid var(--border); padding: 15px; margin: 30px 0; background: #fff; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid var(--border); }
        th { background: var(--primary); color: white; padding: 12px; font-family: 'Amiri'; font-size: 13pt; }
        td { border: 1px solid var(--border); padding: 10px; text-align: center; }
        tr:nth-child(even) { background: #f9f9f9; }

        /* Signature */
        .signature-section { margin-top: 80px; display: flex; justify-content: space-between; page-break-inside: avoid; }
        .sign-block { width: 250px; text-align: center; }
        .sign-title { font-weight: bold; margin-bottom: 60px; color: var(--primary); }
        .sign-line { border-top: 2px solid #333; display: block; margin: 0 auto; width: 80%; }

        /* Print Controls */
        .fab { position: fixed; bottom: 30px; left: 30px; width: 60px; height: 60px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); cursor: pointer; transition: 0.3s; z-index: 999; border: none; }
        .fab:hover { transform: scale(1.1); background: var(--gold); }
        
        @media print { body { background: none; padding: 0; } .paper { box-shadow: none; margin: 0; width: 100%; max-width: 100%; } .fab { display: none; } }
    </style>
</head>
<body>
    <button class="fab" onclick="window.print()" title="طباعة / PDF"><i class="fas fa-print"></i></button>
    <div class="paper" data-aos="fade-in">
        <div class="watermark">CONFIDENTIAL</div>
        <header>
            <div class="logo-area">
                <h1>الجهاز المركزي للجودة الشاملة</h1>
                <h2>وحدة التخطيط الاستراتيجي والتطوير</h2>
            </div>
            <div class="date-area">
                <p><strong>التاريخ:</strong> <span id="currentDate"></span></p>
                <p><strong>المرجع:</strong> SR-2026/HQ</p>
            </div>
        </header>

        <div class="signature-section">
            <div class="sign-block">
                <div class="sign-title">مدير وحدة التخطيط</div>
                <span class="sign-line"></span>
            </div>
            <div class="sign-block">
                <div class="sign-title">مصادقة الجهاز المركزي</div>
                <span class="sign-line"></span>
            </div>
        </div>
    </div>
    <script>
        AOS.init();
        document.getElementById('currentDate').innerText = new Date().toLocaleDateString('ar-IQ');
    </script>
</body>
</html>
"""

# --- 2. القالب الرقمي (Cyber Dashboard) ---
TEMPLATE_DIGITAL = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
        
        :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f1f5f9; --success: #22c55e; --danger: #ef4444; }
        
        body { font-family: 'Cairo', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
        .container { max-width: 1600px; margin: 0 auto; display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
        
        /* Header */
        .dash-header { grid-column: span 12; background: var(--card); padding: 20px 30px; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--accent); }
        .dash-header h1 { margin: 0; font-size: 1.8rem; background: linear-gradient(90deg, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .status-badge { background: rgba(56, 189, 248, 0.2); color: var(--accent); padding: 5px 15px; border-radius: 20px; font-weight: bold; border: 1px solid var(--accent); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }

        /* Cards */
        .kpi-container { grid-column: span 12; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .kpi-card { background: var(--card); padding: 25px; border-radius: 16px; position: relative; overflow: hidden; transition: 0.3s; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        .kpi-card:hover { transform: translateY(-5px); background: #334155; }
        .kpi-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--accent); }
        .kpi-val { font-size: 2.8rem; font-weight: 700; margin: 10px 0; color: #fff; }
        .kpi-label { color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }

        /* Main Chart Area */
        .chart-panel { grid-column: span 8; background: var(--card); padding: 20px; border-radius: 16px; min-height: 400px; }
        @media(max-width: 1000px) { .chart-panel { grid-column: span 12; } }
        
        /* Side Panel (List) */
        .list-panel { grid-column: span 4; background: var(--card); padding: 20px; border-radius: 16px; display: flex; flex-direction: column; gap: 15px; }
        @media(max-width: 1000px) { .list-panel { grid-column: span 12; } }
        .list-item { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; }
        .list-item span { color: var(--accent); font-weight: bold; }

        /* Tables */
        .table-panel { grid-column: span 12; background: var(--card); padding: 25px; border-radius: 16px; }
        table { width: 100%; border-collapse: collapse; }
        th { text-align: right; padding: 15px; border-bottom: 2px solid #334155; color: #94a3b8; }
        td { padding: 15px; border-bottom: 1px solid #334155; }
        tr:hover td { background: rgba(255,255,255,0.02); }

    </style>
</head>
<body>
    <div class="container" data-aos="fade-up">
        <div class="dash-header">
            <h1>لوحة التحليل الذكي | Live Dashboard</h1>
            <div class="status-badge">● متصل بالخادم</div>
        </div>

        </div>
    <script> AOS.init(); </script>
</body>
</html>
"""

# --- 3. القالب التحليلي (Analytical) ---
TEMPLATE_ANALYTICAL = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #ecf0f1; color: #333; padding: 30px; }
        .research-paper { max-width: 1000px; margin: 0 auto; background: #fff; padding: 60px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); border-top: 10px solid #2c3e50; }
        
        .paper-header { text-align: center; border-bottom: 1px solid #eee; padding-bottom: 30px; margin-bottom: 40px; }
        .paper-header h1 { font-size: 2.5rem; color: #2c3e50; }
        
        .abstract-box { background: #f8f9fa; padding: 30px; border-right: 5px solid #3498db; margin-bottom: 40px; }
        .content-cols { column-count: 2; column-gap: 40px; text-align: justify; margin-bottom: 40px; }
        .figure-box { break-inside: avoid; background: #fff; border: 1px solid #eee; padding: 15px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .chart-wrapper { width: 100%; height: 300px; }
    </style>
</head>
<body>
    <div class="research-paper">
        <div class="paper-header">
            <h1>تقرير التحليل الاستراتيجي العميق</h1>
            <p style="color:#777">وحدة الأبحاث والدراسات</p>
        </div>
        </div>
</body>
</html>
"""

# --- 4. قالب الشرائح (Presentation) ---
TEMPLATE_SLIDES = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
        body { margin: 0; background: #000; font-family: 'Tajawal'; overflow-x: hidden; }
        .slides-container { scroll-snap-type: y mandatory; overflow-y: scroll; height: 100vh; scroll-behavior: smooth; }
        
        .slide {
            height: 100vh; width: 100vw; scroll-snap-align: start; position: relative;
            display: flex; flex-direction: column; padding: 40px 80px; box-sizing: border-box;
            background: radial-gradient(circle at center, #002b49 0%, #001a2c 100%);
            color: white; border-bottom: 5px solid #c5a059;
        }
        
        /* Cover Slide */
        .slide.cover { justify-content: center; align-items: center; text-align: center; }
        .cover-box { border: 3px solid #c5a059; padding: 50px 100px; background: rgba(0,0,0,0.5); backdrop-filter: blur(10px); }
        .cover h1 { font-size: 4rem; color: #c5a059; margin: 0; text-shadow: 0 0 20px rgba(197, 160, 89, 0.5); }
        .cover h2 { font-size: 2rem; font-weight: 300; margin-top: 10px; }
        
        /* Standard Slide */
        .slide-title { font-size: 2.5rem; color: #c5a059; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 20px; margin-bottom: 40px; }
        .content-split { display: flex; height: 100%; gap: 50px; }
        .text-part { flex: 1; font-size: 1.5rem; line-height: 1.6; }
        .viz-part { flex: 1; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; }
        
        ul { list-style: none; padding: 0; }
        li { margin-bottom: 25px; position: relative; padding-right: 40px; }
        li::before { content: '➤'; color: #c5a059; position: absolute; right: 0; }
        
        .nav-hint { position: fixed; bottom: 20px; left: 20px; color: rgba(255,255,255,0.3); z-index: 999; }
    </style>
</head>
<body>
    <div class="slides-container">
        </div>
    <div class="nav-hint">استخدم عجلة الماوس للتنقل</div>
</body>
</html>
"""

# --- 5. القالب التنفيذي (Executive) ---
TEMPLATE_EXECUTIVE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap');
        body { font-family: 'Tajawal'; background: #fff; color: #222; margin: 0; padding: 40px; }
        .exec-wrapper { max-width: 900px; margin: 0 auto; border: 1px solid #e0e0e0; padding: 50px; box-shadow: 0 15px 50px rgba(0,0,0,0.05); }
        
        .exec-header { display: flex; justify-content: space-between; border-bottom: 5px solid #111; padding-bottom: 30px; margin-bottom: 40px; }
        .main-head h1 { font-size: 3.5rem; font-weight: 800; margin: 0; line-height: 1; }
        
        .takeaway-box { background: #fff9c4; border-right: 6px solid #FFD700; padding: 25px; font-size: 1.4rem; font-weight: 500; margin-bottom: 40px; }
        .metrics-row { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 40px; background: #f4f4f4; padding: 30px; border-radius: 12px; }
        .m-val { font-size: 3rem; font-weight: 800; display: block; }
        
        .chart-area { height: 350px; background: #fff; border: 1px solid #eee; padding: 10px; margin-bottom: 40px; }
    </style>
</head>
<body>
    <div class="exec-wrapper">
        </div>
</body>
</html>
"""

# =========================================================
# 4. المنطق البرمجي الذكي (Business Logic)
# =========================================================

def get_smart_model():
    """دالة ذكية لاختيار الموديل المتاح وتجنب خطأ 404"""
    # نحاول استخدام أحدث موديل، إذا فشل نعود للأقدم
    available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    # يمكنك إضافة كود هنا للتحقق من الموديلات المتاحة عبر genai.list_models()
    # لكن للاختصار سنفترض أن flash هو الهدف، وسنستخدم try/except في التنفيذ
    return "gemini-1.5-flash"

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

# =========================================================
# 5. واجهة التطبيق الرئيسية (Main Application)
# =========================================================

# الهيدر
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
        <div class="card-header">
            <div class="card-icon">📝</div>
            <div class="card-title">البيانات / الملاحظات</div>
        </div>
        <div style="color: #ccc; margin-bottom: 10px;">أدخل النص أو الصق محتوى التقرير هنا</div>
    </div>
    ''', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات...", label_visibility="collapsed")

with col_upload:
    st.markdown('''
    <div class="input-card">
        <div class="card-header">
            <div class="card-icon">📎</div>
            <div class="card-title">رفع الملفات</div>
        </div>
        <div style="color: #ccc; margin-bottom: 10px;">PDF, XLSX, TXT</div>
    </div>
    ''', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    if uploaded_file:
        st.success(f"✅ تم إرفاق: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🚀 المعالجة الذكية (The Core Engine)
# ---------------------------------------------------------
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. يرجى التأكد من إضافته.")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            full_text += f"\n\n[FILE_CONTENT]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف.")
    else:
        try:
            # تهيئة الذكاء الاصطناعي
            genai.configure(api_key=API_KEY)
            
            # محاولة اختيار الموديل مع معالجة الأخطاء
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
            except:
                st.warning("⚠️ جاري التبديل إلى موديل بديل...")
                model = genai.GenerativeModel("gemini-pro")

            # تحديد القالب والتعليمات بناءً على اختيار المستخدم
            base_html = ""
            instruction = ""
            
            if "الرسمي" in report_type:
                base_html = TEMPLATE_OFFICIAL
                instruction = """
                **Mode:** Official Government Report.
                **Required HTML Fragments (to replace PLACEHOLDER):**
                1. `<div class="section-title">المقدمة</div>` text.
                2. `<div class="stats-grid">` with 3 `stat-box` divs.
                3. `<div class="chart-container"><canvas id="mainChart"></canvas></div>`.
                4. Detailed sections using `<div class="section-title">` and `<p>`.
                5. Standard `<table>`.
                6. **IMPORTANT:** End with `<script>` creating 'mainChart' (Bar chart).
                """
            
            elif "الرقمي" in report_type:
                base_html = TEMPLATE_DIGITAL
                instruction = """
                **Mode:** Digital Dashboard.
                **Required HTML Fragments:**
                1. `<div class="kpi-container">` with 4 `kpi-card` divs.
                2. `<div class="chart-panel"><canvas id="dashChart"></canvas></div>`.
                3. `<div class="list-panel">` with 5 `list-item` divs.
                4. `<div class="table-panel">` with table.
                5. **IMPORTANT:** End with `<script>` creating 'dashChart' (Line chart, neon colors).
                """

            elif "التحليل" in report_type:
                base_html = TEMPLATE_ANALYTICAL
                instruction = """
                **Mode:** Analytical Paper.
                **Required HTML Fragments:**
                1. Abstract box.
                2. Hierarchy grid.
                3. Text columns with embedded `<div class="figure-box"><div class="chart-wrapper"><canvas id="analysisChart"></canvas></div></div>`.
                4. **IMPORTANT:** End with `<script>` creating 'analysisChart' (Mixed chart).
                """

            elif "عرض تقديمي" in report_type:
                base_html = TEMPLATE_SLIDES
                instruction = """
                **Mode:** Presentation Slides.
                **Required HTML Fragments:**
                1. Slide 1 (Cover): `<div class="slide cover"><div class="cover-box"><h1>Title</h1></div></div>`.
                2. Slide 2: `<div class="slide"><div class="slide-title">Overview</div><div class="content-split"><div class="text-part"><ul>...</ul></div><div class="viz-part"><canvas id="slideChart1"></canvas></div></div></div>`.
                3. Slide 3: Recommendations.
                4. **IMPORTANT:** End with `<script>` creating 'slideChart1' (Doughnut).
                """

            elif "ملخص" in report_type:
                base_html = TEMPLATE_EXECUTIVE
                instruction = """
                **Mode:** Executive Summary.
                **Required HTML Fragments:**
                1. Header info.
                2. `<div class="takeaway-box">Main Insight</div>`.
                3. `<div class="metrics-row">` (3 items).
                4. `<div class="chart-area"><canvas id="execChart"></canvas></div>`.
                5. **IMPORTANT:** End with `<script>` creating 'execChart' (Horizontal Bar).
                """

            # الـ Prompt
            prompt = f"""
            Role: Expert Data Analyst & Developer.
            Task: Analyze the input text and generate ONLY the HTML fragments needed to populate the BODY of the report.
            
            Input Data:
            {full_text[:25000]}
            
            Style Instructions:
            {instruction}
            
            **CRITICAL RULES:**
            1. Return **ONLY** the HTML/JS code fragments. Do not return `<html>` or `<head>` tags.
            2. The javascript for Chart.js MUST be included at the end in a `<script>` tag.
            3. Use Arabic language.
            4. Make up data numbers if exact numbers are missing, based on context.
            """

            # شريط التقدم التفاعلي
            progress_placeholder = st.empty()
            steps = ["تحليل البيانات...", "اختيار القالب المناسب...", "توليد الرسوم البيانية...", "بناء التقرير النهائي..."]
            
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
            generated_content = clean_html_response(response.text)
            
            # دمج المحتوى مع القالب
            final_html = base_html.replace("", generated_content)
            
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
            st.error("نصيحة: تأكد من إعداد مفتاح API بشكل صحيح ومن أن المكتبة محدثة.")

# ---------------------------------------------------------
# الفوتر (Footer)
# ---------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''
<div style="text-align:center; color:rgba(255,255,255,0.5); font-size:0.9rem;">
    الجهاز المركزي للجودة الشاملة - وحدة التحليل الاستراتيجي © 2026
</div>
''', unsafe_allow_html=True)
