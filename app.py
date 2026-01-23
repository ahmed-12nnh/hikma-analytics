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
# 📦 تهيئة التخزين المؤقت (Session State)
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

# تطبيق التصميم الرئيسي + إخفاء الشريط الافتراضي
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
# 🎨 الشريط الجانبي المخصص (مثل Gemini) - الحل الجذري
# ---------------------------------------------------------
def render_custom_sidebar():
    reports_count = len(st.session_state.reports_history)
    
    # بناء HTML للتقارير
    # ملاحظة: النصوص هنا تبدأ من بداية السطر لتجنب مشكلة التفسير الخاطئ
    reports_html = ""
    if reports_count > 0:
        for i, report in enumerate(st.session_state.reports_history):
            title_short = report['title'][:20] + "..." if len(report['title']) > 20 else report['title']
            reports_html += f"""
<div class="sidebar-report-card">
    <div class="report-title">📄 {title_short}</div>
    <div class="report-meta">
        <span>{report['type']}</span>
        <span>•</span>
        <span>{report['size']}</span>
    </div>
    <div class="report-time">🕐 {report['timestamp']}</div>
</div>
"""
    else:
        reports_html = """
<div class="sidebar-empty">
    <div class="empty-icon">📭</div>
    <div class="empty-text">لا توجد تقارير بعد</div>
    <div class="empty-hint">ستظهر هنا بعد إنشائها</div>
</div>
"""
    
    # الشريط الجانبي المخصص بالكامل
    # هام جداً: تم إزالة المسافات البادئة (Indentation) هنا عمداً
    # هذا يحل مشكلة ظهور الكود كنص في المتصفح ويضمن تنفيذه كـ HTML
    # تم تحديث الجافا سكربت ليعمل بفعالية
    sidebar_html = f"""
<div class="custom-sidebar" id="customSidebar">
    <div class="sidebar-strip">
        <div class="strip-btn menu-toggle" onclick="toggleSidebar()" title="فتح/إغلاق القائمة">
            <div class="hamburger" id="hamburgerIcon">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        
        <div class="strip-btn" onclick="toggleSidebar()" title="سجل التقارير ({reports_count})">
            <span class="strip-icon">📚</span>
            <span class="strip-badge">{reports_count}</span>
        </div>
        
        <div class="strip-divider"></div>
        
        <div class="strip-btn" title="الإعدادات">
            <span class="strip-icon">⚙️</span>
        </div>
    </div>
    
    <div class="sidebar-panel">
        <div class="sidebar-header">
            <h3>📚 سجل التقارير</h3>
            <p>التقارير المُنشأة خلال الجلسة الحالية</p>
        </div>
        
        <div class="sidebar-content">
            {reports_html}
        </div>
        
        <div class="sidebar-footer">
            <span>تيار الحكمة الوطني</span>
        </div>
    </div>
</div>

<script>
    // ربط الدالة بالنافذة مباشرة لضمان الوصول إليها
    window.toggleSidebar = function() {{
        var sidebar = document.getElementById('customSidebar');
        var hamburger = document.getElementById('hamburgerIcon');
        
        if (sidebar) {{
            sidebar.classList.toggle('expanded');
        }}
        
        if (hamburger) {{
            hamburger.classList.toggle('active');
        }}
    }};

    // إغلاق عند النقر خارج الشريط
    document.addEventListener('click', function(e) {{
        var sidebar = document.getElementById('customSidebar');
        var hamburger = document.getElementById('hamburgerIcon');
        
        // التحقق من أن النقر لم يكن على الشريط نفسه أو زر الفتح
        if (sidebar && sidebar.classList.contains('expanded') && !sidebar.contains(e.target)) {{
            // التأكد من عدم النقر على زر الفتح
            let clickedOnButton = false;
            if (e.target.closest('.menu-toggle') || e.target.closest('.strip-btn')) {{
                clickedOnButton = true;
            }}
            
            if (!clickedOnButton) {{
                sidebar.classList.remove('expanded');
                if (hamburger) hamburger.classList.remove('active');
            }}
        }}
    }});
</script>
"""
    
    return sidebar_html

# تطبيق CSS الشريط الجانبي
st.markdown(CUSTOM_SIDEBAR_CSS, unsafe_allow_html=True)

# عرض الشريط الجانبي
st.markdown(render_custom_sidebar(), unsafe_allow_html=True)

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

# عرض معاينة التقرير إذا كانت مفعّلة
if st.session_state.preview_report:
    st.markdown(f'''
    <div class="preview-banner">
        <span>👁️ معاينة: {st.session_state.preview_title}</span>
    </div>
    ''', unsafe_allow_html=True)
    
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
            
            selected_model = get_best_available_model()
            
            generation_config = genai.types.GenerationConfig(
                temperature=0.1,
                top_p=0.95,
                top_k=40,
                max_output_tokens=16384,  # زيادة الحد الأقصى للإخراج
            )
            
            model = genai.GenerativeModel(selected_model)

            target_css = ""
            design_rules = ""
            file_label = "Report"
            report_type_short = ""
            
            # ===== التوقيع في المنتصف =====
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
                Style: Official Corporate Report with MODERN design.
                Structure:
                - Use <header> for title with gradient background
                - Use <div class="card"> for each major section with shadow and border
                - Use <h3> with decorative right border for section titles
                - Use <table class="data-table"> for tabular data with zebra striping
                - Use <ul class="info-list"> with custom bullets for lists
                - Add icons (emoji) before important items
                - Use <div class="highlight-box"> for key findings
                - Use <div class="stats-row"> with <div class="stat-item"> for statistics
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                report_type_short = "📱 رقمي"
                design_rules = """
                Style: Modern Digital Dashboard with cards and metrics.
                Structure:
                - Use <div class="dashboard-header"> for title area
                - Use <div class="metrics-grid"> with <div class="metric-card"> for KPIs
                - Inside metric-card: <div class="metric-value">, <div class="metric-label">, <div class="metric-trend">
                - Use <div class="chart-section"> for data visualization areas
                - Use <div class="data-card"> for detailed sections
                - Use <div class="progress-indicator"> for percentages
                - Use <div class="alert-box success/warning/info"> for notifications
                - Add sparkline effects with CSS gradients
                """
            
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                report_type_short = "📊 تحليلي"
                design_rules = """
                Style: Statistical Analysis Report with visual hierarchy.
                Structure:
                - Use <header class="analysis-header"> with dark background
                - Use <div class="stats-grid"> for top-level statistics
                - Use <div class="stat-card"> with <span class="stat-value"> and <span class="stat-label">
                - Use <div class="analysis-section"> for each analysis area
                - Use <div class="comparison-table"> for comparisons
                - Use <div class="bar-chart"> with <div class="bar" style="width: X%"> for visual bars
                - Use <div class="insight-box"> for key insights
                - Use <div class="recommendation-card"> for recommendations
                """
            
            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE
                file_label = "Executive_Summary"
                report_type_short = "✨ تنفيذي"
                design_rules = """
                Style: Clean Executive Summary with minimal design.
                Structure:
                - Use <header class="exec-header"> with brand colors
                - Use <div class="exec-summary"> for main summary text
                - Use <div class="key-metrics"> with <div class="metric"> for important numbers
                - Use <div class="section"> with <h2 class="section-title"> for each part
                - Use <div class="bullet-list"> for key points
                - Use <div class="action-items"> for recommendations
                - Use <blockquote class="quote"> for important quotes
                - Keep design clean and professional
                """

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Presentation_Slides"
                report_type_short = "📽️ عرض"
                design_rules = """
                Style: Interactive Presentation Slides.
                Structure:
                1. First slide: <div class="slide cover active" id="slide-1"> with main title
                2. Content slides: <div class="slide" id="slide-N">
                3. Inside each slide:
                   - <div class="slide-header"> with <div class="header-title"><h2>Title</h2></div>
                   - <div class="slide-content"> with <div class="text-panel"> and <div class="visual-panel">
                4. Use FontAwesome icons: <i class="fas fa-icon"></i>
                5. Last slide must have signature box
                6. Create 6-10 slides minimum
                7. DO NOT output CSS or JavaScript, only HTML content
                """
                unified_signature = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                <div class="page-number" id="page-num">1 / 1</div>
                """

            # ===== الـ PROMPT المُحسّن لإنتاج تقارير كاملة =====
            prompt = f"""
أنت محلل بيانات ومطور محترف. مهمتك تحويل النص المُعطى إلى تقرير HTML احترافي كامل.

⚠️ قواعد صارمة يجب الالتزام بها (عدم الالتزام = فشل):

1️⃣ المحتوى الكامل (مهم جداً):
   - يجب تضمين كل المعلومات والبيانات من النص الأصلي بدون أي اختصار أو حذف
   - لا تختصر أي جملة أو فقرة أو نقطة
   - انقل كل الأرقام والإحصائيات والنسب كما هي
   - حافظ على جميع الأسماء والتواريخ والتفاصيل
   - إذا كان النص طويلاً، اجعل التقرير طويلاً أيضاً

2️⃣ صيغة الإخراج:
   - غلّف الكود داخل ```html و ```
   - لا تكتب أي نص قبل أو بعد كود HTML
   - استخدم UTF-8 للعربية

3️⃣ الأسماء والنصوص:
   - انسخ أسماء الأشخاص كما هي بالضبط
   - لا تعكس أي حرف أو كلمة عربية
   - حافظ على ترتيب الكلمات الأصلي

4️⃣ التصميم المطلوب:
{design_rules}

5️⃣ الهيكل العام:
   - ابدأ بـ <!DOCTYPE html>
   - استخدم <html lang="ar" dir="rtl">
   - أضف جميع الأقسام المطلوبة
   - اجعل التصميم عصرياً وجذاباً

📊 البيانات المُدخلة (يجب تضمينها كاملة):
{full_text}

🎯 التوقيع (أضفه في منتصف التقرير قبل نهاية المحتوى):
{unified_signature}

اللغة: العربية الفصحى المهنية
"""

            progress_placeholder = st.empty()
            
            # ===== شريط التحميل المُحسّن (بدون اسم الموديل) =====
            progress_messages = [
                "🔍 جاري تحليل البيانات...",
                "📊 استخراج المعلومات الرئيسية...",
                "🎨 تطبيق التصميم المطلوب...",
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
                    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
                    {target_css}
                </head>
                <body>
                    <div class="{ 'presentation-container' if 'عرض تقديمي' in report_type else 'container' }">
                        {html_body}
                        {unified_signature if 'عرض تقديمي' not in report_type else ''}
                    </div>
                    
                    {SCRIPT_PRESENTATION if 'عرض تقديمي' in report_type else ''}
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
                    💡 يمكنك الوصول للتقارير المحفوظة من الشريط الجانبي (☰)
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
                st.error(f"❌ حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {api_error}")

        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع: {e}")

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
