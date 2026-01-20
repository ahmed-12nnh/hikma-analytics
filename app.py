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
# 🎨 CSS الأصلي للمنصة (للحفاظ على الهوية والتصميم 100%)
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
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 15px 40px rgba(218, 165, 32, 0.5),
            0 0 30px rgba(255, 215, 0, 0.3) !important;
        background-position: right center !important;
    }

    /* ===== شريط التقدم والنجاح ===== */
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🛠️ القالب الذكي (Smart HTML Template) - هذا للمخرجات فقط
# هذا الكود هو الذي سيولد التقرير الحديث والتفاعلي
# ---------------------------------------------------------

SMART_HTML_TEMPLATE = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #001f3f; --secondary: #c5a059; --bg: #f4f7f6; --text: #333;
            --card-bg: #ffffff; --card-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }
        
        /* === 🎨 ثيمات ديناميكية (تتغير حسب المحتوى) === */
        
        /* 1. الثيم الاستراتيجي (أزرق وذهبي - رسمي) */
        body.theme-strategic { --primary: #002b49; --secondary: #c5a059; --bg: #f8f9fa; } 
        body.theme-strategic header { background: linear-gradient(135deg, #002b49 0%, #001f35 100%); color: white; }
        body.theme-strategic .stat-card .value { color: #c5a059; }

        /* 2. ثيم الأزمات/التحذير (أحمر ورمادي - تنبيه) */
        body.theme-crisis { --primary: #2c3e50; --secondary: #e74c3c; --bg: #fff5f5; } 
        body.theme-crisis header { background: linear-gradient(135deg, #c0392b 0%, #8e44ad 100%); color: white; }
        body.theme-crisis .stat-card .value { color: #e74c3c; }

        /* 3. ثيم المال والنمو (أزرق سماوي وأخضر - إيجابي) */
        body.theme-financial { --primary: #004e89; --secondary: #27ae60; --bg: #f0f8ff; } 
        body.theme-financial header { background: linear-gradient(135deg, #004e89 0%, #00b4db 100%); color: white; }
        body.theme-financial .stat-card .value { color: #27ae60; }
        
        /* === الأساسيات === */
        body { font-family: 'Cairo', sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 0; direction: rtl; transition: background 0.5s; }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        
        /* الهيدر */
        header { padding: 60px 20px; text-align: center; border-radius: 0 0 30px 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 50px; position: relative; overflow: hidden; }
        header h1 { font-size: 3rem; font-weight: 900; margin: 0; font-family: 'Tajawal'; text-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        header .meta { margin-top: 15px; opacity: 0.9; font-size: 1.1rem; }
        
        /* البطاقات الإحصائية */
        .grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 25px; margin-bottom: 50px; }
        .stat-card { background: white; padding: 30px; border-radius: 20px; position: relative; overflow: hidden; box-shadow: var(--card-shadow); transition: transform 0.3s ease, box-shadow 0.3s ease; border-bottom: 5px solid var(--secondary); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
        .stat-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .stat-card .icon { font-size: 3rem; margin-bottom: 15px; color: var(--secondary); opacity: 0.2; position: absolute; top: 20px; right: 20px; }
        .stat-card h3 { margin: 0 0 10px 0; color: #777; font-size: 1rem; font-weight: 600; }
        .stat-card .value { font-size: 2.5rem; font-weight: 800; font-family: 'Tajawal'; z-index: 1; }

        /* الأقسام والمحتوى */
        .content-section { background: white; border-radius: 20px; padding: 40px; margin-bottom: 30px; box-shadow: var(--card-shadow); border: 1px solid rgba(0,0,0,0.02); }
        .section-header { display: flex; align-items: center; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 2px solid #f0f0f0; }
        .section-header i { font-size: 1.5rem; color: var(--secondary); margin-left: 15px; background: rgba(0,0,0,0.03); padding: 12px; border-radius: 12px; }
        .section-header h2 { margin: 0; color: var(--primary); font-size: 1.8rem; font-family: 'Tajawal'; }
        
        p { line-height: 1.9; font-size: 1.1rem; color: #555; margin-bottom: 20px; text-align: justify; }

        /* الجداول الحديثة */
        .table-responsive { overflow-x: auto; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.03); }
        table { width: 100%; border-collapse: collapse; background: white; }
        th { background: var(--primary); color: white; padding: 18px; font-family: 'Tajawal'; text-align: center; white-space: nowrap; }
        td { padding: 15px; border-bottom: 1px solid #eee; text-align: center; font-weight: 500; color: #444; }
        tr:hover td { background-color: #f9f9f9; }

        /* منطقة الرسم البياني */
        .chart-container { position: relative; height: 400px; width: 100%; margin: 20px 0; }

        /* قائمة التوصيات */
        .rec-list { list-style: none; padding: 0; counter-reset: rec-counter; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .rec-item { background: #f8f9fa; padding: 20px; border-radius: 15px; position: relative; border-right: 4px solid var(--secondary); transition: 0.3s; }
        .rec-item:hover { background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); transform: translateY(-3px); }
        .rec-item::before { counter-increment: rec-counter; content: counter(rec-counter); position: absolute; left: 20px; top: 20px; font-size: 2rem; font-weight: 900; color: rgba(0,0,0,0.05); font-family: 'Tajawal'; }
        .rec-item h4 { margin: 0 0 10px 0; color: var(--primary); font-size: 1.1rem; }
        .rec-item p { margin: 0; font-size: 0.95rem; line-height: 1.6; }

        /* الفوتر وزر الطباعة */
        .footer { text-align: center; margin-top: 50px; padding: 30px; color: #888; font-size: 0.9rem; border-top: 1px solid #ddd; }
        .print-fab { position: fixed; bottom: 30px; left: 30px; width: 60px; height: 60px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: 0.3s; z-index: 1000; border: none; }
        .print-fab:hover { transform: scale(1.1) rotate(15deg); background: var(--secondary); }
        
        @media print { .print-fab { display: none; } header { box-shadow: none; border-radius: 0; } body { background: white; } }
    </style>
</head>
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
    return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ بناء الواجهة (نفس الهيكلية الأصلية بالضبط)
# ---------------------------------------------------------

# الهيدر الرئيسي
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

# منطقة الإدخال (نفس التقسيم الأصلي)
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
# 🚀 المعالجة الذكية (هنا التغيير الوحيد: المحرك فقط)
# ---------------------------------------------------------
if st.button("🚀 بدء المعالجة وإنشاء التقرير"):
    
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

            # 🧠 الـ Prompt المطور (توليد HTML فقط + تفاعلية)
            prompt = f"""
            You are an elite Data Analyst & Web Developer.
            **Objective:** Create a **standalone, modern, interactive HTML report** based on the input text.
            
            **Input Data:**
            {full_text}
            
            **INSTRUCTIONS:**
            1. **Analyze the Content Tone:**
               - Strategic/General -> Use class `theme-strategic`
               - Crisis/Warning -> Use class `theme-crisis`
               - Financial/Growth -> Use class `theme-financial`
               *Decide the class and apply it to the `<body>` tag.*

            2. **Structure (Generate HTML Body Content ONLY):**
               - **Header:** `<header><h1>Title</h1><div class="meta">Subtitle/Date</div></header>`
               - **Key Stats:** Extract 3-4 key numbers. Use `<div class="grid-cards">`. Each card: `<div class="stat-card"><div class="icon"><i class="fas fa-layer-group"></i></div><h3>Label</h3><div class="value">Number</div></div>`.
               - **Main Sections:** Use `<div class="content-section">`. Header: `<div class="section-header"><i class="fas fa-file-alt"></i><h2>Title</h2></div>`. Text inside `<p>`.
               - **Tables:** If data fits a table, create a `<div class="table-responsive"><table>...</table></div>`.
               - **Recommendations:** Use `<ul class="rec-list">`. Item: `<li class="rec-item"><h4>Title</h4><p>Details</p></li>`.
               
            3. **INTERACTIVITY (The Chart):**
               - Identify the main dataset suitable for a chart (e.g., votes, budget, progress).
               - Create a canvas container: `<div class="content-section"><div class="section-header"><i class="fas fa-chart-pie"></i><h2>التحليل البياني التفاعلي</h2></div><div class="chart-container"><canvas id="mainChart"></canvas></div></div>`.
               - **AT THE END of the HTML**, write a `<script>` block.
               - Inside the script, initialize `new Chart(...)`. Select the best type (bar, line, doughnut) for the data. Use colors compatible with the chosen theme.

            **Output Requirement:**
            - Output ONLY the HTML code starting from `<body class="...">`.
            - Do NOT include `<html>` or `<head>` tags (I have them ready).
            - Do NOT wrap in markdown blocks.
            - Language: Arabic.
            """

            # شريط التقدم (نفس تصميمك الأصلي)
            progress_placeholder = st.empty()
            for i in range(0, 101, 10):
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🤖</div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {i}%;"></div>
                    </div>
                    <div class="progress-text">جاري تحليل البيانات وتوليد المخططات التفاعلية... {i}%</div>
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(0.05)
            
            # توليد المحتوى
            response = model.generate_content(prompt)
            html_body = clean_html_response(response.text)
            
            # تجميع الملف النهائي (Header + Body + Footer)
            final_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            {SMART_HTML_TEMPLATE}
            {html_body}
            <button class="print-fab" onclick="window.print()" title="طباعة / PDF"><i class="fas fa-print"></i></button>
            <div class="footer">صادر عن الجهاز المركزي للجودة الشاملة - وحدة التخطيط الاستراتيجي © 2026</div>
            </html>
            """
            
            progress_placeholder.empty()
            
            # عرض النتيجة والتحميل
            st.markdown('''
            <div class="success-banner">
                <span>✅ تم إنشاء التقرير التفاعلي بنجاح!</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.components.v1.html(final_html, height=850, scrolling=True)

            st.download_button(
                label="📥 تحميل التقرير (HTML تفاعلي)",
                data=final_html,
                file_name="Smart_Report.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")

# الفوتر الأصلي للمنصة
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
