# styles.py

# ---------------------------------------------------------
# 🎨 CSS الرئيسي للواجهة (Streamlit Interface)
# ---------------------------------------------------------
# ملاحظة: واجهة البرنامج ستبقى بألوان الهوية (أزرق/ذهبي) لتميزها، 
# لكن التقارير المخرجة ستكون بيضاء بالكامل كما طلبت.
MAIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(ellipse at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }
    
    /* إخفاء عناصر Streamlit الافتراضية */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="stSidebarCollapseButton"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    
    .viewerBadge_container__1QSob { display: none !important; }
    .st-emotion-cache-164nlkn { display: none !important; }
    div[class^="viewerBadge"] { display: none !important; }
    .stDeployButton { display: none !important; }

    .main .block-container {
        padding-right: 90px !important;
        max-width: 100% !important;
    }

    /* الهيدر الرئيسي */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 20px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.8);
        position: relative;
        overflow: hidden;
    }

    .main-title {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }

    .sub-title {
        color: #e0e0e0;
        font-size: 18px;
        letter-spacing: 2px;
        font-weight: 500;
    }
    
    /* تحسين البطاقات والأزرار */
    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 10px;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }

    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 100%) !important;
        color: #001f3f !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        border: none !important;
        font-size: 1.2rem !important;
        width: 100% !important;
    }

    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    /* نجاح */
    .success-banner {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin: 20px;
        color: #22c55e;
        font-weight: bold;
    }
    
    @media (max-width: 768px) {
        .main .block-container { padding-right: 60px !important; }
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 CSS الشريط الجانبي (ثابت)
# ---------------------------------------------------------
CUSTOM_SIDEBAR_CSS = """
<style>
    .custom-sidebar {
        position: fixed; top: 0; right: 0; height: 100vh; width: 70px;
        background: linear-gradient(180deg, #001f3f 0%, #0a1628 100%);
        border-left: 2px solid rgba(255, 215, 0, 0.3);
        z-index: 999999; display: flex; flex-direction: row-reverse;
        transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: -5px 0 30px rgba(0,0,0,0.5);
    }
    .custom-sidebar.expanded { width: 320px; }
    
    .sidebar-strip {
        width: 70px; min-width: 70px; height: 100%;
        display: flex; flex-direction: column; align-items: center; padding-top: 20px;
    }
    
    .strip-btn {
        width: 50px; height: 50px; border-radius: 12px;
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,215,0,0.2);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; margin-bottom: 15px; color: #FFD700; font-size: 1.5rem;
    }
    .strip-btn:hover { background: rgba(255,215,0,0.1); border-color: #FFD700; }
    
    .sidebar-panel {
        flex: 1; padding: 20px; opacity: 0; visibility: hidden;
        transition: all 0.3s; overflow-y: auto; color: white;
    }
    .custom-sidebar.expanded .sidebar-panel { opacity: 1; visibility: visible; }
    
    .sidebar-header { text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; margin-bottom: 15px; }
    .sidebar-report-card {
        background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;
        margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); cursor: pointer;
    }
    .sidebar-report-card:hover { border-color: #FFD700; background: rgba(255,255,255,0.1); }
</style>
"""

# ---------------------------------------------------------
# 🏛️ النمط الرسمي (أبيض نظيف مع أزرق ملكي)
# ---------------------------------------------------------
STYLE_OFFICIAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    :root {
        --primary: #003366; /* كحلي رسمي */
        --secondary: #c5a059; /* ذهبي */
        --bg: #ffffff;
        --text: #333333;
        --light-gray: #f8f9fa;
    }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background-color: #f0f2f5; /* خلفية الصفحة الخارجية رمادي فاتح جداً */
        color: var(--text);
        margin: 0;
        padding: 40px;
        direction: rtl;
        line-height: 1.8;
    }
    
    .container {
        max-width: 210mm; /* عرض A4 تقريباً */
        margin: 0 auto;
        background: white;
        padding: 60px;
        border-radius: 2px;
        box-shadow: 0 0 25px rgba(0,0,0,0.05);
        border-top: 10px solid var(--primary);
    }
    
    /* Header */
    header {
        text-align: center;
        border-bottom: 2px solid var(--light-gray);
        padding-bottom: 30px;
        margin-bottom: 40px;
    }
    
    header h1 {
        color: var(--primary);
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    header p {
        color: #666;
        font-size: 16px;
        margin: 5px 0;
    }
    
    /* Typography */
    h2 {
        color: var(--primary);
        font-size: 20px;
        border-right: 5px solid var(--secondary);
        padding-right: 15px;
        margin-top: 40px;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #f9f9f9, white);
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    h3 {
        color: #444;
        font-size: 18px;
        margin-top: 25px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }
    
    /* Stats Cards */
    .stats-row {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    
    .stat-item {
        flex: 1;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    
    .stat-item .stat-value {
        display: block;
        font-size: 32px;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 5px;
    }
    
    .stat-item .stat-label {
        font-size: 14px;
        color: #777;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 15px;
    }
    
    thead th {
        background-color: var(--primary);
        color: white;
        padding: 12px 15px;
        text-align: right;
        font-weight: 600;
    }
    
    tbody td {
        border-bottom: 1px solid #eee;
        padding: 12px 15px;
        color: #444;
    }
    
    tbody tr:nth-child(even) { background-color: #fcfcfc; }
    
    /* Lists */
    ul { padding-right: 20px; }
    ul li { margin-bottom: 10px; position: relative; }
    ul li::before {
        content: "•";
        color: var(--secondary);
        font-weight: bold;
        display: inline-block;
        width: 1em;
        margin-left: -1em;
    }
    
    /* Highlights */
    .highlight-box {
        background: #f8fcfd;
        border: 1px solid #bce8f1;
        color: #31708f;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    /* Signature (Unified) */
    .report-signature {
        margin-top: 80px;
        text-align: center;
        padding: 30px;
        border-top: 1px solid #eee;
    }
    .signature-icon { font-size: 40px; margin-bottom: 10px; }
    .signature-org { color: var(--primary); font-weight: 800; font-size: 18px; margin: 0; }
    .signature-unit { color: var(--secondary); font-size: 16px; margin: 5px 0; }
    
</style>
"""

# ---------------------------------------------------------
# 📱 النمط الرقمي (Light Dashboard) - أبيض نظيف
# ---------------------------------------------------------
STYLE_DIGITAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    :root {
        --primary: #2563eb; /* أزرق مشرق */
        --accent: #7c3aed; /* بنفسجي مشرق */
        --bg: #f3f4f6; /* رمادي فاتح جداً */
        --card-bg: #ffffff;
        --text-main: #1f2937;
        --text-muted: #6b7280;
    }
    
    body {
        font-family: 'Cairo', sans-serif;
        background-color: var(--bg);
        color: var(--text-main);
        margin: 0;
        padding: 40px;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header */
    .dashboard-header {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 40px;
        border-bottom: 4px solid var(--primary);
    }
    
    .dashboard-header h1 {
        margin: 0;
        font-size: 36px;
        color: var(--primary);
        font-weight: 900;
    }
    
    .dashboard-header p {
        color: var(--text-muted);
        font-size: 18px;
        margin-top: 10px;
    }
    
    /* Metric Cards (White) */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        transition: transform 0.3s;
        border: 1px solid #eee;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover { transform: translateY(-5px); border-color: var(--primary); }
    
    /* Colorful Accents for numbers */
    .metric-card:nth-child(1) .metric-value { color: #2563eb; } /* Blue */
    .metric-card:nth-child(2) .metric-value { color: #7c3aed; } /* Purple */
    .metric-card:nth-child(3) .metric-value { color: #059669; } /* Green */
    .metric-card:nth-child(4) .metric-value { color: #db2777; } /* Pink */
    
    .metric-value {
        display: block;
        font-size: 42px;
        font-weight: 900;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    
    .metric-label {
        color: var(--text-muted);
        font-size: 16px;
        font-weight: 600;
    }
    
    /* Charts/Data Sections */
    .data-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    }
    
    .data-card h2 {
        color: var(--text-main);
        font-size: 22px;
        border-right: 4px solid var(--primary);
        padding-right: 15px;
        margin-bottom: 25px;
    }
    
    /* Progress Bars */
    .progress-bar {
        background: #f3f4f6;
        height: 12px;
        border-radius: 6px;
        overflow: hidden;
        margin-top: 10px;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 6px;
    }
    
    /* Tables (Modern) */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 20px 0;
    }
    
    thead th {
        background-color: #f8fafc;
        color: var(--text-main);
        padding: 15px;
        font-weight: 700;
        border-bottom: 2px solid #e5e7eb;
    }
    
    tbody td {
        padding: 15px;
        border-bottom: 1px solid #f3f4f6;
    }
    
    /* Alerts */
    .alert-box {
        padding: 15px;
        border-radius: 8px;
        background: #eff6ff;
        color: #1e40af;
        border: 1px solid #dbeafe;
        margin: 15px 0;
    }
    
    /* Signature */
    .report-signature {
        background: white;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }
    .signature-icon { font-size: 35px; margin-bottom: 15px; }
    .signature-org { color: var(--primary); font-size: 20px; font-weight: 800; margin: 0; }
    .signature-unit { color: var(--text-muted); margin-top: 5px; }
</style>
"""

# ---------------------------------------------------------
# 📊 النمط التحليلي (أبيض، رسوم بيانية، نظيف)
# ---------------------------------------------------------
STYLE_ANALYTICAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    :root {
        --primary: #0056b3;
        --secondary: #17a2b8;
        --bg: #ffffff;
    }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: #fdfdfd;
        color: #333;
        padding: 40px;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        background: white;
        padding: 40px;
        border: 1px solid #eee;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
    }
    
    /* Header */
    header {
        text-align: center;
        background: #f8f9fa;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 40px;
        border-bottom: 4px solid var(--primary);
    }
    
    header h1 {
        margin: 0;
        color: var(--primary);
        font-size: 32px;
    }
    
    /* Stats */
    .stats-grid {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 40px;
    }
    
    .stat-card {
        background: white;
        border: 1px solid #dee2e6;
        flex: 1;
        padding: 20px;
        text-align: center;
        border-radius: 5px;
        border-top: 3px solid var(--secondary);
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #333;
    }
    
    .stat-label { color: #666; font-size: 14px; }
    
    /* Sections */
    .analysis-section {
        margin-bottom: 40px;
    }
    
    h2 {
        color: var(--primary);
        font-size: 24px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Chart Bars (Visual) */
    .bar-container {
        background: #e9ecef;
        height: 20px;
        border-radius: 4px;
        margin: 10px 0 20px 0;
        overflow: hidden;
    }
    .bar {
        height: 100%;
        background: var(--primary);
    }
    
    /* Table */
    table { width: 100%; border-collapse: collapse; }
    th { background: var(--primary); color: white; padding: 10px; }
    td { border: 1px solid #dee2e6; padding: 10px; }
    
    /* Signature */
    .report-signature {
        text-align: center;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 2px solid #eee;
    }
    .signature-org { font-weight: bold; font-size: 18px; color: var(--primary); }
</style>
"""

# ---------------------------------------------------------
# 📽️ عرض تقديمي (شرائح بيضاء نظيفة)
# ---------------------------------------------------------
STYLE_PRESENTATION = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    body {
        font-family: 'Cairo', sans-serif;
        background: #222; /* خلفية العرض خارج الشريحة */
        margin: 0;
        height: 100vh;
        overflow: hidden;
        direction: rtl;
    }
    
    .presentation-container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .slide {
        background: white; /* الشريحة بيضاء */
        width: 90%;
        height: 90%;
        position: absolute;
        opacity: 0;
        transition: opacity 0.5s;
        border-radius: 15px;
        padding: 50px;
        box-shadow: 0 0 50px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
        border: 1px solid #ddd;
    }
    
    .slide.active { opacity: 1; z-index: 10; }
    
    /* Slide Content */
    .slide-header {
        border-bottom: 4px solid #c5a059; /* ذهبي */
        padding-bottom: 20px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-title h2 {
        color: #002b49; /* كحلي */
        font-size: 36px;
        margin: 0;
    }
    
    .slide-content {
        flex: 1;
        font-size: 24px;
        color: #333;
        line-height: 1.6;
    }
    
    .slide.cover {
        text-align: center;
        justify-content: center;
        background: linear-gradient(135deg, #fdfbf7 0%, #fff 100%);
        border: 10px solid #002b49;
    }
    
    .main-title { font-size: 60px; color: #002b49; margin-bottom: 20px; }
    .sub-title { font-size: 30px; color: #c5a059; }
    
    /* Navigation */
    .nav-controls {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 20px;
        z-index: 100;
    }
    .nav-btn {
        background: #002b49;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 18px;
    }
    
    /* Signature Slide */
    .signature-box {
        margin-top: auto;
        text-align: center;
        color: #002b49;
        font-weight: bold;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

STYLE_EXECUTIVE = """
<style>
    /* ملخص تنفيذي بسيط - أبيض */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    body { font-family: 'Tajawal', sans-serif; background: white; color: black; padding: 50px; direction: rtl; }
    h1 { color: #000; border-bottom: 2px solid #000; padding-bottom: 10px; }
    .exec-summary { font-size: 18px; line-height: 1.8; background: #f9f9f9; padding: 20px; border-radius: 8px; }
    .report-signature { margin-top: 50px; text-align: center; font-weight: bold; border-top: 1px solid #ccc; padding-top: 20px; }
</style>
"""

SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    function updateSlide() {
        const slides = document.querySelectorAll('.slide');
        slides.forEach(s => s.classList.remove('active'));
        const active = document.getElementById('slide-' + currentSlideIndex);
        if(active) active.classList.add('active');
        document.getElementById('page-num').innerText = currentSlideIndex + ' / ' + slides.length;
    }
    function nextSlide() { 
        if(currentSlideIndex < document.querySelectorAll('.slide').length) { currentSlideIndex++; updateSlide(); } 
    }
    function prevSlide() { 
        if(currentSlideIndex > 1) { currentSlideIndex--; updateSlide(); } 
    }
</script>
"""
