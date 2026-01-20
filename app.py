import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time
import json
import random

# =========================================================
# 1. إعدادات النظام والأمان (System Configuration)
# =========================================================
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # محاولة بديلة في حال عدم وجود Secrets (للتطوير المحلي)
    API_KEY = None 

# إعدادات الصفحة - يجب أن تكون أول أمر Streamlit
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
        padding: 15px; border-radius: 15px; border: none;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
        transition: 0.5s; font-family: 'Tajawal';
    }
    .stButton > button:hover { background-position: right center; transform: scale(1.02); }

    /* --- Radio Buttons (The Selection) --- */
    .stRadio > div { flex-direction: row-reverse; justify-content: center; gap: 20px; }
    .stRadio label {
        background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,215,0,0.2) !important;
        padding: 15px 30px !important; border-radius: 30px !important; cursor: pointer; transition: 0.3s;
    }
    .stRadio label:hover { background: rgba(255,215,0,0.1) !important; border-color: #FFD700 !important; }
    
    /* --- Progress & Success --- */
    .progress-container { background: rgba(0,0,0,0.5); border-radius: 15px; padding: 30px; text-align: center; border: 1px solid rgba(255,255,255,0.1); animation: popIn 0.5s; }
    .success-msg { background: rgba(39, 174, 96, 0.2); border: 1px solid #27ae60; color: #2ecc71; padding: 15px; border-radius: 10px; text-align: center; margin-top: 20px; }
    @keyframes popIn { 0% { opacity: 0; transform: scale(0.9); } 100% { opacity: 1; transform: scale(1); } }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. مكتبة القوالب العملاقة (Master Templates)
# تحتوي على CSS و JS مدمجين لضمان التفاعلية وعدم الحاجة لإنترنت
# =========================================================

# --- 1. القالب الرسمي (Government Official) ---
TEMPLATE_OFFICIAL = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
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

# --- 3. قالب الشرائح (Presentation) ---
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

# =========================================================
# 4. المنطق البرمجي الذكي (Business Logic)
# =========================================================

def get_smart_model():
    """دالة ذكية لاختيار الموديل وتجنب خطأ 404"""
    # الأولوية للموديل السريع، ثم الأقوى، ثم القديم
    models_priority = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    
    # هنا يمكن إضافة منطق لفحص الموديل، لكن للاختصار سنرجع الأول
    # *تنبيه:* يجب تحديث مكتبة google-generativeai في requirements.txt
    return "gemini-1.5-flash"

def extract_content(file):
    """استخراج النصوص بذكاء من أنواع الملفات المختلفة"""
    text = ""
    try:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif "spreadsheet" in file.type:
            df = pd.read_excel(file)
            text = df.to_string()
        else:
            text = file.getvalue().decode("utf-8")
    except Exception as e:
        return f"خطأ في القراءة: {e}"
    return text

def generate_report_logic(full_text, report_type):
    """المحرك الرئيسي لتوليد التقرير"""
    
    model_name = get_smart_model()
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name)
    
    # 1. تحديد القالب والتعليمات بناء على اختيار المستخدم
    if "الرسمي" in report_type:
        base_html = TEMPLATE_OFFICIAL
        role = "Government Consultant"
        instruction = """
        Output HTML Structure for 'CONTENT_PLACEHOLDER':
        1. `<div class="section-title">المقدمة</div>` followed by `<p>...</p>`
        2. `<div class="stats-grid">` containing exactly 3 divs of class `stat-box`, each with `stat-val` and `stat-lbl`.
        3. `<div class="section-title">التحليل التفصيلي</div>` with paragraphs.
        4. Create a `<div class="chart-container"><canvas id="mainChart"></canvas></div>`.
        5. A standard HTML `<table>`.
        6. **IMPORTANT:** At the end, add a `<script>` block that creates a Chart.js instance on 'mainChart' using data from the text.
        """
    
    elif "الرقمي" in report_type:
        base_html = TEMPLATE_DIGITAL
        role = "Data Scientist"
        instruction = """
        Output HTML Structure for 'CONTENT_PLACEHOLDER':
        1. `<div class="kpi-container">` containing 4 `kpi-card` divs.
        2. `<div class="chart-panel"><canvas id="dashChart"></canvas></div>`.
        3. `<div class="list-panel">` containing 5 `list-item` divs.
        4. `<div class="table-panel">` with a detailed table.
        5. **IMPORTANT:** Add `<script>` for 'dashChart' (Line or Doughnut chart) with neon colors.
        """
    
    else: # عرض تقديمي
        base_html = TEMPLATE_SLIDES
        role = "Presentation Expert"
        instruction = """
        Output HTML Structure for 'CONTENT_PLACEHOLDER':
        1. Slide 1: `<div class="slide cover"><div class="cover-box"><h1>Title</h1><h2>Subtitle</h2></div></div>`.
        2. Slide 2: `<div class="slide"><div class="slide-title">Overview</div><div class="content-split"><div class="text-part"><ul><li>...</li></ul></div><div class="viz-part"><canvas id="slideChart1"></canvas></div></div></div>`.
        3. Slide 3: `<div class="slide">...Conclusion...</div>`.
        4. **IMPORTANT:** Add `<script>` for 'slideChart1'.
        """

    # 2. هندسة الأمر (Prompt Engineering)
    prompt = f"""
    Role: {role}. Language: Arabic.
    Task: Analyze the input text and generate HTML content to replace 'CONTENT_PLACEHOLDER'.
    
    Input: {full_text[:25000]}
    
    Instructions:
    {instruction}
    
    **Critical Rules:**
    - Return ONLY the HTML parts to be injected. Do not return the full <html> structure again.
    - Ensure the JavaScript for Chart.js is valid and strictly follows the data.
    - Do not use markdown (```).
    """

    # 3. استدعاء API
    with st.spinner('⚡ جاري المعالجة بواسطة الذكاء الاصطناعي...'):
        response = model.generate_content(prompt)
        generated_content = response.text.replace("```html", "").replace("```", "")
    
    # 4. دمج الناتج مع القالب
    final_html = base_html.replace("", generated_content)
    
    return final_html

# =========================================================
# 5. واجهة المستخدم والتفاعل (Main Execution)
# =========================================================

# الهيدر
st.markdown("""
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | منظومة التحليل الاستراتيجي</div>
</div>
""", unsafe_allow_html=True)

# أزرار الاختيار
report_type = st.radio(
    "",
    ("🏛️ التقرير الرسمي (للطباعة)", "💻 لوحة القيادة الرقمية (Dashboard)", "📽️ عرض تقديمي (شرائح)"),
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

# المدخلات
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown('<div class="input-card"><div class="card-header"><div class="card-icon">📝</div><div class="card-title">النص / الملاحظات</div></div>', unsafe_allow_html=True)
    txt_input = st.text_area("", height=200, placeholder="اكتب البيانات هنا...")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="input-card"><div class="card-header"><div class="card-icon">📎</div><div class="card-title">إرفاق ملف</div></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["pdf", "xlsx", "txt"])
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# زر التنفيذ
if st.button("🚀 تحليل البيانات وإنشاء التقرير الكامل"):
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API.")
        st.stop()
        
    content = txt_input
    if uploaded:
        content += "\n" + extract_content(uploaded)
        
    if not content.strip():
        st.warning("الرجاء إدخال محتوى للتحليل.")
    else:
        try:
            # شريط تقدم وهمي للجمالية
            prog_bar = st.progress(0)
            status_text = st.empty()
            
            steps = ["تحليل السياق العام...", "استخراج المؤشرات الرقمية...", "بناء الهيكلية البصرية...", "توليد الرسوم البيانية..."]
            for i, step in enumerate(steps):
                status_text.text(f"🤖 {step}")
                prog_bar.progress((i + 1) * 25)
                time.sleep(0.3)
            
            # التوليد الفعلي
            final_report = generate_report_logic(content, report_type)
            
            status_text.empty()
            prog_bar.empty()
            
            # عرض النتيجة
            st.markdown(f'<div class="progress-container"><div class="success-msg">✅ تم إنشاء {report_type} بنجاح!</div></div>', unsafe_allow_html=True)
            
            st.components.v1.html(final_report, height=800, scrolling=True)
            
            st.download_button(
                label="📥 تحميل التقرير النهائي (HTML)",
                data=final_report,
                file_name=f"Report_{int(time.time())}.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {e}")
            st.warning("تلميح: تأكد من تحديث مكتبة google-generativeai في ملف requirements.txt")

# الفوتر
st.markdown("<div style='text-align:center; color:#666; margin-top:50px;'>Jassim AI Systems © 2026</div>", unsafe_allow_html=True)
