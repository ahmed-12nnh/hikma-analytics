import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO, BytesIO
import time
import base64
import re
from collections import Counter

# ---------------------------------------------------------
# 📦 استيراد المكتبات الإضافية (مع معالجة الأخطاء)
# ---------------------------------------------------------
try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = None

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 📝 القوالب الجاهزة
# ---------------------------------------------------------
REPORT_TEMPLATES = {
    "تقرير أداء": {
        "icon": "📊",
        "description": "تقرير لقياس ومتابعة مؤشرات الأداء",
        "template": """
## تقرير الأداء

### الفترة: [حدد الفترة]

### ملخص تنفيذي:
[اكتب ملخصاً موجزاً عن الأداء العام]

### مؤشرات الأداء الرئيسية (KPIs):
- المؤشر الأول: [القيمة] - [النسبة المئوية]%
- المؤشر الثاني: [القيمة] - [النسبة المئوية]%
- المؤشر الثالث: [القيمة] - [النسبة المئوية]%

### الإنجازات:
1. [الإنجاز الأول]
2. [الإنجاز الثاني]
3. [الإنجاز الثالث]

### التحديات:
1. [التحدي الأول]
2. [التحدي الثاني]

### التوصيات:
1. [التوصية الأولى]
2. [التوصية الثانية]
"""
    },
    "خطة استراتيجية": {
        "icon": "🎯",
        "description": "خطة استراتيجية شاملة للمشاريع",
        "template": """
## الخطة الاستراتيجية

### الرؤية:
[اكتب الرؤية هنا]

### الرسالة:
[اكتب الرسالة هنا]

### الأهداف الاستراتيجية:
1. الهدف الأول: [وصف الهدف]
   - المؤشر: [مؤشر القياس]
   - المستهدف: [القيمة المستهدفة]

2. الهدف الثاني: [وصف الهدف]
   - المؤشر: [مؤشر القياس]
   - المستهدف: [القيمة المستهدفة]

### المبادرات والمشاريع:
| المبادرة | المسؤول | الجدول الزمني | الميزانية |
|----------|---------|---------------|-----------|
| [المبادرة 1] | [الاسم] | [الفترة] | [المبلغ] |
| [المبادرة 2] | [الاسم] | [الفترة] | [المبلغ] |

### المخاطر والتحديات:
1. [المخاطرة الأولى] - خطة المعالجة: [الخطة]
2. [المخاطرة الثانية] - خطة المعالجة: [الخطة]
"""
    },
    "محضر اجتماع": {
        "icon": "📋",
        "description": "محضر اجتماع رسمي مع القرارات",
        "template": """
## محضر اجتماع

### بيانات الاجتماع:
- **التاريخ:** [اليوم/الشهر/السنة]
- **الوقت:** [من الساعة] إلى [الساعة]
- **المكان:** [مكان الاجتماع]
- **رئيس الاجتماع:** [الاسم]

### الحضور:
1. [الاسم] - [المنصب]
2. [الاسم] - [المنصب]
3. [الاسم] - [المنصب]

### جدول الأعمال:
1. [البند الأول]
2. [البند الثاني]
3. [البند الثالث]

### المناقشات:
[تفاصيل ما تم مناقشته]

### القرارات:
| # | القرار | المسؤول | الموعد النهائي |
|---|--------|---------|----------------|
| 1 | [القرار] | [الاسم] | [التاريخ] |
| 2 | [القرار] | [الاسم] | [التاريخ] |

### موعد الاجتماع القادم:
[التاريخ والوقت]
"""
    },
    "تقرير مالي": {
        "icon": "💰",
        "description": "تقرير مالي شامل بالأرقام والنسب",
        "template": """
## التقرير المالي

### الفترة المالية: [من تاريخ] إلى [تاريخ]

### ملخص الإيرادات:
- إجمالي الإيرادات: [المبلغ] دينار
- نسبة النمو: [النسبة]%

### ملخص المصروفات:
- إجمالي المصروفات: [المبلغ] دينار
- نسبة التغير: [النسبة]%

### تفاصيل الميزانية:
| البند | المخطط | الفعلي | الفرق | النسبة |
|-------|--------|--------|-------|--------|
| [البند 1] | [مبلغ] | [مبلغ] | [مبلغ] | [%] |
| [البند 2] | [مبلغ] | [مبلغ] | [مبلغ] | [%] |

### المؤشرات المالية:
- صافي الربح: [المبلغ] دينار
- هامش الربح: [النسبة]%
- العائد على الاستثمار: [النسبة]%

### التوصيات المالية:
1. [التوصية الأولى]
2. [التوصية الثانية]
"""
    },
    "تقرير مشروع": {
        "icon": "🚀",
        "description": "تقرير متابعة تقدم المشروع",
        "template": """
## تقرير متابعة المشروع

### معلومات المشروع:
- **اسم المشروع:** [اسم المشروع]
- **مدير المشروع:** [الاسم]
- **تاريخ البداية:** [التاريخ]
- **تاريخ النهاية المتوقع:** [التاريخ]

### حالة المشروع: 🟢 على المسار / 🟡 متأخر قليلاً / 🔴 متأخر

### نسبة الإنجاز: [النسبة]%

### المهام المنجزة:
1. ✅ [المهمة الأولى]
2. ✅ [المهمة الثانية]

### المهام الجارية:
1. 🔄 [المهمة] - نسبة الإنجاز: [%]
2. 🔄 [المهمة] - نسبة الإنجاز: [%]

### المهام القادمة:
1. ⏳ [المهمة] - الموعد: [التاريخ]
2. ⏳ [المهمة] - الموعد: [التاريخ]

### المخاطر والمشاكل:
| المشكلة | الأثر | الحل المقترح |
|---------|-------|--------------|
| [المشكلة] | [عالي/متوسط/منخفض] | [الحل] |

### الميزانية:
- المخصص: [المبلغ]
- المصروف: [المبلغ]
- المتبقي: [المبلغ]
"""
    },
    "تقرير فارغ": {
        "icon": "📄",
        "description": "ابدأ من صفحة فارغة",
        "template": ""
    }
}

# ---------------------------------------------------------
# 🎨 CSS المحسن
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* الهيدر */
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
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        box-shadow: 0 0 20px #FFD700;
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

    /* عنوان القسم */
    .section-header {
        text-align: center;
        margin: 30px 20px;
        color: #FFD700;
        font-size: 1.4rem;
        font-weight: bold;
    }

    /* بطاقات القوالب */
    .template-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95));
        border: 2px solid rgba(255, 215, 0, 0.2);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .template-card:hover {
        border-color: #FFD700;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
    }
    
    .template-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .template-title {
        color: #FFD700;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .template-desc {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
    }

    /* بطاقة تحليل النص */
    .analysis-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(0, 15, 30, 0.98));
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
    }
    
    .analysis-title {
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
    }
    
    .stat-item {
        background: rgba(255, 215, 0, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FFD700;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 5px;
    }

    .keyword-tag {
        display: inline-block;
        background: rgba(255, 215, 0, 0.15);
        border: 1px solid rgba(255, 215, 0, 0.3);
        color: #FFD700;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.85rem;
    }

    /* أزرار الاختيار */
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
        transition: all 0.4s ease !important;
        text-align: center !important;
        flex: 1 !important;
        min-width: 160px !important;
        max-width: 220px !important;
        color: white !important;
        font-weight: 600 !important;
    }

    div[role="radiogroup"] label:hover {
        border-color: #FFD700 !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
    }

    /* بطاقات الإدخال */
    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 10px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
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
        width: 50px;
        height: 50px;
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

    /* حقل النص */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        padding: 20px !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2) !important;
    }

    /* رفع الملفات */
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

    /* زر المعالجة */
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
        transition: all 0.4s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(218, 165, 32, 0.5) !important;
    }

    /* أزرار التحميل */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 12px 25px !important;
        border-radius: 10px !important;
        border: none !important;
        margin: 5px !important;
    }

    /* خيارات التصدير */
    .export-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(0, 15, 30, 0.98));
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
    }
    
    .export-title {
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-align: center;
    }

    /* شريط التقدم */
    .progress-box {
        background: rgba(0, 31, 63, 0.9);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 30px;
        margin: 20px;
        text-align: center;
    }
    
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 12px;
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

    /* التنبيهات */
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

    /* معاينة الشعار */
    .logo-preview {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-top: 15px;
    }
    
    .logo-preview img {
        max-height: 80px;
        border-radius: 8px;
    }

    /* إخفاء التسميات */
    .stTextArea > label,
    .stFileUploader > label,
    .stRadio > label,
    .stSelectbox > label {
        display: none !important;
    }

    /* المعاينة */
    iframe {
        border-radius: 15px !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
    }

    @media (max-width: 768px) {
        .main-title { font-size: 36px; }
        .sub-title { font-size: 14px; }
        .hero-section { padding: 30px 20px; margin: 10px; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب للتقارير (نفس السابق)
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    :root { --navy-blue: #001f3f; --gold: #FFD700; --light-gold: #FFEB84; --white: #ffffff; --gray: #f4f4f4; --dark-gray: #333; }
    body { font-family: 'Tajawal', sans-serif; background-color: var(--gray); color: var(--dark-gray); line-height: 1.6; direction: rtl; text-align: right; margin: 0; padding: 0; }
    .container { max-width: 1200px; margin: 20px auto; padding: 20px; }
    .card-grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
    header { background-color: var(--navy-blue); color: var(--gold); padding: 30px 0; text-align: center; margin-bottom: 20px; border-radius: 8px; }
    header h1 { margin: 0; font-size: 2.5em; font-weight: 700; }
    header h2 { margin: 10px 0 0; font-size: 1.5em; color: var(--light-gold); }
    .logo-container { text-align: center; margin-bottom: 15px; }
    .logo-container img { max-height: 80px; }
    .card { background-color: var(--white); border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); padding: 25px; margin-bottom: 20px; }
    .card h3 { color: var(--navy-blue); font-size: 1.8em; margin-top: 0; border-bottom: 2px solid var(--gold); padding-bottom: 10px; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    table th { background-color: var(--navy-blue); color: var(--light-gold); padding: 12px; border: 1px solid #ddd; }
    table td { border: 1px solid #ddd; padding: 12px; text-align: right; }
    ul { list-style: none; padding: 0; }
    ul li { padding: 10px 0; border-bottom: 1px dashed #eee; display: flex; justify-content: space-between; }
    ul li span.value { font-weight: 700; color: var(--gold); background: #001f3f; padding: 2px 8px; border-radius: 4px; }
    footer { text-align: center; margin-top: 40px; padding: 20px; color: #666; border-top: 2px solid var(--navy-blue); }
</style>
"""

STYLE_DIGITAL = """
<style>
    body { font-family: 'Cairo', sans-serif; line-height: 1.7; background-color: #f4f7f9; color: #333; direction: rtl; }
    .container { max-width: 1200px; margin: 20px auto; padding: 25px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07); }
    header { text-align: center; padding-bottom: 20px; margin-bottom: 30px; border-bottom: 3px solid #0056b3; }
    .logo-container { text-align: center; margin-bottom: 15px; }
    .logo-container img { max-height: 80px; }
    h1 { color: #0056b3; font-size: 2.4em; font-weight: 700; }
    h2 { color: #007bff; font-size: 2em; border-bottom: 2px solid #f0f0f0; margin-bottom: 20px; }
    .card { background-color: #fdfdfd; border: 1px solid #e0e0e0; border-radius: 8px; padding: 25px; margin-top: 20px; }
    ul li { position: relative; padding-right: 35px; margin-bottom: 12px; }
    ul li::before { content: '•'; position: absolute; right: 0; color: #007bff; font-size: 1.8em; }
    .goal { background-color: #e6f7ff; border: 1px solid #b3e0ff; padding: 18px; border-radius: 8px; text-align: center; margin-top: 20px; font-weight: bold; color: #0056b3; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    thead th { background-color: #007bff; color: white; padding: 14px; }
    td { padding: 14px; border: 1px solid #e0e0e0; text-align: center; }
    footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; color: #777; }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    body { font-family: 'Cairo', sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.7; direction: rtl; }
    .container { max-width: 1100px; margin: 20px auto; padding: 20px; }
    header { background-color: #004a99; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; }
    .logo-container { text-align: center; margin-bottom: 15px; }
    .logo-container img { max-height: 80px; }
    .report-section { background-color: #fff; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.07); margin-bottom: 25px; padding: 25px; }
    .report-section h2 { color: #004a99; border-bottom: 3px solid #0056b3; padding-bottom: 10px; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }
    .stat-card { background-color: #eef5ff; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #d0e3ff; }
    .stat-card .value { font-size: 2.2rem; font-weight: 700; color: #004a99; }
    .pyramid-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    .tier-card { border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; background-color: #fcfcfc; border-top: 6px solid; }
    .tier-upper { border-top-color: #d90429; }
    .tier-middle { border-top-color: #f7b801; }
    .bar-container { background-color: #e0e0e0; border-radius: 5px; height: 12px; margin-top: 12px; overflow: hidden; }
    .bar { height: 100%; border-radius: 5px; }
    .tier-upper .bar { background-color: #d90429; }
    .tier-middle .bar { background-color: #f7b801; }
    footer { text-align: center; margin-top: 30px; color: #888; border-top: 1px solid #ccc; padding-top: 20px; }
</style>
"""

STYLE_PRESENTATION = """
<style>
    :root { --primary-navy: #002b49; --primary-blue: #004e89; --gold-main: #c5a059; --gold-light: #e6c885; --white: #ffffff; --text-dark: #333333; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Cairo', sans-serif; background-color: var(--primary-navy); overflow: hidden; height: 100vh; width: 100vw; direction: rtl; }
    .presentation-container { width: 100%; height: 100%; position: relative; background: radial-gradient(circle at center, #003865 0%, #002035 100%); }
    .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; visibility: hidden; transform: scale(0.95); transition: all 0.6s ease; display: flex; flex-direction: column; padding: 40px 60px; }
    .slide.active { opacity: 1; visibility: visible; transform: scale(1); z-index: 10; }
    .slide-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--gold-main); padding-bottom: 15px; margin-bottom: 25px; }
    .header-title h2 { color: var(--gold-main); font-size: 2rem; font-weight: 800; }
    .header-logo { font-family: 'Tajawal'; color: var(--white); font-weight: bold; }
    .header-logo img { max-height: 50px; }
    .slide-content { flex-grow: 1; display: flex; gap: 40px; height: 100%; overflow: hidden; }
    .text-panel { flex: 3; background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 30px; color: var(--text-dark); overflow-y: auto; border-right: 5px solid var(--gold-main); }
    .visual-panel { flex: 2; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--white); text-align: center; }
    h3 { color: var(--primary-blue); font-size: 1.6rem; margin-bottom: 15px; }
    p { font-size: 1.2rem; line-height: 1.8; margin-bottom: 20px; }
    li { font-size: 1.15rem; margin-bottom: 10px; }
    .icon-box { font-size: 5rem; color: var(--gold-main); margin-bottom: 20px; animation: float 4s ease-in-out infinite; }
    .slide.cover { align-items: center; justify-content: center; text-align: center; background: linear-gradient(135deg, var(--primary-navy) 30%, #001a2c 100%); }
    .cover-content { border: 2px solid var(--gold-main); padding: 60px; background: rgba(0,0,0,0.4); }
    .cover-logo { margin-bottom: 20px; }
    .cover-logo img { max-height: 100px; }
    .main-title { font-size: 3.5rem; color: var(--white); margin-bottom: 15px; }
    .sub-title { font-size: 1.8rem; color: var(--gold-main); }
    .nav-controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 100; }
    .nav-btn { background: transparent; border: 2px solid var(--gold-main); color: var(--gold-main); width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 1.2rem; transition: 0.3s; }
    .nav-btn:hover { background: var(--gold-main); color: var(--primary-navy); }
    .page-number { position: absolute; bottom: 25px; right: 60px; color: var(--gold-main); font-size: 1.2rem; font-weight: bold; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
    .signature-box { margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--gold-main); text-align: center; }
    .signature-title { font-size: 0.9rem; color: #aaa; margin-bottom: 10px; }
    .signature-name { font-size: 1.4rem; color: var(--gold-main); font-weight: bold; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

STYLE_EXECUTIVE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;800&display=swap');
    body { font-family: 'Tajawal', sans-serif; background-color: #ffffff; color: #222; direction: rtl; }
    .container { max-width: 900px; margin: 40px auto; padding: 40px; border: 1px solid #eee; box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid #000; padding-bottom: 20px; margin-bottom: 40px; }
    .brand { font-size: 1.5rem; font-weight: 800; color: #002b49; }
    .logo-container img { max-height: 60px; }
    h1 { font-size: 2.8rem; font-weight: 900; line-height: 1.1; margin-bottom: 10px; color: #000; }
    .executive-summary { font-size: 1.3rem; line-height: 1.6; color: #444; margin-bottom: 40px; border-right: 5px solid #FFD700; padding-right: 20px; background: #fafafa; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; margin-bottom: 30px; }
    .metric-box { padding: 20px; background: #f9f9f9; border-radius: 8px; border: 1px solid #eee; }
    .metric-val { font-size: 2.5rem; font-weight: 800; color: #002b49; }
    .metric-lbl { font-size: 1rem; color: #666; text-transform: uppercase; }
    .section-title { font-size: 1.2rem; font-weight: 800; text-transform: uppercase; margin-top: 30px; margin-bottom: 15px; color: #c5a059; border-bottom: 2px solid #eee; }
    footer { margin-top: 60px; border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #999; }
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
    function nextSlide() {
        const totalSlides = document.querySelectorAll('.slide').length;
        if (currentSlideIndex < totalSlides) { currentSlideIndex++; updateSlide(); }
    }
    function prevSlide() {
        if (currentSlideIndex > 1) { currentSlideIndex--; updateSlide(); }
    }
    document.addEventListener('keydown', function(event) {
        if (event.key === "ArrowLeft" || event.key === " ") nextSlide();
        else if (event.key === "ArrowRight") prevSlide();
    });
    setTimeout(updateSlide, 100);
</script>
"""

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    """استخراج النص من الملفات"""
    text_content = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            text_content = df.to_string()
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text_content = stringio.read()
    except Exception as e:
        return f"خطأ في قراءة الملف: {e}"
    return text_content

def clean_html_response(text):
    """تنظيف رد الذكاء الاصطناعي"""
    text = text.replace("```html", "").replace("```", "")
    return text.strip()

def get_working_model():
    """الحصول على نموذج Gemini"""
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name:
                    return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

def analyze_text(text):
    """تحليل النص واستخراج الإحصائيات"""
    if not text.strip():
        return None
    
    # تنظيف النص
    clean_text = re.sub(r'[^\w\s]', '', text)
    
    # عدد الكلمات
    words = clean_text.split()
    word_count = len(words)
    
    # عدد الجمل
    sentences = re.split(r'[.!?؟،]', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # عدد الفقرات
    paragraphs = text.split('\n\n')
    paragraph_count = len([p for p in paragraphs if p.strip()])
    
    # عدد الأحرف
    char_count = len(text)
    
    # استخراج الأرقام والنسب
    numbers = re.findall(r'\d+(?:\.\d+)?%?', text)
    
    # الكلمات المفتاحية (أكثر الكلمات تكراراً)
    # استبعاد الكلمات الشائعة
    stop_words = {'في', 'من', 'إلى', 'على', 'عن', 'مع', 'هذا', 'هذه', 'التي', 'الذي', 'أن', 'كان', 'كانت', 'يكون', 'تكون', 'هو', 'هي', 'ذلك', 'تلك', 'و', 'أو', 'ثم', 'لكن', 'بل', 'حتى', 'إذا', 'لو', 'ما', 'لا', 'نعم', 'قد', 'لقد', 'سوف', 'عند', 'بعد', 'قبل', 'فوق', 'تحت', 'بين', 'خلال', 'حول', 'ضد', 'منذ', 'أما', 'إما', 'سواء', 'كل', 'بعض', 'غير', 'أي', 'كيف', 'متى', 'أين', 'لماذا', 'كم', 'هل'}
    
    filtered_words = [w for w in words if len(w) > 2 and w not in stop_words]
    word_freq = Counter(filtered_words)
    keywords = word_freq.most_common(8)
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'paragraph_count': paragraph_count,
        'char_count': char_count,
        'numbers': numbers[:10],
        'keywords': keywords,
        'reading_time': max(1, word_count // 200)  # دقائق القراءة
    }

def image_to_base64(uploaded_image):
    """تحويل الصورة إلى Base64"""
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        base64_str = base64.b64encode(bytes_data).decode()
        return f"data:image/{uploaded_image.type.split('/')[-1]};base64,{base64_str}"
    return None

def create_pdf(html_content):
    """إنشاء ملف PDF من HTML"""
    if not WEASYPRINT_AVAILABLE:
        return None
    try:
        pdf_bytes = WeasyHTML(string=html_content).write_pdf()
        return pdf_bytes
    except Exception as e:
        st.error(f"خطأ في إنشاء PDF: {e}")
        return None

def create_docx(html_content, title="تقرير"):
    """إنشاء ملف Word من HTML"""
    if not DOCX_AVAILABLE:
        return None
    try:
        doc = Document()
        
        # إعداد الاتجاه RTL
        section = doc.sections[0]
        
        # العنوان
        heading = doc.add_heading(title, 0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # استخراج النص من HTML (تبسيط)
        text_content = re.sub(r'<[^>]+>', '\n', html_content)
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
        
        # إضافة المحتوى
        for para in text_content.split('\n\n'):
            if para.strip():
                p = doc.add_paragraph(para.strip())
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # حفظ في الذاكرة
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"خطأ في إنشاء Word: {e}")
        return None

# ---------------------------------------------------------
# 🏗️ بناء الواجهة
# ---------------------------------------------------------

# الهيدر
st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

# ===== قسم القوالب الجاهزة =====
st.markdown('<div class="section-header">📋 اختر قالب جاهز أو ابدأ من الصفر</div>', unsafe_allow_html=True)

template_cols = st.columns(6)
selected_template = None

for idx, (template_name, template_data) in enumerate(REPORT_TEMPLATES.items()):
    with template_cols[idx % 6]:
        if st.button(f"{template_data['icon']}\n{template_name}", key=f"template_{idx}", use_container_width=True):
            selected_template = template_name
            st.session_state['selected_template'] = template_name

# عرض وصف القالب المختار
if 'selected_template' in st.session_state and st.session_state['selected_template']:
    template_info = REPORT_TEMPLATES[st.session_state['selected_template']]
    st.info(f"📌 **{st.session_state['selected_template']}**: {template_info['description']}")

st.markdown("<br>", unsafe_allow_html=True)

# ===== قسم الشعار =====
st.markdown('<div class="section-header">🏷️ شعار المؤسسة (اختياري)</div>', unsafe_allow_html=True)

logo_col1, logo_col2 = st.columns([1, 3])

with logo_col1:
    uploaded_logo = st.file_uploader("ارفع شعار المؤسسة", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key="logo_uploader")
    
with logo_col2:
    if uploaded_logo:
        logo_base64 = image_to_base64(uploaded_logo)
        st.markdown(f'''
        <div class="logo-preview">
            <img src="{logo_base64}" alt="شعار المؤسسة">
            <p style="color: #22c55e; margin-top: 10px; font-size: 0.9rem;">✅ تم رفع الشعار بنجاح</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">لم يتم رفع شعار - سيتم استخدام التصميم الافتراضي</p>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== قسم اختيار النمط =====
st.markdown('<div class="section-header">🎨 اختر نمط الإخراج المطلوب</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي (PPT)", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# ===== قسم الإدخال =====
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
    
    # تحميل القالب إذا تم اختياره
    default_text = ""
    if 'selected_template' in st.session_state and st.session_state['selected_template']:
        default_text = REPORT_TEMPLATES[st.session_state['selected_template']]['template']
    
    user_text = st.text_area("", height=250, value=default_text, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...", label_visibility="collapsed")

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
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed", key="file_uploader")
    
    if uploaded_file:
        st.success(f"✅ تم إرفاق: {uploaded_file.name}")

# ===== تحليل النص الذكي =====
if user_text.strip():
    analysis = analyze_text(user_text)
    if analysis:
        st.markdown('''
        <div class="analysis-card">
            <div class="analysis-title">📊 تحليل النص الذكي</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # إحصائيات النص
        stat_cols = st.columns(5)
        
        with stat_cols[0]:
            st.markdown(f'''
            <div class="stat-item">
                <div class="stat-value">{analysis['word_count']}</div>
                <div class="stat-label">كلمة</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with stat_cols[1]:
            st.markdown(f'''
            <div class="stat-item">
                <div class="stat-value">{analysis['sentence_count']}</div>
                <div class="stat-label">جملة</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with stat_cols[2]:
            st.markdown(f'''
            <div class="stat-item">
                <div class="stat-value">{analysis['paragraph_count']}</div>
                <div class="stat-label">فقرة</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with stat_cols[3]:
            st.markdown(f'''
            <div class="stat-item">
                <div class="stat-value">{analysis['char_count']}</div>
                <div class="stat-label">حرف</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with stat_cols[4]:
            st.markdown(f'''
            <div class="stat-item">
                <div class="stat-value">{analysis['reading_time']}</div>
                <div class="stat-label">دقائق للقراءة</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # الكلمات المفتاحية
        if analysis['keywords']:
            st.markdown("<p style='color: #FFD700; margin: 15px 0 10px 0; font-weight: 600;'>🔑 الكلمات المفتاحية:</p>", unsafe_allow_html=True)
            keywords_html = " ".join([f'<span class="keyword-tag">{word} ({count})</span>' for word, count in analysis['keywords']])
            st.markdown(f'<div>{keywords_html}</div>', unsafe_allow_html=True)
        
        # الأرقام المكتشفة
        if analysis['numbers']:
            st.markdown("<p style='color: #FFD700; margin: 15px 0 10px 0; font-weight: 600;'>🔢 الأرقام المكتشفة:</p>", unsafe_allow_html=True)
            numbers_html = " ".join([f'<span class="keyword-tag">{num}</span>' for num in analysis['numbers']])
            st.markdown(f'<div>{numbers_html}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== زر المعالجة =====
if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. يرجى إضافته في Secrets.")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            full_text += f"\n\n[محتوى الملف]:\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())

            target_css = ""
            design_rules = ""
            file_label = "Report"
            
            # معالجة الشعار
            logo_html = ""
            if uploaded_logo:
                logo_base64 = image_to_base64(uploaded_logo)
                logo_html = f'<div class="logo-container"><img src="{logo_base64}" alt="شعار المؤسسة"></div>'
            
            unified_signature = """
            <div style="margin-top: 50px; text-align: center; padding-top: 20px; border-top: 2px solid #ccc; font-family: 'Tajawal'; color: #555;">
                <p style="margin-bottom: 5px;"><strong>صادر من الجهاز المركزي للجودة الشاملة</strong></p>
                <p style="font-size: 1.1em; color: #001f3f;"><strong>وحدة التخطيط الاستراتيجي والتطوير</strong></p>
            </div>
            """

            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Report"
                design_rules = f"""
                Style: Official Corporate Report.
                - Start with this logo HTML if provided: {logo_html}
                - Wrap card sections in <div class="card">.
                - Use HTML <table> inside cards for tabular data.
                - Use <ul> with <li> for lists.
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                design_rules = f"""
                Style: Modern Digital Dashboard.
                - Start with this logo HTML if provided: {logo_html}
                - Use <section class="card"> for sections.
                - Use <div class="goal"> for key takeaways.
                """
            
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                design_rules = f"""
                Style: Statistical Hierarchy.
                - Start with this logo HTML if provided: {logo_html}
                - Use <div class="stats-grid"> for statistics.
                - Use <div class="pyramid-grid"> for hierarchy.
                """
            
            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE
                file_label = "Executive_Summary"
                design_rules = f"""
                Style: Modern Executive Summary.
                - Include logo in header if provided: {logo_html}
                - Use <div class="executive-summary"> for main text.
                - Use <div class="grid-2"> with <div class="metric-box"> for metrics.
                """

            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Presentation_Slides"
                cover_logo = f'<div class="cover-logo"><img src="{image_to_base64(uploaded_logo)}" alt="شعار"></div>' if uploaded_logo else ''
                header_logo = f'<div class="header-logo"><img src="{image_to_base64(uploaded_logo)}" alt="شعار"></div>' if uploaded_logo else '<div class="header-logo">تيار الحكمة</div>'
                design_rules = f"""
                Style: Interactive Presentation Slides.
                Structure:
                1. First slide cover must include: {cover_logo}
                2. Each slide header must include: {header_logo}
                3. Use FontAwesome icons in visual-panel.
                4. Output ONLY HTML body content.
                """
                unified_signature = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                <div class="page-number" id="page-num">1 / 1</div>
                """

            prompt = f"""
            You are an expert Data Analyst & Developer for 'Al-Hikma National Movement'.
            **Objective:** Create a FULL, DETAILED HTML report.
            
            **CRITICAL INSTRUCTIONS:**
            1. **FULL CONTENT:** Do NOT summarize. Include EVERY detail.
            2. **DATE:** Detect date from input or use current context.
            3. **FORMAT:** Output ONLY valid HTML (body content). No markdown.
            4. **DESIGN:** Follow these rules: {design_rules}
            
            **INPUT DATA:**
            {full_text}
            
            **LANGUAGE:** Arabic (Professional).
            """

            # شريط التقدم
            progress_placeholder = st.empty()
            
            for i in range(0, 101, 5):
                progress_placeholder.markdown(f'''
                <div class="progress-box">
                    <div style="font-size: 2rem; margin-bottom: 15px;">🤖</div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {i}%;"></div>
                    </div>
                    <div style="color: rgba(255,255,255,0.8);">جاري تحليل البيانات وتوليد التقرير... {i}%</div>
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(0.05)
            
            response = model.generate_content(prompt)
            html_body = clean_html_response(response.text)
            
            progress_placeholder.empty()
            
            # تجميع HTML النهائي
            container_class = 'presentation-container' if 'عرض تقديمي' in report_type else 'container'
            
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
                <div class="{container_class}">
                    {html_body}
                    {unified_signature}
                </div>
                {SCRIPT_PRESENTATION if 'عرض تقديمي' in report_type else ''}
            </body>
            </html>
            """
            
            # حفظ في session state
            st.session_state['final_html'] = final_html
            st.session_state['file_label'] = file_label

            st.markdown('''
            <div class="success-banner">
                <span>✅ تم إنشاء التقرير بنجاح!</span>
            </div>
            ''', unsafe_allow_html=True)
            
            # عرض المعاينة
            st.components.v1.html(final_html, height=850, scrolling=True)
            
            # ===== قسم التصدير المتعدد =====
            st.markdown('''
            <div class="export-section">
                <div class="export-title">📥 تحميل التقرير بصيغ مختلفة</div>
            </div>
            ''', unsafe_allow_html=True)
            
            export_cols = st.columns(3)
            
            # تحميل HTML
            with export_cols[0]:
                st.download_button(
                    label="📄 تحميل HTML",
                    data=final_html,
                    file_name=f"{file_label}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            # تحميل PDF
            with export_cols[1]:
                if WEASYPRINT_AVAILABLE:
                    pdf_data = create_pdf(final_html)
                    if pdf_data:
                        st.download_button(
                            label="📕 تحميل PDF",
                            data=pdf_data,
                            file_name=f"{file_label}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.button("📕 PDF (غير متاح)", disabled=True, use_container_width=True)
                    st.caption("يحتاج مكتبة weasyprint")
            
            # تحميل Word
            with export_cols[2]:
                if DOCX_AVAILABLE:
                    docx_data = create_docx(final_html, file_label)
                    if docx_data:
                        st.download_button(
                            label="📘 تحميل Word",
                            data=docx_data,
                            file_name=f"{file_label}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                else:
                    st.button("📘 Word (غير متاح)", disabled=True, use_container_width=True)
                    st.caption("يحتاج مكتبة python-docx")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")

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
">
    <div style="width: 60px; height: 3px; background: linear-gradient(90deg, transparent, #FFD700, transparent); margin: 0 auto 20px auto;"></div>
    <p style="color: #FFD700; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">الجهاز المركزي للجودة الشاملة</p>
    <p style="color: rgba(255, 255, 255, 0.8); font-size: 1rem; font-weight: 500; margin-bottom: 15px;">وحدة التخطيط الاستراتيجي والتطوير</p>
    <div style="width: 100px; height: 1px; background: rgba(255, 215, 0, 0.3); margin: 15px auto;"></div>
    <p style="color: rgba(255, 255, 255, 0.5); font-size: 0.85rem;">جميع الحقوق محفوظة © 2026</p>
</div>
''', unsafe_allow_html=True)
