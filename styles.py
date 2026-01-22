# styles.py

# ---------------------------------------------------------
# 🎨 CSS الرئيسي للواجهة (Streamlit Interface)
# ---------------------------------------------------------
MAIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    /* ========================================================= */
    /* 1. إعدادات الصفحة والهيكلية العامة */
    /* ========================================================= */
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    /* ========================================================= */
    /* 2. 🔥 الزر العائم (Gemini Style Trigger) 🔥 */
    /* ========================================================= */
    
    /* الخطوة 1: التعامل مع الهيدر ليكون شفافاً ويسمح بالمرور */
    header[data-testid="stHeader"] {
        background: transparent !important;
        border-bottom: none !important;
        pointer-events: none !important; /* يسمح بالضغط على العناصر خلف الهيدر */
        height: 0 !important; /* تقليص ارتفاعه لمنع حجز مساحة */
    }

    /* الخطوة 2: إجبار الزر على الظهور وتغيير مكانه وشكله */
    /* نستهدف جميع الاحتمالات لزر القائمة في نسخ Streamlit المختلفة */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    button[kind="header"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important; /* إعادة تفعيل النقر للزر */
        
        /* التثبيت في الموقع (مثل Gemini) */
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        z-index: 99999999 !important; /* طبقة عليا جداً */
        
        /* التصميم الجمالي (دائري ونظيف) */
        background: rgba(0, 31, 63, 0.6) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 50% !important; /* دائري مثل تطبيقات جوجل */
        width: 45px !important;
        height: 45px !important;
        
        align-items: center !important;
        justify-content: center !important;
        
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }

    /* تأثير التحويم (Hover) */
    [data-testid="collapsedControl"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover,
    button[kind="header"]:hover {
        background: #FFD700 !important; /* ذهبي عند التحويم */
        color: #001f3f !important;
        transform: scale(1.1);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
        border-color: #FFD700 !important;
    }

    /* الخطوة 3: أيقونة القائمة (Hamburger Icon) */
    /* نخفي SVG الافتراضي للسهم */
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        display: none !important;
    }

    /* نضع خطوط القائمة الثلاثية */
    [data-testid="collapsedControl"]::after,
    [data-testid="stSidebarCollapsedControl"]::after {
        content: "☰" !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: inherit !important; /* يأخذ لون العنصر الأب */
        line-height: 1 !important;
        margin-top: -2px !important;
    }
    
    /* لون الأيقونة الافتراضي */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {
        color: #FFD700 !important;
    }

    /* ========================================================= */
    /* 3. الشريط الجانبي السلس (Smooth Sidebar Overlay) */
    /* ========================================================= */
    
    [data-testid="stSidebar"] {
        /* جعله يطفو فوق المحتوى بدلاً من دفعه */
        position: fixed !important;
        top: 0 !important;
        right: 0 !important;
        height: 100vh !important;
        width: 320px !important; /* عرض ثابت وأنيق */
        min-width: 320px !important;
        
        /* الخلفية والتصميم */
        background: linear-gradient(180deg, #001f3f 0%, #0a1628 100%) !important;
        border-left: 1px solid rgba(255, 215, 0, 0.2) !important;
        box-shadow: -10px 0 30px rgba(0, 0, 0, 0.7) !important;
        z-index: 999999 !important;
        
        /* تحسين الحركة لتكون ناعمة مثل Gemini */
        transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    
    /* إخفاء القوائم الافتراضية داخل الشريط */
    [data-testid="stSidebarNav"] { display: none !important; }
    
    /* زر إغلاق الشريط (X) */
    button[data-testid="stSidebarCollapseButton"] {
        position: absolute !important;
        top: 20px !important;
        left: 20px !important; /* في الجهة اليسرى للشريط */
        background: transparent !important;
        border: none !important;
        color: rgba(255, 255, 255, 0.5) !important;
        transition: 0.3s !important;
    }
    
    button[data-testid="stSidebarCollapseButton"]:hover {
        color: #FFD700 !important;
        transform: rotate(90deg);
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 50%;
    }

    /* محتوى الشريط */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 70px !important;
    }

    /* إخفاء الزخارف العلوية المزعجة */
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* ========================================================= */
    /* 4. تنسيقات العناصر الداخلية (بطاقات، نصوص) */
    /* ========================================================= */

    /* الهيدر الرئيسي (Hero) */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.85));
        border-radius: 20px;
        padding: 60px 30px;
        text-align: center;
        margin: 20px auto;
        margin-top: 80px; /* مسافة لعدم تداخل الزر */
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 50px rgba(0, 10, 30, 0.5);
        position: relative;
        overflow: hidden;
        animation: slideDown 0.8s ease-out;
    }
    @keyframes slideDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }

    .main-title {
        font-size: 48px; font-weight: 800;
        background: linear-gradient(180deg, #FFD700 0%, #F0E68C 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 15px; text-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .sub-title { color: #ccc; font-size: 1.1rem; letter-spacing: 1px; }

    /* البطاقات (Inputs & Selection) */
    .input-card {
        background: rgba(0, 31, 63, 0.7);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 16px;
        padding: 25px;
        margin: 10px 0;
        transition: transform 0.3s ease, border-color 0.3s;
    }
    .input-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 215, 0, 0.4);
    }
    
    /* تنسيق أزرار الراديو لتكون بطاقات */
    div[role="radiogroup"] {
        background: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 15px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        direction: rtl;
    }
    div[role="radiogroup"] label {
        background: rgba(0, 31, 63, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px 20px;
        flex: 1;
        min-width: 150px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: #FFD700;
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(0, 0, 0, 0));
        border-color: #FFD700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
    }
    .stRadio label { display: none !important; }

    /* حقول الإدخال */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #fff !important;
        padding: 15px !important;
        direction: rtl;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; }
    
    /* أزرار الرفع والتحميل */
    button { font-family: 'Tajawal', sans-serif !important; }
    
    /* زر المعالجة الكبير */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700, #DAA520) !important;
        color: #001f3f !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        box-shadow: 0 5px 20px rgba(218, 165, 32, 0.3) !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(218, 165, 32, 0.5) !important;
    }

    /* عناصر الشريط الجانبي */
    .sidebar-header {
        text-align: center; padding: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    .sidebar-title { color: #FFD700; font-size: 1.2rem; font-weight: bold; }
    .sidebar-report-card {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid transparent;
        transition: 0.2s;
    }
    .sidebar-report-card:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(255,215,0,0.3);
    }
    .report-card-title { color: #fff; font-weight: 600; font-size: 0.9rem; }
    .report-card-time { color: #aaa; font-size: 0.75rem; margin-top: 5px; }

    /* إخفاء أي Labels زائدة */
    .stFileUploader label, .stTextArea label { display: none !important; }

    /* الاستجابة للجوال */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] { width: 100% !important; min-width: 100% !important; }
        .hero-section { padding: 40px 20px; margin-top: 70px; }
        .main-title { font-size: 32px; }
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 القوالب (Templates) - لم يتم تغييرها للحفاظ على الهيكلية
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    :root { --navy-blue: #001f3f; --gold: #c5a059; --light-gold: #f0e6d2; --white: #ffffff; --gray: #f9f9f9; --text: #333; }
    body { font-family: 'Tajawal', sans-serif; background-color: var(--gray); color: var(--text); line-height: 1.8; direction: rtl; text-align: right; margin: 0; padding: 0; }
    .container { max-width: 1200px; margin: 30px auto; padding: 40px; background: white; box-shadow: 0 0 50px rgba(0,0,0,0.05); }
    header { border-bottom: 4px solid var(--navy-blue); padding-bottom: 20px; margin-bottom: 40px; text-align: center; }
    header h1 { color: var(--navy-blue); font-size: 2.2em; margin: 0; font-weight: 800; }
    header h2 { color: var(--gold); font-size: 1.4em; margin-top: 10px; font-weight: 600; }
    .card { background-color: #fff; margin-bottom: 30px; padding: 10px; }
    .card h3 { color: var(--navy-blue); font-size: 1.6em; border-right: 5px solid var(--gold); padding-right: 15px; margin-bottom: 20px; background: linear-gradient(90deg, var(--light-gold) 0%, transparent 100%); padding: 10px 15px; border-radius: 4px; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.95em; border: 1px solid #eee; }
    table th { background-color: var(--navy-blue); color: white; padding: 15px; font-weight: bold; border: 1px solid #001f3f; }
    table td { border: 1px solid #ddd; padding: 12px 15px; color: #444; }
    table tr:nth-child(even) { background-color: #f8f9fa; }
    ul { list-style: none; padding: 0; margin: 0; }
    ul li { padding: 12px 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; transition: background 0.2s; }
    ul li:hover { background-color: #fcfcfc; }
    ul li span { font-weight: 600; color: #555; font-size: 1rem; }
    ul li span.value { color: var(--navy-blue); font-weight: 800; font-size: 1.1rem; background: transparent; padding: 0; border: none; }
    footer { text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 0.85rem; }
</style>
"""

STYLE_DIGITAL = """
<style>
    body { font-family: 'Cairo', sans-serif; line-height: 1.7; background-color: #f4f7f9; color: #333; direction: rtl; }
    .container { max-width: 1200px; margin: 20px auto; padding: 25px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07); }
    header { text-align: center; padding-bottom: 20px; margin-bottom: 30px; border-bottom: 3px solid #0056b3; }
    h1 { color: #0056b3; font-size: 2.4em; font-weight: 700; }
    h2 { color: #007bff; font-size: 2em; border-bottom: 2px solid #f0f0f0; margin-bottom: 20px; }
    .card { background-color: #fdfdfd; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; margin-top: 20px; box-shadow: 0 3px 8px rgba(0,0,0,0.05); }
    ul li { position: relative; padding-right: 35px; margin-bottom: 12px; }
    ul li::before { content: '•'; position: absolute; right: 0; color: #007bff; font-size: 1.8em; line-height: 1; }
    .goal { background-color: #e6f7ff; border: 1px solid #b3e0ff; padding: 18px; border-radius: 8px; text-align: center; margin-top: 20px; font-weight: bold; color: #0056b3; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; display: block; overflow-x: auto; white-space: nowrap; }
    thead th { background-color: #007bff; color: white; padding: 14px; }
    td { padding: 14px; border: 1px solid #e0e0e0; text-align: center; }
    footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-style: italic; color: #777; }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    body { font-family: 'Cairo', sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.7; direction: rtl; }
    .container { max-width: 1100px; margin: 20px auto; padding: 20px; }
    header { background-color: #004a99; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0, 74, 153, 0.2); }
    .report-section { background-color: #fff; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.07); margin-bottom: 25px; padding: 25px; }
    .report-section h2 { color: #004a99; border-bottom: 3px solid #0056b3; padding-bottom: 10px; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
    .stat-card { background-color: #eef5ff; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #d0e3ff; }
    .stat-card .value { font-size: 2.2rem; font-weight: 700; color: #004a99; word-break: break-all; }
    .pyramid-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    .tier-card { border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background-color: #fcfcfc; border-top: 6px solid; }
    .tier-upper { border-top-color: #d90429; } .tier-middle { border-top-color: #f7b801; } 
    .bar-container { background-color: #e0e0e0; border-radius: 5px; height: 12px; margin-top: 12px; width: 100%; overflow: hidden; }
    .bar { height: 100%; border-radius: 5px; } .tier-upper .bar { background-color: #d90429; } .tier-middle .bar { background-color: #f7b801; }
    footer { text-align: center; margin-top: 30px; color: #888; font-size: 0.9rem; border-top: 1px solid #ccc; padding-top: 20px;}
</style>
"""

STYLE_PRESENTATION = """
<style>
    :root { --primary-navy: #002b49; --primary-blue: #004e89; --gold-main: #c5a059; --gold-light: #e6c885; --white: #ffffff; --grey-light: #f8f9fa; --text-dark: #333333; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Cairo', sans-serif; background-color: var(--primary-navy); overflow: hidden; height: 100vh; width: 100vw; direction: rtl; margin:0;}
    .presentation-container { width: 100%; height: 100%; position: relative; background: radial-gradient(circle at center, #003865 0%, #002035 100%); }
    .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; visibility: hidden; transform: scale(0.95); transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1); display: flex; flex-direction: column; padding: 40px 60px; background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIiBvcGFjaXR5PSIwLjAzIj48cGF0aCBkPSJNMjAgMjBMMCAwSDQwTDgwIDgwIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMSIvPjwvc3ZnPg=='); }
    .slide.active { opacity: 1; visibility: visible; transform: scale(1); z-index: 10; }
    .slide-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--gold-main); padding-bottom: 15px; margin-bottom: 25px; flex-shrink: 0; }
    .header-title h2 { color: var(--gold-main); font-size: 2rem; font-weight: 800; }
    .header-logo { font-family: 'Tajawal'; color: var(--white); font-weight: bold; display: flex; align-items: center; gap: 10px; }
    .slide-content { flex-grow: 1; display: flex; gap: 40px; height: 100%; overflow: hidden; }
    .text-panel { flex: 3; background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 30px; color: var(--text-dark); box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow-y: auto; border-right: 5px solid var(--gold-main); }
    .visual-panel { flex: 2; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--white); text-align: center; }
    h3 { color: var(--primary-blue); font-size: 1.6rem; margin-bottom: 15px; border-bottom: 1px dashed #ccc; padding-bottom: 5px; }
    p { font-size: 1.2rem; line-height: 1.8; margin-bottom: 20px; text-align: justify; }
    li { font-size: 1.15rem; margin-bottom: 10px; line-height: 1.6; }
    strong { color: var(--primary-navy); font-weight: 800; }
    .icon-box { font-size: 5rem; color: var(--gold-main); margin-bottom: 20px; text-shadow: 0 5px 15px rgba(0,0,0,0.5); animation: float 4s ease-in-out infinite; }
    .slide.cover { align-items: center; justify-content: center; text-align: center; background: linear-gradient(135deg, var(--primary-navy) 30%, #001a2c 100%); }
    .cover-content { border: 2px solid var(--gold-main); padding: 60px; position: relative; background: rgba(0,0,0,0.4); backdrop-filter: blur(5px); }
    .main-title { font-size: 3.5rem; color: var(--white); margin-bottom: 15px; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .sub-title { font-size: 1.8rem; color: var(--gold-main); margin-bottom: 40px; font-weight: 300; }
    .nav-controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 100; }
    .nav-btn { background: transparent; border: 2px solid var(--gold-main); color: var(--gold-main); width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 1.2rem; transition: 0.3s; display: flex; align-items: center; justify-content: center; }
    .nav-btn:hover { background: var(--gold-main); color: var(--primary-navy); transform: scale(1.1); }
    .page-number { position: absolute; bottom: 25px; right: 60px; color: var(--gold-main); font-size: 1.2rem; font-weight: bold; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    .signature-box { margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--gold-main); text-align: center; }
    .signature-title { font-size: 0.9rem; color: #aaa; margin-bottom: 10px; }
    .signature-name { font-size: 1.4rem; color: var(--gold-main); font-weight: bold; font-family: 'Tajawal'; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

STYLE_EXECUTIVE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;800&display=swap');
    body { font-family: 'Tajawal', sans-serif; background-color: #ffffff; color: #222; direction: rtl; }
    .container { max-width: 900px; margin: 40px auto; padding: 40px; border: 1px solid #eee; box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid #000; padding-bottom: 20px; margin-bottom: 40px; }
    .brand { font-size: 1.5rem; font-weight: 800; letter-spacing: -1px; color: #002b49; }
    h1 { font-size: 2.8rem; font-weight: 900; line-height: 1.1; margin-bottom: 10px; color: #000; }
    .executive-summary { font-size: 1.3rem; line-height: 1.6; color: #444; margin-bottom: 40px; border-right: 5px solid #FFD700; padding-right: 20px; background: #fafafa; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; margin-bottom: 30px; }
    .metric-box { padding: 20px; background: #f9f9f9; border-radius: 8px; border: 1px solid #eee; }
    .metric-val { font-size: 2.5rem; font-weight: 800; color: #002b49; }
    .metric-lbl { font-size: 1rem; color: #666; text-transform: uppercase; }
    .section-title { font-size: 1.2rem; font-weight: 800; text-transform: uppercase; margin-top: 30px; margin-bottom: 15px; color: #c5a059; border-bottom: 2px solid #eee; display: inline-block;}
    footer { margin-top: 60px; border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #999; font-size: 0.8rem; }
</style>
"""

SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    function updateSlide() {
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        if(totalSlides === 0) return;
        
        slides.forEach(slide => { slide.classList.remove('active'); });
        
        const activeSlide = document.getElementById(`slide-${currentSlideIndex}`);
        if(activeSlide) activeSlide.classList.add('active');
        
        const pageNum = document.getElementById('page-num');
        if(pageNum) pageNum.innerText = `${currentSlideIndex} / ${totalSlides}`;
    }
    function nextSlide() { const totalSlides = document.querySelectorAll('.slide').length; if (currentSlideIndex < totalSlides) { currentSlideIndex++; updateSlide(); } }
    function prevSlide() { if (currentSlideIndex > 1) { currentSlideIndex--; updateSlide(); } }
    document.addEventListener('keydown', function(event) { if (event.key === "ArrowLeft" || event.key === "Space") nextSlide(); else if (event.key === "ArrowRight") prevSlide(); });
    setTimeout(updateSlide, 100);
</script>
"""
