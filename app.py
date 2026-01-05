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
# 🎨 التصميم والمظهر (تحديث حديث وتفاعلي)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# حقن CSS الاحترافي المحدث (مع رسوم متحركة وتفاعلية)
st.markdown("""
<style>
    /* استيراد خط تجوال */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* الخلفية والخطوط مع gradient حديث */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #000d1a 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
        animation: fadeIn 1s ease-in-out;
    }

    /* إخفاء العناصر الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem !important;}

    /* الهيدر (العنوان الرئيسي) مع تأثيرات حديثة */
    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(10, 46, 92, 0.8), rgba(0, 51, 102, 0.7));
        border-radius: 25px;
        padding: 50px 30px;
        text-align: center;
        margin-bottom: 50px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 10px 40px rgba(0, 31, 63, 0.6), inset 0 0 30px rgba(0,0,0,0.6);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
        animation: slideInFromTop 1.2s ease-out;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 8px;
        background: linear-gradient(90deg, transparent, #FFD700, #FFA500, transparent);
        animation: shimmer 2s infinite;
    }

    .main-title {
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(to right, #FFD700, #FFA500, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        text-shadow: 0px 6px 15px rgba(0,0,0,0.7);
        animation: glow 2s ease-in-out infinite alternate;
    }

    .sub-title {
        font-size: 24px;
        color: #e0e0e0;
        font-weight: 500;
        letter-spacing: 1.5px;
        animation: fadeInUp 1.5s ease-out;
    }

    /* حقول الإدخال مع تأثيرات تفاعلية */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #fff !important;
        font-size: 18px !important;
        transition: all 0.4s ease;
        text-align: right;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-top: 5px !important;  /* تعديل لجعل العنوان أقرب */
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.3), 0 4px 30px rgba(0,0,0,0.5) !important;
        transform: scale(1.02);
    }

    /* الأزرار مع hover وتأثيرات */
    .stButton button {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
        color: #001f3f !important;
        font-weight: 900 !important;
        font-size: 22px !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 6px 20px rgba(218, 165, 32, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    .stButton button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(218, 165, 32, 0.6);
    }
    .stButton button:hover::before {
        left: 100%;
    }

    /* صندوق رفع الملفات مع تحسينات */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 2px dashed rgba(255, 215, 0, 0.4);
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .stFileUploader:hover {
        border-color: #FFD700;
        box-shadow: 0 6px 30px rgba(255, 215, 0, 0.2);
    }

    /* تعديل على العناوين لجعلها أقرب */
    .stMarkdown h3 {
        margin-bottom: 5px !important;  /* تقليل المسافة أكثر */
    }

    /* رسوم متحركة عامة */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInFromTop {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes fadeInUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes glow {
        from { text-shadow: 0px 6px 15px rgba(0,0,0,0.7); }
        to { text-shadow: 0px 6px 25px rgba(255, 215, 0, 0.5); }
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* تحسينات للعناصر الأخرى */
    .stSuccess, .stWarning, .stError {
        border-radius: 15px;
        padding: 15px;
        animation: fadeIn 0.5s ease;
    }
    .stSpinner {
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
    st.markdown("### 📝 محتوى التقرير الاستراتيجي")  # العنوان أقرب الآن
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

# استخدام columns للزر ودائرة التحميل بجانبه
col_button, col_spinner = st.columns([3, 1])  # الزر أكبر، الspinner صغير

generate_button = None
with col_button:
    generate_button = st.button("🚀 توليد التقرير التفصيلي (بدون اختصار)")

spinner_placeholder = st.empty()  # placeholder للspinner

# عناصر ثابتة للرسائل لتجنب الحركة
success_placeholder = st.empty()
error_placeholder = st.empty()
download_placeholder = st.empty()

if generate_button:
    # إظهار الspinner في العمود الثاني
    with col_spinner:
        with st.spinner('جاري التحليل...'):
            pass  # الspinner سيظهر هنا
    
    # 1. تجميع البيانات
    final_input = report_text
    
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف المرفق واستخراج كافة البيانات...'):
            file_content = extract_text_from_file(uploaded_file)
            final_input += f"\n\n--- محتوى الملف المرفق ---\n{file_content}"
    
    # 2. التحقق
    if not final_input.strip():
        with error_placeholder:
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
                
                # إخفاء الspinner بعد الانتهاء
                spinner_placeholder.empty()
                
                # عرض الرسائل في الأماكن الثابتة
                with success_placeholder:
                    st.balloons()
                    st.success("✅ تم إنشاء التقرير المفصل بنجاح!")
                
                # عرض النتيجة
                st.components.v1.html(html_code, height=1000, scrolling=True)
                
                # زر التحميل في مكان ثابت
                with download_placeholder:
                    st.download_button(
                        label="📥 تحميل التقرير (HTML)",
                        data=html_code,
                        file_name="Strategic_Report_AlHikma.html",
                        mime="text/html"
                    )

        except Exception as e:
            # إخفاء الspinner عند الخطأ
            spinner_placeholder.empty()
            with error_placeholder:
                st.error(f"حدث خطأ: {e}")
