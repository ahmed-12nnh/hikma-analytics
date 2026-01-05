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
# 🛠️ دالة ذكية لقراءة الملفات (لحل مشكلة الكلام غير المفهوم)
# ---------------------------------------------------------
def extract_text_from_file(uploaded_file):
    """دالة تستخرج النص الصافي من PDF أو Excel أو TXT"""
    text_content = ""
    try:
        # 1. قراءة PDF
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
        
        # 2. قراءة Excel
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            text_content = df.to_string()
            
        # 3. قراءة ملف نصي
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text_content = stringio.read()
            
    except Exception as e:
        return f"خطأ في قراءة الملف: {e}"
    
    return text_content

# ---------------------------------------------------------
# 🎨 إعداد الصفحة والتصميم (نفس التصميم الذي طلبته)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# حقن CSS احترافي (الأزرق والذهبي - تيار الحكمة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 5px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }

    .main-title {
        font-size: 55px;
        font-weight: 900;
        background: linear-gradient(to bottom, #FFD700, #B8860B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }

    .sub-title {
        font-size: 22px;
        color: #e0e0e0;
        font-weight: 500;
        letter-spacing: 1px;
    }

    /* حقول الإدخال */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
        text-align: right;
    }
    
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.1) !important;
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
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
    }

    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px dashed rgba(255, 215, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. الهيكل الرئيسي (Header)
st.markdown("""
    <div class="hero-section">
        <div class="main-title">تيار الحكمة الوطني</div>
        <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
    </div>
""", unsafe_allow_html=True)

# 4. التخطيط الشبكي
col_input, col_upload = st.columns([2, 1])

with col_input:
    st.markdown("### 📝 محتوى التقرير الاستراتيجي")
    report_text = st.text_area("أدخل البيانات الخام هنا لتحويلها:", height=250, placeholder="ابدأ الكتابة هنا...")

with col_upload:
    st.markdown("### 📎 المصادر والبيانات")
    st.markdown("يمكنك رفع ملفات مساعدة للتحليل:")
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'])
    
    st.info("""
    **💡 كيف يعمل النظام؟**
    1. أدخل النص أو ارفع ملفاً.
    2. اضغط زر التوليد بالأسفل.
    3. سيقوم الذكاء الاصطناعي بتحليل الملفات وبناء موقع HTML.
    """)

# دالة لاختيار الموديل المتاح تلقائياً
def get_working_model():
    try:
        available_models = genai.list_models()
        for m in available_models:
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace("models/", "")
                if "flash" in name: return name
                if "pro" in name and "vision" not in name: return name
        return "gemini-1.5-flash"
    except:
        return "gemini-pro"

# 5. منطقة العمليات والتشغيل
st.markdown("---")
if st.button("🚀 توليد الموقع والتقرير التفاعلي"):
    
    # --- دمج النصوص مع محتوى الملفات (الحل السحري) ---
    final_input = report_text
    
    if uploaded_file:
        with st.spinner('📂 جاري استخراج البيانات من الملف المرفق...'):
            file_content = extract_text_from_file(uploaded_file)
            final_input += f"\n\n--- بيانات من الملف المرفق ---\n{file_content}"
            
    if not final_input.strip():
        st.warning("⚠️ يرجى تزويد النظام ببيانات (نص أو ملف) للبدء.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            
            with st.spinner('🔍 جاري تأمين الاتصال واختيار الموديل المناسب...'):
                active_model = get_working_model()
                model = genai.GenerativeModel(active_model)
            
            with st.spinner('🛠️ جاري هندسة الكود وبناء الموقع...'):
                prompt = f"""
                You are a World-Class UI/UX Developer & Data Analyst.
                Objective: Transform the following raw text/data into a High-End, Professional HTML Dashboard/Report.
                
                Input Data: "{final_input[:20000]}"
                
                Design Specs (Strictly Follow):
                1. Framework: Use embedded CSS that mimics 'Tailwind CSS' or 'Bootstrap 5' aesthetics.
                2. Theme: "Al-Hikma Corporate" -> Deep Navy Blue (#001f3f) backgrounds, White Cards, Gold (#FFD700) Accents/Headers.
                3. Typography: Use a modern Arabic font (e.g., 'Cairo' or 'Tajawal') via Google Fonts.
                4. Components: - A Hero Header with the title.
                    - "Stats Cards" for any numbers found in text.
                    - Clean sections with shadows and rounded corners.
                    - Responsive layout.
                5. Language: Arabic (RTL).
                
                Technical Constraint: 
                - Return ONLY raw HTML code. 
                - CSS must be inside <style> tags.
                - Do NOT use markdown backticks.
                """
                
                response = model.generate_content(prompt)
                html_code = response.text.replace("```html", "").replace("```", "")
                
                st.balloons()
                st.success("✅ تم بناء الموقع بنجاح!")
                
                st.components.v1.html(html_code, height=800, scrolling=True)
                
                st.download_button(
                    label="📥 تحميل التقرير كملف ويب (HTML)",
                    data=html_code,
                    file_name="Strategic_Report_AlHikma.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
