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
# 🛠️ دالة قراءة الملفات
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
        return f"خطأ: {e}"
    return text_content

# ---------------------------------------------------------
# 🎨 إعداد الصفحة والتصميم (الأزرق والذهبي)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');
    .stApp { background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%); font-family: 'Tajawal', sans-serif; color: white; direction: rtl; }
    #MainMenu, footer, header {visibility: hidden;} .block-container {padding-top: 2rem !important;}
    
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8));
        border-radius: 20px; padding: 40px 20px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3); box-shadow: 0 0 30px rgba(0, 31, 63, 0.5);
    }
    .main-title { font-size: 55px; font-weight: 900; color: #FFD700; margin-bottom: 10px; }
    .sub-title { font-size: 22px; color: #e0e0e0; }
    .stTextArea textarea { background-color: rgba(255, 255, 255, 0.05) !important; color: white !important; border: 1px solid #FFD700 !important; text-align: right; }
    .stButton button { background: linear-gradient(45deg, #FFD700, #DAA520); color: #001f3f !important; font-weight: 900 !important; width: 100%; padding: 0.75rem 2rem !important; }
    .stFileUploader { background-color: rgba(255, 255, 255, 0.03); padding: 20px; border-radius: 15px; border: 1px dashed rgba(255, 215, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

col_input, col_upload = st.columns([2, 1])
with col_input:
    st.markdown("### 📝 محتوى التقرير")
    report_text = st.text_area("أدخل البيانات:", height=250)
with col_upload:
    st.markdown("### 📎 المصادر")
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'])

# دالة الموديل
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

st.markdown("---")
if st.button("🚀 توليد تقرير تفصيلي كامل"):
    
    # 1. تجميع النص
    final_input = report_text
    if uploaded_file:
        with st.spinner('📂 قراءة الملف كاملاً...'):
            final_input += f"\n\n--- محتوى الملف المرفق ---\n{extract_text_from_file(uploaded_file)}"

    if not final_input.strip():
        st.warning("⚠️ لا توجد بيانات للتحليل.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model_name = get_working_model()
            model = genai.GenerativeModel(model_name)
            
            with st.spinner('جاري تحليل كافة البيانات وإنشاء تقرير مفصل (قد يستغرق وقتاً لكبر حجم البيانات)...'):
                
                # --- التعديل الجوهري في الأمر (Prompt) ---
                prompt = f"""
                You are a Strategic Data Analyst for 'Al-Hikma National Movement'.
                
                **CRITICAL INSTRUCTIONS:**
                1. **NO SUMMARIZATION:** Do NOT summarize the input. You must process and present ALL provided details, numbers, and names.
                2. **FULL SCOPE:** If the input is long, generate a long HTML report. Do not skip any sections.
                3. **ACCURACY:** Copy numbers and statistics exactly as they appear in the source.
                
                **Task:** Convert the provided raw data into a Detailed Professional HTML Report.
                
                **Design Specs:**
                - Use 'Al-Hikma' Theme (Navy Blue #001f3f & Gold #FFD700).
                - Use valid HTML/CSS (Tailwind-like style).
                - Font: 'Tajawal'.
                - Direction: RTL (Arabic).
                
                **Input Data:** {final_input} 
                
                **Output:** Return ONLY valid HTML code.
                """
                
                # إرسال الطلب (لاحظ أننا أزلنا القيد [:20000] وأرسلنا النص كاملاً)
                response = model.generate_content(prompt)
                html_code = response.text.replace("```html", "").replace("```", "")
                
                st.success("✅ تم إنشاء التقرير المفصل!")
                st.components.v1.html(html_code, height=800, scrolling=True)
                st.download_button("📥 تحميل التقرير (HTML)", html_code, "Full_Report.html", "text/html")

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
