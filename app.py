import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import pandas as pd
from io import StringIO
import time
import streamlit.components.v1 as components
import re
from datetime import datetime

# استيراد التصاميم من ملف styles.py
from styles import (
    MAIN_CSS,
    CUSTOM_SIDEBAR_CSS,
    STYLE_OFFICIAL,
    STYLE_DIGITAL,
    STYLE_ANALYTICAL,
    STYLE_PRESENTATION,
    STYLE_EXECUTIVE,
    SCRIPT_PRESENTATION
)

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = None

# ---------------------------------------------------------
# 📦 تهيئة التخزين المؤقت
# ---------------------------------------------------------
if 'reports_history' not in st.session_state:
    st.session_state.reports_history = []

if 'preview_report' not in st.session_state:
    st.session_state.preview_report = None

if 'preview_title' not in st.session_state:
    st.session_state.preview_title = ""

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------
def extract_text_from_file(uploaded_file):
    text_content = ""
    try:
        if uploaded_file.type == "application/pdf":
            try:
                doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
                for page in doc:
                    text_content += page.get_text() + "\n"
            except Exception as pdf_err:
                return f"⚠️ خطأ في قراءة PDF: {pdf_err}"
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            try:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
                text_content = df.to_csv(index=False)
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
    match = re.search(r"```html(.*?)```", text, re.DOTALL)
    if match: return match.group(1).strip()
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match: return match.group(1).strip()
    return text.strip()

def get_best_available_model():
    return "models/gemini-1.5-flash"

# ---------------------------------------------------------
# 📚 دوال التخزين والعرض
# ---------------------------------------------------------
def save_report_to_history(title, report_type, html_content, source_name=""):
    report_entry = {
        'id': int(time.time() * 1000),
        'title': title,
        'type': report_type,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'html': html_content,
        'source': source_name,
        'size': f"{len(html_content) / 1024:.1f} KB"
    }
    st.session_state.reports_history.insert(0, report_entry)
    if len(st.session_state.reports_history) > 10:
        st.session_state.reports_history = st.session_state.reports_history[:10]

def render_custom_sidebar():
    reports_count = len(st.session_state.reports_history)
    reports_html = ""
    if reports_count > 0:
        for i, report in enumerate(st.session_state.reports_history):
            title_short = report['title'][:20] + "..." if len(report['title']) > 20 else report['title']
            reports_html += f"""<div class="sidebar-report-card"><div class="report-title">📄 {title_short}</div><div class="report-meta"><span>{report['type']}</span></div></div>"""
    else:
        reports_html = """<div class="sidebar-empty"><div class="empty-text">لا توجد تقارير</div></div>"""
    
    return f"""
    <div class="custom-sidebar" id="customSidebar">
        <div class="sidebar-strip">
            <div class="strip-btn" onclick="document.getElementById('customSidebar').classList.toggle('expanded')">☰</div>
            <div class="strip-btn">📊</div>
        </div>
        <div class="sidebar-panel">
            <div class="sidebar-header"><h3>السجل ({reports_count})</h3></div>
            {reports_html}
        </div>
    </div>
    """

st.markdown(CUSTOM_SIDEBAR_CSS, unsafe_allow_html=True)
st.markdown(render_custom_sidebar(), unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الواجهة الرئيسية
# ---------------------------------------------------------
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="section-header">🎨 اختر نمط التقرير (جميع التصاميم بخلفية بيضاء احترافية)</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ التقرير الرسمي (أبيض/أزرق)", "📱 الداشبورد الرقمي (أبيض/ملون)", "📊 التحليل البياني (أبيض)", "📽️ عرض تقديمي (شرائح بيضاء)", "✨ ملخص تنفيذي"),
    horizontal=True,
    label_visibility="collapsed"
)

col1, col2 = st.columns([2, 1])
with col1:
    user_text = st.text_area("البيانات:", height=150, placeholder="أدخل النص هنا...")
with col2:
    uploaded_file = st.file_uploader("رفع ملف (PDF/Excel)", type=['pdf', 'xlsx'])

if st.button("🚀 إنشاء التقرير الآن"):
    if not API_KEY:
        st.error("المفتاح مفقود!")
        st.stop()
        
    full_text = user_text
    source_file_name = ""
    if uploaded_file:
        source_file_name = uploaded_file.name
        content = extract_text_from_file(uploaded_file)
        full_text += f"\n\n[الملف]:\n{content}"
    
    full_text = clean_input_text(full_text)
    if not full_text:
        st.warning("الرجاء إدخال بيانات.")
        st.stop()

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # إعداد التصميم المختار
        target_css = ""
        design_instructions = ""
        
        # التوقيع الموحد (يُضاف تلقائياً للكود النهائي)
        unified_signature = """
        <div class="report-signature">
            <div class="signature-line"></div>
            <div class="signature-icon">🦅</div>
            <p class="signature-org">صادر من الجهاز المركزي للجودة الشاملة</p>
            <p class="signature-unit">وحدة التخطيط الاستراتيجي والتطوير</p>
            <div class="signature-line"></div>
        </div>
        """

        if "الرسمي" in report_type:
            target_css = STYLE_OFFICIAL
            design_instructions = """
            Design: Clean Official White Paper.
            Structure:
            - <header><h1>Title</h1><p>Subtitle</p></header>
            - <div class="stats-row"><div class="stat-item">...</div></div>
            - Sections with <h2>
            - Standard <table>
            - <ul> lists
            """
        elif "الرقمي" in report_type:
            target_css = STYLE_DIGITAL
            design_instructions = """
            Design: Modern Light Dashboard (White Background).
            Structure:
            - <div class="dashboard-header">...</div>
            - <div class="metrics-grid"><div class="metric-card">...</div></div>
            - <div class="data-card">...</div>
            """
        elif "التحليل" in report_type:
            target_css = STYLE_ANALYTICAL
            design_instructions = "Design: Analytical Report, White background, Clear Charts."
        elif "عرض تقديمي" in report_type:
            target_css = STYLE_PRESENTATION
            design_instructions = """
            Structure:
            <div class="slide cover active" id="slide-1">...</div>
            <div class="slide" id="slide-2">...</div>
            Note: Use white background for slides.
            """
            unified_signature = '<div class="signature-box">صادر من الجهاز المركزي للجودة الشاملة</div><div class="nav-controls"><button class="nav-btn" onclick="prevSlide()">السابق</button><button class="nav-btn" onclick="nextSlide()">التالي</button></div><div class="page-number" id="page-num">1 / 1</div>'
        else:
            target_css = STYLE_EXECUTIVE
            design_instructions = "Simple Executive Summary on White paper."

        # Prompt
        prompt = f"""
        حول البيانات التالية إلى تقرير HTML كامل.
        
        القواعد:
        1. الخلفية يجب أن تكون بيضاء (White Background) في كل الأقسام.
        2. استخدم التصميم التالي: {design_instructions}
        3. لا تكتب التوقيع في النص، سأضيفه أنا برمجياً.
        4. اللغة عربية فصحى.
        5. أعطني فقط كود HTML داخل Body.

        البيانات:
        {full_text}
        """

        with st.spinner("جاري الإعداد..."):
            response = model.generate_content(prompt)
            html_body = clean_html_response(response.text)
            
            final_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                {target_css}
            </head>
            <body>
                <div class="{ 'presentation-container' if 'عرض' in report_type else 'container' }">
                    {html_body}
                    {unified_signature if 'عرض' not in report_type else ''}
                </div>
                {unified_signature if 'عرض' in report_type else ''}
                {SCRIPT_PRESENTATION if 'عرض' in report_type else ''}
            </body>
            </html>
            """
            
            save_report_to_history("تقرير جديد", report_type, final_html, source_file_name)
            
            st.success("تم الإنشاء!")
            components.html(final_html, height=800, scrolling=True)
            st.download_button("تحميل التقرير", final_html, "report.html", "text/html")

    except Exception as e:
        st.error(f"خطأ: {e}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="footer-section"><p>الجهاز المركزي للجودة الشاملة © 2026</p></div>', unsafe_allow_html=True)
