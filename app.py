import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import pandas as pd
from io import StringIO
import time
import streamlit.components.v1 as components
import re
from datetime import datetime  # <--- إضافة جديدة

# استيراد التصاميم من ملف styles.py
from styles import (
    MAIN_CSS,
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
# 📦 تهيئة التخزين المؤقت (Session State)
# ---------------------------------------------------------
if 'reports_history' not in st.session_state:
    st.session_state.reports_history = []

if 'show_history' not in st.session_state:
    st.session_state.show_history = False

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة وتطبيق الـ CSS الرئيسي
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تطبيق التصميم الرئيسي من الملف الخارجي
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    """استخراج النص باستخدام مكتبة fitz (PyMuPDF)"""
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
        return f"⚠️ خطأ عام في قراءة الملف: {e}"
        
    if not text_content.strip():
        return "⚠️ تحذير: الملف يبدو فارغاً."
        
    return text_content

def clean_input_text(text):
    if not text: return ""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

def clean_html_response(text):
    match = re.search(r"```html(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    match = re.search(r"(<html|<!DOCTYPE)(.*)", text, re.DOTALL)
    if match:
        return match.group(1) + match.group(2)
    
    return text.strip()

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name:
                    return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

# ---------------------------------------------------------
# 📚 دالة حفظ التقرير في السجل
# ---------------------------------------------------------
def save_report_to_history(title, report_type, html_content, source_name=""):
    """حفظ التقرير في سجل الجلسة"""
    report_entry = {
        'id': len(st.session_state.reports_history) + 1,
        'title': title,
        'type': report_type,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'html': html_content,
        'source': source_name,
        'size': f"{len(html_content) / 1024:.1f} KB"
    }
    st.session_state.reports_history.insert(0, report_entry)  # الأحدث أولاً
    
    # الاحتفاظ بآخر 10 تقارير فقط لتوفير الذاكرة
    if len(st.session_state.reports_history) > 10:
        st.session_state.reports_history = st.session_state.reports_history[:10]

def delete_report(report_id):
    """حذف تقرير من السجل"""
    st.session_state.reports_history = [
        r for r in st.session_state.reports_history if r['id'] != report_id
    ]

def clear_all_reports():
    """مسح جميع التقارير"""
    st.session_state.reports_history = []

# ---------------------------------------------------------
# 🏗️ بناء الواجهة
# ---------------------------------------------------------

# الهيدر الرئيسي
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

# ---------------------------------------------------------
# 📚 شريط سجل التقارير (أعلى الصفحة)
# ---------------------------------------------------------
reports_count = len(st.session_state.reports_history)

st.markdown(f'''
<div class="history-toggle-bar">
    <div class="history-info">
        <span class="history-icon">📚</span>
        <span class="history-text">سجل التقارير المؤقت</span>
        <span class="history-badge">{reports_count}</span>
    </div>
</div>
''', unsafe_allow_html=True)

# زر عرض/إخفاء السجل
col_toggle, col_clear = st.columns([4, 1])

with col_toggle:
    if st.button(f"{'🔽 إخفاء' if st.session_state.show_history else '🔼 عرض'} سجل التقارير ({reports_count})", 
                 key="toggle_history", 
                 use_container_width=True):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()

with col_clear:
    if reports_count > 0:
        if st.button("🗑️ مسح الكل", key="clear_all", use_container_width=True):
            clear_all_reports()
            st.rerun()

# عرض سجل التقارير
if st.session_state.show_history and reports_count > 0:
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    
    for report in st.session_state.reports_history:
        st.markdown(f'''
        <div class="history-card">
            <div class="history-card-header">
                <div class="history-card-title">
                    <span class="report-icon">📄</span>
                    <span>{report['title']}</span>
                </div>
                <div class="history-card-badge">{report['type']}</div>
            </div>
            <div class="history-card-meta">
                <span>🕐 {report['timestamp']}</span>
                <span>📦 {report['size']}</span>
                {f"<span>📎 {report['source']}</span>" if report['source'] else ""}
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        col_view, col_download, col_delete = st.columns([2, 2, 1])
        
        with col_view:
            if st.button(f"👁️ معاينة", key=f"view_{report['id']}", use_container_width=True):
                st.session_state.preview_report = report['html']
                
        with col_download:
            st.download_button(
                label="📥 تحميل",
                data=report['html'],
                file_name=f"{report['title']}_{report['timestamp'].replace(':', '-')}.html",
                mime="text/html",
                key=f"download_{report['id']}",
                use_container_width=True
            )
        
        with col_delete:
            if st.button("🗑️", key=f"delete_{report['id']}", use_container_width=True):
                delete_report(report['id'])
                st.rerun()
        
        st.markdown("<hr style='border: 1px solid rgba(255,215,0,0.1); margin: 10px 0;'>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# معاينة التقرير المحدد
if 'preview_report' in st.session_state and st.session_state.preview_report:
    st.markdown('''
    <div class="preview-header">
        <span>👁️ معاينة التقرير</span>
    </div>
    ''', unsafe_allow_html=True)
    
    components.html(st.session_state.preview_report, height=600, scrolling=True)
    
    if st.button("❌ إغلاق المعاينة", use_container_width=True):
        st.session_state.preview_report = None
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

elif st.session_state.show_history and reports_count == 0:
    st.markdown('''
    <div class="empty-history">
        <div class="empty-icon">📭</div>
        <div class="empty-text">لا توجد تقارير محفوظة بعد</div>
        <div class="empty-hint">ستظهر التقارير هنا بعد إنشائها</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 اختيار النمط
# ---------------------------------------------------------
st.markdown('<div class="section-header">🎨 اختر نمط الإخراج المطلوب</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي (PPT)", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# منطقة الإدخال
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

# زر المعالجة
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. يرجى إضافته في Secrets.")
        st.stop()
    
    full_text = user_text
    source_file_name = ""
    
    if uploaded_file:
        source_file_name = uploaded_file.name
        with st.spinner('📂 جاري قراءة الملف ومعالجة النصوص العربية...'):
            file_content = extract_text_from_file(uploaded_file)
            if "⚠️" in file_content and len(file_content) < 200: 
                st.warning(file_content)
            full_text += f"\n\n[محتوى الملف]:\n{file_content}"

    full_text = clean_input_text(full_text)

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف صالح.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model_name = get_working_model()
            
            generation_config = genai.types.GenerationConfig(
                temperature=0.0,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
            )
            
            model = genai.GenerativeModel(model_name)

            target_css = ""
            design_rules = ""
            file_label = "Report"
            report_type_short = ""
            
            unified_signature = """
            <div style="margin-top: 50px; text-align: center; padding-top: 20px; border-top: 2px solid #ccc; font-family: 'Tajawal'; color: #555;">
                <p style="margin-bottom: 5px;"><strong>صادر من الجهاز المركزي للجودة الشاملة</strong></p>
                <p style="font-size: 1.1em; color: #001f3f;"><strong>وحدة التخطيط الاستراتيجي والتطوير</strong></p>
            </div>
            """

            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Report"
                report_type_short = "📄 رسمي"
                design_rules = """
                Style: Official Corporate Report.
                - Wrap card sections in <div class="card">.
                - Use HTML <table> inside cards for tabular data.
                - Use <ul> with <li><span>Label</span> <span class="value">Value</span></li> for lists.
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                report_type_short = "📱 رقمي"
                design_rules = """
                Style: Modern Digital Dashboard.
                - Use <section id="summary"> for highlights.
                - Use <article class="card"> for detailed sections.
                - Use <div class="goal"> for key takeaways.
                """
            
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                report_type_short = "📊 تحليلي"
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
                report_type_short = "✨ تنفيذي"
                design_rules = """
                Style: Modern Executive Summary.
                - Header is already provided in CSS, just use <h1>.
                - Use <div class="executive-summary"> for the main text.
                - Use <div class="grid-2"> with <div class="metric-box"> for key metrics.
                """

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Presentation_Slides"
                report_type_short = "📽️ عرض"
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
                unified_signature = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                <div class="page-number" id="page-num">1 / 1</div>
                """

            prompt = f"""
            You are a strict Data Analyst & Developer.
            **Objective:** Convert the provided text into a Professional HTML Report.
            
            **CRITICAL RULES (ZERO TOLERANCE):**
            1. **OUTPUT FORMAT:** You MUST wrap the HTML code inside a markdown block like this:
```html
               <!DOCTYPE html>
               ... code ...
```
               Do NOT include any text before or after this block.
            2. **NAMES PRESERVATION:** Copy person names EXACTLY (e.g. "بليغ ابو كلل").
            3. **REVERSED TEXT:** Fix reversed Arabic letters but keep words unchanged.
            4. **DESIGN:** Follow these rules:
            {design_rules}
            
            **INPUT DATA:**
            {full_text}
            
            **LANGUAGE:** Arabic (Professional).
            """

            progress_placeholder = st.empty()
            
            for i in range(0, 90, 10):
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🤖</div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {i}%;"></div>
                    </div>
                    <div class="progress-text">جاري معالجة البيانات وتصحيح النصوص... {i}%</div>
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(0.1)
            
            try:
                response = model.generate_content(prompt, generation_config=generation_config)
                
                if response.prompt_feedback.block_reason:
                    st.error("⚠️ تم حظر المحتوى من قبل Google AI لأسباب تتعلق بالسياسة أو السلامة.")
                    st.stop()
                    
                html_body = clean_html_response(response.text)
                
                progress_placeholder.empty()
                
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

                # ✅ حفظ التقرير في السجل
                save_report_to_history(
                    title=file_label,
                    report_type=report_type_short,
                    html_content=final_html,
                    source_name=source_file_name
                )

                st.markdown('''
                <div class="success-banner">
                    <span>✅ تم إنشاء التقرير وحفظه في السجل بنجاح!</span>
                </div>
                ''', unsafe_allow_html=True)
                
                components.html(final_html, height=850, scrolling=True)

                st.download_button(
                    label="📥 تحميل التقرير (HTML)",
                    data=final_html,
                    file_name=f"{file_label}.html",
                    mime="text/html"
                )
            
            except Exception as api_error:
                progress_placeholder.empty()
                st.error(f"❌ حدث خطأ أثناء الاتصال بـ Google AI: {api_error}")

        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {e}")

# الفوتر
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
