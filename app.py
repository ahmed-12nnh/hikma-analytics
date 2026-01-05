import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time
import random

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. نظام تدوير المفاتيح (الحل الجذري لمشكلة 429)
# ---------------------------------------------------------
def configure_api_key():
    # نحاول جلب المفاتيح من الأسرار
    keys = []
    try:
        if "KEY_1" in st.secrets: keys.append(st.secrets["KEY_1"])
        if "KEY_2" in st.secrets: keys.append(st.secrets["KEY_2"])
        if "KEY_3" in st.secrets: keys.append(st.secrets["KEY_3"])
        # للتوافق مع الإعداد القديم
        if "GOOGLE_API_KEY" in st.secrets: keys.append(st.secrets["GOOGLE_API_KEY"])
    except:
        pass

    if not keys:
        st.error("⚠️ لم يتم العثور على مفاتيح! يرجى إضافة KEY_1, KEY_2, KEY_3 في Secrets.")
        st.stop()
    
    # اختيار مفتاح عشوائي للبدء
    return keys

API_KEYS = configure_api_key()

# ---------------------------------------------------------
# 3. محرك الاتصال الذكي (مع التبديل عند الخطأ)
# ---------------------------------------------------------
def generate_content_with_rotation(prompt):
    # نجرب المفاتيح بالترتيب العشوائي
    shuffled_keys = random.sample(API_KEYS, len(API_KEYS))
    
    for i, key in enumerate(shuffled_keys):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # إذا كان الخطأ بسبب السرعة (429)، ننتقل للمفتاح التالي
            if "429" in str(e):
                print(f"Key {i+1} exhausted, switching...")
                continue # جرب المفتاح التالي
            else:
                # إذا كان خطأ آخر، نظهره
                return f"ERROR: {str(e)}"
    
    # إذا فشلت كل المفاتيح
    return "ERROR_QUOTA: جميع المفاتيح مشغولة حالياً. يرجى الانتظار دقيقة."

# ---------------------------------------------------------
# 4. دوال مساعدة
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

# ---------------------------------------------------------
# 5. تصميم الواجهة (القديم الكحلي والذهبي)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    .block-container { padding-top: 1rem !important; }
    header, footer { visibility: hidden; }

    /* الهيدر القديم */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px; padding: 40px 20px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 30px rgba(0, 31, 63, 0.5);
    }
    .main-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-title { font-size: 22px; color: #e0e0e0; }

    /* الحقول */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important; color: white !important;
        text-align: right;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; }

    /* الزر */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 20px !important;
        padding: 0.75rem 2rem !important; border-radius: 50px !important; width: 100%;
        border: none !important;
    }
    .stButton button:hover { transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. بناء الصفحة
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 محتوى التقرير الاستراتيجي")
    report_text = st.text_area("input", height=250, label_visibility="collapsed", placeholder="أدخل البيانات...")

with col2:
    st.markdown("### 📎 المصادر والبيانات")
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.info("💡 النظام مدعم بمفاتيح متعددة لضمان الاستمرارية.")

st.markdown("---")

# ---------------------------------------------------------
# 7. التشغيل
# ---------------------------------------------------------
if st.button("🚀 توليد الموقع والتقرير التفاعلي"):
    
    final_input = report_text
    if uploaded_file:
        final_input += f"\n\n--- DATA ---\n{extract_text_from_file(uploaded_file)}"
    
    if not final_input.strip():
        st.warning("⚠️ الرجاء إدخال بيانات.")
    else:
        with st.spinner("جاري التحليل وتوليد التقرير..."):
            # هذا هو البرومبت الذي يولد التصميم التركوازي (Teal) الذي طلبته
            prompt = f"""
            You are a Senior Web Developer.
            Task: Create a Single-File HTML Dashboard Report.
            
            **DESIGN STYLE (Teal & Amber - As Requested):**
            Use this exact CSS styling approach:
            - Primary Color: #00796b (Teal)
            - Secondary: #ff6f00 (Amber)
            - Background: #f8f9fa
            - Cards: White background, border-radius 8px, padding 20px.
            - Font: 'Cairo', sans-serif.
            - Layout: Centered container (max-width: 1300px), RTL direction.
            
            **STRUCTURE:**
            1. Header with Teal bottom border.
            2. "Stats Grid" at the top (Cards with key numbers).
            3. Sections with clear titles (background-color: #f1f1f1).
            4. Detailed Tables with Teal headers (#00796b).
            
            **CONTENT:**
            - **NO SUMMARIZATION:** Include ALL details/numbers from input.
            - **Language:** Arabic.
            
            **Input Data:** {final_input}
            **Output:** ONLY raw HTML code.
            """
            
            # استدعاء دالة التدوير
            result_code = generate_content_with_rotation(prompt)
            
            if "ERROR" in result_code:
                st.error(result_code)
            else:
                html_code = result_code.replace("```html", "").replace("```", "")
                st.balloons()
                st.components.v1.html(html_code, height=1200, scrolling=True)
                st.download_button("📥 تحميل التقرير (HTML)", html_code, "Report.html", "text/html")
