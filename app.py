import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ المفتاح غير موجود في Secrets.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ الدوال المساعدة
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
    except Exception as e: return f"Error: {e}"
    return text

def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🎨 واجهة Streamlit (التصميم الذي أحببته مع إصلاح المسافات)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');

    /* الخلفية الفخمة (Radial Gradient) التي طلبتها سابقاً */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }
    
    .block-container { padding-top: 2rem !important; }
    header, footer { visibility: hidden; }

    /* الهيدر */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.7);
        position: relative; overflow: hidden;
    }
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }
    .main-title {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #DAA520);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    /* إصلاح المسافات (تقريب العناوين من الحقول) */
    h3 {
        margin-bottom: -15px !important;
        position: relative; z-index: 10;
        color: #FFD700 !important; font-size: 1.3rem !important;
    }

    /* حقول الإدخال */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important; color: white !important;
        font-size: 1.1rem !important; margin-top: 0px !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; box-shadow: 0 0 15px rgba(255, 215, 0, 0.2) !important; }

    /* صندوق الرفع */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03); margin-top: 0px !important;
        padding: 20px; border-radius: 15px; border: 1px dashed rgba(255, 215, 0, 0.3);
    }

    /* الزر */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 1.2rem !important;
        padding: 15px 30px !important; border-radius: 50px !important; border: none !important;
        width: 100%; box-shadow: 0 5px 15px rgba(218, 165, 32, 0.3); transition: 0.3s;
    }
    .stButton button:hover { transform: scale(1.02); }

    /* سبينر التحميل */
    .stSpinner > div { border-top-color: #FFD700 !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكلية
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div style="color: #ddd; font-size: 1.2rem;">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 محتوى التقرير")
    report_text = st.text_area("input", height=280, placeholder="اكتب البيانات هنا...", label_visibility="collapsed")

with col2:
    st.markdown("### 📎 المصادر")
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.info("النظام جاهز لتحليل التقارير الطويلة والمعقدة.")

st.markdown("---")

# ---------------------------------------------------------
# 🚀 الزر والتشغيل (مع الأمر البرمجي القديم)
# ---------------------------------------------------------
col_btn, col_spin = st.columns([4, 1])

with col_btn:
    run = st.button("🚀 توليد التقرير الاستراتيجي (التصميم الأصلي)")

if run:
    with col_spin:
        with st.spinner(""):
            final_input = report_text
            if uploaded_file:
                final_input += f"\n\n--- FILE CONTENT ---\n{extract_text_from_file(uploaded_file)}"
            
            if not final_input.strip():
                st.warning("⚠️ لا توجد بيانات")
            else:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_model())
                    
                    # 🔥 هنا السر: هذا هو الـ Prompt (الأمر) الذي كنت أستخدمه سابقاً وأعطاك أفضل النتائج
                    prompt = f"""
                    You are a World-Class UI/UX Developer & Data Analyst.
                    
                    **Objective:** Transform the following raw data into a High-End, Professional HTML Dashboard/Report.
                    
                    **Design Theme (Al-Hikma Corporate):**
                    - **Backgrounds:** Deep Navy Blue (#001f3f) for headers/sidebars, White (#ffffff) for content cards.
                    - **Accents:** Gold (#FFD700) for titles, buttons, and highlights.
                    - **Typography:** 'Tajawal' (Arabic), Modern, Bold.
                    - **Structure:** Dashboard style (Stat Cards at top, Charts if possible, Clean Tables).
                    
                    **CRITICAL REQUIREMENTS:**
                    1. **NO SUMMARIZATION:** You must include ALL details, numbers, and names from the input.
                    2. **Visuals:** Use CSS Grid/Flexbox to create a "Dashboard" look, not just a document.
                    3. **Components:** - Hero Section (Title & Date).
                       - "Key Metrics" row (Cards with big numbers).
                       - "Detailed Analysis" sections (White cards with shadow).
                    4. **Tech:** Single file HTML with embedded CSS. Responsive. RTL Direction.
                    
                    **Input Data:** {final_input}
                    
                    **Output:** ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    html_code = response.text.replace("```html", "").replace("```", "")
                    
                    st.balloons()
                    st.components.v1.html(html_code, height=1000, scrolling=True)
                    
                    # زر التحميل
                    st.download_button("📥 تحميل التقرير (HTML)", html_code, "Strategic_Report.html", "text/html")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
