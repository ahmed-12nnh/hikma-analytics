import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO

# ---------------------------------------------------------
# 1. إعدادات الأمان والمحرك
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ المفتاح غير موجود في Secrets.")
    st.stop()

def extract_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages: text += page.extract_text() + "\n"
        elif "sheet" in uploaded_file.type:
            df = pd.read_excel(uploaded_file)
            text = df.to_string()
        else:
            text = uploaded_file.getvalue().decode("utf-8")
    except Exception as e: return ""
    return text

def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 2. تصميم الواجهة (تم ضبطه ليكون ثابتاً بدون خربطة)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');

    /* الخلفية الكحلية الفخمة */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    /* إخفاء الهوامش الزائدة */
    .block-container { padding-top: 2rem !important; }
    header, footer { visibility: hidden; }

    /* تنسيق العنوان الرئيسي */
    .hero-title {
        text-align: center; font-weight: 900; font-size: 3rem;
        background: linear-gradient(to bottom, #FFD700, #DAA520);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px; text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }
    .hero-subtitle {
        text-align: center; color: #ddd; font-size: 1.2rem; margin-bottom: 40px;
    }

    /* --- الحل الجذري لمشكلة المسافات --- */
    /* هذا الكود يقرب العناوين من الحقول بالقوة */
    .custom-label {
        font-size: 1.2rem; font-weight: 700; color: #FFD700;
        margin-bottom: -15px; /* يسحب العنصر التالي للأعلى */
        z-index: 10; position: relative; padding-right: 5px;
    }

    /* تنسيق الحقول (Input Fields) */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important; color: white !important;
        padding-top: 20px !important; /* مساحة للنص */
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; box-shadow: 0 0 15px rgba(255, 215, 0, 0.2) !important; }

    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 215, 0, 0.3); border-radius: 12px;
        padding: 10px; margin-top: 5px;
    }

    /* تنسيق الزر (ثابت وقوي) */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 1.3rem !important;
        padding: 12px 0px !important; border-radius: 50px !important; border: none !important;
        width: 100%; box-shadow: 0 5px 15px rgba(218, 165, 32, 0.3);
    }
    .stButton button:hover { transform: scale(1.02); }

    /* لون دائرة التحميل */
    .stSpinner > div { border-top-color: #FFD700 !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. بناء الصفحة
# ---------------------------------------------------------

# الهيدر
st.markdown('<div class="hero-title">تيار الحكمة الوطني</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # العنوان المخصص الملتصق
    st.markdown('<div class="custom-label">📝 محتوى التقرير</div>', unsafe_allow_html=True)
    report_text = st.text_area("input", height=280, label_visibility="collapsed", placeholder="اكتب هنا...")

with col2:
    st.markdown('<div class="custom-label">📎 المصادر</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.info("💡 النظام يدعم التقارير الطويلة والتحليل العميق.")

st.markdown("---")

# ---------------------------------------------------------
# 4. زر التشغيل (مع دائرة التحميل الجانبية)
# ---------------------------------------------------------
c_btn, c_spin = st.columns([4, 1])

with c_btn:
    run_btn = st.button("🚀 توليد التقرير الاستراتيجي (التصميم الأصلي)")

if run_btn:
    # الدائرة تظهر بجانب الزر في العمود الصغير
    with c_spin:
        with st.spinner(""):
            # --- المعالجة ---
            final_input = report_text
            if uploaded_file:
                final_input += f"\n\n--- FILE CONTENT ---\n{extract_text_from_file(uploaded_file)}"
            
            if not final_input.strip():
                st.warning("⚠️ لا توجد بيانات")
            else:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_model())
                    
                    # 🔥 البرومبت الأصلي الذي يعطي تصميم "تيار الحكمة" الفخم 🔥
                    prompt = f"""
                    You are a High-End UI Developer & Strategic Analyst.
                    
                    **Mission:** Convert raw data into a PRESTIGIOUS HTML REPORT for 'Al-Hikma National Movement'.
                    
                    **Design DNA (Strictly enforce this style):**
                    1.  **Background:** The main page background must be Deep Navy Blue (#001f3f).
                    2.  **Cards:** Content must be inside Clean White Cards (#ffffff) with soft shadows and rounded corners (15px).
                    3.  **Headers:** All titles (h1, h2, h3) must be Gold (#FFD700) or Dark Blue.
                    4.  **Font:** Use 'Tajawal' or 'Cairo' (Arabic).
                    5.  **Layout:** Dashboard Grid Style (Stats at top, detailed text below).
                    
                    **Content Rules:**
                    - **NO SUMMARIZATION:** Include every single detail, number, and name from the input.
                    - **RTL Direction:** The entire page must be Right-to-Left.
                    
                    **Input Data:** {final_input}
                    
                    **Output:** ONLY raw HTML code (full page with embedded CSS).
                    """
                    
                    response = model.generate_content(prompt)
                    html_code = response.text.replace("```html", "").replace("```", "")
                    
                    # عرض النتيجة
                    st.balloons()
                    st.components.v1.html(html_code, height=1200, scrolling=True)
                    
                    # زر التحميل
                    st.download_button("📥 تحميل التقرير (HTML)", html_code, "AlHikma_Report.html", "text/html")
                    
                except Exception as e:
                    st.error(f"خطأ: {e}")
