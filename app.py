import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import random # مكتبة العشوائية للتنوع

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
# 🎨 واجهة التطبيق (التصميم الكحلي الثابت - بدون خربطة)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');

    /* الخلفية العامة */
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
        border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 30px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.7);
    }
    .main-title {
        font-size: 3rem; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #DAA520);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* العناوين الملتصقة (Fix Spacing) */
    .custom-label {
        font-size: 1.2rem; font-weight: 700; color: #FFD700;
        margin-bottom: -15px; z-index: 10; position: relative; padding-right: 5px;
    }

    /* الحقول */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important; color: white !important;
        padding-top: 20px !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; }

    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 215, 0, 0.3); border-radius: 12px;
        padding: 15px; margin-top: 5px;
    }

    /* الزر */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 1.3rem !important;
        padding: 10px 0px !important; border-radius: 50px !important; border: none !important;
        width: 100%; box-shadow: 0 5px 15px rgba(218, 165, 32, 0.3);
    }
    .stButton button:hover { transform: scale(1.02); }

    /* السبينر */
    .stSpinner > div { border-top-color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكلية
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div style="color: #ddd;">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="custom-label">📝 البيانات والتقارير</div>', unsafe_allow_html=True)
    report_text = st.text_area("input", height=250, label_visibility="collapsed", placeholder="اكتب التقرير هنا...")

with col2:
    st.markdown('<div class="custom-label">📎 المصادر</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    st.info("💡 سيتم اختيار تصميم احترافي تلقائياً بواسطة الذكاء الاصطناعي.")

st.markdown("---")

# ---------------------------------------------------------
# 🧠 محرك التصميم العشوائي (AI Design Engine)
# ---------------------------------------------------------
# هنا نحدد القوالب التي سيختار منها الذكاء الاصطناعي عشوائياً

style_1_teal = """
**Design Theme: Modern Teal & Amber (Strictly follow this style)**
- **Colors:** Primary (#00796b), Secondary (#ff6f00), Background (#f8f9fa).
- **Structure:**
  - Header with bottom border.
  - "Stats Grid" using CSS Grid for key numbers (Cards with white bg).
  - Clean Tables with teal headers.
  - Use class 'card' for sections.
- **Vibe:** Clean, Analytical, Modern Report (Like the example provided).
"""

style_2_corporate = """
**Design Theme: Al-Hikma Official (Navy & Gold)**
- **Colors:** Deep Navy Blue (#001f3f) Background, Gold (#FFD700) Text/Borders, White Cards.
- **Structure:**
  - Dark mode dashboard.
  - High contrast tables.
  - Luxury/Prestigious feel.
- **Vibe:** Official, Governmental, Executive.
"""

style_3_minimal = """
**Design Theme: Silicon Valley Minimal**
- **Colors:** Pure White, Light Grey, Royal Blue Accents (#2563eb).
- **Structure:**
  - Lots of whitespace (Padding).
  - Soft shadows (box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1)).
  - Rounded corners (border-radius: 12px).
- **Vibe:** Tech startup, Clean, Fast reading.
"""

# القائمة التي يختار منها
design_options = [style_1_teal, style_2_corporate, style_3_minimal, style_1_teal] # كررت الأول لزيادة فرص ظهوره

# ---------------------------------------------------------
# 🚀 التشغيل
# ---------------------------------------------------------
c_btn, c_spin = st.columns([4, 1])

with c_btn:
    run_btn = st.button("🚀 توليد التقرير (تصميم ذكي تلقائي)")

if run_btn:
    with c_spin:
        with st.spinner(""):
            final_input = report_text
            if uploaded_file:
                final_input += f"\n\n--- FILE CONTENT ---\n{extract_text_from_file(uploaded_file)}"
            
            if not final_input.strip():
                st.warning("⚠️ الرجاء إدخال بيانات")
            else:
                try:
                    # اختيار تصميم عشوائي
                    selected_style = random.choice(design_options)
                    
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_model())
                    
                    prompt = f"""
                    You are an Expert UI Designer & Data Analyst.
                    Task: Convert data into a HTML Dashboard Report.
                    
                    {selected_style}
                    
                    **CRITICAL RULES:**
                    1. **NO SUMMARIZATION:** Include ALL details/numbers.
                    2. **Language:** Arabic (RTL).
                    3. **Tech:** Single file HTML with embedded CSS.
                    4. **Responsiveness:** Make it work on mobile.
                    
                    **Input Data:** {final_input}
                    
                    **Output:** ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    html_code = response.text.replace("```html", "").replace("```", "")
                    
                    st.balloons()
                    st.components.v1.html(html_code, height=1000, scrolling=True)
                    st.download_button("📥 تحميل التقرير (HTML)", html_code, "Report.html", "text/html")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
