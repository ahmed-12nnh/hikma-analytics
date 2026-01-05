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
    st.error("⚠️ لم يتم العثور على المفتاح في Secrets.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ المحرك (الدوال)
# ---------------------------------------------------------
def extract_text_from_file(uploaded_file):
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

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🎨 التصميم (دمج الجمالية مع إصلاح المسافات)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* الخلفية والأنيميشن (من كودك) */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #000d1a 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
        animation: fadeIn 1s ease-in-out;
    }

    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem !important;}

    /* الهيدر المتحرك */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8), rgba(0, 51, 102, 0.7));
        border-radius: 25px; padding: 50px 30px; text-align: center; margin-bottom: 50px;
        border: 2px solid rgba(255, 215, 0, 0.4); box-shadow: 0 10px 40px rgba(0, 31, 63, 0.6);
        position: relative; overflow: hidden; animation: slideInFromTop 1.2s ease-out;
    }
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 8px;
        background: linear-gradient(90deg, transparent, #FFD700, #FFA500, transparent);
        animation: shimmer 2s infinite;
    }
    .main-title {
        font-size: 60px; font-weight: 900;
        background: linear-gradient(to right, #FFD700, #FFA500, #FFD700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 15px; text-shadow: 0px 6px 15px rgba(0,0,0,0.7);
        animation: glow 2s ease-in-out infinite alternate;
    }
    .sub-title { font-size: 24px; color: #e0e0e0; letter-spacing: 1.5px; animation: fadeInUp 1.5s ease-out; }

    /* --- إصلاح المسافات (العناوين قريبة من المربعات) --- */
    h3 {
        margin-bottom: -15px !important; /* تقليل المسافة بقوة */
        padding-bottom: 0px !important;
        position: relative; z-index: 10;
    }

    /* تنسيق الحقول */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important; color: #fff !important;
        font-size: 18px !important; text-align: right; padding: 15px;
        margin-top: 0px !important; /* إلغاء المسافة العلوية */
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.3) !important; transform: scale(1.02);
    }

    /* تنسيق صندوق الرفع */
    .stFileUploader {
        margin-top: 0px !important;
        background-color: rgba(255, 255, 255, 0.05); padding: 25px;
        border-radius: 20px; border: 2px dashed rgba(255, 215, 0, 0.4);
    }
    .stFileUploader:hover { border-color: #FFD700; box-shadow: 0 6px 30px rgba(255, 215, 0, 0.2); }

    /* الزر */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700) !important;
        color: #001f3f !important; font-weight: 900 !important; font-size: 22px !important;
        border-radius: 50px !important; border: none !important; width: 100%; height: 65px;
        box-shadow: 0 6px 20px rgba(218, 165, 32, 0.4); position: relative; overflow: hidden;
    }
    .stButton button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 30px rgba(218, 165, 32, 0.6); }

    /* الأنيميشن */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideInFromTop { from { transform: translateY(-50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes fadeInUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes glow { from { text-shadow: 0px 6px 15px rgba(0,0,0,0.7); } to { text-shadow: 0px 6px 25px rgba(255, 215, 0, 0.5); } }
    @keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    
    /* لون سبينر التحميل */
    .stSpinner > div { border-top-color: #FFD700 !important; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكلية
# ---------------------------------------------------------

# الهيدر
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

# المدخلات
col_input, col_upload = st.columns([2, 1])

with col_input:
    # عنوان مخصص + حقل بدون عنوان (للالتصاق)
    st.markdown("### 📝 محتوى التقرير الاستراتيجي")
    report_text = st.text_area("input", height=250, placeholder="ابدأ الكتابة هنا...", label_visibility="collapsed")

with col_upload:
    st.markdown("### 📎 المصادر والبيانات")
    uploaded_file = st.file_uploader("files", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.info("💡 سيتم دمج النص مع الملف المرفق تلقائياً.")

st.markdown("---")

# ---------------------------------------------------------
# 🚀 زر التشغيل + التحميل الجانبي
# ---------------------------------------------------------

# تقسيم المساحة: زر كبير (4) ومساحة صغيرة للتحميل (1)
col_btn, col_loader = st.columns([4, 1])

with col_btn:
    run_btn = st.button("🚀 توليد التقرير التفصيلي (بدون اختصار)")

if run_btn:
    
    # دائرة التحميل تظهر هنا بجانب الزر
    with col_loader:
        with st.spinner(''): # سبينر صامت
            
            # العمليات
            final_input = report_text
            if uploaded_file:
                file_content = extract_text_from_file(uploaded_file)
                final_input += f"\n\n--- محتوى الملف المرفق ---\n{file_content}"
            
            if not final_input.strip():
                st.warning("⚠️ لا توجد بيانات!")
                result_html = None
            else:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_working_model())
                    
                    prompt = f"""
                    You are a Strategic Data Analyst for 'Al-Hikma National Movement'.
                    **CRITICAL INSTRUCTIONS:**
                    1. **NO SUMMARIZATION:** Do NOT summarize. Present ALL details.
                    2. **FULL REPORT:** Generate a comprehensive HTML report.
                    3. **Theme:** Al-Hikma Corporate (Navy Blue #001f3f & Gold #FFD700). RTL Arabic.
                    
                    **Input Data:** {final_input}
                    **Output:** Return ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    result_html = response.text.replace("```html", "").replace("```", "")
                except Exception as e:
                    st.error(f"خطأ: {e}")
                    result_html = None

    # عرض النتائج
    if result_html:
        st.balloons()
        st.success("✅ تم الإنشاء بنجاح!")
        st.components.v1.html(result_html, height=1000, scrolling=True)
        st.download_button("📥 تحميل التقرير (HTML)", result_html, "Report.html", "text/html")
