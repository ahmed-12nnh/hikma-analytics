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
# 🎨 التصميم والمظهر (تحديث الـ CSS للمسافات)
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
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #000d1a 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem !important;}

    /* --- الهيدر --- */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 25px;
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 40px; /* مسافة تحت الهيدر */
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 10px 40px rgba(0, 31, 63, 0.6);
        position: relative; overflow: hidden;
    }
    .hero-section::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }
    .main-title {
        font-size: 50px; font-weight: 900;
        background: linear-gradient(to right, #FFD700, #FFA500);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-title { font-size: 20px; color: #e0e0e0; letter-spacing: 1px; }

    /* --- تحسين المسافات (الحل لمشكلة البعد) --- */
    /* تقريب العناوين من الحقول */
    div[data-testid="stMarkdownContainer"] > h3 {
        margin-bottom: -15px !important; /* سحب العنوان للأسفل */
        padding-bottom: 0px !important;
        font-size: 22px !important;
        color: #FFD700 !important;
    }
    
    /* تنسيق الحقول */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #fff !important;
        text-align: right;
        margin-top: 5px !important;
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2) !important;
    }

    /* تنسيق صندوق الرفع */
    .stFileUploader {
        margin-top: 5px !important;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px; border: 1px dashed rgba(255, 215, 0, 0.4);
    }

    /* --- تنسيق الزر ودائرة التحميل --- */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #DAA520) !important;
        color: #001f3f !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        height: 60px; /* تثبيت ارتفاع الزر */
        box-shadow: 0 6px 20px rgba(218, 165, 32, 0.3);
        transition: transform 0.2s;
    }
    .stButton button:hover { transform: scale(1.02); }
    
    /* تنسيق الـ Spinner */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }

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

# الأعمدة الرئيسية
col_input, col_upload = st.columns([2, 1])

with col_input:
    st.markdown("### 📝 محتوى التقرير الاستراتيجي") 
    report_text = st.text_area("input_area", height=250, placeholder="ابدأ الكتابة هنا...", label_visibility="collapsed")

with col_upload:
    st.markdown("### 📎 المصادر والبيانات")
    uploaded_file = st.file_uploader("upload_area", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    st.info("سيتم دمج النص مع الملف المرفق تلقائياً.")

st.markdown("---")

# ---------------------------------------------------------
# 🚀 زر التشغيل + دائرة التحميل الجانبية
# ---------------------------------------------------------

# تقسيم المنطقة السفلية: الزر يأخذ مساحة كبيرة (4)، ومساحة صغيرة (1) لدائرة التحميل
col_btn, col_loading = st.columns([4, 1])

with col_btn:
    # الزر الثابت
    run_process = st.button("🚀 توليد التقرير التفصيلي (بدون اختصار)")

# المنطق البرمجي
if run_process:
    
    # التحقق من المدخلات
    final_input = report_text
    
    # نظهر دائرة التحميل في العمود الجانبي الصغير
    with col_loading:
        with st.spinner(''): # سبينر بدون نص ليكون شكله دائرة فقط
            
            # --- العمليات الثقيلة تبدأ هنا ---
            if uploaded_file:
                file_content = extract_text_from_file(uploaded_file)
                final_input += f"\n\n--- محتوى الملف المرفق ---\n{file_content}"
            
            if not final_input.strip():
                st.warning("⚠️ لا توجد بيانات!")
                processed = False
            else:
                try:
                    genai.configure(api_key=API_KEY)
                    model = genai.GenerativeModel(get_working_model())
                    
                    prompt = f"""
                    You are a Strategic Data Analyst for 'Al-Hikma National Movement'.
                    **CRITICAL INSTRUCTIONS:**
                    1. **NO SUMMARIZATION:** Do NOT summarize. Present ALL details.
                    2. **FULL REPORT:** Generate a comprehensive HTML report.
                    3. **Design:** Al-Hikma Theme (Navy Blue #001f3f & Gold #FFD700). RTL Arabic.
                    
                    **Input Data:** {final_input}
                    
                    **Output:** Return ONLY raw HTML code.
                    """
                    
                    response = model.generate_content(prompt)
                    html_code = response.text.replace("```html", "").replace("```", "")
                    processed = True
                except Exception as e:
                    st.error(f"خطأ: {e}")
                    processed = False
            # --- انتهت العمليات الثقيلة ---

    # الآن نظهر النتائج تحت المنطقة (بعد اختفاء التحميل)
    if processed:
        st.balloons()
        st.success("✅ تم الإنشاء بنجاح!")
        st.components.v1.html(html_code, height=1000, scrolling=True)
        st.download_button("📥 تحميل التقرير (HTML)", html_code, "Strategic_Report.html", "text/html")
