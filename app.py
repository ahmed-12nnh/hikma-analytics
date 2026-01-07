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
# 🎨 إعدادات الصفحة والتصميم الفخم
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide")

# CSS الواجهة الرئيسية للموقع (Dark Navy & Gold)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* الهيدر الملكي */
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
        gap: 10px;
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
        padding: 10px 15px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        flex: 1;
        min-width: 120px;
        color: white !important;
        font-weight: bold;
        font-size: 0.9rem;
    }

    div[role="radiogroup"] label:hover {
        background-color: rgba(255, 215, 0, 0.15);
        border-color: #FFD700;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* الحقول */
    .stTextArea textarea, .stFileUploader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: right;
    }
    
    /* زر الإجراء */
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

    /* العناوين المخصصة */
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
# 🎨 القوالب (CSS & HTML Structures)
# ---------------------------------------------------------

# 1. القالب الرسمي (للمخاطبات)
STYLE_OFFICIAL = """
<style>
    :root { --navy-blue: #001f3f; --gold: #FFD700; --light-gold: #FFEB84; --white: #ffffff; --gray: #f4f4f4; --dark-gray: #333; }
    body { font-family: 'Tajawal', sans-serif; background-color: var(--gray); color: var(--dark-gray); line-height: 1.6; direction: rtl; text-align: right; }
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

# 2. القالب الرقمي (للشاشات)
STYLE_DIGITAL = """
<style>
    body { font-family: 'Cairo', sans-serif; line-height: 1.7; background-color: #f4f7f9; color: #333; direction: rtl; }
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

# 3. القالب التحليلي (للإحصائيات)
STYLE_ANALYTICAL = """
<style>
    body { font-family: 'Cairo', sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.7; direction: rtl; }
    .container { max-width: 1100px; margin: 20px auto; padding: 20px; }
    header { background-color: #004a99; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0, 74, 153, 0.2); }
    .report-section { background-color: #fff; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.07); margin-bottom: 25px; padding: 25px; }
    .report-section h2 { color: #004a99; border-bottom: 3px solid #0056b3; padding-bottom: 10px; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
    .stat-card { background-color: #eef5ff; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #d0e3ff; }
    .stat-card .value { font-size: 2.2rem; font-weight: 700; color: #004a99; }
    .pyramid-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    .tier-card { border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background-color: #fcfcfc; border-top: 6px solid; }
    .tier-upper { border-top-color: #d90429; } .tier-middle { border-top-color: #f7b801; } 
    .bar-container { background-color: #e0e0e0; border-radius: 5px; height: 12px; margin-top: 12px; }
    .bar { height: 100%; border-radius: 5px; }
    .tier-upper .bar { background-color: #d90429; } .tier-middle .bar { background-color: #f7b801; }
    footer { text-align: center; margin-top: 30px; color: #888; font-size: 0.9rem; border-top: 1px solid #ccc; padding-top: 20px;}
</style>
"""

# 4. 🔥 نمط العرض التقديمي التفاعلي (NEW: Presentation Mode)
STYLE_PRESENTATION = """
<style>
    :root { --primary-navy: #002b49; --primary-blue: #004e89; --gold-main: #c5a059; --white: #ffffff; --text-dark: #333333; }
    body { font-family: 'Cairo', sans-serif; background-color: var(--primary-navy); overflow: hidden; height: 100vh; width: 100vw; margin: 0; }
    .presentation-container { width: 100%; height: 100%; position: relative; background: radial-gradient(circle at center, #003865 0%, #002035 100%); }
    .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; visibility: hidden; transform: scale(0.95); transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1); display: flex; flex-direction: column; padding: 40px 60px; box-sizing: border-box; }
    .slide.active { opacity: 1; visibility: visible; transform: scale(1); z-index: 10; }
    
    /* Header */
    .slide-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--gold-main); padding-bottom: 15px; margin-bottom: 25px; flex-shrink: 0; }
    .header-title h2 { color: var(--gold-main); font-size: 2rem; margin: 0; font-weight: 800; }
    .header-logo { font-family: 'Tajawal'; color: var(--white); font-weight: bold; }
    
    /* Content Split */
    .slide-content { flex-grow: 1; display: flex; gap: 40px; height: 100%; overflow: hidden; }
    .text-panel { flex: 3; background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 30px; color: var(--text-dark); overflow-y: auto; border-right: 5px solid var(--gold-main); }
    .visual-panel { flex: 2; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--white); text-align: center; }
    
    /* Elements */
    h3 { color: var(--primary-blue); border-bottom: 1px dashed #ccc; padding-bottom: 5px; }
    p, li { font-size: 1.2rem; line-height: 1.8; }
    .icon-box { font-size: 5rem; color: var(--gold-main); margin-bottom: 20px; animation: float 4s infinite; }
    .stat-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid var(--gold-main); backdrop-filter: blur(5px); width: 100%; }
    
    /* Cover Slide */
    .slide.cover { align-items: center; justify-content: center; text-align: center; background: linear-gradient(135deg, var(--primary-navy) 30%, #001a2c 100%); }
    .cover-content { border: 2px solid var(--gold-main); padding: 60px; background: rgba(0,0,0,0.4); backdrop-filter: blur(5px); }
    .main-title-slide { font-size: 3.5rem; color: var(--white); text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    
    /* Controls */
    .nav-controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 100; }
    .nav-btn { background: transparent; border: 2px solid var(--gold-main); color: var(--gold-main); width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; transition: 0.3s; }
    .nav-btn:hover { background: var(--gold-main); color: var(--primary-navy); }
    
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script>
    let currentSlide = 1;
    function showSlide(n) {
        let slides = document.querySelectorAll('.slide');
        let total = slides.length;
        if (n > total) currentSlide = 1;
        if (n < 1) currentSlide = total;
        slides.forEach(s => s.classList.remove('active'));
        document.getElementById('slide-' + currentSlide).classList.add('active');
    }
    function nextSlide() { showSlide(++currentSlide); }
    function prevSlide() { showSlide(--currentSlide); }
    // Initialize
    setTimeout(() => showSlide(1), 500);
</script>
"""

# 5. ✨ نمط الملخص التنفيذي الحديث (NEW: Modern Executive)
STYLE_MODERN_EXECUTIVE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;800&display=swap');
    body { font-family: 'Tajawal', sans-serif; background-color: #ffffff; color: #222; direction: rtl; }
    .container { max-width: 900px; margin: 40px auto; padding: 40px; border: 1px solid #eee; box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
    
    /* Header */
    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid #000; padding-bottom: 20px; margin-bottom: 40px; }
    .brand { font-size: 1.5rem; font-weight: 800; letter-spacing: -1px; }
    .date { color: #888; font-size: 0.9rem; }
    
    /* Content */
    h1 { font-size: 3rem; font-weight: 900; line-height: 1.1; margin-bottom: 10px; color: #000; }
    .executive-summary { font-size: 1.4rem; line-height: 1.6; color: #444; margin-bottom: 40px; border-right: 5px solid #FFD700; padding-right: 20px; }
    
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
    .metric-box { padding: 20px; background: #f9f9f9; border-radius: 8px; }
    .metric-val { font-size: 2.5rem; font-weight: 800; color: #002b49; }
    .metric-lbl { font-size: 1rem; color: #666; text-transform: uppercase; letter-spacing: 1px; }
    
    .section-title { font-size: 1.2rem; font-weight: 800; text-transform: uppercase; margin-top: 30px; margin-bottom: 15px; color: #c5a059; }
    p { font-size: 1.1rem; color: #555; line-height: 1.8; }
    
    footer { margin-top: 60px; border-top: 1px solid #eee; padding-top: 20px; display: flex; justify-content: space-between; color: #999; font-size: 0.8rem; }
</style>
"""

# ---------------------------------------------------------
# 🛠️ الدوال المساعدة
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

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🏗️ واجهة التطبيق
# ---------------------------------------------------------

st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

# خيارات الأنماط (تحديث جديد)
st.markdown('<div style="text-align: center; margin-bottom: 15px; color: #FFD700; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">اختر نمط الإخراج المطلوب:</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ الكتاب الرسمي", "📱 الداشبورد الرقمي", "📊 التحليل العميق", "📽️ عرض تقديمي تفاعلي (PPT)", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

col_input, col_upload = st.columns([2, 1])

with col_input:
    st.markdown('<div class="custom-header">📝 البيانات / الملاحظات</div>', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب هنا أو اترك فارغاً عند رفع ملف...")

with col_upload:
    st.markdown('<div class="custom-header">📎 رفع الملفات</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'])
    if uploaded_file:
        st.success(f"تم: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 توليد التقرير الذكي"):
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري تحليل الملف...'):
            full_text += f"\n\n[محتوى الملف]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات للبدء.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            target_css = ""
            design_rules = ""
            file_label = "Report"
            
            # --- منطق الأنماط الجديد ---
            
            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Doc"
                design_rules = "Style: Official Report. Use <div class='card'>, HTML <table>, <ul> lists."

            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Dashboard"
                design_rules = "Style: Digital Dashboard. Use <section id='summary'>, <article class='card'>, <div class='goal'>."

            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                design_rules = "Style: Analytical Hierarchy. Use <div class='stats-grid'>, <div class='pyramid-grid'>, percentages."

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Presentation_Slides"
                design_rules = """
                Style: Interactive Reveal.js style Presentation.
                Structure:
                - Create 5 to 8 slides using <div class="slide" id="slide-N">.
                - Slide 1 must be <div class="slide cover active" id="slide-1">.
                - Inside slides, use <div class="slide-header">, <div class="slide-content">.
                - Split content into <div class="text-panel"> (for text) and <div class="visual-panel"> (for icons/stats).
                - Use FontAwesome icons <i class="fas fa-icon"></i>.
                - DO NOT write the Javascript or CSS, just the HTML body content for the slides.
                """
                
            elif "ملخص تنفيذي" in report_type:
                target_css = STYLE_MODERN_EXECUTIVE
                file_label = "Executive_Summary"
                design_rules = """
                Style: Modern Clean Executive Summary (White & Black & Gold).
                - Use <header> with <div class='brand'>AL-HIKMA</div>.
                - Use <div class='executive-summary'> for the main insight.
                - Use <div class='grid-2'> with <div class='metric-box'> for key numbers.
                """

            # الفوتر المشترك (ما عدا العرض التقديمي له فوتر خاص)
            footer_content = ""
            if "عرض تقديمي" not in report_type:
                footer_content = "<footer><p>صادر عن الجهاز المركزي للجودة الشاملة</p></footer>"
            else:
                # للعرض التقديمي نضيف أزرار التحكم
                footer_content = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                """

            prompt = f"""
            You are an expert Data Analyst for 'Al-Hikma National Movement'.
            **Task:** Convert data into a specific High-End HTML format.
            **Design Style:** {report_type}
            **Strict Design Rules:** {design_rules}
            **Input Data:** {full_text}
            
            **Output:** - Return ONLY the HTML Body Content (inside <body>).
            - Embed the provided CSS in <head>.
            - Insert the Footer/Controls at the end.
            - Language: Arabic.
            """

            with st.spinner('🤖 جاري الهندسة والتصميم...'):
                response = model.generate_content(prompt)
                html_output = response.text.replace("```html", "").replace("```", "")
                
                # تجميع الكود النهائي (لضمان وجود الستايل والسكريبت)
                final_html = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    {target_css}
                </head>
                <body>
                    {html_output}
                    {footer_content}
                </body>
                </html>
                """

            st.success("✅ تم الإنشاء بنجاح!")
            st.components.v1.html(final_html, height=800, scrolling=True)

            st.download_button(
                label="📥 تحميل الملف (HTML)",
                data=final_html,
                file_name=f"{file_label}_2026.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
