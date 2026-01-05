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
# 🎨 القوالب والتصاميم (CSS Styles)
# ---------------------------------------------------------

# 1. القالب الرسمي (Strategic)
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

# 2. القالب الرقمي (Media)
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

# 3. القالب التحليلي (Analytical)
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
# 🚀 إعدادات الصفحة والتصميم
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي - الحكمة", page_icon="🦅", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');
    .stApp { background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%); font-family: 'Tajawal', sans-serif; color: white; direction: rtl; }
    .hero-section { background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8)); border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 20px; border: 1px solid rgba(255, 215, 0, 0.3); }
    .main-title { font-size: 45px; font-weight: 900; color: #FFD700; text-shadow: 0px 4px 10px rgba(0,0,0,0.5); }
    .stButton button { background: linear-gradient(45deg, #FFD700, #DAA520); color: #001f3f !important; font-weight: 900; border-radius: 50px; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الواجهة الرئيسية (التعديل هنا على المسميات)
# ---------------------------------------------------------

st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div style="color: #e0e0e0; font-size: 18px;">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية (محدثة بأسماء وظيفية)
with st.sidebar:
    st.header("⚙️ إخراج التقرير")
    st.markdown("اختر النمط الأنسب لطبيعة البيانات:")
    report_type = st.radio(
        "نوع القالب:",
        ("🏛️ نمط الكتاب الرسمي (Official)", 
         "📱 نمط الداشبورد الرقمي (Digital)", 
         "📊 نمط التحليل العميق (Analysis)")
    )
    st.success(f"النمط المختار: {report_type.split('(')[0]}")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 البيانات والمدخلات")
    user_text = st.text_area("أدخل نص التقرير أو الملاحظات هنا:", height=200)

with col2:
    st.markdown("### 📎 المصادر (اختياري)")
    uploaded_file = st.file_uploader("رفع ملف (PDF, Excel)", type=['pdf', 'xlsx', 'txt'])

# ---------------------------------------------------------
# 🧠 المنطق البرمجي
# ---------------------------------------------------------
if st.button("🚀 إنشاء التقرير الاحترافي"):
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('جاري استخراج البيانات...'):
            full_text += f"\n\n[محتوى الملف]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ يرجى إدخال بيانات أو رفع ملف.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            # تحديد المتغيرات بناءً على الاسم الجديد
            target_css = ""
            design_rules = ""
            
            # 1. القالب الرسمي (كان اسمه الاستراتيجي)
            if "Official" in report_type:
                target_css = STYLE_OFFICIAL
                design_rules = """
                Style: Official, High-End Corporate Report.
                - Use <div class="card"> for sections.
                - Use <div class="card full-width"> for wide sections.
                - Use HTML <table> inside cards for structured data.
                - Use <ul> with <li><span>Label</span> <span class="value">Value</span></li> for key stats.
                """
            
            # 2. القالب الرقمي (كان اسمه الإعلامي)
            elif "Digital" in report_type:
                target_css = STYLE_DIGITAL
                design_rules = """
                Style: Modern Digital Dashboard (Social Media style).
                - Use <section id="summary"> for highlights.
                - Use <article class="card"> for specific platform details.
                - Use <div class="goal"> for final recommendations.
                - Focus on readability and visual hierarchy.
                """
            
            # 3. القالب التحليلي
            else:
                target_css = STYLE_ANALYTICAL
                design_rules = """
                Style: Statistical & Hierarchical Analysis.
                - Use <div class="stats-grid"> for top KPIs.
                - Use <div class="pyramid-grid"> for tiered data (hierarchy).
                - Inside pyramid grid, use <div class="tier-card tier-upper"> (or middle/weak).
                - MUST calculate percentages and use <div class="bar-container"><div class="bar" style="width: X%;"></div></div>.
                """

            footer_content = """
            <footer>
                <p><strong>صادر من الجهاز المركزي للجودة الشاملة - وحدة التخطيط الاستراتيجي والتطوير</strong></p>
                <p>حقوق النشر محفوظة © 2026</p>
            </footer>
            """

            prompt = f"""
            You are an expert Data Analyst & Web Developer for 'Al-Hikma National Movement'.
            
            **OBJECTIVE:** Convert the provided raw text/data into a professional HTML report.

            **DESIGN CHOICE:** {report_type}
            **DESIGN RULES (Strictly Follow):**
            {design_rules}

            **DATA:**
            {full_text}

            **CSS TO EMBED:**
            {target_css}

            **INSTRUCTIONS:**
            1. Output ONLY valid HTML code.
            2. Do not summarize; include all details.
            3. Insert the provided CSS in <head>.
            4. Insert the provided Footer before </body>.
            5. Language: Arabic (Professional).

            Generate the full HTML now.
            """

            with st.spinner('جاري تحليل البيانات وتطبيق القالب المختار...'):
                response = model.generate_content(prompt)
                html_output = response.text.replace("```html", "").replace("```", "")

            st.success("✅ تم إنشاء التقرير بنجاح!")
            st.components.v1.html(html_output, height=800, scrolling=True)

            file_label = "Official_Report" if "Official" in report_type else "Digital_Report" if "Digital" in report_type else "Analysis_Report"
            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=html_output,
                file_name=f"{file_label}_2026.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
