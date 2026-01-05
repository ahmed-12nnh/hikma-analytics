import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import random

# ---------------------------------------------------------
# 🔑 إعدادات الأمان
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ المفتاح غير موجود في Secrets.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ المحرك والدوال
# ---------------------------------------------------------
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
# 🎨 واجهة التطبيق (التصميم الكحلي الفخم - الثابت)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* خلفية التطبيق (الكحلي المتدرج) */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    .block-container { padding-top: 1rem !important; max-width: 95% !important; }
    header, footer { visibility: hidden; }

    /* الهيدر */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 30px rgba(0, 31, 63, 0.5);
    }
    .main-title {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px; text-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    /* إصلاح العناوين (ملتصقة بالحقول) */
    .custom-label {
        font-size: 1.2rem; font-weight: 700; color: #FFD700;
        margin-bottom: -15px; z-index: 10; position: relative; padding-right: 10px;
    }

    /* الحقول */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important; color: white !important;
        font-size: 1.1rem !important; text-align: right;
        padding-top: 25px !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; background-color: rgba(255, 255, 255, 0.08) !important; }

    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03); margin-top: 5px;
        padding: 15px; border-radius: 15px; border: 1px dashed rgba(255, 215, 0, 0.3);
    }

    /* الزر الثابت */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 1.3rem !important;
        padding: 0.8rem 0rem !important; border-radius: 50px !important; border: none !important;
        width: 100%; box-shadow: 0 4px 15px rgba(218, 165, 32, 0.3);
    }
    .stButton button:hover { transform: scale(1.01); }

    /* سبينر */
    .stSpinner > div { border-top-color: #FFD700 !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكلية
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div style="color: #ddd; font-size: 1.1rem;">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="custom-label">📝 محتوى التقرير الاستراتيجي</div>', unsafe_allow_html=True)
    report_text = st.text_area("input", height=250, label_visibility="collapsed", placeholder="أدخل البيانات هنا...")

with col2:
    st.markdown('<div class="custom-label">📎 المصادر والبيانات</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.info("💡 النظام يدعم التقارير الطويلة والتحليل العميق.")

st.markdown("---")

# ---------------------------------------------------------
# 🚀 الزر والمنطق البرمجي (تم إصلاح المحاذاة)
# ---------------------------------------------------------
c_btn, c_spin = st.columns([4, 1])

with c_btn:
    run_btn = st.button("🚀 توليد الموقع والتقرير التفاعلي")

if run_btn:
    with c_spin:
        with st.spinner(""):
            # 1. التجهيز
            final_input = report_text
            if uploaded_file:
                final_input += f"\n\n--- FILE DATA ---\n{extract_text_from_file(uploaded_file)}"
            
            if not final_input.strip():
                st.warning("⚠️ الرجاء إدخال بيانات.")
            else:
                try:
                    # 2. الاتصال
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_model())
                    
                    # 🔥 البرومبت (الأمر) المخصص لإصلاح التصميم وجعله في الوسط 🔥
                    prompt = f"""
                    You are a Senior Web Developer. 
                    Task: Create a Single-File HTML Dashboard Report based on the input data.
                    
                    **DESIGN STYLE (TEAL & AMBER - FIXED LAYOUT):**
                    1.  **Colors:** Primary Teal (#00796b), Accent Amber (#ff6f00), Background (#f4f6f8).
                    2.  **Layout:** The main container MUST be centered (`margin: 0 auto`) with a `max-width: 1200px`.
                    3.  **Typography:** Use 'Cairo' font from Google Fonts.
                    4.  **Components:** - Top: Stats Grid (Cards with white background).
                        - Middle: Sections with clear Teal headings.
                        - Bottom: Data tables (if data exists).
                    
                    **CRITICAL CSS RULES (To Fix Alignment):**
                    - `body {{ background-color: #f4f6f8; direction: rtl; margin: 0; padding: 20px; }}`
                    - `.container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}`
                    - `.stat-card {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 10px; padding: 20px; text-align: center; }}`
                    
                    **CONTENT RULES:**
                    - **NO SUMMARIZATION:** Include ALL details.
                    - **Language:** Arabic.
                    
                    **Input Data:** {final_input}
                    
                    **Output:** ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    html_code = response.text.replace("```html", "").replace("```", "")
                    
                    # 3. العرض (إصلاح المحاذاة في Streamlit)
                    st.balloons()
                    
                    # نستخدم container لضمان العرض الصحيح
                    with st.container():
                        st.components.v1.html(html_code, height=1000, scrolling=True)
                    
                    # 4. التحميل
                    st.download_button("📥 تحميل التقرير (HTML)", html_code, "Report.html", "text/html")
                    
                except Exception as e:
                    # في حال حدوث خطأ 429 (السرعة)
                    if "429" in str(e):
                        st.error("⏳ تجاوزت الحد المسموح من الطلبات. يرجى الانتظار 30 ثانية والمحاولة مجدداً.")
                    else:
                        st.error(f"حدث خطأ: {e}")
