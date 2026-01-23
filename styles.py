# styles.py

# ---------------------------------------------------------
# Font Awesome Link
# ---------------------------------------------------------
FONT_AWESOME_LINK = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">"""

# ---------------------------------------------------------
# 🎨 CSS الرئيسي للواجهة
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
    
    /* إخفاء عناصر Streamlit الافتراضية */
    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    .viewerBadge_container__1QSob { display: none !important; }
    .st-emotion-cache-164nlkn { display: none !important; }
    div[class^="viewerBadge"] { display: none !important; }
    .stDeployButton { display: none !important; }

    /* ===== الهيدر الرئيسي ===== */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        margin: 10px 0 20px 0;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.8);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }
    
    .hero-logo {
        font-size: 60px;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        color: #e0e0e0;
        font-size: 16px;
        letter-spacing: 2px;
        font-weight: 500;
    }
    
    /* ===== هيدر صفحة التقارير ===== */
    .page-header {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        margin: 10px 0 20px 0;
        border: 2px solid rgba(255, 215, 0, 0.4);
    }
    
    .page-icon {
        font-size: 50px;
        margin-bottom: 10px;
    }
    
    .page-title {
        font-size: 36px;
        font-weight: 800;
        color: #FFD700;
        margin-bottom: 10px;
    }
    
    .page-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 14px;
    }
    
    /* ===== إشعار التقارير ===== */
    .info-banner {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(184, 134, 11, 0.05));
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 12px;
        padding: 15px 25px;
        margin: 15px 0;
        color: #FFD700;
        font-size: 0.95rem;
        text-align: center;
    }
    
    /* ===== شريط الإحصائيات ===== */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        padding: 20px;
        background: rgba(0, 31, 63, 0.5);
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .stat-item-small {
        text-align: center;
        padding: 10px 25px;
    }
    
    .stat-number {
        display: block;
        font-size: 2rem;
        font-weight: 800;
        color: #FFD700;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
    }
    
    /* ===== عنوان القسم ===== */
    .section-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 215, 0, 0.2);
    }
    
    /* ===== بطاقات التقارير ===== */
    .report-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95));
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    
    .report-card:hover {
        border-color: rgba(255, 215, 0, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .card-icon {
        font-size: 1.5rem;
    }
    
    .card-type {
        background: rgba(255, 215, 0, 0.2);
        color: #FFD700;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .card-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .card-meta {
        display: flex;
        gap: 15px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
    }
    
    /* ===== حالة فارغة ===== */
    .empty-state {
        text-align: center;
        padding: 60px 30px;
        background: rgba(0, 31, 63, 0.5);
        border-radius: 20px;
        border: 2px dashed rgba(255, 215, 0, 0.2);
        margin: 30px 0;
    }
    
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 20px;
        opacity: 0.6;
    }
    
    .empty-title {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .empty-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 1rem;
    }
    
    /* ===== معاينة التقرير ===== */
    .preview-header {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .preview-icon {
        font-size: 1.3rem;
    }
    
    .preview-title {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* ===== العناصر العامة ===== */
    .section-header {
        text-align: center;
        margin: 25px 0 20px 0;
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: bold;
    }

    /* ===== أزرار الاختيار ===== */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row-reverse !important;
        justify-content: center !important;
        gap: 12px !important;
        flex-wrap: wrap !important;
        background: rgba(0, 0, 0, 0.3) !important;
        padding: 15px !important;
        border-radius: 15px !important;
        margin: 0 0 25px 0 !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95)) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        flex: 1 !important;
        min-width: 140px !important;
        max-width: 200px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    div[role="radiogroup"] label:hover {
        border-color: #FFD700 !important;
        transform: translateY(-2px) !important;
    }
    
    div[role="radiogroup"] label[data-checked="true"],
    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(184, 134, 11, 0.15)) !important;
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3) !important;
    }

    /* ===== بطاقات الإدخال ===== */
    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 15px;
        padding: 20px;
        margin: 8px 0;
        border: 1px solid rgba(255, 215, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .input-card:hover {
        border-color: rgba(255, 215, 0, 0.4);
    }

    .input-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .input-icon {
        width: 45px; height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #FFD700, #B8860B);
        border-radius: 10px;
        font-size: 1.3rem;
    }

    .input-title {
        color: #FFD700;
        font-size: 1.1rem;
        font-weight: 700;
    }

    .input-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin-top: 3px;
    }

    /* ===== حقل النص ===== */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1rem !important;
        padding: 15px !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2) !important;
    }

    /* ===== رفع الملفات ===== */
    [data-testid="stFileUploader"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px dashed rgba(255, 215, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #FFD700 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #FFD700, #B8860B) !important;
        color: #001f3f !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    /* ===== الأزرار ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #DAA520 50%, #FFD700 100%) !important;
        background-size: 200% auto !important;
        color: #001f3f !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        border: none !important;
        box-shadow: 0 5px 20px rgba(218, 165, 32, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(218, 165, 32, 0.4) !important;
    }

    /* ===== زر التحميل ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 12px 30px !important;
        border-radius: 10px !important;
        border: none !important;
    }

    /* ===== شريط النجاح ===== */
    .success-banner {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 18px 25px;
        text-align: center;
        margin: 15px 0;
    }
    
    .success-banner span {
        color: #22c55e;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .success-hint {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 8px;
        padding: 10px 18px;
        margin: 10px 0;
        color: rgba(34, 197, 94, 0.85);
        font-size: 0.85rem;
        text-align: center;
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
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        text-align: center;
    }
    
    .progress-icon {
        font-size: 2rem;
        margin-bottom: 12px;
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        height: 12px;
        overflow: hidden;
        margin: 15px 0;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
        background-size: 200% 100%;
        border-radius: 8px;
        animation: progressShine 1.5s infinite linear;
    }
    
    @keyframes progressShine {
        0% { background-position: 200% center; }
        100% { background-position: -200% center; }
    }
    
    .progress-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        margin-top: 8px;
    }

    /* ===== الفوتر ===== */
    .footer-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 12px;
        padding: 25px 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 215, 0, 0.3);
        text-align: center;
    }
    
    .footer-line {
        width: 50px; height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 0 auto 15px auto;
    }
    
    .footer-org {
        color: #FFD700;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .footer-unit {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-bottom: 12px;
    }
    
    .footer-divider {
        width: 80px; height: 1px;
        background: rgba(255, 215, 0, 0.3);
        margin: 12px auto;
    }
    
    .footer-copy {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
    }

    /* ===== الجدول ===== */
    .stDataFrame {
        background: rgba(0, 31, 63, 0.5) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame table {
        color: white !important;
    }
    
    .stDataFrame th {
        background: rgba(255, 215, 0, 0.2) !important;
        color: #FFD700 !important;
    }

    /* ===== الاستجابة ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 32px; }
        .hero-section { padding: 25px 15px; }
        .stats-bar { flex-direction: column; gap: 15px; }
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 CSS الشريط الجانبي
# ---------------------------------------------------------
SIDEBAR_CSS = """
<style>
    /* تخصيص الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001f3f 0%, #0a1628 50%, #001f3f 100%) !important;
        border-left: 2px solid rgba(255, 215, 0, 0.3) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 20px;
    }
    
    /* عناصر الشريط الجانبي */
    .sidebar-container {
        text-align: center;
        padding: 20px 10px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        margin-bottom: 20px;
    }
    
    .sidebar-logo {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    .sidebar-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: 800;
    }
    
    .sidebar-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent);
        margin: 20px 0;
    }
    
    .sidebar-info {
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 15px;
        text-align: center;
    }
    
    .sidebar-info p {
        color: rgba(255, 255, 255, 0.7);
        margin: 0;
        font-size: 0.85rem;
    }
    
    .sidebar-info .info-count {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: 800;
        display: block;
        margin-top: 5px;
    }
    
    .sidebar-footer-text {
        text-align: center;
        padding: 15px;
        border-top: 1px solid rgba(255, 215, 0, 0.1);
        margin-top: auto;
    }
    
    .sidebar-footer-text p {
        color: rgba(255, 255, 255, 0.4);
        margin: 3px 0;
        font-size: 0.75rem;
    }
    
    /* أزرار الشريط الجانبي */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05)) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 215, 0, 0.1)) !important;
        border-color: #FFD700 !important;
        transform: translateX(-3px) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(184, 134, 11, 0.2)) !important;
        border-color: #FFD700 !important;
        color: #FFD700 !important;
        font-weight: 700 !important;
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 القوالب (خلفية بيضاء)
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Tajawal:wght@400;700&display=swap');
    
    :root {
        --primary: #003366;
        --secondary: #c5a059;
        --bg: #ffffff;
        --text: #333333;
    }
    
    body {
        font-family: 'Cairo', sans-serif;
        background-color: #f9fafb;
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
    
    header {
        text-align: center;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 30px;
        margin-bottom: 40px;
    }
    
    header h1 {
        color: var(--primary);
        font-size: 2.4em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    header p { color: #666; font-size: 1.1em; margin: 5px 0; }
    
    .card {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    
    .card:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    
    h2 {
        color: var(--primary);
        font-size: 1.8em;
        border-right: 5px solid var(--secondary);
        padding-right: 15px;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    
    h3 { color: #444; font-size: 1.4em; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
    
    .stats-row { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
    
    .stat-item {
        flex: 1;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    
    .stat-item .stat-value { display: block; font-size: 2.2em; font-weight: bold; color: var(--primary); margin-bottom: 5px; }
    .stat-item .stat-label { font-size: 1em; color: #777; }
    
    table { width: 100%; border-collapse: collapse; margin: 25px 0; }
    thead th { background-color: var(--primary); color: white; padding: 15px; text-align: right; font-weight: 600; }
    tbody td { border-bottom: 1px solid #eee; padding: 12px 15px; color: #444; }
    tbody tr:nth-child(even) { background-color: #fcfcfc; }
    tbody tr:hover { background-color: #f0f4f8; }
    
    ul li { margin-bottom: 10px; position: relative; padding-right: 20px; }
    ul li::before { content: "•"; color: var(--secondary); font-weight: bold; font-size: 1.5em; position: absolute; right: 0; top: -5px; }

    .report-signature { margin-top: 80px; text-align: center; padding: 40px; border-top: 1px solid #eee; background-color: #fcfcfc; border-radius: 8px; }
    .signature-icon { font-size: 40px; margin-bottom: 15px; display: block; }
    .signature-org { color: var(--primary); font-weight: 800; font-size: 1.3em; margin: 0; }
    .signature-unit { color: var(--secondary); font-size: 1.1em; margin: 5px 0; font-weight: 600; }
    .signature-line { width: 80px; height: 3px; background: var(--secondary); margin: 20px auto; }
</style>
"""

STYLE_DIGITAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    :root { --primary: #2563eb; --accent: #7c3aed; --bg: #f3f4f6; --text-main: #1f2937; --text-muted: #6b7280; }
    
    body { font-family: 'Cairo', sans-serif; background-color: var(--bg); color: var(--text-main); margin: 0; padding: 40px; direction: rtl; }
    .container { max-width: 1200px; margin: 0 auto; }
    
    .dashboard-header { background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); text-align: center; margin-bottom: 40px; border-bottom: 4px solid var(--primary); }
    .dashboard-header h1 { margin: 0; font-size: 2.5em; color: var(--primary); font-weight: 900; }
    .dashboard-header p { color: var(--text-muted); font-size: 1.2em; margin-top: 10px; }
    
    .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; margin-bottom: 40px; }
    .metric-card { background: white; border-radius: 16px; padding: 30px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.04); border: 1px solid #e5e7eb; }
    .metric-card:hover { transform: translateY(-5px); border-color: var(--primary); }
    .metric-value { display: block; font-size: 3em; font-weight: 900; color: var(--accent); margin-bottom: 10px; }
    .metric-label { color: var(--text-muted); font-size: 1.1em; font-weight: 600; }
    
    .data-card { background: white; border-radius: 16px; padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); }
    .data-card h2 { color: var(--text-main); font-size: 1.5em; border-right: 4px solid var(--primary); padding-right: 15px; margin-bottom: 25px; }
    
    .report-signature { background: white; border-radius: 20px; padding: 40px; text-align: center; margin-top: 50px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
    .signature-icon { font-size: 35px; margin-bottom: 15px; }
    .signature-org { color: var(--primary); font-size: 1.4em; font-weight: 800; margin: 0; }
    .signature-unit { color: var(--text-muted); margin-top: 5px; font-size: 1.1em; }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    body { font-family: 'Cairo', sans-serif; background: #f8f9fa; color: #333; padding: 40px; direction: rtl; }
    .container { max-width: 1200px; margin: 0 auto; background: white; padding: 50px; border: 1px solid #e9ecef; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-radius: 8px; }
    
    header { text-align: center; background: #f1f3f5; padding: 40px; border-radius: 12px; margin-bottom: 40px; border-bottom: 5px solid #0056b3; }
    header h1 { margin: 0; color: #0056b3; font-size: 2.5em; font-weight: 800; }
    
    .stats-grid { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 40px; flex-wrap: wrap; }
    .stat-card { background: white; border: 1px solid #dee2e6; flex: 1; min-width: 200px; padding: 25px; text-align: center; border-radius: 8px; border-top: 4px solid #17a2b8; }
    .stat-value { font-size: 2.5em; font-weight: bold; color: #0056b3; display: block; }
    .stat-label { color: #6c757d; font-size: 1.1em; }
    
    .analysis-section { margin-bottom: 40px; }
    h2 { color: #0056b3; font-size: 1.8em; border-bottom: 2px solid #e9ecef; padding-bottom: 15px; margin-bottom: 25px; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    th { background: #0056b3; color: white; padding: 15px; font-weight: 600; }
    td { border: 1px solid #dee2e6; padding: 15px; }
    tr:nth-child(even) { background: #f8f9fa; }
    
    .report-signature { text-align: center; margin-top: 80px; padding-top: 30px; border-top: 2px solid #e9ecef; }
    .signature-org { font-weight: bold; font-size: 1.2em; color: #0056b3; }
</style>
"""

STYLE_PRESENTATION = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Cairo', sans-serif; background: #2c3e50; margin: 0; height: 100vh; overflow: hidden; display: flex; align-items: center; justify-content: center; direction: rtl; }
    
    .presentation-container { width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; position: relative; }
    
    .slide { background: white; width: 90%; height: 85%; position: absolute; opacity: 0; visibility: hidden; transition: opacity 0.6s ease; border-radius: 20px; padding: 60px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); display: flex; flex-direction: column; overflow-y: auto; }
    .slide.active { opacity: 1; visibility: visible; z-index: 10; }
    
    .slide-header { border-bottom: 5px solid #c5a059; padding-bottom: 20px; margin-bottom: 40px; }
    .header-title h2 { color: #003366; font-size: 2.5em; margin: 0; font-weight: 800; }
    .slide-content { flex: 1; font-size: 1.6em; color: #333; line-height: 1.8; }
    .slide-content ul { list-style: none; padding: 0; }
    .slide-content ul li { padding: 15px 0; border-bottom: 1px solid #eee; padding-right: 30px; position: relative; }
    .slide-content ul li::before { content: "◆"; color: #c5a059; position: absolute; right: 0; font-size: 0.8em; }
    
    .slide.cover { text-align: center; justify-content: center; align-items: center; background: linear-gradient(135deg, #fdfbf7 0%, #fff 100%); border: 15px solid #003366; }
    .main-title { font-size: 4em; color: #003366; margin-bottom: 30px; font-weight: 900; }
    .sub-title { font-size: 2em; color: #c5a059; }
    
    .nav-controls { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 1000; }
    .nav-btn { background: linear-gradient(135deg, #003366, #004080); color: white; border: none; width: 60px; height: 60px; border-radius: 50%; cursor: pointer; font-size: 1.4em; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .nav-btn:hover { background: linear-gradient(135deg, #004080, #0056b3); transform: scale(1.1); }
    
    .page-number { position: fixed; bottom: 30px; right: 30px; background: rgba(0, 51, 102, 0.9); color: white; padding: 12px 24px; border-radius: 30px; font-size: 1.1em; font-weight: 700; z-index: 1000; }
    .presentation-signature { position: fixed; bottom: 30px; left: 30px; background: rgba(0, 51, 102, 0.9); color: white; padding: 12px 20px; border-radius: 10px; font-size: 0.9em; z-index: 1000; max-width: 300px; text-align: center; }
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

SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    let totalSlides = 0;
    
    function initPresentation() {
        const slides = document.querySelectorAll('.slide');
        totalSlides = slides.length;
        if (totalSlides > 0) {
            slides.forEach((slide, index) => {
                slide.classList.remove('active');
                if (index === 0) slide.classList.add('active');
            });
            currentSlideIndex = 1;
            updatePageNumber();
        }
    }
    
    function updatePageNumber() {
        const pageNum = document.getElementById('page-num');
        if (pageNum) pageNum.innerText = currentSlideIndex + ' / ' + totalSlides;
    }
    
    function showSlide(index) {
        const slides = document.querySelectorAll('.slide');
        if (index < 1) index = 1;
        if (index > totalSlides) index = totalSlides;
        currentSlideIndex = index;
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === currentSlideIndex - 1) slide.classList.add('active');
        });
        updatePageNumber();
    }
    
    function nextSlide() { if (currentSlideIndex < totalSlides) showSlide(currentSlideIndex + 1); }
    function prevSlide() { if (currentSlideIndex > 1) showSlide(currentSlideIndex - 1); }
    
    document.addEventListener('keydown', function(e) { 
        if (e.key === "ArrowLeft" || e.key === " ") { e.preventDefault(); nextSlide(); }
        if (e.key === "ArrowRight") { e.preventDefault(); prevSlide(); }
    });
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPresentation);
    } else {
        setTimeout(initPresentation, 100);
    }
</script>
"""
