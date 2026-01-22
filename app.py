import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import pandas as pd
from io import StringIO
import time
import streamlit.components.v1 as components
import re
from datetime import datetime

# استيراد التصاميم من ملف styles.py (نفس الملف الذي لديك)
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

if 'preview_report' not in st.session_state:
    st.session_state.preview_report = None

if 'preview_title' not in st.session_state:
    st.session_state.preview_title = ""

# تهيئة حالة الشريط الجانبي
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة (هنا يتم التحكم بفتح/غلق الشريط)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state # يعتمد على القيمة المحفوظة
)

# تطبيق التصميم الرئيسي
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🛠️ دوال المساعدة (نفس دوالك الأصلية)
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
    if match: return match.group(1).strip()
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match: return match.group(1).strip()
    match = re.search(r"(<html|<!DOCTYPE)(.*)", text, re.DOTALL)
    if match: return match.group(1) + match.group(2)
    return text.strip()

# الدالة الذكية لاختيار الموديل (لتجنب مشاكل Quota و 404)
def get_best_available_model():
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        # البحث بالأولوية
        for m in available_models:
            if 'gemini-1.5-flash' in m and 'exp' not in m and '002' not in m: return m 
        for m in available_models:
            if 'gemini-1.5-pro' in m and 'exp' not in m: return m
        for m in available_models:
            if 'gemini-pro' in m and '1.0' in m: return m
        for m in available_models:
            if 'exp' not in m and '2.0' not in m: return m
        return "models/gemini-1.5-flash"
    except:
        return "models/gemini-pro"

# ---------------------------------------------------------
# 📚 دوال التخزين المؤقت
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

def delete_report(report_id):
    st.session_state.reports_history = [
        r for r in st.session_state.reports_history if r['id'] != report_id
    ]

def clear_all_reports():
    st.session_state.reports_history = []
    st.session_state.preview_report = None

# ---------------------------------------------------------
# 📚 الشريط الجانبي (Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    # زر الإغلاق: يغير الحالة ثم يعيد تحميل الصفحة ليتم التطبيق
    if st.button("✖️ إغلاق السجل", key="close_sidebar_btn", use_container_width=True):
        st.session_state.sidebar_state = "collapsed"
        st.rerun() # <--- الحل السحري: إعادة تحميل لتطبيق الإغلاق

    reports_count = len(st.session_state.reports_history)
    
    st.markdown(f'''
    <div class="sidebar-header">
        <div class="sidebar-icon">📚</div>
        <div class="sidebar-title">سجل التقارير</div>
        <div class="sidebar-badge">{reports_count}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-hint">التقارير تُحفظ مؤقتاً خلال الجلسة</p>', unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,215,0,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
    
    if reports_count > 0:
        if st.button("🗑️ مسح جميع التقارير", key="clear_all", use_container_width=True):
            clear_all_reports()
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for report in st.session_state.reports_history:
            st.markdown(f'''
            <div class="sidebar-report-card">
                <div class="report-card-title">📄 {report['title']}</div>
                <div class="report-card-meta">
                    <span>{report['type']}</span><span>•</span><span>{report['size']}</span>
                </div>
                <div class="report-card-time">🕐 {report['timestamp']}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👁️ معاينة", key=f"view_{report['id']}", use_container_width=True):
                    st.session_state.preview_report = report['html']
                    st.session_state.preview_title = report['title']
                    st.session_state.sidebar_state = "collapsed" # إغلاق السجل عند المعاينة
                    st.rerun()
            with col2:
                st.download_button(label="📥 تحميل", data=report['html'], file_name=f"{report['title']}.html", mime="text/html", key=f"dl_{report['id']}", use_container_width=True)
            
            if st.button("🗑️ حذف", key=f"del_{report['id']}", use_container_width=True):
                delete_report(report['id'])
                if st.session_state.preview_title == report['title']:
                    st.session_state.preview_report = None
                st.rerun()
            st.markdown("<hr style='border: 1px solid rgba(255,215,0,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
    else:
        st.markdown('''<div class="sidebar-empty"><div class="empty-icon">📭</div><div class="empty-text">لا توجد تقارير</div></div>''', unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ بناء الواجهة الرئيسية
# ---------------------------------------------------------

# الهيدر الرئيسي
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

# زر فتح السجل في الواجهة الرئيسية
reports_count = len(st.session_state.reports_history)
col_spacer1, col_btn, col_spacer2 = st.columns([1.5, 2, 1.5])

with col_btn:
    # الحل السحري هنا: نغير الحالة ثم نعيد التحميل st.rerun()
    if st.button(f"📚 فتح سجل التقارير ({reports_count})", key="open_sidebar_main_btn", use_container_width=True):
        st.session_state.sidebar_state = "expanded"
        st.rerun() # <--- هذا السطر هو الذي سيجعل الزر يعمل فوراً

# عرض المعاينة
if st.session_state.preview_report:
    st.markdown(f'''<div class="preview-banner"><span>👁️ معاينة: {st.session_state.preview_title}</span></div>''', unsafe_allow_html=True)
    components.html(st.session_state.preview_report, height=600, scrolling=True)
    if st.button("❌ إغلاق المعاينة", key="close_preview", use_container_width=True):
        st.session_state.preview_report = None
        st.session_state.preview_title = ""
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

# عنوان اختيار النمط
st.markdown('<div class="section-header">🎨 اختر نمط الإخراج المطلوب</div>', unsafe_allow_html=True)

# أزرار الاختيار
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
    st.markdown('''<div class="input-card"><div class="input-header"><div class="input-icon">📝</div><div><div class="input-title">البيانات / الملاحظات</div><div class="input-subtitle">أدخل النص أو الصق محتوى التقرير هنا</div></div></div></div>''', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات...", label_visibility="collapsed")

with col_upload:
    st.markdown('''<div class="input-card"><div class="input-header"><div class="input-icon">📎</div><div><div class="input-title">رفع الملفات</div><div class="input-subtitle">PDF, XLSX, TXT - حتى 200MB</div></div></div></div>''', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"✅ تم إرفاق: {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

# زر المعالجة
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API.")
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
            
            # البحث الذكي عن الموديل (تجنب 404 و 429)
            selected_model = get_best_available_model()
            
            # إعدادات صارمة (تجنب الهلوسة)
            generation_config = genai.types.GenerationConfig(
                temperature=0.0,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
            )
            
            model = genai.GenerativeModel(selected_model)

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
                file_label, report_type_short = "Official_Report", "📄 رسمي"
                design_rules = """Style: Official Corporate Report. Wrap cards in <div class="card">. Use HTML <table> inside cards. Use <ul> with <li><span>Label</span> <span class="value">Value</span></li>."""
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label, report_type_short = "Digital_Dashboard", "📱 رقمي"
                design_rules = """Style: Modern Digital Dashboard. Use <section id="summary">. Use <article class="card">. Use <div class="goal">."""
            
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label, report_type_short = "Deep_Analysis", "📊 تحليلي"
                design_rules = """Style: Statistical Hierarchy. Use <div class="stats-grid">. Use <div class="pyramid-grid">. Use <div class="tier-card tier-upper">. Use <div class="bar-container">."""
            
            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE
                file_label, report_type_short = "Executive_Summary", "✨ تنفيذي"
                design_rules = """Style: Modern Executive Summary. Use <h1> for header. Use <div class="executive-summary">. Use <div class="grid-2"> with <div class="metric-box">."""

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label, report_type_short = "Presentation_Slides", "📽️ عرض"
                design_rules = """Style: Interactive Presentation Slides. Output HTML `div` elements with class `slide`. First slide `<div class="slide cover active" id="slide-1">`. Use `<div class="slide-content">`."""
                unified_signature = """<div class="nav-controls"><button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button><button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button></div><div class="page-number" id="page-num">1 / 1</div>"""

            prompt = f"""
            You are a strict Data Analyst.
            Objective: Convert input to HTML Report.
            
            CRITICAL RULES:
            1. Output ONLY raw HTML code inside ```html block.
            2. Copy names EXACTLY.
            3. Fix reversed Arabic letters.
            4. Rules: {design_rules}
            
            INPUT:
            {full_text}
            
            Language: Arabic.
            """

            progress_placeholder = st.empty()
            for i in range(0, 90, 10):
                progress_placeholder.markdown(f'<div class="progress-box"><div style="font-size: 2rem;">🤖</div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {i}%;"></div></div><div class="progress-text">جاري المعالجة... {i}%</div></div>', unsafe_allow_html=True)
                time.sleep(0.1)
            
            try:
                response = model.generate_content(prompt, generation_config=generation_config)
                
                if response.prompt_feedback.block_reason:
                    st.error("⚠️ تم حظر المحتوى.")
                    st.stop()
                    
                html_body = clean_html_response(response.text)
                progress_placeholder.empty()
                
                final_html = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{file_label}</title><link href="[https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;700&display=swap](https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;700&display=swap)" rel="stylesheet">{target_css}</head><body><div class="{ 'presentation-container' if 'عرض تقديمي' in report_type else 'container' }">{html_body}{unified_signature}</div>{SCRIPT_PRESENTATION if 'عرض تقديمي' in report_type else ''}</body></html>"""

                save_report_to_history(file_label, report_type_short, final_html, source_file_name)

                st.markdown('<div class="success-banner"><span>✅ تم إنشاء التقرير وحفظه في السجل بنجاح!</span></div>', unsafe_allow_html=True)
                st.markdown('<div class="success-hint">💡 يمكنك الوصول للتقارير المحفوظة من زر "فتح سجل التقارير" أعلاه</div>', unsafe_allow_html=True)
                
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
st.markdown('''<div style="background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9)); border-radius: 15px; padding: 30px 20px; margin: 20px; border: 1px solid rgba(255, 215, 0, 0.3); text-align: center; box-shadow: 0 -5px 30px rgba(0, 0, 0, 0.3);"><div style="width: 60px; height: 3px; background: linear-gradient(90deg, transparent, #FFD700, transparent); margin: 0 auto 20px auto; border-radius: 2px;"></div><p style="color: #FFD700; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; font-family: 'Tajawal', sans-serif;">الجهاز المركزي للجودة الشاملة</p><p style="color: rgba(255, 255, 255, 0.8); font-size: 1rem; font-weight: 500; margin-bottom: 15px; font-family: 'Tajawal', sans-serif;">وحدة التخطيط الاستراتيجي والتطوير</p><div style="width: 100px; height: 1px; background: rgba(255, 215, 0, 0.3); margin: 15px auto;"></div><p style="color: rgba(255, 255, 255, 0.5); font-size: 0.85rem; font-family: 'Tajawal', sans-serif;">جميع الحقوق محفوظة © 2026</p></div>''', unsafe_allow_html=True)
