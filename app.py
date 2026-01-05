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
# 🎨 إعدادات الصفحة والتصميم الحديث (Modern UI)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide")

# CSS متطور جداً
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');
    
    /* إعدادات الخط والاتجاه */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* إخفاء القائمة الجانبية والهيدر الافتراضي */
    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* تصميم الهيدر الزجاجي */
    .hero-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 30px;
        animation: fadeIn 1s ease-in-out;
    }

    .main-title {
        font-size: 40px;
        font-weight: 900;
        background: linear-gradient(to right, #FFD700, #FDB931);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #e0e0e0;
        font-size: 16px;
        letter-spacing: 1px;
    }

    /* تنسيق أزرار الراديو (البطاقات العلوية) */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row-reverse;
        justify-content: center;
        gap: 15px;
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    div[role="radiogroup"] label {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        flex: 1;
        color: white !important;
    }

    div[role="radiogroup"] label:hover {
        background-color: rgba(255, 215, 0, 0.1);
        border-color: #FFD700;
        transform: translateY(-3px);
    }

    /* حقول الإدخال */
    .stTextArea textarea, .stFileUploader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: right;
    }
    
    /* زر التشغيل */
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
        box-shadow: 0 6px 20px rgba(218, 165, 32, 0.6);
    }

    /* أنيميشن */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* تنسيق العناوين المخصصة */
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
# 🎨 القوالب (CSS Styles)
# ---------------------------------------------------------
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
# 🏗️ بناء الواجهة (Layout)
# ---------------------------------------------------------

# 1. الهيدر
st.markdown("""
    <div class="hero-container">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

# 2. بطاقات الاختيار العلوية
st.markdown('<div style="text-align: center; margin-bottom: 10px; color: #FFD700; font-weight: bold;">اختر نمط التقرير المطلوب:</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

# 3. منطقة العمل (مع تعديل المحاذاة الدقيقة)
col_input, col_upload = st.columns([2, 1])

with col_input:
    # استخدام HTML لإجبار المحاذاة لليمين بدقة
    st.markdown('<div class="custom-header">📝 النص / البيانات الخام</div>', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...")

with col_upload:
    # استخدام HTML لإجبار المحاذاة لليمين بدقة
    st.markdown('<div class="custom-header">📎 ملفات مساعدة</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'])
    if uploaded_file:
        st.success(f"تم إرفاق: {uploaded_file.name}")

# 4. زر التنفيذ
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 بدء المعالجة وإنشاء التقرير"):
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            full_text += f"\n\n[محتوى الملف]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ لا توجد بيانات للتحليل! يرجى كتابة نص أو رفع ملف.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            target_css = ""
            design_rules = ""
            file_label = "Report"

            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Report"
                design_rules = """
                Style: Official Corporate Report.
                - Use <div class="card"> for sections.
                - Use HTML <table> inside cards.
                - Use <ul> with <li><span>Label</span> <span class="value">Value</span></li>.
                """
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                design_rules = """
                Style: Modern Digital Dashboard.
                - Use <section id="summary"> for highlights.
                - Use <article class="card"> for details.
                - Use <div class="goal"> for conclusion.
                """
            else: 
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                design_rules = """
                Style: Statistical Hierarchy.
                - Use <div class="stats-grid"> for numbers.
                - Use <div class="pyramid-grid"> for tiers.
                - Use <div class="bar-container"> for percentages.
                """

            footer_content = """
            <footer>
                <p><strong>صادر من الجهاز المركزي للجودة الشاملة - وحدة التخطيط الاستراتيجي والتطوير</strong></p>
                <p>حقوق النشر محفوظة © 2026</p>
            </footer>
            """

            prompt = f"""
            You are an expert Data Analyst for 'Al-Hikma National Movement'.
            **Role:** Convert raw data into a specific HTML format.
            **Design Rules:** {design_rules}
            **Input Data:** {full_text}
            **Instructions:**
            1. Output ONLY valid HTML code.
            2. Embed the following CSS in <head>: {target_css}
            3. Insert this footer before </body>: {footer_content}
            4. Language: Arabic.
            """

            with st.spinner('🤖 جاري التحليل وصياغة التقرير...'):
                response = model.generate_content(prompt)
                html_output = response.text.replace("```html", "").replace("```", "")

            st.success("✅ تم إنشاء التقرير بنجاح!")
            st.components.v1.html(html_output, height=800, scrolling=True)

            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=html_output,
                file_name=f"{file_label}_2026.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
