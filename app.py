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
    page_title="منصة التحليل الاستراتيجي - الجيل الجديد",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 🎨 CSS واجهة التطبيق (Streamlit UI)
# حافظنا على التصميم الخارجي كما هو لأنه يعبر عن الهوية
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * { box-sizing: border-box; }
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    
    /* الهيدر الرئيسي */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.8), inset 0 0 30px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    /* الخط الذهبي المتوهج */
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }

    .main-title {
        font-size: 48px; font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .sub-title { color: #e0e0e0; font-size: 18px; letter-spacing: 1px; margin-top: 10px; opacity: 0.9; }

    /* بطاقات الإدخال */
    .input-card {
        background: rgba(0, 31, 63, 0.6);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 15px; padding: 20px;
        transition: transform 0.3s;
    }
    .input-card:hover { transform: translateY(-5px); border-color: rgba(255, 215, 0, 0.5); }
    
    /* تحسين حقول النص */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        color: white !important;
        font-family: 'Tajawal' !important;
        border-radius: 10px !important;
    }
    
    /* زر المعالجة */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 100%) !important;
        color: #001f3f !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        border-radius: 12px !important;
        width: 100% !important;
        padding: 15px !important;
        border: none !important;
        box-shadow: 0 5px 20px rgba(218, 165, 32, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(218, 165, 32, 0.6) !important;
    }

    /* شريط التقدم */
    .progress-box {
        background: rgba(0, 31, 63, 0.9); border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px; padding: 25px; margin: 20px 0; text-align: center;
    }
    .progress-bar-bg { background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; overflow: hidden; margin: 15px 0; }
    .progress-bar-fill {
        height: 100%; background: linear-gradient(90deg, #FFD700, #FFA500);
        transition: width 0.3s ease;
    }
    .progress-text { color: #fff; font-size: 0.9rem; }
    
    /* شريط النجاح */
    .success-banner {
        background: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e;
        color: #22c55e; padding: 15px; border-radius: 10px; text-align: center; margin: 20px 0; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🛠️ القالب الذكي (Smart HTML Template)
# هذا القالب يحتوي على مكتبات JS و CSS الحديث
# ---------------------------------------------------------
SMART_HEADER = """
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #001f3f; --secondary: #c5a059; --bg: #f4f7f6; --text: #333;
            --card-bg: #ffffff; --card-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }
        
        /* --- ثيمات ديناميكية --- */
        /* 1. الثيم الاستراتيجي (الافتراضي) */
        body.theme-strategic { --primary: #002b49; --secondary: #c5a059; --bg: #f8f9fa; } 
        /* 2. ثيم الأزمات/التحذير (أحمر ورمادي) */
        body.theme-crisis { --primary: #2c3e50; --secondary: #e74c3c; --bg: #fff5f5; } 
        /* 3. ثيم المال والنمو (أزرق سماوي وأخضر) */
        body.theme-financial { --primary: #004e89; --secondary: #27ae60; --bg: #f0f8ff; } 
        
        body { font-family: 'Cairo', sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 20px; direction: rtl; }
        
        .container { max-width: 1200px; margin: 0 auto; background: var(--bg); }
        
        /* الهيدر */
        header { text-align: center; padding: 40px 0; border-bottom: 3px solid var(--secondary); margin-bottom: 40px; background: white; border-radius: 20px; box-shadow: var(--card-shadow); }
        header h1 { color: var(--primary); font-size: 2.5rem; font-weight: 900; margin: 0; font-family: 'Tajawal'; }
        header .meta-tags { margin-top: 15px; }
        header .tag { display: inline-block; background: var(--bg); padding: 5px 15px; border-radius: 20px; color: #666; font-size: 0.9rem; margin: 0 5px; border: 1px solid #ddd; }

        /* البطاقات الإحصائية */
        .grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .stat-card { background: white; padding: 25px; border-radius: 16px; position: relative; overflow: hidden; box-shadow: var(--card-shadow); transition: transform 0.3s; border-bottom: 4px solid var(--secondary); }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card .icon { position: absolute; left: 20px; top: 20px; font-size: 2.5rem; color: var(--secondary); opacity: 0.15; }
        .stat-card h3 { margin: 0 0 10px 0; color: #777; font-size: 0.9rem; }
        .stat-card .value { font-size: 2.2rem; font-weight: 800; color: var(--primary); font-family: 'Tajawal'; }

        /* الأقسام */
        .section-box { background: white; border-radius: 20px; padding: 35px; margin-bottom: 30px; box-shadow: var(--card-shadow); }
        h2.section-title { color: var(--primary); font-size: 1.6rem; margin-top: 0; margin-bottom: 25px; display: flex; align-items: center; gap: 10px; }
        h2.section-title::before { content: ''; display: block; width: 6px; height: 30px; background: var(--secondary); border-radius: 3px; }

        /* الجداول */
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th { background: var(--primary); color: white; padding: 15px; font-family: 'Tajawal'; }
        td { padding: 12px; border-bottom: 1px solid #eee; text-align: center; }
        tr:last-child td { border-bottom: none; }
        tr:hover { background-color: rgba(0,0,0,0.02); }

        /* منطقة الرسم البياني */
        .chart-wrapper { position: relative; height: 350px; width: 100%; margin-top: 20px; }

        /* التوصيات */
        .rec-item { display: flex; gap: 15px; margin-bottom: 15px; align-items: flex-start; }
        .rec-num { background: var(--secondary); color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
        .rec-text { background: #f9f9f9; padding: 15px; border-radius: 12px; width: 100%; border: 1px solid #eee; transition: 0.3s; }
        .rec-text:hover { background: white; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transform: translateX(-5px); }

        /* زر الطباعة */
        .fab-print { position: fixed; bottom: 30px; left: 30px; width: 60px; height: 60px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); cursor: pointer; transition: 0.3s; z-index: 999; border: none; }
        .fab-print:hover { transform: scale(1.1); background: var(--secondary); }
        
        @media print { .fab-print { display: none; } body { background: white; padding: 0; } .container { box-shadow: none; } }
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
    # نحاول استخدام أسرع موديل متاح
    return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ بناء الواجهة
# ---------------------------------------------------------

# الهيدر
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | منصة التحليل الذكي</div>
</div>
''', unsafe_allow_html=True)

# منطقة الإدخال
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="input-card"><h3 style="color:#FFD700; margin:0;">📝 البيانات / الملاحظات</h3></div>', unsafe_allow_html=True)
    user_text = st.text_area("", height=180, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...", label_visibility="collapsed")

with col2:
    st.markdown('<div class="input-card"><h3 style="color:#FFD700; margin:0;">📎 رفع الملفات</h3></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"تم إرفاق: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🚀 منطق المعالجة (الذكي والتفاعلي)
# ---------------------------------------------------------
if st.button("🚀 تحليل البيانات وإنشاء التقرير التفاعلي"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. تأكد من إضافته في Secrets.")
        st.stop()
    
    # تجميع النص
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة محتوى الملف...'):
            full_text += f"\n\n[FILE_CONTENT]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف للبدء.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            # 🧠 الـ Prompt المطور (Design & Logic Expert)
            prompt = f"""
            You are an elite Data Analyst & UI Developer for a political/strategic organization.
            
            **Goal:** Transform the provided text into a **High-End Interactive HTML Report**.
            
            **Input Data:**
            {full_text}
            
            **CRITICAL INSTRUCTIONS (Follow Strictly):**
            
            1. **Theme Detection:** Analyze the content tone.
               - If content is about budgets/finance/growth -> Use CSS class `theme-financial` for the `<body>`.
               - If content is about risks/threats/declines -> Use CSS class `theme-crisis` for the `<body>`.
               - If content is general/strategic/reports -> Use CSS class `theme-strategic` for the `<body>`.
            
            2. **HTML Structure (Return ONLY the body content):**
               - **Header:** `<header><h1>Title</h1><div class="meta-tags"><span class="tag">Date</span>...</div></header>`
               - **Key Metrics:** Extract 3-4 key numbers. Put them in `<div class="grid-cards">`. Each card: `<div class="stat-card"><div class="icon"><i class="fas fa-chart-line"></i></div><h3>Label</h3><div class="value">123</div></div>`.
               - **Analysis:** Group content into `<div class="section-box">`. Use `<h2 class="section-title"><i class="fas fa-file-alt"></i> Title</h2>`.
               - **Tables:** If data exists, create a table inside a section.
               - **Interactive Chart (The Magic):**
                 - Identify the MOST important dataset for visualization (e.g., Votes per City, Budget vs Expenses).
                 - Create a container: `<div class="section-box"><h2 class="section-title">📊 الرسم البياني التفاعلي</h2><div class="chart-wrapper"><canvas id="mainChart"></canvas></div></div>`.
               - **Recommendations:** Use `<div class="rec-item"><div class="rec-num">1</div><div class="rec-text">Text...</div></div>`.
            
            3. **JavaScript Injection (Chart.js):**
               - At the very end of your response, write a `<script>` block.
               - Initialize `new Chart(document.getElementById('mainChart'), ...)`
               - Choose the best chart type (bar, doughnut, or line) based on the data.
               - Use colors that match the selected theme (Navy/Gold for strategic, Red/Grey for crisis, Blue/Green for financial).
               - **IMPORTANT:** Ensure the script is valid and runs immediately.

            **Output Format:** - Return ONLY valid HTML code to be placed inside the `<body>` tag. 
            - Start with `<body class="...">`.
            - Do not use markdown blocks (```html).
            - Language: Arabic (Professional).
            """

            # شريط التقدم التفاعلي
            progress_placeholder = st.empty()
            steps = ["جاري تحليل البيانات...", "تحديد النمط البصري المناسب...", "بناء الرسوم البيانية التفاعلية...", "توليد كود التقرير..."]
            
            for i, step in enumerate(steps):
                prog = (i + 1) * 25
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 10px;">🤖</div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {prog}%;"></div></div>
                    <div class="progress-text">{step} ({prog}%)</div>
                </div>''', unsafe_allow_html=True)
                time.sleep(0.5)
            
            # توليد المحتوى
            response = model.generate_content(prompt)
            html_body = clean_html_response(response.text)
            
            # تجميع الملف النهائي
            final_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            {SMART_HEADER}
            {html_body}
            <button class="fab-print" onclick="window.print()" title="طباعة التقرير"><i class="fas fa-print"></i></button>
            </html>
            """
            
            progress_placeholder.empty()

            # عرض النتيجة
            st.markdown('''
            <div class="success-banner">
                <span style="font-size: 1.2rem;">✨ تم إنشاء التقرير التفاعلي بنجاح!</span><br>
                <span style="font-size: 0.9rem; opacity: 0.8;">التقرير يحتوي على رسوم بيانية تفاعلية وتصميم ذكي يتناسب مع المحتوى.</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.components.v1.html(final_html, height=1000, scrolling=True)

            # زر التحميل
            st.download_button(
                label="📥 تحميل التقرير النهائي (HTML)",
                data=final_html,
                file_name="Smart_Report.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {e}")

# الفوتر البسيط
st.markdown("<br><hr style='border-color:rgba(255,215,0,0.2);'><p style='text-align:center; color:#888; font-size:0.8rem;'>Jassim AI System © 2026</p>", unsafe_allow_html=True)
