import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import random

# ---------------------------------------------------------
# 🔑 إعدادات الأمان والمفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ المفتاح غير موجود في Secrets. يرجى إضافته.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ المحرك والدوال المساعدة
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
# 🎨 واجهة التطبيق (التصميم الكحلي الفخم الذي طلبته)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* 1. الخلفية الكحلية المتدرجة (نفس الكود القديم) */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    /* إخفاء الهوامش الزائدة */
    .block-container { padding-top: 2rem !important; }
    header, footer { visibility: hidden; }

    /* 2. الهيدر الفخم */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px; padding: 40px 20px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 30px rgba(0, 31, 63, 0.5), inset 0 0 20px rgba(0,0,0,0.5);
        position: relative; overflow: hidden;
    }
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }
    .main-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px; text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }
    .sub-title { font-size: 22px; color: #e0e0e0; font-weight: 500; letter-spacing: 1px; }

    /* 3. إصلاح العناوين (تقريبها من المربعات) */
    .custom-label {
        font-size: 1.3rem; font-weight: 700; color: #FFD700;
        margin-bottom: -15px; /* سحب العنوان للأسفل */
        z-index: 10; position: relative; padding-right: 10px;
    }

    /* 4. تنسيق الحقول (شفافة وفخمة) */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important; color: #fff !important;
        font-size: 16px !important; text-align: right;
        padding-top: 25px !important; /* مساحة للعنوان الملتصق */
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03); margin-top: 5px;
        padding: 20px; border-radius: 15px; border: 1px dashed rgba(255, 215, 0, 0.3);
    }

    /* 5. الزر الذهبي (ثابت) */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 20px !important;
        padding: 0.75rem 2rem !important; border-radius: 50px !important; border: none !important;
        width: 100%; box-shadow: 0 4px 15px rgba(218, 165, 32, 0.3); transition: transform 0.2s;
    }
    .stButton button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(218, 165, 32, 0.5); }

    /* لون دائرة التحميل */
    .stSpinner > div { border-top-color: #FFD700 !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكلية (Layout)
# ---------------------------------------------------------

# الهيدر
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="custom-label">📝 محتوى التقرير الاستراتيجي</div>', unsafe_allow_html=True)
    report_text = st.text_area("input", height=250, label_visibility="collapsed", placeholder="أدخل البيانات هنا...")

with col2:
    st.markdown('<div class="custom-label">📎 المصادر والبيانات</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    st.info("💡 النظام مصمم لتوليد تقارير بتصاميم متنوعة واحترافية تلقائياً.")

st.markdown("---")

# ---------------------------------------------------------
# 🧠 مكتبة التصاميم (AI Design Styles)
# ---------------------------------------------------------
# 1. التصميم الأخضر والبرتقالي (الذي أرسلته في المثال الأخير)
style_teal_amber = """
**Design Style:** 'Teal & Amber Analytics'.
- **Colors:** Primary Teal (#00796b), Secondary Amber (#ff6f00), Background (#f8f9fa).
- **Structure:** Clean cards with light shadows.
- **Headings:** Teal color with bottom borders.
- **Tables:** Professional data tables with Teal headers.
- **Vibe:** Analytical, Sharp, Modern (Identical to the example provided).
"""

# 2. التصميم الكحلي والذهبي (تيار الحكمة)
style_hikma_classic = """
**Design Style:** 'Al-Hikma Official Corporate'.
- **Colors:** Deep Navy Blue (#001f3f) Background, Gold (#FFD700) Text/Borders, White Content Cards.
- **Structure:** Dashboard style, High contrast.
- **Components:** Gold-bordered stat cards, Dark headers.
- **Vibe:** Prestigious, Executive, Governmental.
"""

# 3. تصميم حديث فاتح (للتنويع)
style_modern_light = """
**Design Style:** 'Silicon Valley Modern'.
- **Colors:** White Background, Dark Gray Text, Royal Blue Accents (#2563eb).
- **Structure:** Minimalist, Rounded corners (20px), Soft gradients.
- **Vibe:** Clean, Tech-focused, Easy to read.
"""

# قائمة الخيارات (نعطي أولوية للتصميمين المفضلين لديك)
design_options = [style_teal_amber, style_hikma_classic, style_teal_amber, style_modern_light]

# ---------------------------------------------------------
# 🚀 الزر والتشغيل (تفاعلي وثابت)
# ---------------------------------------------------------
# تقسيم المنطقة: زر كبير + مساحة صغيرة للتحميل
c_btn, c_spin = st.columns([4, 1])

with c_btn:
    run_btn = st.button("🚀 توليد الموقع والتقرير التفاعلي")

if run_btn:
    # ظهور التحميل بجانب الزر
    with c_spin:
        with st.spinner(""):
            # 1. تجهيز البيانات
            final_input = report_text
            if uploaded_file:
                final_input += f"\n\n--- FILE DATA ---\n{extract_text_from_file(uploaded_file)}"
            
            if not final_input.strip():
                st.warning("⚠️ الرجاء إدخال بيانات.")
            else:
                try:
                    # 2. اختيار تصميم عشوائي
                    selected_style = random.choice(design_options)
                    
                    # 3. الاتصال بالذكاء الاصطناعي
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_model())
                    
                    prompt = f"""
                    Act as a Senior UI/UX Developer.
                    **Task:** Convert this data into a fully responsive HTML Dashboard.
                    
                    **DESIGN INSTRUCTIONS (STRICTLY FOLLOW):**
                    {selected_style}
                    
                    **CONTENT RULES:**
                    1. **NO SUMMARIZATION:** Include ALL details, numbers, and names from the input.
                    2. **Language:** Arabic (RTL).
                    3. **Tech:** Single file HTML with embedded CSS.
                    4. **Stats:** Extract numbers and show them in "Stat Cards" at the top.
                    
                    **Input Data:** {final_input}
                    
                    **Output:** ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    html_code = response.text.replace("```html", "").replace("```", "")
                    
                    # 4. عرض النتيجة
                    st.balloons()
                    st.components.v1.html(html_code, height=1000, scrolling=True)
                    
                    # زر التحميل
                    st.download_button("📥 تحميل التقرير (HTML)", html_code, "Strategic_Report.html", "text/html")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
