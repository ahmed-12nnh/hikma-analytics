# styles.py

# ---------------------------------------------------------
# ✅ [إصلاح #4] Font Awesome Link منفصل
# ---------------------------------------------------------
FONT_AWESOME_LINK = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">"""

# ---------------------------------------------------------
# 🎨 CSS الرئيسي للواجهة (Streamlit Interface)
# حافظنا عليه كما هو في نسختك الأصلية (النمط الداكن)
# ---------------------------------------------------------
MAIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(ellipse at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }
    
    /* ===== إخفاء عناصر Streamlit الافتراضية المزعجة ===== */
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

    /* تعديل المحتوى للشريط الجانبي */
    .main .block-container {
        padding-right: 90px !important;
        max-width: 100% !important;
    }

    /* ===== الهيدر الرئيسي ===== */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 20px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.8), inset 0 0 30px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        animation: fadeIn 1s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }

    .main-title {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.3)); }
        to { filter: drop-shadow(0 0 25px rgba(255, 215, 0, 0.6)); }
    }

    .sub-title {
        color: #e0e0e0;
        font-size: 18px;
        letter-spacing: 2px;
        font-weight: 500;
    }
    
    /* ===== العناصر العامة ===== */
    .preview-banner {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 14px 22px;
        border-radius: 12px;
        margin: 20px;
        font-weight: 600;
        text-align: center;
    }
    
    .success-hint {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 10px;
        padding: 12px 20px;
        margin: 10px 20px;
        color: rgba(34, 197, 94, 0.85);
        font-size: 0.88rem;
        text-align: center;
    }

    .section-header {
        text-align: center;
        margin: 30px 20px;
        color: #FFD700;
        font-size: 1.4rem;
        font-weight: bold;
    }

    /* ===== أزرار الاختيار ===== */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row-reverse !important;
        justify-content: center !important;
        gap: 15px !important;
        flex-wrap: wrap !important;
        background: rgba(0, 0, 0, 0.3) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 0 20px 30px 20px !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95)) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        padding: 15px 25px !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        flex: 1 !important;
        min-width: 160px !important;
        max-width: 220px !important;
        color: white !important;
        font-weight: 600 !important;
    }

    div[role="radiogroup"] label:hover {
        border-color: #FFD700 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    }
    
    div[role="radiogroup"] label[data-checked="true"],
    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(184, 134, 11, 0.15)) !important;
        border-color: #FFD700 !important;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.3) !important;
    }

    /* ===== بطاقات الإدخال ===== */
    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 10px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .input-card:hover {
        border-color: rgba(255, 215, 0, 0.4);
        transform: translateY(-3px);
    }

    .input-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .input-icon {
        width: 50px; height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #FFD700, #B8860B);
        border-radius: 12px;
        font-size: 1.5rem;
    }

    .input-title {
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: 700;
    }

    .input-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* ===== حقل النص ===== */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1rem !important;
        padding: 20px !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important;
    }

    /* ===== رفع الملفات ===== */
    [data-testid="stFileUploader"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px dashed rgba(255, 215, 0, 0.3) !important;
        border-radius: 15px !important;
        padding: 25px !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #FFD700 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #FFD700, #B8860B) !important;
        color: #001f3f !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    /* ===== زر المعالجة ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 50%, #FFD700 100%) !important;
        background-size: 200% auto !important;
        color: #001f3f !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        border-radius: 15px !important;
        width: 100% !important;
        padding: 18px 40px !important;
        border: none !important;
        box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4) !important;
        transition: all 0.3s ease !important;
        animation: buttonPulse 2s infinite !important;
    }
    
    @keyframes buttonPulse {
        0%, 100% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.4); }
        50% { box-shadow: 0 8px 30px rgba(218, 165, 32, 0.6), 0 0 0 8px rgba(255, 215, 0, 0); }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(218, 165, 32, 0.5) !important;
    }

    /* ===== زر التحميل ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 15px 40px !important;
        border-radius: 12px !important;
        border: none !important;
        animation: none !important;
    }

    /* ===== شريط النجاح ===== */
    .success-banner {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 20px 30px;
        text-align: center;
        margin: 20px;
    }
    
    .success-banner span {
        color: #22c55e;
        font-size: 1.2rem;
        font-weight: 700;
    }

    /* ===== إخفاء التسميات ===== */
    .stTextArea > label,
    .stFileUploader > label,
    .stRadio > label {
        display: none !important;
    }

    /* ===== شريط التقدم ===== */
    .progress-box {
        background: rgba(0, 31, 63, 0.9);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 30px;
        margin: 20px;
        text-align: center;
    }
    
    .progress-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 14px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% 100%;
        border-radius: 10px;
        animation: progressShine 1.5s infinite linear;
    }
    
    @keyframes progressShine {
        0% { background-position: 200% center; }
        100% { background-position: -200% center; }
    }
    
    .progress-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.05rem;
        margin-top: 10px;
        font-weight: 500;
    }

    /* ===== الفوتر ===== */
    .footer-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 15px;
        padding: 30px 20px;
        margin: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        text-align: center;
    }
    
    .footer-line {
        width: 60px; height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 0 auto 20px auto;
    }
    
    .footer-org {
        color: #FFD700;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .footer-unit {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        margin-bottom: 15px;
    }
    
    .footer-divider {
        width: 100px; height: 1px;
        background: rgba(255, 215, 0, 0.3);
        margin: 15px auto;
    }
    
    .footer-copy {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85rem;
    }

    /* ===== الاستجابة ===== */
    @media (max-width: 768px) {
        .main-title { font-size: 36px; }
        .hero-section { padding: 30px 20px; margin: 10px; }
        .main .block-container { padding-right: 80px !important; }
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 CSS الشريط الجانبي المخصص (الحل النهائي)
# ---------------------------------------------------------
CUSTOM_SIDEBAR_CSS = """
<style>
    /* ===== الشريط الجانبي المخصص ===== */
    .custom-sidebar {
        position: fixed;
        top: 0;
        right: 0;
        height: 100vh;
        width: 70px;
        background: linear-gradient(180deg, #001f3f 0%, #0a1628 50%, #001f3f 100%);
        border-left: 2px solid rgba(255, 215, 0, 0.3);
        z-index: 999999;
        display: flex;
        flex-direction: row-reverse;
        transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: -5px 0 30px rgba(0, 0, 0, 0.5);
    }
    
    .custom-sidebar.expanded {
        width: 320px;
    }
    
    /* الشريط الضيق */
    .sidebar-strip {
        width: 70px;
        min-width: 70px;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;
        background: linear-gradient(180deg, rgba(0, 31, 63, 0.98) 0%, rgba(10, 22, 40, 0.98) 100%);
        border-left: 1px solid rgba(255, 215, 0, 0.15);
    }
    
    /* أزرار الشريط الضيق */
    .strip-btn {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.08), rgba(255, 215, 0, 0.03));
        border: 2px solid rgba(255, 215, 0, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 15px;
        position: relative;
    }
    
    .strip-btn:hover {
        background: linear-gradient(135deg, #FFD700, #B8860B);
        border-color: #FFD700;
        transform: scale(1.08);
        box-shadow: 0 5px 25px rgba(255, 215, 0, 0.5);
    }
    
    .strip-btn:hover .hamburger span,
    .strip-btn:hover .strip-icon {
        color: #001f3f;
    }
    
    /* أيقونة الهامبرغر */
    .hamburger {
        width: 24px;
        height: 18px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .hamburger span {
        display: block;
        width: 100%;
        height: 3px;
        background: #FFD700;
        border-radius: 3px;
        transition: all 0.35s ease;
    }
    
    .strip-btn:hover .hamburger span {
        background: #001f3f;
    }
    
    /* تحويل لـ X */
    .hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .hamburger.active span:nth-child(2) {
        opacity: 0;
        transform: translateX(20px);
    }
    
    .hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(6px, -6px);
    }
    
    /* الأيقونات */
    .strip-icon {
        font-size: 1.5rem;
        transition: all 0.3s ease;
    }
    
    /* شارة العدد */
    .strip-badge {
        position: absolute;
        top: -6px;
        left: -6px;
        background: linear-gradient(135deg, #FFD700, #B8860B);
        color: #001f3f;
        font-size: 0.72rem;
        font-weight: 800;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(255, 215, 0, 0.4);
    }
    
    /* الفاصل */
    .strip-divider {
        width: 35px;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent);
        margin: 10px 0;
    }
    
    /* لوحة المحتوى */
    .sidebar-panel {
        flex: 1;
        padding: 20px 15px;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease 0.1s;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
    }
    
    .custom-sidebar.expanded .sidebar-panel {
        opacity: 1;
        visibility: visible;
    }
    
    /* رأس الشريط */
    .sidebar-header {
        text-align: center;
        padding-bottom: 18px;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .sidebar-header h3 {
        color: #FFD700;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    
    .sidebar-header p {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.78rem;
        margin: 0;
    }
    
    /* محتوى الشريط */
    .sidebar-content {
        flex: 1;
        overflow-y: auto;
    }
    
    /* ✅ [إصلاح #2] بطاقات التقارير - قابلة للنقر */
    .sidebar-report-card {
        background: linear-gradient(135deg, rgba(26, 45, 74, 0.8), rgba(13, 31, 60, 0.9));
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 215, 0, 0.12);
        transition: all 0.3s ease;
        cursor: pointer;
        user-select: none;
    }
    
    .sidebar-report-card:hover {
        border-color: rgba(255, 215, 0, 0.5);
        transform: translateX(-5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, rgba(36, 55, 84, 0.9), rgba(23, 41, 70, 0.95));
    }
    
    .sidebar-report-card:active {
        transform: translateX(-3px) scale(0.98);
    }
    
    .sidebar-report-card .report-title {
        color: #FFD700;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .sidebar-report-card .report-meta {
        display: flex;
        gap: 8px;
        color: rgba(255, 255, 255, 0.55);
        font-size: 0.72rem;
        margin-bottom: 4px;
    }
    
    .sidebar-report-card .report-time {
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.68rem;
    }
    
    /* حالة فارغة */
    .sidebar-empty {
        text-align: center;
        padding: 40px 15px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        border: 1px dashed rgba(255, 215, 0, 0.2);
    }
    
    .sidebar-empty .empty-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        opacity: 0.6;
    }
    
    .sidebar-empty .empty-text {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95rem;
        margin-bottom: 8px;
    }
    
    .sidebar-empty .empty-hint {
        color: rgba(255, 255, 255, 0.35);
        font-size: 0.8rem;
    }
    
    /* فوتر الشريط */
    .sidebar-footer {
        text-align: center;
        padding-top: 15px;
        margin-top: auto;
        border-top: 1px solid rgba(255, 215, 0, 0.15);
    }
    
    .sidebar-footer span {
        color: rgba(255, 215, 0, 0.5);
        font-size: 0.75rem;
    }
    
    /* Scrollbar */
    .sidebar-content::-webkit-scrollbar {
        width: 5px;
    }
    
    .sidebar-content::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .sidebar-content::-webkit-scrollbar-thumb {
        background: rgba(255, 215, 0, 0.3);
        border-radius: 5px;
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 القوالب العصرية (الجديدة كلياً - خلفية بيضاء)
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Tajawal:wght@400;700&display=swap');
    
    :root {
        --primary: #003366; /* كحلي رسمي */
        --secondary: #c5a059; /* ذهبي */
        --bg: #ffffff;
        --text: #333333;
        --light-gray: #f8f9fa;
        --border-color: #e0e0e0;
    }
    
    body {
        font-family: 'Cairo', sans-serif;
        background-color: #f9fafb; /* خلفية خارجية رمادية فاتحة جدا */
        color: var(--text);
        margin: 0;
        padding: 40px;
        direction: rtl;
        line-height: 1.8;
    }
    
    .container {
        max-width: 1100px;
        margin: 0 auto;
        background: white;
        padding: 60px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-top: 8px solid var(--primary);
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
        font-size: 2.4em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    header p {
        color: #666;
        font-size: 1.1em;
        margin: 5px 0;
    }
    
    /* Sections & Cards */
    .card {
        background: #fff;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    h2 {
        color: var(--primary);
        font-size: 1.8em;
        border-right: 5px solid var(--secondary);
        padding-right: 15px;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    
    h3 {
        color: #444;
        font-size: 1.4em;
        margin-bottom: 15px;
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
    }
    
    /* Stats */
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
        font-size: 2.2em;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 5px;
    }
    
    .stat-item .stat-label {
        font-size: 1em;
        color: #777;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 1em;
    }
    
    thead th {
        background-color: var(--primary);
        color: white;
        padding: 15px;
        text-align: right;
        font-weight: 600;
    }
    
    tbody td {
        border-bottom: 1px solid #eee;
        padding: 12px 15px;
        color: #444;
    }
    
    tbody tr:nth-child(even) { background-color: #fcfcfc; }
    tbody tr:hover { background-color: #f0f4f8; }
    
    /* Highlights */
    .highlight-box {
        background: #f0f7ff;
        border: 1px solid #cce5ff;
        color: #004085;
        padding: 20px;
        border-radius: 6px;
        margin: 20px 0;
        font-weight: 600;
    }
    
    /* Lists */
    ul li {
        margin-bottom: 10px;
        position: relative;
        padding-right: 20px;
    }
    ul li::before {
        content: "•";
        color: var(--secondary);
        font-weight: bold;
        font-size: 1.5em;
        position: absolute;
        right: 0;
        top: -5px;
    }

    /* Signature Styles */
    .report-signature {
        margin-top: 80px;
        text-align: center;
        padding: 40px;
        border-top: 1px solid #eee;
        background-color: #fcfcfc;
        border-radius: 8px;
    }
    .signature-icon { font-size: 40px; margin-bottom: 15px; display: block; }
    .signature-org { color: var(--primary); font-weight: 800; font-size: 1.3em; margin: 0; }
    .signature-unit { color: var(--secondary); font-size: 1.1em; margin: 5px 0; font-weight: 600; }
    .signature-line { width: 80px; height: 3px; background: var(--secondary); margin: 20px auto; }
</style>
"""

STYLE_DIGITAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    :root {
        --primary: #2563eb; /* أزرق مشرق */
        --accent: #7c3aed; /* بنفسجي */
        --bg: #f3f4f6;
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
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 40px;
        border-bottom: 4px solid var(--primary);
    }
    
    .dashboard-header h1 {
        margin: 0;
        font-size: 2.5em;
        color: var(--primary);
        font-weight: 900;
    }
    
    .dashboard-header p {
        color: var(--text-muted);
        font-size: 1.2em;
        margin-top: 10px;
    }
    
    /* Metrics Grid */
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
        border: 1px solid #e5e7eb;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover { transform: translateY(-5px); border-color: var(--primary); }
    
    .metric-value {
        display: block;
        font-size: 3em;
        font-weight: 900;
        color: var(--accent);
        margin-bottom: 10px;
    }
    
    .metric-label {
        color: var(--text-muted);
        font-size: 1.1em;
        font-weight: 600;
    }
    
    /* Cards */
    .data-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    }
    
    .data-card h2 {
        color: var(--text-main);
        font-size: 1.5em;
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
    
    /* Alerts */
    .alert-box {
        padding: 20px;
        border-radius: 12px;
        background: #eff6ff;
        color: #1e40af;
        border: 1px solid #dbeafe;
        margin: 15px 0;
        font-weight: 600;
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
    .signature-org { color: var(--primary); font-size: 1.4em; font-weight: 800; margin: 0; }
    .signature-unit { color: var(--text-muted); margin-top: 5px; font-size: 1.1em; }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    body {
        font-family: 'Cairo', sans-serif;
        background: #f8f9fa;
        color: #333;
        padding: 40px;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        background: white;
        padding: 50px;
        border: 1px solid #e9ecef;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-radius: 8px;
    }
    
    /* Header */
    header {
        text-align: center;
        background: #f1f3f5;
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 40px;
        border-bottom: 5px solid #0056b3;
    }
    
    header h1 {
        margin: 0;
        color: #0056b3;
        font-size: 2.5em;
        font-weight: 800;
    }
    
    /* Stats */
    .stats-grid {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 40px;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: white;
        border: 1px solid #dee2e6;
        flex: 1;
        min-width: 200px;
        padding: 25px;
        text-align: center;
        border-radius: 8px;
        border-top: 4px solid #17a2b8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .stat-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #0056b3;
        display: block;
    }
    
    .stat-label { color: #6c757d; font-size: 1.1em; }
    
    /* Analysis Sections */
    .analysis-section { margin-bottom: 40px; }
    
    h2 {
        color: #0056b3;
        font-size: 1.8em;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    
    /* Visual Bars */
    .bar-container {
        background: #e9ecef;
        height: 24px;
        border-radius: 4px;
        margin: 15px 0 25px 0;
        overflow: hidden;
    }
    .bar { height: 100%; background: #0056b3; }
    
    /* Tables */
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    th { background: #0056b3; color: white; padding: 15px; font-weight: 600; }
    td { border: 1px solid #dee2e6; padding: 15px; }
    tr:nth-child(even) { background: #f8f9fa; }
    
    /* Signature */
    .report-signature {
        text-align: center;
        margin-top: 80px;
        padding-top: 30px;
        border-top: 2px solid #e9ecef;
    }
    .signature-org { font-weight: bold; font-size: 1.2em; color: #0056b3; }
</style>
"""

# ✅ [إصلاح #4 و #5] تحديث STYLE_PRESENTATION - إزالة link من داخل style وإضافة CSS للعناصر الناقصة
STYLE_PRESENTATION = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: #2c3e50; /* خلفية داكنة خارج الشريحة */
        margin: 0;
        height: 100vh;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        direction: rtl;
    }
    
    .presentation-container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    
    .slide {
        background: white;
        width: 90%;
        height: 85%;
        position: absolute;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.6s ease, visibility 0.6s ease;
        border-radius: 20px;
        padding: 60px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
        border: 1px solid #ccc;
        overflow-y: auto;
    }
    
    .slide.active { 
        opacity: 1; 
        visibility: visible;
        z-index: 10; 
    }
    
    /* Slide Content */
    .slide-header {
        border-bottom: 5px solid #c5a059;
        padding-bottom: 20px;
        margin-bottom: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-title h2 {
        color: #003366;
        font-size: 2.5em;
        margin: 0;
        font-weight: 800;
    }
    
    .slide-content {
        flex: 1;
        font-size: 1.6em;
        color: #333;
        line-height: 1.8;
        overflow-y: auto;
    }
    
    .slide-content ul {
        list-style: none;
        padding: 0;
    }
    
    .slide-content ul li {
        padding: 15px 0;
        border-bottom: 1px solid #eee;
        padding-right: 30px;
        position: relative;
    }
    
    .slide-content ul li::before {
        content: "◆";
        color: #c5a059;
        position: absolute;
        right: 0;
        font-size: 0.8em;
    }
    
    /* Cover Slide */
    .slide.cover {
        text-align: center;
        justify-content: center;
        align-items: center;
        background: linear-gradient(135deg, #fdfbf7 0%, #fff 100%);
        border: 15px solid #003366;
    }
    
    .slide.cover .main-title,
    .main-title { 
        font-size: 4em; 
        color: #003366; 
        margin-bottom: 30px; 
        font-weight: 900; 
    }
    
    .slide.cover .sub-title,
    .sub-title { 
        font-size: 2em; 
        color: #c5a059; 
    }
    
    /* ✅ [إصلاح #5] Navigation Controls - تم تحسين التصميم */
    .nav-controls {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 20px;
        z-index: 1000;
    }
    
    .nav-btn {
        background: linear-gradient(135deg, #003366, #004080);
        color: white;
        border: none;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.4em;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .nav-btn:hover { 
        background: linear-gradient(135deg, #004080, #0056b3);
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .nav-btn:active {
        transform: scale(0.95);
    }
    
    /* ✅ [إصلاح #5] Page Number - تصميم جديد */
    .page-number {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: rgba(0, 51, 102, 0.9);
        color: white;
        padding: 12px 24px;
        border-radius: 30px;
        font-size: 1.1em;
        font-weight: 700;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* ✅ Presentation Signature - التوقيع للعرض التقديمي */
    .presentation-signature {
        position: fixed;
        bottom: 30px;
        left: 30px;
        background: rgba(0, 51, 102, 0.9);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 0.9em;
        font-weight: 600;
        z-index: 1000;
        max-width: 300px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .slide {
            padding: 30px;
            width: 95%;
            height: 90%;
        }
        
        .main-title { font-size: 2.5em; }
        .sub-title { font-size: 1.5em; }
        .header-title h2 { font-size: 1.8em; }
        .slide-content { font-size: 1.2em; }
        
        .nav-btn {
            width: 50px;
            height: 50px;
            font-size: 1.2em;
        }
        
        .page-number {
            padding: 8px 16px;
            font-size: 0.9em;
        }
        
        .presentation-signature {
            display: none;
        }
    }
</style>
"""

STYLE_EXECUTIVE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    body { font-family: 'Tajawal', sans-serif; background: white; padding: 60px; direction: rtl; color: #333; line-height: 2; }
    .container { max-width: 900px; margin: 0 auto; }
    h1 { color: #000; border-bottom: 3px solid #000; padding-bottom: 15px; margin-bottom: 40px; font-size: 2.5em; }
    h2 { color: #003366; font-size: 1.8em; margin-top: 40px; margin-bottom: 20px; }
    .exec-summary { font-size: 1.4em; background: #f8f9fa; padding: 30px; border-radius: 10px; border-right: 8px solid #003366; margin-bottom: 30px; }
    .key-metrics { display: flex; gap: 20px; flex-wrap: wrap; margin: 30px 0; }
    .key-metric { flex: 1; min-width: 200px; background: #f8f9fa; padding: 25px; border-radius: 10px; text-align: center; }
    .key-metric .value { font-size: 2.5em; font-weight: bold; color: #003366; display: block; }
    .key-metric .label { color: #666; font-size: 1.1em; }
    .report-signature { margin-top: 80px; text-align: center; font-weight: bold; border-top: 2px solid #ccc; padding-top: 30px; font-size: 1.2em; }
    .signature-org { color: #003366; }
</style>
"""

# ✅ [إصلاح #3] تحديث SCRIPT_PRESENTATION - تحسين التنقل بين الشرائح
SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    let totalSlides = 0;
    
    function initPresentation() {
        const slides = document.querySelectorAll('.slide');
        totalSlides = slides.length;
        
        if (totalSlides > 0) {
            // التأكد من أن الشريحة الأولى مفعلة
            slides.forEach((slide, index) => {
                slide.classList.remove('active');
                if (index === 0) {
                    slide.classList.add('active');
                }
            });
            currentSlideIndex = 1;
            updatePageNumber();
        }
    }
    
    function updatePageNumber() {
        const pageNum = document.getElementById('page-num');
        if (pageNum) {
            pageNum.innerText = currentSlideIndex + ' / ' + totalSlides;
        }
    }
    
    function showSlide(index) {
        const slides = document.querySelectorAll('.slide');
        
        if (index < 1) index = 1;
        if (index > totalSlides) index = totalSlides;
        
        currentSlideIndex = index;
        
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === currentSlideIndex - 1) {
                slide.classList.add('active');
            }
        });
        
        updatePageNumber();
    }
    
    function nextSlide() { 
        if (currentSlideIndex < totalSlides) { 
            showSlide(currentSlideIndex + 1);
        } 
    }
    
    function prevSlide() { 
        if (currentSlideIndex > 1) { 
            showSlide(currentSlideIndex - 1);
        } 
    }
    
    // التنقل بالأسهم
    document.addEventListener('keydown', function(e) { 
        if (e.key === "ArrowLeft" || e.key === " ") {
            e.preventDefault();
            nextSlide();
        }
        if (e.key === "ArrowRight") {
            e.preventDefault();
            prevSlide();
        }
        // الانتقال للشريحة الأولى
        if (e.key === "Home") {
            e.preventDefault();
            showSlide(1);
        }
        // الانتقال للشريحة الأخيرة
        if (e.key === "End") {
            e.preventDefault();
            showSlide(totalSlides);
        }
    });
    
    // تهيئة العرض عند التحميل
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPresentation);
    } else {
        // DOM already loaded
        setTimeout(initPresentation, 100);
    }
</script>
"""
