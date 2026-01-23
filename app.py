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
    SIDEBAR_CSS,
    STYLE_OFFICIAL,
    STYLE_DIGITAL,
    STYLE_ANALYTICAL,
    STYLE_PRESENTATION,
    STYLE_EXECUTIVE,
    SCRIPT_PRESENTATION,
    FONT_AWESOME_LINK
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

# ✅ [جديد] صفحة التنقل الحالية
if 'current_page' not in st.session_state:
    st.session_state.current_page = "platform"  # "platform" أو "reports"

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تطبيق التصميم الرئيسي
st.markdown(MAIN_CSS, unsafe_allow_html=True)
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

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

def get_best_available_model():
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        for m in available_models:
            if 'gemini-1.5-flash' in m and 'exp' not in m and '002' not in m:
                return m 
        
        for m in available_models:
            if 'gemini-1.5-pro' in m and 'exp' not in m:
                return m
                
        for m in available_models:
            if 'gemini-pro' in m and '1.0' in m:
                return m
        
        for m in available_models:
            if 'exp' not in m and '2.0' not in m:
                return m
                
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

# ---------------------------------------------------------
# 🎨 الشريط الجانبي (أزرار Streamlit فعلية)
# ---------------------------------------------------------
def render_sidebar():
    """الشريط الجانبي مع أزرار التنقل"""
    
    with st.container():
        st.markdown("""
        <div class="sidebar-container">
            <div class="sidebar-logo">🦅</div>
            <div class="sidebar-title">تيار الحكمة</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # زر المنصة الرئيسية
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            if st.button("🏠 المنصة الرئيسية", key="nav_platform", use_container_width=True,
                        type="primary" if st.session_state.current_page == "platform" else "secondary"):
                st.session_state.current_page = "platform"
                st.session_state.preview_report = None
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # زر التقارير المحفوظة
        reports_count = len(st.session_state.reports_history)
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            btn_label = f"📚 التقارير المحفوظة ({reports_count})"
            if st.button(btn_label, key="nav_reports", use_container_width=True,
                        type="primary" if st.session_state.current_page == "reports" else "secondary"):
                st.session_state.current_page = "reports"
                st.session_state.preview_report = None
                st.rerun()
        
        st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
        
        # معلومات إضافية
        st.markdown("""
        <div class="sidebar-info">
            <p>📊 الجلسة الحالية</p>
            <p class="info-count">{} تقرير</p>
        </div>
        """.format(reports_count), unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-footer-text">
            <p>الجهاز المركزي للجودة الشاملة</p>
            <p>وحدة التخطيط الاستراتيجي</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 📄 صفحة التقارير المحفوظة
# ---------------------------------------------------------
def render_reports_page():
    """صفحة عرض التقارير المحفوظة"""
    
    # الهيدر
    st.markdown('''
    <div class="page-header">
        <div class="page-icon">📚</div>
        <div class="page-title">التقارير المحفوظة</div>
        <div class="page-subtitle">جميع التقارير المُنشأة خلال الجلسة الحالية</div>
    </div>
    ''', unsafe_allow_html=True)
    
    reports = st.session_state.reports_history
    
    if not reports:
        # لا توجد تقارير
        st.markdown('''
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-title">لا توجد تقارير بعد</div>
            <div class="empty-text">قم بإنشاء تقرير من المنصة الرئيسية وسيظهر هنا</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🏠 العودة للمنصة الرئيسية", key="back_to_platform_empty", use_container_width=True):
            st.session_state.current_page = "platform"
            st.rerun()
        return
    
    # عرض المعاينة إذا كانت مفعّلة
    if st.session_state.preview_report:
        st.markdown(f'''
        <div class="preview-header">
            <span class="preview-icon">👁️</span>
            <span class="preview-title">معاينة: {st.session_state.preview_title}</span>
        </div>
        ''', unsafe_allow_html=True)
        
        components.html(st.session_state.preview_report, height=500, scrolling=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("❌ إغلاق المعاينة", key="close_preview_reports", use_container_width=True):
                st.session_state.preview_report = None
                st.session_state.preview_title = ""
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
    
    # إحصائيات سريعة
    st.markdown(f'''
    <div class="stats-bar">
        <div class="stat-item-small">
            <span class="stat-number">{len(reports)}</span>
            <span class="stat-label">إجمالي التقارير</span>
        </div>
        <div class="stat-item-small">
            <span class="stat-number">{sum(1 for r in reports if "رسمي" in r["type"])}</span>
            <span class="stat-label">تقارير رسمية</span>
        </div>
        <div class="stat-item-small">
            <span class="stat-number">{sum(1 for r in reports if "عرض" in r["type"])}</span>
            <span class="stat-label">عروض تقديمية</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # عرض البطاقات
    st.markdown('<div class="section-title">📋 البطاقات</div>', unsafe_allow_html=True)
    
    # عرض التقارير كبطاقات
    cols_count = min(len(reports), 3)
    rows = (len(reports) + cols_count - 1) // cols_count
    
    for row in range(rows):
        cols = st.columns(cols_count)
        for col_idx in range(cols_count):
            report_idx = row * cols_count + col_idx
            if report_idx < len(reports):
                report = reports[report_idx]
                with cols[col_idx]:
                    st.markdown(f'''
                    <div class="report-card">
                        <div class="card-header">
                            <span class="card-icon">📄</span>
                            <span class="card-type">{report['type']}</span>
                        </div>
                        <div class="card-title">{report['title']}</div>
                        <div class="card-meta">
                            <span>📦 {report['size']}</span>
                            <span>🕐 {report['timestamp']}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("👁️ معاينة", key=f"preview_{report_idx}", use_container_width=True):
                            st.session_state.preview_report = report['html']
                            st.session_state.preview_title = report['title']
                            st.rerun()
                    with btn_col2:
                        st.download_button(
                            label="💾 حفظ",
                            data=report['html'],
                            file_name=f"{report['title']}.html",
                            mime="text/html",
                            key=f"download_{report_idx}",
                            use_container_width=True
                        )
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # عرض الجدول
    st.markdown('<div class="section-title">📊 جدول التقارير</div>', unsafe_allow_html=True)
    
    # تحويل البيانات لجدول
    table_data = []
    for i, report in enumerate(reports):
        table_data.append({
            "#": i + 1,
            "العنوان": report['title'],
            "النوع": report['type'],
            "الحجم": report['size'],
            "التاريخ": report['timestamp']
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر العودة
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 العودة للمنصة الرئيسية", key="back_to_platform", use_container_width=True):
            st.session_state.current_page = "platform"
            st.rerun()

# ---------------------------------------------------------
# 🏠 صفحة المنصة الرئيسية
# ---------------------------------------------------------
def render_platform_page():
    """صفحة المنصة الرئيسية لإنشاء التقارير"""
    
    # الهيدر الرئيسي
    st.markdown('''
    <div class="hero-section">
        <div class="hero-logo">🦅</div>
        <div class="hero-title">تيار الحكمة الوطني</div>
        <div class="hero-subtitle">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # إشعار بعدد التقارير
    if st.session_state.reports_history:
        st.markdown(f'''
        <div class="info-banner">
            <span>📚</span> لديك <strong>{len(st.session_state.reports_history)}</strong> تقرير محفوظ - 
            <span style="cursor:pointer; text-decoration:underline;">انقر على "التقارير المحفوظة" للعرض</span>
        </div>
        ''', unsafe_allow_html=True)
    
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
    if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل", use_container_width=True):
        process_report(user_text, uploaded_file, report_type)

# ---------------------------------------------------------
# ⚙️ معالجة إنشاء التقرير
# ---------------------------------------------------------
def process_report(user_text, uploaded_file, report_type):
    """معالجة إنشاء التقرير"""
    
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
        return
    
    try:
        genai.configure(api_key=API_KEY)
        
        selected_model = get_best_available_model()
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=16384,
        )
        
        model = genai.GenerativeModel(selected_model)

        target_css = ""
        design_rules = ""
        file_label = "Report"
        report_type_short = ""
        is_presentation = False
        
        # التوقيع الموحد
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
            file_label = "Official_Report"
            report_type_short = "📄 رسمي"
            design_rules = """
            Style: Official Professional Report (White Background).
            Structure:
            - Use <header> for title
            - Use <div class="card"> for content sections
            - Use Standard <table class="data-table">
            - Use <div class="stats-row"> for statistics
            - **BACKGROUND MUST BE WHITE**
            """
        
        elif "الرقمي" in report_type:
            target_css = STYLE_DIGITAL
            file_label = "Digital_Dashboard"
            report_type_short = "📱 رقمي"
            design_rules = """
            Style: Modern Light Dashboard (White Background).
            Structure:
            - Use <div class="dashboard-header">
            - Use <div class="metrics-grid"> with <div class="metric-card">
            - Use <div class="data-card"> for details
            - **BACKGROUND MUST BE WHITE**
            """
        
        elif "التحليل" in report_type:
            target_css = STYLE_ANALYTICAL
            file_label = "Deep_Analysis"
            report_type_short = "📊 تحليلي"
            design_rules = """
            Style: Analytical Report (White Background).
            Structure:
            - Use <header class="analysis-header">
            - Use <div class="stats-grid">
            - Use <div class="analysis-section">
            - **BACKGROUND MUST BE WHITE**
            """
        
        elif "ملخص" in report_type:
            target_css = STYLE_EXECUTIVE
            file_label = "Executive_Summary"
            report_type_short = "✨ تنفيذي"
            design_rules = """
            Style: Clean Executive Summary (White Background).
            Structure:
            - Use <header class="exec-header">
            - Use <div class="exec-summary">
            - Use <div class="key-metrics">
            - **BACKGROUND MUST BE WHITE**
            """

        elif "عرض تقديمي" in report_type:
            target_css = STYLE_PRESENTATION
            file_label = "Presentation_Slides"
            report_type_short = "📽️ عرض"
            is_presentation = True
            design_rules = """
            Style: Presentation Slides (White Background).
            
            ⚠️ CRITICAL RULES FOR SLIDES:
            1. Each slide MUST have a unique id: id="slide-1", id="slide-2", id="slide-3", etc.
            2. First slide MUST have: <div class="slide cover active" id="slide-1">
            3. Other slides: <div class="slide" id="slide-2">, <div class="slide" id="slide-3">, etc.
            4. Use <div class="slide-header"> with <div class="header-title"><h2>Title</h2></div>
            5. Use <div class="slide-content"> for the main content
            6. Create 5-8 slides maximum
            7. **SLIDE BACKGROUND MUST BE WHITE**
            """

        # الـ PROMPT
        prompt = f"""
أنت محلل بيانات ومطور محترف. حول البيانات التالية إلى تقرير HTML كامل.

⚠️ القواعد الصارمة:
1. **الخلفية بيضاء (White Background)** لجميع التقارير.
2. استخدم بنية HTML المتوافقة مع الكلاسات التالية:
{design_rules}
3. لا تقم أبداً بإضافة "التوقيع" أو "الخاتمة" (صادر عن...) داخل النص. سأقوم أنا بإضافتها برمجياً في نهاية الملف.
4. اللغة العربية الفصحى.
5. أعطني كود HTML فقط داخل Body.

📊 البيانات:
{full_text}
"""

        progress_placeholder = st.empty()
        
        # شريط التحميل
        progress_messages = [
            "🔍 جاري تحليل البيانات...",
            "📊 استخراج المعلومات الرئيسية...",
            "🎨 تطبيق التصميم الاحترافي...",
            "✍️ إنشاء محتوى التقرير...",
            "🔧 معالجة النصوص العربية...",
            "📝 تنسيق الجداول والقوائم...",
            "🎯 إضافة اللمسات النهائية...",
            "✅ اكتمال المعالجة..."
        ]
        
        for i, msg in enumerate(progress_messages):
            progress_percent = int((i + 1) / len(progress_messages) * 100)
            progress_placeholder.markdown(f'''
            <div class="progress-box">
                <div class="progress-icon">🤖</div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {progress_percent}%;"></div>
                </div>
                <div class="progress-text">{msg} {progress_percent}%</div>
            </div>
            ''', unsafe_allow_html=True)
            time.sleep(0.2)
        
        try:
            response = model.generate_content(
                prompt, 
                generation_config=generation_config,
                request_options={"timeout": 120}
            )
            
            if response.prompt_feedback.block_reason:
                st.error("⚠️ تم حظر المحتوى من قبل Google AI لأسباب تتعلق بالسياسة أو السلامة.")
                st.stop()
                
            html_body = clean_html_response(response.text)
            
            progress_placeholder.empty()
            
            # تجميع الملف النهائي
            if is_presentation:
                final_html = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير {file_label}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    {FONT_AWESOME_LINK}
    {target_css}
</head>
<body>
    <div class="presentation-container">
        {html_body}
        
        <div class="nav-controls">
            <button class="nav-btn" onclick="prevSlide()" title="السابق">
                <i class="fas fa-chevron-right"></i>
            </button>
            <button class="nav-btn" onclick="nextSlide()" title="التالي">
                <i class="fas fa-chevron-left"></i>
            </button>
        </div>
        
        <div class="page-number" id="page-num">1 / 1</div>
        
        <div class="presentation-signature">
            صادر من الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي
        </div>
    </div>
    
    {SCRIPT_PRESENTATION}
</body>
</html>
"""
            else:
                final_html = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير {file_label}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    {target_css}
</head>
<body>
    <div class="container">
        {html_body}
        {unified_signature}
    </div>
</body>
</html>
"""

            save_report_to_history(
                title=file_label,
                report_type=report_type_short,
                html_content=final_html,
                source_name=source_file_name
            )

            st.markdown('''
            <div class="success-banner">
                <span>✅ تم إنشاء التقرير الكامل وحفظه بنجاح!</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('''
            <div class="success-hint">
                💡 يمكنك الوصول للتقارير المحفوظة من زر "التقارير المحفوظة" في الأعلى
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
            error_msg = str(api_error)
            if "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
                st.error("⚠️ انتهت مهلة الاتصال بالذكاء الاصطناعي. يرجى المحاولة مرة أخرى.")
            else:
                st.error(f"❌ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {api_error}")

    except Exception as e:
        st.error(f"❌ حدث خطأ غير متوقع: {e}")

# ---------------------------------------------------------
# 🚀 التطبيق الرئيسي
# ---------------------------------------------------------

# الشريط الجانبي
with st.sidebar:
    render_sidebar()

# عرض الصفحة المناسبة
if st.session_state.current_page == "platform":
    render_platform_page()
elif st.session_state.current_page == "reports":
    render_reports_page()

# الفوتر
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''
<div class="footer-section">
    <div class="footer-line"></div>
    <p class="footer-org">الجهاز المركزي للجودة الشاملة</p>
    <p class="footer-unit">وحدة التخطيط الاستراتيجي والتطوير</p>
    <div class="footer-divider"></div>
    <p class="footer-copy">جميع الحقوق محفوظة © 2026</p>
</div>
''', unsafe_allow_html=True)
