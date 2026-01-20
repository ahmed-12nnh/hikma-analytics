import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
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
# 🎨 CSS المحسن (واجهة المنصة الخارجية - كما هي)
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

    [data-testid="stSidebar"], header, #MainMenu, footer, [data-testid="stToolbar"] { display: none; }

    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 20px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.8), inset 0 0 30px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        animation: fadeIn 1s ease-in-out;
    }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        box-shadow: 0 0 20px #FFD700; animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }

    .main-title {
        font-size: 52px; font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 15px; text-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }

    .sub-title { color: #e0e0e0; font-size: 18px; letter-spacing: 2px; font-weight: 500; opacity: 0.9; }
    .section-header { text-align: center; margin: 30px 20px; color: #FFD700; font-size: 1.4rem; font-weight: bold; }

    div[role="radiogroup"] {
        display: flex !important; flex-direction: row-reverse !important; justify-content: center !important;
        gap: 15px !important; background: rgba(0, 0, 0, 0.3) !important; padding: 20px !important;
        border-radius: 15px !important; margin: 0 20px 30px 20px !important; border: 1px solid rgba(255, 215, 0, 0.15) !important;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95)) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important; padding: 15px 25px !important;
        border-radius: 12px !important; cursor: pointer !important; transition: all 0.4s !important;
        text-align: center !important; flex: 1 !important; color: white !important; font-weight: 600 !important;
    }
    
    div[role="radiogroup"] label:hover {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 31, 63, 0.95)) !important;
        border-color: #FFD700 !important; transform: translateY(-5px) scale(1.02) !important;
    }
    
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(184, 134, 11, 0.15)) !important;
        border-color: #FFD700 !important; box-shadow: 0 0 25px rgba(255, 215, 0, 0.3) !important;
    }

    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px; padding: 30px; margin: 10px; border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .input-header { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; border-bottom: 1px solid rgba(255, 215, 0, 0.2); padding-bottom: 15px; }
    .input-icon { width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #FFD700, #B8860B); border-radius: 12px; font-size: 1.5rem; }
    .input-title { color: #FFD700; font-size: 1.2rem; font-weight: 700; }
    .input-subtitle { color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; }

    .stTextArea textarea { background-color: rgba(0, 0, 0, 0.4) !important; border: 2px solid rgba(255, 215, 0, 0.2) !important; border-radius: 15px !important; color: white !important; font-family: 'Tajawal', sans-serif !important; padding: 20px !important; text-align: right !important; direction: rtl !important; }
    .stTextArea textarea:focus { border-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important; }

    [data-testid="stFileUploader"] { background: rgba(0, 0, 0, 0.3) !important; border: 2px dashed rgba(255, 215, 0, 0.3) !important; border-radius: 15px !important; padding: 25px !important; }
    [data-testid="stFileUploader"] button { background: linear-gradient(135deg, #FFD700, #B8860B) !important; color: #001f3f !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; }

    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 50%, #FFD700 100%) !important;
        background-size: 200% auto !important; color: #001f3f !important; font-family: 'Tajawal', sans-serif !important;
        font-weight: 900 !important; font-size: 1.3rem !important; border-radius: 15px !important; width: 100% !important;
        padding: 18px 40px !important; border: none !important; box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4) !important;
        animation: buttonPulse 2s infinite !important;
    }
    
    @keyframes buttonPulse { 0%, 100% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4); } 50% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.6), 0 0 0 10px rgba(255, 215, 0, 0); } }

    .stDownloadButton > button { background: linear-gradient(135deg, #6366f1, #8b5cf6) !important; color: white !important; font-weight: 700 !important; border-radius: 12px !important; border: none !important; box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important; }
    
    .success-banner { background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1)); border: 2px solid #22c55e; border-radius: 15px; padding: 20px; text-align: center; margin: 20px; }
    .success-banner span { color: #22c55e; font-size: 1.2rem; font-weight: 700; }
    
    iframe { border-radius: 15px !important; border: 2px solid rgba(255, 215, 0, 0.3) !important; box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important; }
    
    .progress-box { background: rgba(0, 31, 63, 0.9); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 15px; padding: 30px; margin: 20px; text-align: center; }
    .progress-bar-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 12px; margin: 20px 0; overflow: hidden; }
    .progress-bar-fill { height: 100%; background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700); background-size: 200% 100%; border-radius: 10px; animation: progressShine 1.5s infinite linear; transition: width 0.3s ease; }
    @keyframes progressShine { 0% { background-position: 200% center; } 100% { background-position: -200% center; } }
    .progress-text { color: rgba(255, 255, 255, 0.8); margin-top: 10px; }
    
    .stTextArea > label, .stFileUploader > label, .stRadio > label { display: none !important; }
    @media (max-width: 768px) { .main-title { font-size: 36px; } }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب (تم تحديثها لتكون عصرية جداً)
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    :root { --navy: #002b49; --gold: #c5a059; --bg-light: #f8f9fa; --white: #ffffff; --text: #333; }
    body { font-family: 'Tajawal', sans-serif; background-color: var(--bg-light); color: var(--text); line-height: 1.8; direction: rtl; margin: 0; padding: 0; }
    .container { max-width: 1000px; margin: 40px auto; padding: 40px; background: var(--white); box-shadow: 0 10px 40px rgba(0,0,0,0.05); border-radius: 16px; border-top: 6px solid var(--navy); }
    
    /* Header Modern */
    header { text-align: center; margin-bottom: 50px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
    header h1 { color: var(--navy); font-size: 2.2rem; margin: 0; font-weight: 800; letter-spacing: -0.5px; }
    header h2 { color: var(--gold); font-size: 1.2rem; margin-top: 8px; font-weight: 500; }
    
    /* Modern Cards for Content */
    .section-card { margin-bottom: 30px; }
    h3.section-title { color: var(--navy); font-size: 1.4rem; font-weight: 700; margin-bottom: 15px; border-right: 4px solid var(--gold); padding-right: 15px; display: flex; align-items: center; }
    
    /* The List Grid Design */
    .members-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-top: 20px; }
    .member-item { 
        background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 15px 20px; 
        display: flex; justify-content: space-between; align-items: center;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .member-item:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.08); border-color: var(--gold); }
    
    .role-badge { background: rgba(0, 43, 73, 0.05); color: var(--navy); padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
    .member-name { font-weight: 700; color: #222; font-size: 1.05rem; }

    /* Clean Tables */
    table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0; border: 1px solid #eee; border-radius: 8px; overflow: hidden; }
    th { background: var(--navy); color: #fff; padding: 15px; font-weight: 500; text-align: right; }
    td { padding: 12px 15px; border-bottom: 1px solid #f0f0f0; color: #555; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background-color: #fcfcfc; }

    footer { text-align: center; margin-top: 50px; font-size: 0.85rem; color: #888; border-top: 1px solid #eee; padding-top: 20px; }
</style>
"""

STYLE_DIGITAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    body { font-family: 'Cairo', sans-serif; background: #f0f2f5; color: #444; direction: rtl; }
    .container { max-width: 1200px; margin: 30px auto; padding: 20px; }
    
    /* Dashboard Header */
    .dash-header { background: #fff; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }
    .dash-title h1 { margin: 0; font-size: 1.8rem; color: #1a1a1a; font-weight: 700; }
    .dash-badge { background: #e3f2fd; color: #1565c0; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; }

    /* KPI Cards */
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
    .kpi-card { background: #fff; padding: 20px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); border-bottom: 4px solid #3b82f6; }
    .kpi-val { font-size: 2rem; font-weight: 700; color: #1e293b; }
    .kpi-label { color: #64748b; font-size: 0.9rem; margin-top: 5px; }

    /* Content Area */
    .content-box { background: #fff; padding: 30px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); margin-bottom: 20px; }
    h2 { font-size: 1.3rem; color: #334155; margin-bottom: 20px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; }
    
    /* List styling */
    ul { list-style: none; padding: 0; }
    ul li { background: #f8fafc; margin-bottom: 10px; padding: 15px; border-radius: 8px; border-right: 3px solid #3b82f6; display: flex; justify-content: space-between; }
</style>
"""

# باقي القوالب (التحليل، العرض التقديمي، الملخص) تبقى كما هي لأنها جيدة، لكن يمكن تحسينها بنفس المنطق
STYLE_ANALYTICAL = STYLE_OFFICIAL # استخدام الرسمي كقاعدة للتحليل مع تعديلات بسيطة لو لزم
STYLE_EXECUTIVE = STYLE_OFFICIAL

STYLE_PRESENTATION = """
<style>
    :root {
        --primary-navy: #002b49; --primary-blue: #004e89;
        --gold-main: #c5a059; --gold-light: #e6c885;
        --white: #ffffff; --grey-light: #f8f9fa; --text-dark: #333333;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Cairo', sans-serif; background-color: var(--primary-navy); overflow: hidden; height: 100vh; width: 100vw; direction: rtl; margin:0;}
    .presentation-container { width: 100%; height: 100%; position: relative; background: radial-gradient(circle at center, #003865 0%, #002035 100%); }
    .slide {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0; visibility: hidden; transform: scale(0.95);
        transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
        display: flex; flex-direction: column; padding: 40px 60px;
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIiBvcGFjaXR5PSIwLjAzIj48cGF0aCBkPSJNMjAgMjBMMCAwSDQwTDgwIDgwIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMSIvPjwvc3ZnPg==');
    }
    .slide.active { opacity: 1; visibility: visible; transform: scale(1); z-index: 10; }
    .slide-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--gold-main); padding-bottom: 15px; margin-bottom: 25px; flex-shrink: 0; }
    .header-title h2 { color: var(--gold-main); font-size: 2rem; font-weight: 800; }
    .header-logo { font-family: 'Tajawal'; color: var(--white); font-weight: bold; display: flex; align-items: center; gap: 10px; }
    .slide-content { flex-grow: 1; display: flex; gap: 40px; height: 100%; overflow: hidden; }
    .text-panel { flex: 3; background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 30px; color: var(--text-dark); box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow-y: auto; border-right: 5px solid var(--gold-main); }
    .visual-panel { flex: 2; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--white); text-align: center; }
    h3 { color: var(--primary-blue); font-size: 1.6rem; margin-bottom: 15px; border-bottom: 1px dashed #ccc; padding-bottom: 5px; }
    p { font-size: 1.2rem; line-height: 1.8; margin-bottom: 20px; text-align: justify; }
    li { font-size: 1.15rem; margin-bottom: 10px; line-height: 1.6; }
    strong { color: var(--primary-navy); font-weight: 800; }
    .icon-box { font-size: 5rem; color: var(--gold-main); margin-bottom: 20px; text-shadow: 0 5px 15px rgba(0,0,0,0.5); animation: float 4s ease-in-out infinite; }
    .slide.cover { align-items: center; justify-content: center; text-align: center; background: linear-gradient(135deg, var(--primary-navy) 30%, #001a2c 100%); }
    .cover-content { border: 2px solid var(--gold-main); padding: 60px; position: relative; background: rgba(0,0,0,0.4); backdrop-filter: blur(5px); }
    .main-title { font-size: 3.5rem; color: var(--white); margin-bottom: 15px; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .sub-title { font-size: 1.8rem; color: var(--gold-main); margin-bottom: 40px; font-weight: 300; }
    .nav-controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 100; }
    .nav-btn { background: transparent; border: 2px solid var(--gold-main); color: var(--gold-main); width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 1.2rem; transition: 0.3s; display: flex; align-items: center; justify-content: center; }
    .nav-btn:hover { background: var(--gold-main); color: var(--primary-navy); transform: scale(1.1); }
    .page-number { position: absolute; bottom: 25px; right: 60px; color: var(--gold-main); font-size: 1.2rem; font-weight: bold; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    .signature-box { margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--gold-main); text-align: center; }
    .signature-title { font-size: 0.9rem; color: #aaa; margin-bottom: 10px; }
    .signature-name { font-size: 1.4rem; color: var(--gold-main); font-weight: bold; font-family: 'Tajawal'; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    function updateSlide() {
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        if(totalSlides === 0) return;
        
        slides.forEach(slide => { slide.classList.remove('active'); });
        
        const activeSlide = document.getElementById(`slide-${currentSlideIndex}`);
        if(activeSlide) activeSlide.classList.add('active');
        
        const pageNum = document.getElementById('page-num');
        if(pageNum) pageNum.innerText = `${currentSlideIndex} / ${totalSlides}`;
    }
    function nextSlide() { 
        const totalSlides = document.querySelectorAll('.slide').length;
        if (currentSlideIndex < totalSlides) { currentSlideIndex++; updateSlide(); } 
    }
    function prevSlide() { 
        if (currentSlideIndex > 1) { currentSlideIndex--; updateSlide(); } 
    }
    document.addEventListener('keydown', function(event) {
        if (event.key === "ArrowLeft" || event.key === "Space") nextSlide();
        else if (event.key === "ArrowRight") prevSlide();
    });
    setTimeout(updateSlide, 100);
</script>
"""

# ---------------------------------------------------------
# 🛠️ دوال المساعدة (باستخدام PyMuPDF)
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    text_content = ""
    try:
        if uploaded_file.type == "application/pdf":
            try:
                # fitz هو الأفضل لدعم العربية
                doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
                for page in doc:
                    text_content += page.get_text() + "\n"
            except Exception as pdf_err:
                return f"⚠️ خطأ في قراءة PDF: {pdf_err}"

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            try:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
                text_content = df.to_string()
            except Exception as xl_err:
                 return f"⚠️ خطأ في قراءة Excel: {xl_err}"
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8", errors='ignore'))
            text_content = stringio.read()
    except Exception as e:
        return f"⚠️ خطأ عام: {e}"
        
    if not text_content.strip():
        return "⚠️ تحذير: الملف فارغ."
    return text_content

def clean_input_text(text):
    if not text: return ""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

def clean_html_response(text):
    text = text.replace("```html", "").replace("```", "")
    return text.strip()

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ بناء الواجهة
# ---------------------------------------------------------

st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="section-header">🎨 اختر نمط الإخراج المطلوب</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي (PPT)", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

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
    user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات...", label_visibility="collapsed")

with col_upload:
    st.markdown('''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📎</div>
            <div>
                <div class="input-title">رفع الملفات</div>
                <div class="input-subtitle">PDF, XLSX, TXT</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    if uploaded_file: st.success(f"✅ تم إرفاق: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API.")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            file_content = extract_text_from_file(uploaded_file)
            if "⚠️" in file_content and len(file_content) < 200: st.warning(file_content)
            full_text += f"\n\n[محتوى الملف]:\n{file_content}"

    full_text = clean_input_text(full_text)

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            target_css = ""
            design_rules = ""
            file_label = "Report"
            
            # التوقيع الموحد
            unified_signature = """
            <div style="margin-top: 50px; text-align: center; padding-top: 20px; border-top: 1px solid #eee; font-family: 'Tajawal'; color: #777;">
                <p style="margin-bottom: 5px; font-weight: bold;">الجهاز المركزي للجودة الشاملة</p>
                <p style="font-size: 0.9em; color: #002b49;">وحدة التخطيط الاستراتيجي والتطوير</p>
            </div>
            """

            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Report"
                design_rules = """
                Style: MODERN Corporate Clean Report (Glassmorphism Light).
                - Use <div class="section-card"> for each main section.
                - Use <h3 class="section-title">Title</h3> for headers.
                - For lists of people/members: Use <div class="members-grid"> containing multiple <div class="member-item"><span class="role-badge">Role</span><span class="member-name">Name</span></div>.
                - Use clean HTML tables with standard <table> tags.
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                design_rules = """
                Style: Modern Digital Dashboard.
                - Use <div class="dash-header"> for the main title.
                - Use <div class="kpi-grid"> containing <div class="kpi-card"> for numbers.
                - Use <div class="content-box"> for text sections.
                """
            
            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Slides"
                design_rules = """
                Style: Interactive Presentation.
                - Create slides with class="slide".
                - First slide is cover.
                - Use font-awesome icons.
                - DO NOT include the script/css in output, just HTML.
                """
                unified_signature = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                <div class="page-number" id="page-num">1 / 1</div>
                """
            
            else: # Fallback for other types to Official style for now
                target_css = STYLE_OFFICIAL
                file_label = "Report"
                design_rules = "Style: Clean Corporate Report. Use cards and grids."

            # هندسة الأوامر (Prompt Engineering) لحل مشكلة الأسماء
            prompt = f"""
            You are an expert Data Analyst & Developer for 'Al-Hikma National Movement'.
            **Objective:** Create a STUNNING, MODERN HTML report.
            
            **CRITICAL INSTRUCTIONS FOR ACCURACY (ZERO HALLUCINATION):**
            1. **VERBATIM NAMES:** You must extract names EXACTLY as they appear in the text.
               - IF text says "الكناني", DO NOT write "الجنابي".
               - IF text says "أبو كلل", DO NOT write "أبو هلال".
               - IF text says "الدراجي", DO NOT write "الراجحي".
               - Copy the characters exactly, even if they seem rare.
            2. **Fix Reversed Text:** If input has "ل ل ك و ب أ", output "أبو كلل".
            
            **DESIGN INSTRUCTIONS:**
            {design_rules}
            
            **INPUT DATA:**
            {full_text}
            
            **OUTPUT:** Only HTML body content.
            """

            progress_placeholder = st.empty()
            for i in range(0, 90, 10):
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🤖</div>
                    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {i}%;"></div></div>
                    <div class="progress-text">جاري التحليل الدقيق وبناء التصميم العصري... {i}%</div>
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(0.1)
            
            try:
                response = model.generate_content(prompt)
                html_body = clean_html_response(response.text)
                progress_placeholder.empty()
                
                final_html = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{file_label}</title>
                    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
                    {target_css}
                </head>
                <body>
                    <div class="{ 'presentation-container' if 'عرض تقديمي' in report_type else 'container' }">
                        {html_body}
                        {unified_signature}
                    </div>
                    {SCRIPT_PRESENTATION if 'عرض تقديمي' in report_type else ''}
                </body>
                </html>
                """

                st.markdown('<div class="success-banner"><span>✅ تم إنشاء التقرير بنجاح!</span></div>', unsafe_allow_html=True)
                st.components.v1.html(final_html, height=850, scrolling=True)
                st.download_button(label="📥 تحميل التقرير (HTML)", data=final_html, file_name=f"{file_label}.html", mime="text/html")
            
            except Exception as e:
                progress_placeholder.empty()
                st.error(f"❌ خطأ: {e}")

        except Exception as e:
            st.error(f"❌ خطأ غير متوقع: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''
<div style="background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9)); border-radius: 15px; padding: 30px 20px; margin: 20px; border: 1px solid rgba(255, 215, 0, 0.3); text-align: center;">
    <p style="color: #FFD700; font-family: 'Tajawal'; font-weight: bold;">الجهاز المركزي للجودة الشاملة</p>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">وحدة التخطيط الاستراتيجي والتطوير © 2026</p>
</div>
''', unsafe_allow_html=True)
