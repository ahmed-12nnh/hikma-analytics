# styles.py

# ---------------------------------------------------------
# 🎨 CSS الرئيسي للواجهة (Streamlit Interface)
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
    /* إخفاء الشريط العلوي والفوتر */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    button[data-testid="stSidebarCollapseButton"] { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    
    /* إخفاء أيقونة "Manage App" والبريد في الأسفل */
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
    
    /* بطاقات التقارير */
    .sidebar-report-card {
        background: linear-gradient(135deg, rgba(26, 45, 74, 0.8), rgba(13, 31, 60, 0.9));
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 215, 0, 0.12);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .sidebar-report-card:hover {
        border-color: rgba(255, 215, 0, 0.5);
        transform: translateX(-5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
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
# 🎨 القوالب العصرية (Templates)
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    :root {
        --navy: #001f3f;
        --gold: #c5a059;
        --gold-light: #f0e6d2;
        --white: #ffffff;
        --gray: #f8f9fa;
        --text: #333;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        color: var(--text);
        line-height: 1.8;
        direction: rtl;
    }
    
    .container {
        max-width: 1100px;
        margin: 30px auto;
        padding: 0;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    /* Header */
    header {
        background: linear-gradient(135deg, var(--navy) 0%, #0a2e5c 100%);
        padding: 40px;
        text-align: center;
        position: relative;
    }
    
    header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, var(--gold), #e6c885, var(--gold));
    }
    
    header h1 {
        color: var(--gold);
        font-size: 2.5em;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    header h2 {
        color: rgba(255,255,255,0.85);
        font-size: 1.2em;
        font-weight: 400;
    }
    
    /* Content */
    .content {
        padding: 40px;
    }
    
    /* Cards */
    .card {
        background: var(--white);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    }
    
    .card h3 {
        color: var(--navy);
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid var(--gold);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 20px 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
    }
    
    table th {
        background: linear-gradient(135deg, var(--navy), #0a2e5c);
        color: white;
        padding: 18px 15px;
        font-weight: 700;
        text-align: right;
    }
    
    table td {
        padding: 15px;
        border-bottom: 1px solid #eee;
        background: white;
    }
    
    table tr:nth-child(even) td {
        background: #f8f9fa;
    }
    
    table tr:hover td {
        background: rgba(197, 160, 89, 0.1);
    }
    
    /* Lists */
    ul {
        list-style: none;
        padding: 0;
    }
    
    ul li {
        padding: 15px 20px;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #f8f9fa, #fff);
        border-radius: 10px;
        border-right: 4px solid var(--gold);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    ul li:hover {
        transform: translateX(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    ul li span.value {
        color: var(--navy);
        font-weight: 800;
        font-size: 1.1em;
    }
    
    /* Stats */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 25px 0;
    }
    
    .stat-item {
        background: linear-gradient(135deg, var(--navy) 0%, #0a2e5c 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: white;
    }
    
    .stat-item .stat-value {
        font-size: 2.5em;
        font-weight: 800;
        color: var(--gold);
        display: block;
        margin-bottom: 5px;
    }
    
    .stat-item .stat-label {
        font-size: 0.95em;
        opacity: 0.9;
    }
    
    /* Highlight */
    .highlight-box {
        background: linear-gradient(135deg, var(--gold-light), #fff8e7);
        border: 2px solid var(--gold);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        text-align: center;
    }
    
    .highlight-box p {
        color: var(--navy);
        font-size: 1.2em;
        font-weight: 600;
        margin: 0;
    }
    
    /* Signature */
    .report-signature {
        text-align: center;
        padding: 40px 20px;
        margin: 40px 0;
        background: linear-gradient(135deg, #f8f9fa, #fff);
        border-radius: 15px;
    }
    
    .signature-line {
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        margin: 15px auto;
    }
    
    .signature-icon {
        font-size: 2.5em;
        margin: 15px 0;
    }
    
    .signature-org {
        color: var(--navy);
        font-size: 1.2em;
        font-weight: 700;
        margin: 10px 0 5px 0;
    }
    
    .signature-unit {
        color: var(--gold);
        font-size: 1.1em;
        font-weight: 600;
        margin: 0;
    }
    
    /* Footer */
    footer {
        background: var(--navy);
        color: rgba(255,255,255,0.7);
        text-align: center;
        padding: 20px;
        font-size: 0.9em;
    }
</style>
"""

STYLE_DIGITAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');
    
    :root {
        --primary: #0066cc;
        --primary-dark: #004a99;
        --accent: #00d4aa;
        --bg: #0f1419;
        --card-bg: #1a2332;
        --text: #e8eaed;
        --text-muted: #8b949e;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.7;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 20px auto;
        padding: 25px;
    }
    
    /* Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, var(--primary-dark) 0%, #002b5c 100%);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 212, 170, 0.1) 0%, transparent 70%);
    }
    
    .dashboard-header h1 {
        color: white;
        font-size: 2.2em;
        font-weight: 800;
        margin-bottom: 10px;
        position: relative;
    }
    
    .dashboard-header p {
        color: var(--accent);
        font-size: 1.1em;
        position: relative;
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, var(--accent) 0%, transparent 70%);
        opacity: 0.1;
        border-radius: 50%;
        transform: translate(30%, -30%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: var(--accent);
        box-shadow: 0 10px 30px rgba(0, 212, 170, 0.2);
    }
    
    .metric-value {
        font-size: 2.8em;
        font-weight: 800;
        color: var(--accent);
        display: block;
        margin-bottom: 5px;
    }
    
    .metric-label {
        color: var(--text-muted);
        font-size: 0.95em;
    }
    
    .metric-trend {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin-top: 10px;
    }
    
    .metric-trend.up {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .metric-trend.down {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    /* Data Cards */
    .data-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .data-card h2 {
        color: white;
        font-size: 1.4em;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid var(--primary);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Progress Bars */
    .progress-indicator {
        margin: 15px 0;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        color: var(--text-muted);
    }
    
    .progress-bar {
        height: 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .alert-box.success {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        color: #22c55e;
    }
    
    .alert-box.warning {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #f59e0b;
    }
    
    .alert-box.info {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #3b82f6;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    
    table th {
        background: var(--primary-dark);
        color: white;
        padding: 15px;
        text-align: right;
    }
    
    table td {
        padding: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    table tr:hover td {
        background: rgba(0, 212, 170, 0.05);
    }
    
    /* Signature */
    .report-signature {
        text-align: center;
        padding: 40px 20px;
        margin: 40px 0;
        background: var(--card-bg);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .signature-line {
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        margin: 15px auto;
    }
    
    .signature-icon { font-size: 2.5em; margin: 15px 0; }
    .signature-org { color: white; font-size: 1.2em; font-weight: 700; margin: 10px 0 5px 0; }
    .signature-unit { color: var(--accent); font-size: 1.1em; font-weight: 600; margin: 0; }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');
    
    :root {
        --primary: #004a99;
        --secondary: #0066cc;
        --accent: #f7b801;
        --danger: #d90429;
        --success: #22c55e;
        --bg: #f4f7f6;
        --card: #ffffff;
        --text: #333;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.7;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 20px auto;
        padding: 20px;
    }
    
    /* Analysis Header */
    .analysis-header, header {
        background: linear-gradient(135deg, var(--primary) 0%, #002b5c 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    
    .analysis-header::before, header::before {
        content: '📊';
        position: absolute;
        top: 20px;
        left: 30px;
        font-size: 3em;
        opacity: 0.2;
    }
    
    header h1, .analysis-header h1 {
        font-size: 2.2em;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .stat-card {
        background: var(--card);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-top: 4px solid var(--primary);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .stat-card .stat-value, .stat-card .value {
        font-size: 2.5em;
        font-weight: 800;
        color: var(--primary);
        display: block;
        margin-bottom: 5px;
    }
    
    .stat-card .stat-label {
        color: #666;
        font-size: 0.95em;
    }
    
    /* Analysis Sections */
    .analysis-section, .report-section {
        background: var(--card);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    .analysis-section h2, .report-section h2 {
        color: var(--primary);
        font-size: 1.4em;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid var(--accent);
    }
    
    /* Bar Charts */
    .bar-chart {
        margin: 20px 0;
    }
    
    .bar-item {
        margin-bottom: 15px;
    }
    
    .bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .bar-container {
        height: 12px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .bar {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    .bar.primary { background: linear-gradient(90deg, var(--primary), var(--secondary)); }
    .bar.accent { background: linear-gradient(90deg, var(--accent), #ffd700); }
    .bar.danger { background: linear-gradient(90deg, var(--danger), #ef4444); }
    .bar.success { background: linear-gradient(90deg, var(--success), #4ade80); }
    
    /* Tier Cards */
    .tier-card {
        background: var(--card);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-right: 5px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    .tier-card.tier-upper { border-right-color: var(--danger); }
    .tier-card.tier-middle { border-right-color: var(--accent); }
    .tier-card.tier-lower { border-right-color: var(--success); }
    
    /* Insights */
    .insight-box {
        background: linear-gradient(135deg, #e6f7ff, #f0f9ff);
        border: 1px solid #b3e0ff;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .insight-box h4 {
        color: var(--primary);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Recommendations */
    .recommendation-card {
        background: linear-gradient(135deg, #f0fdf4, #f7fee7);
        border: 1px solid #86efac;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Signature */
    .report-signature {
        text-align: center;
        padding: 40px 20px;
        margin: 40px 0;
        background: var(--card);
        border-radius: 16px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    .signature-line {
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        margin: 15px auto;
    }
    
    .signature-icon { font-size: 2.5em; margin: 15px 0; }
    .signature-org { color: var(--primary); font-size: 1.2em; font-weight: 700; margin: 10px 0 5px 0; }
    .signature-unit { color: var(--accent); font-size: 1.1em; font-weight: 600; margin: 0; }
    
    /* Footer */
    footer {
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 0.9em;
    }
</style>
"""

STYLE_PRESENTATION = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Tajawal:wght@400;700&display=swap');
    
    :root {
        --navy: #002b49;
        --blue: #004e89;
        --gold: #c5a059;
        --gold-light: #e6c885;
        --white: #ffffff;
        --text: #333333;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--navy);
        overflow: hidden;
        height: 100vh;
        width: 100vw;
        direction: rtl;
    }
    
    .presentation-container {
        width: 100%;
        height: 100%;
        position: relative;
        background: radial-gradient(circle at center, #003865 0%, #001a2c 100%);
    }
    
    .slide {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        opacity: 0;
        visibility: hidden;
        transform: scale(0.95);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        padding: 40px 60px;
    }
    
    .slide.active {
        opacity: 1;
        visibility: visible;
        transform: scale(1);
        z-index: 10;
    }
    
    .slide.cover {
        align-items: center;
        justify-content: center;
        text-align: center;
        background: linear-gradient(135deg, var(--navy) 30%, #001a2c 100%);
    }
    
    .cover-content {
        border: 3px solid var(--gold);
        padding: 60px 80px;
        background: rgba(0,0,0,0.4);
        backdrop-filter: blur(5px);
        border-radius: 20px;
    }
    
    .main-title {
        font-size: 3.5em;
        color: var(--white);
        margin-bottom: 15px;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    
    .sub-title {
        font-size: 1.8em;
        color: var(--gold);
        font-weight: 300;
    }
    
    .slide-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid var(--gold);
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    
    .header-title h2 {
        color: var(--gold);
        font-size: 2em;
        font-weight: 800;
    }
    
    .header-logo {
        color: var(--white);
        font-weight: bold;
    }
    
    .slide-content {
        flex-grow: 1;
        display: flex;
        gap: 40px;
        height: 100%;
        overflow: hidden;
    }
    
    .text-panel {
        flex: 3;
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 30px;
        color: var(--text);
        overflow-y: auto;
        border-right: 5px solid var(--gold);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    .visual-panel {
        flex: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: var(--white);
        text-align: center;
    }
    
    .icon-box {
        font-size: 5em;
        color: var(--gold);
        margin-bottom: 20px;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    h3 {
        color: var(--blue);
        font-size: 1.5em;
        margin-bottom: 15px;
        border-bottom: 2px dashed #ccc;
        padding-bottom: 10px;
    }
    
    p { font-size: 1.15em; line-height: 1.9; margin-bottom: 15px; }
    li { font-size: 1.1em; margin-bottom: 10px; line-height: 1.7; }
    strong { color: var(--navy); font-weight: 800; }
    
    .nav-controls {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 20px;
        z-index: 100;
    }
    
    .nav-btn {
        background: transparent;
        border: 2px solid var(--gold);
        color: var(--gold);
        width: 55px; height: 55px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.3em;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .nav-btn:hover {
        background: var(--gold);
        color: var(--navy);
        transform: scale(1.1);
    }
    
    .page-number {
        position: absolute;
        bottom: 25px;
        right: 60px;
        color: var(--gold);
        font-size: 1.2em;
        font-weight: bold;
    }
    
    .signature-box {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 2px solid var(--gold);
        text-align: center;
    }
    
    .signature-title { color: #aaa; font-size: 0.9em; margin-bottom: 10px; }
    .signature-name { color: var(--gold); font-size: 1.3em; font-weight: bold; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

STYLE_EXECUTIVE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    :root {
        --navy: #002b49;
        --gold: #c5a059;
        --black: #1a1a1a;
        --white: #ffffff;
        --gray: #666;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background: var(--white);
        color: var(--black);
        line-height: 1.8;
        direction: rtl;
    }
    
    .container {
        max-width: 900px;
        margin: 40px auto;
        padding: 50px;
        border: 1px solid #eee;
        box-shadow: 0 20px 60px rgba(0,0,0,0.08);
    }
    
    /* Exec Header */
    .exec-header, header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 4px solid var(--black);
        padding-bottom: 25px;
        margin-bottom: 40px;
    }
    
    .brand {
        font-size: 1.5em;
        font-weight: 800;
        color: var(--navy);
        letter-spacing: -1px;
    }
    
    h1 {
        font-size: 2.8em;
        font-weight: 900;
        line-height: 1.2;
        margin-bottom: 15px;
        color: var(--black);
    }
    
    /* Executive Summary */
    .exec-summary, .executive-summary {
        font-size: 1.25em;
        line-height: 1.8;
        color: #444;
        margin-bottom: 40px;
        padding: 25px 30px;
        border-right: 5px solid var(--gold);
        background: #fafafa;
    }
    
    /* Key Metrics */
    .key-metrics, .grid-2 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .metric, .metric-box {
        padding: 25px;
        background: #f9f9f9;
        border-radius: 8px;
        border: 1px solid #eee;
    }
    
    .metric-val {
        font-size: 2.8em;
        font-weight: 800;
        color: var(--navy);
        display: block;
        margin-bottom: 5px;
    }
    
    .metric-lbl {
        font-size: 1em;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sections */
    .section {
        margin-bottom: 35px;
    }
    
    .section-title, h2 {
        font-size: 1.3em;
        font-weight: 800;
        text-transform: uppercase;
        color: var(--gold);
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: inline-block;
    }
    
    /* Bullet List */
    .bullet-list ul {
        list-style: none;
        padding: 0;
    }
    
    .bullet-list li {
        padding: 12px 20px;
        margin-bottom: 10px;
        background: #f9f9f9;
        border-radius: 5px;
        position: relative;
        padding-right: 35px;
    }
    
    .bullet-list li::before {
        content: '▸';
        position: absolute;
        right: 15px;
        color: var(--gold);
        font-weight: bold;
    }
    
    /* Action Items */
    .action-items {
        background: linear-gradient(135deg, #f8f9fa, #fff);
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 25px;
        margin: 25px 0;
    }
    
    .action-items h4 {
        color: var(--navy);
        margin-bottom: 15px;
    }
    
    /* Quote */
    blockquote, .quote {
        border-right: 4px solid var(--gold);
        padding: 20px 25px;
        margin: 25px 0;
        background: #fafafa;
        font-style: italic;
        color: #555;
    }
    
    /* Signature */
    .report-signature {
        text-align: center;
        padding: 40px 20px;
        margin: 50px 0 30px 0;
        border-top: 2px solid #eee;
        border-bottom: 2px solid #eee;
    }
    
    .signature-line {
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        margin: 15px auto;
    }
    
    .signature-icon { font-size: 2em; margin: 15px 0; }
    .signature-org { color: var(--navy); font-size: 1.15em; font-weight: 700; margin: 10px 0 5px 0; }
    .signature-unit { color: var(--gold); font-size: 1.05em; font-weight: 600; margin: 0; }
    
    /* Footer */
    footer {
        text-align: center;
        padding: 20px;
        color: #999;
        font-size: 0.85em;
        border-top: 1px solid #eee;
        margin-top: 40px;
    }
</style>
"""

SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    
    function updateSlide() {
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        if(totalSlides === 0) return;
        
        slides.forEach(slide => slide.classList.remove('active'));
        
        const activeSlide = document.getElementById('slide-' + currentSlideIndex);
        if(activeSlide) activeSlide.classList.add('active');
        
        const pageNum = document.getElementById('page-num');
        if(pageNum) pageNum.innerText = currentSlideIndex + ' / ' + totalSlides;
    }
    
    function nextSlide() { 
        const totalSlides = document.querySelectorAll('.slide').length;
        if (currentSlideIndex < totalSlides) { currentSlideIndex++; updateSlide(); } 
    }
    
    function prevSlide() { 
        if (currentSlideIndex > 1) { currentSlideIndex--; updateSlide(); } 
    }
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowLeft' || event.key === ' ') nextSlide();
        else if (event.key === 'ArrowRight') prevSlide();
    });
    
    setTimeout(updateSlide, 100);
</script>
"""
