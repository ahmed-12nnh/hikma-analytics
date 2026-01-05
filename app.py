import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح (من الخزنة السرية)
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح في Secrets. يرجى إضافته في إعدادات الموقع.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ الدوال الذكية (المحرك)
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
# 🎨 التصميم والمظهر (نفس تصميمك مع تعديلات المسافات)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* الخلفية والخطوط */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem !important;}

    /* الهيدر */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 30px rgba(0, 31, 63, 0.5), inset 0 0 20px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }
    .main-title {
        font-size: 55px; font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }
    .sub-title { font-size: 22px; color: #e0e0e0; font-weight: 500; letter-spacing: 1px; }

    /* --- تعديل 1: تقريب العناوين من الحقول --- */
    h3 {
        margin-bottom: -1rem !important; /* سحب العنوان للأسفل */
        padding-bottom: 0px !important;
        z-index: 99;
        position: relative;
    }
    
    /* تنسيق الحقول */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 16px !important;
        text-align: right;
        margin-top: 0px !important; /* إلغاء المسافة العلوية */
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.1) !important;
    }

    /* تنسيق صندوق الرفع */
    .stFileUploader {
        margin-top: 5px !important;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 20px; border-radius: 15px;
        border: 1px dashed rgba(255, 215, 0, 0.3);
    }

    /* الأزرار */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520);
        color: #001f3f !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        height: 60px; /* تثبيت الارتفاع */
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.3);
        transition: transform 0.2s;
    }
    .stButton button:hover { transform: scale(1.02); }
    
    /* لون دائرة التحميل */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكل الرئيسي
# ---------------------------------------------------------

# الهيدر
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

# التقسيم
col_input, col_upload = st.columns([2, 1])

with col_input:
    # استخدام markdown عادي ليكون العنوان قريباً جداً
    st.markdown("### 📝 محتوى التقرير الاستراتيجي")
    # label_visibility="collapsed" لإخفاء العنوان الأصلي البعيد
    report_text = st.text_area("report", height=250, placeholder="ابدأ الكتابة هنا...", label_visibility="collapsed")

with col_upload:
    st.markdown("### 📎 المصادر والبيانات")
    uploaded_file = st.file_uploader("files", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    st.info("""
    **💡 تلميح:**
    النظام مصمم لاستيعاب التقارير الطويلة.
    """)

st.markdown("---")

# ---------------------------------------------------------
# 🚀 زر التشغيل + دائرة التحميل الجانبية (تعديل 2)
# ---------------------------------------------------------

# نقسم السطر الأخير إلى: [زر كبير] و [مكان صغير للتحميل]
col_btn, col_loader = st.columns([4, 1])

with col_btn:
    run_btn = st.button("🚀 توليد التقرير التفصيلي (بدون اختصار)")

# المنطق البرمجي
if run_btn:
    
    # نظهر دائرة التحميل في العمود الصغير المجاور
    with col_loader:
        with st.spinner(''): # سبينر صامت (دائرة فقط)
            
            # --- العمليات ---
            final_input = report_text
            
            if uploaded_file:
                file_content = extract_text_from_file(uploaded_file)
                final_input += f"\n\n--- محتوى الملف المرفق ---\n{file_content}"
            
            if not final_input.strip():
                st.warning("⚠️ الرجاء إدخال بيانات.")
                result_html = None
            else:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_working_model())
                    
                    prompt = f"""
                    You are a Strategic Data Analyst for 'Al-Hikma National Movement'.
                    **CRITICAL INSTRUCTIONS:**
                    1. **NO SUMMARIZATION:** Do NOT summarize. Process and present ALL details.
                    2. **FULL REPORT:** Generate a comprehensive HTML report.
                    3. **Theme:** Al-Hikma Corporate (Navy Blue #001f3f & Gold #FFD700). RTL.
                    
                    **Input Data:** {final_input}
                    **Output:** Return ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    result_html = response.text.replace("```html", "").replace("```", "")
                    
                except Exception as e:
                    st.error(f"خطأ: {e}")
                    result_html = None
            # --- انتهى التحميل ---

    # عرض النتائج (خارج منطقة التحميل)
    if result_html:
        st.balloons()
        st.success("✅ تم الإنشاء بنجاح!")
        st.components.v1.html(result_html, height=1000, scrolling=True)
        st.download_button("📥 تحميل التقرير (HTML)", result_html, "Report.html", "text/html")
