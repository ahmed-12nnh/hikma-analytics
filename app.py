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
# 🎨 إعدادات الصفحة والتصميم (تم إصلاح مشاكل العرض)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide")

# CSS الواجهة (مع إصلاحات التداخل RTL Fixes)
st.markdown("""
<style>
    @import url('[https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap](https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap)');
    
    /* إعدادات عامة لمنع التداخل */
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* الهيدر الفخم */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 30px rgba(0, 31, 63, 0.7), inset 0 0 20px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
        animation: fadeIn 1s ease-in-out;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 6px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        box-shadow: 0 0 15px #FFD700;
    }

    .main-title {
        font-size: 50px;
        font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.6);
    }

    .sub-title {
        color: #e0e0e0;
        font-size: 18px;
        letter-spacing: 1px;
        font-weight: 500;
    }

    /* أزرار الاختيار */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row-reverse;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }

    div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px 20px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        flex: 1;
        min-width: 140px;
        color: white !important;
        font-weight: bold;
    }

    div[role="radiogroup"] label:hover {
        background-color: rgba(255, 215, 0, 0.15);
        border-color: #FFD700;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* الحقول والأزرار */
    .stTextArea textarea, .stFileUploader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: right;
    }
    
    .stButton button {
        background: linear-gradient(90deg, #FFD700, #DAA520);
        color: #001f3f !important;
        font-weight: 900;
        font-size: 20px;
        border-radius: 12px;
        width: 100%;
        padding: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.4);
        transition: transform 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(218, 165, 32, 0.7);
    }

    .custom-header {
        text-align: right !important;
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        border-right: 4px solid #FFD700;
        padding-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب (تم تحسين CSS لمنع الأخطاء)
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    :root { --navy-blue: #001f3f; --gold: #FFD700; --light-gold: #FFEB84; --white: #ffffff; --gray: #f4f4f4; --dark-gray: #333; }
    body { font-family: 'Tajawal', sans-serif; background-color: var(--gray); color: var(--dark-gray); line-height: 1.6; direction: rtl; text-align: right; margin: 0; padding: 0; }
    .container { max-width: 1200px; margin: 20px auto; padding: 20px; display: block; }
    /* Fix: Use Flexbox for better wrapping */
    .card-grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
    
    header { background-color: var(--navy-blue); color: var(--gold); padding: 30px 0; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; border-radius: 8px; }
    header h1 { margin: 0; font-size: 2.5em; font-weight: 700; }
    header h2 { margin: 10px 0 0; font-size: 1.5em; color: var(--light-gold); }
    
    .card { background-color: var(--white); border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); padding: 25px; margin-bottom: 20px; break-inside: avoid; }
    .card h3 { color: var(--navy-blue); font-size: 1.8em; margin-top: 0; border-bottom: 2px solid var(--gold); padding-bottom: 10px; }
    
    table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.95em; }
    table th { background-color: var(--navy-blue); color: var(--light-gold); padding: 12px; border: 1px solid #ddd; }
    table td { border: 1px solid #ddd; padding: 12px; text-align: right; }
    
    ul { list-style: none; padding: 0; }
    ul li { padding: 10px 0; border-bottom: 1px dashed #eee; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; }
    ul li span.value { font-weight: 700; color: var(--gold); font-size: 1.1em; background: #001f3f; padding: 2px 8px; border-radius: 4px; margin-right: 10px; }
    
    footer { grid-column: 1 / -1; text-align: center; margin-top: 40px; padding: 20px; color: #666; font-size: 0.9em; border-top: 2px solid var(--navy-blue); }
</style>
"""

STYLE_DIGITAL = """
<style>
    body { font-family: 'Cairo', sans-serif; line-height: 1.7; background-color: #f4f7f9; color: #333; direction: rtl; }
    .container { max-width: 1200px; margin: 20px auto; padding: 25px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07); }
    header { text-align: center; padding-bottom: 20px; margin-bottom: 30px; border-bottom: 3px solid #0056b3; }
    h1 { color: #0056b3; font-size: 2.4em; font-weight: 700; }
    h2 { color: #007bff; font-size: 2em; border-bottom: 2px solid #f0f0f0; margin-bottom: 20px; }
    
    .card { background-color: #fdfdfd; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; margin-top: 20px; box-shadow: 0 3px 8px rgba(0,0,0,0.05); }
    
    ul li { position: relative; padding-right: 35px; margin-bottom: 12px; }
    ul li::before { content: '•'; position: absolute; right: 0; color: #007bff; font-size: 1.8em; line-height: 1; }
    
    .goal { background-color: #e6f7ff; border: 1px solid #b3e0ff; padding: 18px; border-radius: 8px; text-align: center; margin-top: 20px; font-weight: bold; color: #0056b3; }
    
    /* Fix Table Overflow */
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; display: block; overflow-x: auto; white-space: nowrap; }
    thead th { background-color: #007bff; color: white; padding: 14px; }
    td { padding: 14px; border: 1px solid #e0e0e0; text-align: center; }
    
    footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-style: italic; color: #777; }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    body { font-family: 'Cairo', sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.7; direction: rtl; }
    .container { max-width: 1100px; margin: 20px auto; padding: 20px; }
    header { background-color: #004a99; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0, 74, 153, 0.2); }
    .report-section { background-color: #fff; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.07); margin-bottom: 25px; padding: 25px; }
    .report-section h2 { color: #004a99; border-bottom: 3px solid #0056b3; padding-bottom: 10px; }
    
    /* Fix Grid Overflow */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
    .stat-card { background-color: #eef5ff; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #d0e3ff; }
    .stat-card .value { font-size: 2.2rem; font-weight: 700; color: #004a99; word-break: break-all; }
    
    .pyramid-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    .tier-card { border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background-color: #fcfcfc; border-top: 6px solid; }
    .tier-upper { border-top-color: #d90429; } 
    .tier-middle { border-top-color: #f7b801; } 
    
    /* Progress Bars */
    .bar-container { background-color: #e0e0e0; border-radius: 5px; height: 12px; margin-top: 12px; width: 100%; overflow: hidden; }
    .bar { height: 100%; border-radius: 5px; }
    .tier-upper .bar { background-color: #d90429; } 
    .tier-middle .bar { background-color: #f7b801; }
    
    footer { text-align: center; margin-top: 30px; color: #888; font-size: 0.9rem; border-top: 1px solid #ccc; padding-top: 20px;}
</style>
"""

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
<link rel="stylesheet" href="[https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css)">
"""

STYLE_EXECUTIVE = """
<style>
    @import url('[https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;800&display=swap](https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;800&display=swap)');
    body { font-family: 'Tajawal', sans-serif; background-color: #ffffff; color: #222; direction: rtl; }
    .container { max-width: 900px; margin: 40px auto; padding: 40px; border: 1px solid #eee; box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid #000; padding-bottom: 20px; margin-bottom: 40px; }
    .brand { font-size: 1.5rem; font-weight: 800; letter-spacing: -1px; color: #002b49; }
    h1 { font-size: 2.8rem; font-weight: 900; line-height: 1.1; margin-bottom: 10px; color: #000; }
    .executive-summary { font-size: 1.3rem; line-height: 1.6; color: #444; margin-bottom: 40px; border-right: 5px solid #FFD700; padding-right: 20px; background: #fafafa; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; margin-bottom: 30px; }
    .metric-box { padding: 20px; background: #f9f9f9; border-radius: 8px; border: 1px solid #eee; }
    .metric-val { font-size: 2.5rem; font-weight: 800; color: #002b49; }
    .metric-lbl { font-size: 1rem; color: #666; text-transform: uppercase; }
    .section-title { font-size: 1.2rem; font-weight: 800; text-transform: uppercase; margin-top: 30px; margin-bottom: 15px; color: #c5a059; border-bottom: 2px solid #eee; display: inline-block;}
    footer { margin-top: 60px; border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #999; font-size: 0.8rem; }
</style>
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
    // Delay initial run to allow DOM to load
    setTimeout(updateSlide, 100);
</script>
"""

# ---------------------------------------------------------
# 🛠️ دوال المساعدة والمعالجة
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
    """تنظيف رد الذكاء الاصطناعي من شوائب الماركداون"""
    text = text.replace("```html", "").replace("```", "")
    return text.strip()

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ بناء الواجهة (Layout)
# ---------------------------------------------------------

st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align: center; margin-bottom: 15px; color: #FFD700; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">اختر نمط الإخراج المطلوب:</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي (PPT)", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

col_input, col_upload = st.columns([2, 1])

with col_input:
    st.markdown('<div class="custom-header">📝 البيانات / الملاحظات</div>', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...")

with col_upload:
    st.markdown('<div class="custom-header">📎 رفع الملفات</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'])
    if uploaded_file:
        st.success(f"تم إرفاق: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            full_text += f"\n\n[محتوى الملف]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            target_css = ""
            design_rules = ""
            file_label = "Report"
            
            # التوقيع الموحد (لجميع التقارير ما عدا العرض التقديمي)
            unified_signature = """
            <div style="margin-top: 50px; text-align: center; padding-top: 20px; border-top: 2px solid #ccc; font-family: 'Tajawal'; color: #555;">
                <p style="margin-bottom: 5px;"><strong>صادر من الجهاز المركزي للجودة الشاملة</strong></p>
                <p style="font-size: 1.1em; color: #001f3f;"><strong>وحدة التخطيط الاستراتيجي والتطوير</strong></p>
            </div>
            """

            # 1. تخصيص الأنماط والقواعد
            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Report"
                design_rules = """
                Style: Official Corporate Report.
                - Wrap card sections in <div class="card">.
                - Use HTML <table> inside cards for tabular data.
                - Use <ul> with <li><span>Label</span> <span class="value">Value</span></li> for lists.
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                design_rules = """
                Style: Modern Digital Dashboard.
                - Use <section id="summary"> for highlights.
                - Use <article class="card"> for detailed sections.
                - Use <div class="goal"> for key takeaways.
                """
            
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                design_rules = """
                Style: Statistical Hierarchy.
                - Use <div class="stats-grid"> for top key numbers.
                - Use <div class="pyramid-grid"> for detailed hierarchy.
                - Inside pyramid, use <div class="tier-card tier-upper"> (or middle/weak) based on importance.
                - Use <div class="bar-container"><div class="bar" style="width: XX%;"></div></div> for percentages.
                """
            
            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE
                file_label = "Executive_Summary"
                design_rules = """
                Style: Modern Executive Summary.
                - Header is already provided in CSS, just use <h1>.
                - Use <div class="executive-summary"> for the main text.
                - Use <div class="grid-2"> with <div class="metric-box"> for key metrics.
                """

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Presentation_Slides"
                design_rules = """
                Style: Interactive Presentation Slides (Reveal.js style).
                Structure Requirement:
                1. Output HTML `div` elements with class `slide`.
                2. The first slide MUST be `<div class="slide cover active" id="slide-1">`.
                3. Subsequent slides must be `<div class="slide" id="slide-2">`, `<div class="slide" id="slide-3">` etc.
                4. Inside slides, use `<div class="slide-header">` (with title & logo).
                5. Use `<div class="slide-content">` split into `<div class="text-panel">` and `<div class="visual-panel">`.
                6. Use FontAwesome icons `<i class="fas fa-icon"></i>` inside the visual panel.
                7. The FINAL slide must include the signature box exactly as:
                   <div class="signature-box">
                        <div class="signature-title">صادر عن</div>
                        <div class="signature-name">الجهاز المركزي للجودة الشاملة</div>
                        <div class="signature-name">وحدة التخطيط الاستراتيجي والتطوير</div>
                   </div>
                8. DO NOT output the Javascript or CSS, only the HTML body content.
                """
                # للعرض التقديمي، التوقيع يكون داخل الشريحة الأخيرة، لذا نلغي التوقيع العام ونضع أزرار التحكم
                unified_signature = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                <div class="page-number" id="page-num">1 / 1</div>
                """

            # 3. هندسة الأمر (Prompt) - صارمة جداً لعدم الاختصار
            prompt = f"""
            You are an expert Data Analyst & Developer for 'Al-Hikma National Movement'.
            **Objective:** Create a FULL, DETAILED HTML report.
            
            **CRITICAL INSTRUCTIONS:**
            1. **FULL CONTENT:** Do NOT summarize. Process every single detail, number, and name from the input. The report must be exhaustive.
            2. **DATE:** Do NOT force a specific year. Detect the date from the input text. If not found, use the current context or leave generic.
            3. **FORMAT:** Output ONLY valid HTML code (inside <body> tags). Do not include ```html markers.
            4. **DESIGN:** Follow these specific design rules:
            {design_rules}
            
            **INPUT DATA:**
            {full_text}
            
            **LANGUAGE:** Arabic (Professional).
            """

            with st.spinner('🤖 جاري تحليل البيانات وتوليد التقرير الكامل (بدون اختصار)...'):
                response = model.generate_content(prompt)
                # تنظيف الرد من أي شوائب
                html_body = clean_html_response(response.text)
                
                # تجميع الملف النهائي
                final_html = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>تقرير {file_label}</title>
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

            st.success("✅ تم الإنشاء بنجاح!")
            # عرض معاينة
            st.components.v1.html(final_html, height=850, scrolling=True)

            # زر التحميل
            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=final_html,
                file_name=f"{file_label}.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"حدث خطأ أثناء المعالجة: {e}")
