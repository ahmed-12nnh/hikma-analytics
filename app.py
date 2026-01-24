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

if 'current_page' not in st.session_state:
    st.session_state.current_page = "platform"

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التصميم الرئيسي
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    """استخراج النص من الملفات"""
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
    """تحديد أفضل نموذج متاح مع أولوية قصوى لنموذج Pro للدقة"""
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # 1. الأولوية القصوى لـ Gemini 1.5 Pro (الأذكى والأدق في الأسماء)
        for m in available_models:
            if 'gemini-1.5-pro' in m and 'exp' not in m:
                return m
        
        # 2. الخيار الثاني Gemini 1.5 Flash (الأسرع)
        for m in available_models:
            if 'gemini-1.5-flash' in m and 'exp' not in m and '002' not in m:
                return m 
                
        # 3. الخيارات القديمة
        for m in available_models:
            if 'gemini-pro' in m and '1.0' in m:
                return m
        
        for m in available_models:
            if 'exp' not in m and '2.0' not in m:
                return m
                
        return "models/gemini-1.5-pro" # محاولة فرض البرو
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
# 🎨 الشريط الجانبي (Streamlit Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    # الشعار والعنوان
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-name">تيار الحكمة الوطني</div>
        <div class="brand-subtitle">منصة التحليل الاستراتيجي</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    # قسم التنقل
    st.markdown("<div class='nav-section-title'>📍 التنقل</div>", unsafe_allow_html=True)
    
    # زر المنصة الرئيسية
    if st.button("🏠 المنصة الرئيسية", key="nav_platform", use_container_width=True,
                type="primary" if st.session_state.current_page == "platform" else "secondary"):
        st.session_state.current_page = "platform"
        st.session_state.preview_report = None
        st.rerun()
    
    # زر سجل التقارير
    reports_count = len(st.session_state.reports_history)
    if st.button(f"📚 سجل التقارير ({reports_count})", key="nav_reports", use_container_width=True,
                type="primary" if st.session_state.current_page == "reports" else "secondary"):
        st.session_state.current_page = "reports"
        st.session_state.preview_report = None
        st.rerun()
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    # إحصائيات الجلسة
    st.markdown(f"""
    <div class="session-stats">
        <div class="stats-title">📊 إحصائيات الجلسة</div>
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-value">{reports_count}</span>
                <span class="stat-label">تقرير</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{sum(1 for r in st.session_state.reports_history if "رسمي" in r.get("type", ""))}</span>
                <span class="stat-label">رسمي</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{sum(1 for r in st.session_state.reports_history if "عرض" in r.get("type", ""))}</span>
                <span class="stat-label">عرض</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # آخر التقارير
    if st.session_state.reports_history:
        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='nav-section-title'>📄 آخر التقارير</div>", unsafe_allow_html=True)
        
        for i, report in enumerate(st.session_state.reports_history[:3]):
            title_short = report['title'][:15] + "..." if len(report['title']) > 15 else report['title']
            st.markdown(f"""
            <div class="recent-report">
                <div class="report-icon">📄</div>
                <div class="report-info">
                    <div class="report-name">{title_short}</div>
                    <div class="report-meta">{report['type']} • {report['size']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # الفوتر
    st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-footer">
        <div class="footer-line"></div>
        <div class="footer-org">الجهاز المركزي للجودة الشاملة</div>
        <div class="footer-unit">وحدة التخطيط الاستراتيجي و التطوير</div>
        <div class="footer-copy">© 2026</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 📄 صفحة التقارير المحفوظة
# ---------------------------------------------------------
def render_reports_page():
    """صفحة عرض التقارير المحفوظة"""
    
    # الهيدر
    st.markdown("""
    <div class="page-header-reports">
        <div class="header-icon">📚</div>
        <h1 class="header-title">سجل التقارير المحفوظة</h1>
        <p class="header-subtitle">جميع التقارير المُنشأة خلال الجلسة الحالية</p>
    </div>
    """, unsafe_allow_html=True)
    
    reports = st.session_state.reports_history
    
    if not reports:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <h3 class="empty-title">لا توجد تقارير بعد</h3>
            <p class="empty-text">قم بإنشاء تقرير من المنصة الرئيسية وسيظهر هنا</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # عرض المعاينة إذا كانت مفعّلة
    if st.session_state.preview_report:
        st.markdown(f"""
        <div class="preview-banner">
            <span class="preview-icon">👁️</span>
            <span class="preview-text">معاينة: {st.session_state.preview_title}</span>
        </div>
        """, unsafe_allow_html=True)
        
        components.html(st.session_state.preview_report, height=500, scrolling=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("❌ إغلاق المعاينة", key="close_preview", use_container_width=True):
                st.session_state.preview_report = None
                st.session_state.preview_title = ""
                st.rerun()
        
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    # شريط الإحصائيات
    st.markdown(f"""
    <div class="stats-bar-reports">
        <div class="stat-box-report">
            <span class="stat-number">{len(reports)}</span>
            <span class="stat-text">إجمالي التقارير</span>
        </div>
        <div class="stat-box-report">
            <span class="stat-number">{sum(1 for r in reports if "رسمي" in r["type"])}</span>
            <span class="stat-text">تقارير رسمية</span>
        </div>
        <div class="stat-box-report">
            <span class="stat-number">{sum(1 for r in reports if "عرض" in r["type"])}</span>
            <span class="stat-text">عروض تقديمية</span>
        </div>
        <div class="stat-box-report">
            <span class="stat-number">{sum(1 for r in reports if "تحليل" in r["type"])}</span>
            <span class="stat-text">تقارير تحليلية</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # عنوان البطاقات
    st.markdown("<h2 class='section-title-reports'>📋 التقارير</h2>", unsafe_allow_html=True)
    
    # عرض البطاقات
    cols_count = min(len(reports), 3)
    rows = (len(reports) + cols_count - 1) // cols_count
    
    for row in range(rows):
        cols = st.columns(cols_count)
        for col_idx in range(cols_count):
            report_idx = row * cols_count + col_idx
            if report_idx < len(reports):
                report = reports[report_idx]
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="report-card">
                        <div class="card-header">
                            <span class="card-icon">📄</span>
                            <span class="card-badge">{report['type']}</span>
                        </div>
                        <h3 class="card-title">{report['title']}</h3>
                        <div class="card-meta">
                            <span>📦 {report['size']}</span>
                            <span>🕐 {report['timestamp']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("👁️ معاينة", key=f"preview_{report_idx}", use_container_width=True):
                            st.session_state.preview_report = report['html']
                            st.session_state.preview_title = report['title']
                            st.rerun()
                    with btn_col2:
                        st.download_button(
                            label="💾 تحميل",
                            data=report['html'],
                            file_name=f"{report['title']}.html",
                            mime="text/html",
                            key=f"download_{report_idx}",
                            use_container_width=True
                        )
    
    # الجدول
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title-reports'>📊 جدول التقارير</h2>", unsafe_allow_html=True)
    
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

# ---------------------------------------------------------
# 🏠 صفحة المنصة الرئيسية
# ---------------------------------------------------------
def render_platform_page():
    """صفحة المنصة الرئيسية لإنشاء التقارير"""
    
    # الهيدر الرئيسي
    st.markdown("""
    <div class="hero-section">
        <div class="hero-glow"></div>
        <div class="hero-content">
            <h1 class="hero-title">تيار الحكمة الوطني</h1>
            <p class="hero-subtitle">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي والتطوير</p>
            <div class="hero-line"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # عنوان اختيار النمط
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🎨</span>
        <span class="section-text">اختر نمط الإخراج المطلوب</span>
        <span class="section-note">(جميع التصاميم بخلفية بيضاء احترافية)</span>
    </div>
    """, unsafe_allow_html=True)
    
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
        st.markdown("""
        <div class="input-card">
            <div class="input-header">
                <div class="input-icon-box">📝</div>
                <div class="input-info">
                    <h3 class="input-title">البيانات / الملاحظات</h3>
                    <p class="input-desc">أدخل النص أو الصق محتوى التقرير هنا</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        user_text = st.text_area("", height=200, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...", label_visibility="collapsed")
    
    with col_upload:
        st.markdown("""
        <div class="input-card">
            <div class="input-header">
                <div class="input-icon-box">📎</div>
                <div class="input-info">
                    <h3 class="input-title">رفع الملفات</h3>
                    <p class="input-desc">PDF, XLSX, TXT - حتى 200MB</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
        
        if uploaded_file:
            st.success(f"✅ تم إرفاق: {uploaded_file.name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر المعالجة
    if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل", use_container_width=True, type="primary"):
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
        with st.spinner('📂 جاري قراءة الملف وتحليل المحتوى...'):
            file_content = extract_text_from_file(uploaded_file)
            if "⚠️" in file_content and len(file_content) < 200: 
                st.warning(file_content)
            full_text += f"\n\n[بداية محتوى الملف المرفق]:\n{file_content}\n[نهاية محتوى الملف المرفق]"

    full_text = clean_input_text(full_text)

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف صالح.")
        return
    
    try:
        genai.configure(api_key=API_KEY)
        selected_model = get_best_available_model()
        
        # تحسين الإعدادات للنموذج الأقوى
        generation_config = genai.types.GenerationConfig(
            temperature=0.0,  # درجة حرارة صفر لتقليل الإبداع والهلوسة تماماً
            top_p=0.95,
            top_k=40,
            max_output_tokens=32000,
        )
        
        model = genai.GenerativeModel(selected_model)

        target_css = ""
        design_rules = ""
        file_label = "Report"
        report_type_short = ""
        is_presentation = False
        
        unified_signature = """
        <div class="report-signature">
            <div class="signature-line"></div>
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
            - Use Standard <table class="data-table"> for ANY tabular data found in text.
            - Use <div class="stats-row"> for statistics if present.
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
            6. Create as many slides as needed to cover ALL content.
            7. **SLIDE BACKGROUND MUST BE WHITE**
            """

        # --------------------------------------------------------------------------------
        # ⚡ هندسة الأوامر المحسنة (الحماية القصوى للأسماء + النموذج الذكي)
        # --------------------------------------------------------------------------------
        prompt = f"""
أنت خبير توثيق رقمي ومدقق بيانات دقيق جداً (Strict Verbatim Transcriber).
المهمة: تحويل محتوى PDF الخام إلى تقرير HTML احترافي، مع الالتزام التام بعدم تغيير الأسماء أو الألقاب.

📥 حالة البيانات المدخلة:
النص مستخرج من PDF عربي وقد يحتوي على:
1. أحرف معكوسة أو مقطعة (بسبب مشاكل التشفير).
2. أسماء أشخاص ومناصب.

⚠️ بروتوكول التنفيذ الصارم (Strict Execution Protocol):

1. **حماية الأسماء (Entities Protection Policy - CRITICAL):**
   - 🚫 **ممنوع منعاً باتاً** استخدام "التصحيح التلقائي" على أسماء الأشخاص أو الألقاب أو العشائر (مثل: "الكلابي"، "الدراجي"، "أبو كلل").
   - انسخ الاسم كما يظهر لك في النص الأصلي تماماً، حتى لو بدا غريباً. لا تخمن اسماً آخر (لا تحول "كلل" إلى "هيل").
   - الاستثناء الوحيد: إذا كانت الأحرف مقطعة (م ت ف ر ق ة)، قم بدمجها فقط، ولا تغير الأحرف نفسها.

2. **معالجة النصوص (Text Processing):**
   - إذا وجدت نصاً مقلوباً (معكوساً)، قم بترتيبه ليصبح مقروءاً.
   - حافظ على كل المعلومات والأرقام بدقة 100%.

3. **التنسيق (Formatting):**
   - استخدم الكلاسات التالية:
{design_rules}
   - الجداول: حول القوائم والبيانات إلى `<table class="data-table">` فوراً.

4. **قواعد السلامة:**
   - لا تكرر الأحرف (sssss).
   - أعطني كود HTML فقط.

📥 النص للمعالجة:
--------------------------------------------------
{full_text}
--------------------------------------------------
"""

        # شريط التقدم
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # ----------------------------------------------------------------------------
        # ⚡ الإصلاح الأساسي: تفعيل الـ Streaming لمنع الـ 504 Timeout
        # ----------------------------------------------------------------------------
        try:
            status_text.markdown(f"<div class='progress-status'>📡 جاري الاتصال بالنموذج الذكي (Pro)...</div>", unsafe_allow_html=True)
            
            # تفعيل stream=True هو السر في منع انقطاع الاتصال
            response_stream = model.generate_content(
                prompt, 
                generation_config=generation_config,
                stream=True 
            )
            
            full_response_text = ""
            
            # حلقة التجميع: تبقي الاتصال حياً وتجمع النص قطعة قطعة
            for chunk in response_stream:
                if chunk.text:
                    full_response_text += chunk.text
                    # تحديث الواجهة ليبدو التطبيق نشطاً للخادم
                    status_text.markdown(f"<div class='progress-status'>⏳ جاري استلام البيانات... ({len(full_response_text)} حرف)</div>", unsafe_allow_html=True)
            
            progress_bar.progress(100)
            status_text.empty()
            
            # معالجة النص المجمع
            html_body = clean_html_response(full_response_text)
            
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
            <button class="nav-btn" onclick="prevSlide()" title="السابق">◀</button>
            <button class="nav-btn" onclick="nextSlide()" title="التالي">▶</button>
        </div>
        
        <div class="page-number" id="page-num">1 / 1</div>
        
        <div class="presentation-signature">
        صادر من الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي و التطوير
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

            st.markdown("""
            <div class="success-message">
                <span class="success-icon">✅</span>
                <span class="success-text">تم إنشاء التقرير بنجاح!</span>
            </div>
            """, unsafe_allow_html=True)
            
            components.html(final_html, height=850, scrolling=True)

            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=final_html,
                file_name=f"{file_label}.html",
                mime="text/html",
                use_container_width=True
            )
        
        except Exception as api_error:
            progress_bar.empty()
            status_text.empty()
            error_msg = str(api_error)
            if "504" in error_msg or "timeout" in error_msg.lower():
                st.error("⚠️ استغرق النموذج وقتاً طويلاً. يرجى المحاولة مرة أخرى (تم تحسين الاتصال في المحاولة القادمة).")
            else:
                st.error(f"❌ خطأ: {api_error}")

    except Exception as e:
        st.error(f"❌ خطأ غير متوقع: {e}")

# ---------------------------------------------------------
# 🚀 عرض الصفحة المناسبة
# ---------------------------------------------------------
if st.session_state.current_page == "platform":
    render_platform_page()
elif st.session_state.current_page == "reports":
    render_reports_page()

# الفوتر
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="main-footer">
    <div class="footer-content">
        <div class="footer-brand"> تيار الحكمة الوطني</div>
        <div class="footer-org">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي والتطوير</div>
        <div class="footer-copy">جميع الحقوق محفوظة © 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)
