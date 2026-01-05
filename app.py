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

# 1. دالة قراءة الملفات (PDF, Excel, TXT)
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

# 2. دالة البحث عن الموديل الشغال (لتفادي خطأ 404)
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name: return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🎨 التصميم والمظهر (التصميم الفخم الذي طلبته)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# حقن CSS الاحترافي (نفس الكود القديم بالضبط)
st.markdown("""
<style>
    /* استيراد خط تجوال */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* الخلفية والخطوط */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem !important;}

    /* الهيدر (العنوان الرئيسي) */
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
        box-shadow: 0 6px 20px rgba(218, 165, 32, 0.5);
    }

    /* صندوق رفع الملفات */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px dashed rgba(255, 215, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ واجهة المستخدم (Layout)
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
    st.markdown("### 📝 محتوى التقرير الاستراتيجي")
    report_text = st.text_area("أدخل البيانات الخام هنا:", height=250, placeholder="ابدأ الكتابة هنا...")

with col_upload:
    st.markdown("### 📎 المصادر والبيانات")
    st.markdown("يمكنك رفع ملفات مساعدة للتحليل:")
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'])
    
    st.info("""
    **💡 تلميح:**
    النظام مصمم لاستيعاب التقارير الطويلة.
    سيتم دمج النص المكتوب مع محتوى الملف المرفق وتحليلهم سوياً.
    """)

# ---------------------------------------------------------
# 🚀 زر التشغيل والمنطق البرمجي
# ---------------------------------------------------------
st.markdown("---")
if st.button("🚀 توليد التقرير التفصيلي (بدون اختصار)"):
    
    # 1. تجميع البيانات
    final_input = report_text
    
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف المرفق واستخراج كافة البيانات...'):
            file_content = extract_text_from_file(uploaded_file)
            final_input += f"\n\n--- محتوى الملف المرفق ---\n{file_content}"
    
    # 2. التحقق
    if not final_input.strip():
        st.warning("⚠️ الرجاء إدخال نص أو رفع ملف للبدء.")
    else:
        try:
            # 3. الاتصال
            genai.configure(api_key=API_KEY)
            
            with st.spinner('🤖 جاري تحليل البيانات وبناء الموقع... (قد يستغرق وقتاً للدقة)'):
                model_name = get_working_model()
                model = genai.GenerativeModel(model_name)
                
                # 4. الأمر المفصل (Prompt)
                prompt = f"""
                You are a Strategic Data Analyst for 'Al-Hikma National Movement'.
                
                **CRITICAL INSTRUCTIONS:**
                1. **NO SUMMARIZATION:** Do NOT summarize. Process and present ALL details, numbers, and names from the input.
                2. **FULL REPORT:** Generate a comprehensive HTML report.
                3. **ACCURACY:** Exact numbers must be preserved.
                
                **Task:** Convert this data into a High-End HTML Dashboard.
                
                **Design Specs (Al-Hikma Corporate):**
                - Colors: Deep Navy Blue (#001f3f) & Gold (#FFD700).
                - Font: 'Tajawal'.
                - Language: Arabic (RTL).
                - Style: Clean cards, shadows, responsive.
                
                **Input Data:** {final_input}
                
                **Output:** Return ONLY raw HTML code.
                """
                
                response = model.generate_content(prompt)
                html_code = response.text.replace("```html", "").replace("```", "")
                
                st.balloons()
                st.success("✅ تم إنشاء التقرير المفصل بنجاح!")
                
                # عرض النتيجة
                st.components.v1.html(html_code, height=1000, scrolling=True)
                
                # زر التحميل
                st.download_button(
                    label="📥 تحميل التقرير (HTML)",
                    data=html_code,
                    file_name="Strategic_Report_AlHikma.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
