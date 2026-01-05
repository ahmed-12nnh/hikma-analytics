import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import random
import time

# ---------------------------------------------------------
# 1. إعداد الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. جلب المفاتيح (Key Rotation)
# ---------------------------------------------------------
def get_api_key():
    keys = []
    # البحث عن أي مفتاح متاح
    for key_name in ["KEY_1", "KEY_2", "KEY_3", "GOOGLE_API_KEY"]:
        if key_name in st.secrets:
            keys.append(st.secrets[key_name])
    
    if not keys:
        st.error("⚠️ لم يتم العثور على مفاتيح في Secrets.")
        st.stop()
    
    return random.choice(keys)

# ---------------------------------------------------------
# 3. محرك الاتصال (بسيط ومباشر)
# ---------------------------------------------------------
def generate_response(prompt):
    try:
        api_key = get_api_key()
        genai.configure(api_key=api_key)
        
        # نستخدم الموديل المستقر
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

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
    except: return ""
    return text

# ---------------------------------------------------------
# 5. التصميم (الكحلي والذهبي - للموقع)
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
    
    .block-container { padding-top: 2rem !important; }
    header, footer { visibility: hidden; }

    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 30px rgba(0, 31, 63, 0.5);
    }
    .main-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px; color: white !important; text-align: right;
    }
    
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important; font-weight: bold; border-radius: 50px;
        width: 100%; border: none; padding: 10px; font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. الهيكلية
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div style="color: #ddd;">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### 📝 البيانات")
    report_text = st.text_area("t", height=200, label_visibility="collapsed", placeholder="أدخل النص هنا...")
with col2:
    st.markdown("### 📎 المرفقات")
    uploaded_file = st.file_uploader("f", label_visibility="collapsed")

# ---------------------------------------------------------
# 7. التشغيل والتوليد
# ---------------------------------------------------------
st.markdown("---")
if st.button("🚀 توليد التقرير الاستراتيجي"):
    
    final_input = report_text
    if uploaded_file: final_input += extract_text_from_file(uploaded_file)
    
    if not final_input.strip():
        st.warning("الرجاء إدخال بيانات.")
    else:
        with st.spinner("جاري التحليل..."):
            # هذا البرومبت يضمن تصميم "التركواز والبرتقالي" للتقرير المولد
            prompt = f"""
            Act as a Senior UI Developer. 
            Task: Create a Single-File HTML Dashboard Report based on the data.
            
            **DESIGN STYLE (Teal & Amber):**
            - Primary: #00796b (Teal)
            - Secondary: #ff6f00 (Amber)
            - Background: #f8f9fa (Light Gray)
            - Cards: White
            
            **CSS MUST INCLUDE:**
            body {{ direction: rtl; font-family: 'Cairo', sans-serif; background: #f8f9fa; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
            h1 {{ color: #004d40; text-align: center; border-bottom: 4px solid #00796b; padding-bottom: 15px; }}
            .stat-card {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .stat-val {{ font-size: 2.5em; color: #00796b; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #00796b; color: white; padding: 10px; }}
            td {{ border: 1px solid #ddd; padding: 8px; text-align: right; }}
            
            **DATA:** {final_input}
            **OUTPUT:** RAW HTML CODE ONLY.
            """
            
            result = generate_response(prompt)
            
            if "Error" in result:
                st.error(f"حدث خطأ: {result}")
                st.info("تلميح: إذا كان الخطأ 404، فهذا يعني أن ملف requirements.txt لم يتم تحديثه بعد.")
            else:
                html_code = result.replace("```html", "").replace("```", "")
                st.balloons()
                st.components.v1.html(html_code, height=1000, scrolling=True)
                st.download_button("📥 تحميل التقرير", html_code, "Report.html", "text/html")
