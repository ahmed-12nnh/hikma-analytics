import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح (تم وضعه كما طلبت)
# ---------------------------------------------------------
API_KEY = st.secrets["GOOGLE_API_KEY"]
# ---------------------------------------------------------

# 1. إعداد الصفحة
st.set_page_config(
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. حقن CSS احترافي (نفس التصميم الذي أعجبك)
st.markdown("""
<style>
    /* استيراد خط تجوال - خط عصري جداً */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700;900&display=swap');

    /* تعيين الخلفية والخطوط العامة */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }

    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem !important;}

    /* --- تصميم الهيدر (رأس الصفحة) --- */
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
    
    /* تأثير لمعان ذهبي */
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

    /* --- تصميم حقول الإدخال --- */
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
        background-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* --- تصميم الأزرار --- */
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
    3. سيقوم الذكاء الاصطناعي ببناء موقع HTML كامل وتفاعلي.
    """)

# --- دالة الإصلاح التلقائي (هذا هو الجزء الجديد لحل المشكلة) ---
def get_working_model():
    """تبحث هذه الدالة عن الموديل المتاح في حسابك لتجنب خطأ 404"""
    try:
        # نحصل على قائمة الموديلات المتاحة للمفتاح
        available_models = genai.list_models()
        for m in available_models:
            # نبحث عن موديل يدعم توليد النصوص
            if 'generateContent' in m.supported_generation_methods:
                name = m.name.replace("models/", "")
                # نفضل الموديلات السريعة Flash أو Pro
                if "flash" in name: return name
                if "pro" in name and "vision" not in name: return name
        
        return "gemini-1.5-flash" # احتياطي
    except:
        return "gemini-pro" # احتياطي أخير

# 5. منطقة العمليات
st.markdown("---")
if st.button("🚀 توليد الموقع والتقرير التفاعلي"):
    
    if not report_text and not uploaded_file:
        st.warning("⚠️ يرجى تزويد النظام ببيانات (نص أو ملف) للبدء.")
    else:
        try:
            # 1. إعداد الاتصال
            genai.configure(api_key=API_KEY)
            
            # 2. استخدام الدالة الذكية لاختيار الموديل
            with st.spinner('🔍 جاري تأمين الاتصال واختيار الموديل المناسب...'):
                active_model = get_working_model()
                # st.success(f"تم الاتصال عبر الموديل: {active_model}") # يمكن إلغاء تعليق هذا السطر للتأكد
                model = genai.GenerativeModel(active_model)
            
            # 3. الطلب من الذكاء الاصطناعي
            with st.spinner('🛠️ جاري هندسة الكود وبناء الموقع...'):
                prompt = f"""
                You are a World-Class UI/UX Developer & Data Analyst.
                
                **Objective:** Transform the following raw text/data into a High-End, Professional HTML Dashboard/Report.
                
                **Input Data:** "{report_text}"
                
                **Design Specs (Strictly Follow):**
                1.  **Framework:** Use embedded CSS that mimics 'Tailwind CSS' or 'Bootstrap 5' aesthetics.
                2.  **Theme:** "Al-Hikma Corporate" -> Deep Navy Blue (#001f3f) backgrounds, White Cards, Gold (#FFD700) Accents/Headers.
                3.  **Typography:** Use a modern Arabic font (e.g., 'Cairo' or 'Tajawal') via Google Fonts.
                4.  **Components:** -   A Hero Header with the title.
                    -   "Stats Cards" for any numbers found in text.
                    -   Clean sections with shadows and rounded corners.
                    -   Responsive layout.
                5.  **Language:** Arabic (RTL).
                
                **Technical Constraint:** - Return ONLY raw HTML code. 
                - CSS must be inside <style> tags.
                - Do NOT use markdown backticks.
                """
                
                response = model.generate_content(prompt)
                html_code = response.text.replace("```html", "").replace("```", "")
                
                # نجاح العملية
                st.balloons()
                st.success("✅ تم بناء الموقع بنجاح!")
                
                # عرض النتيجة
                st.components.v1.html(html_code, height=800, scrolling=True)
                
                # زر التحميل
                st.download_button(
                    label="📥 تحميل التقرير كملف ويب (HTML)",
                    data=html_code,
                    file_name="Strategic_Report_AlHikma.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")

            st.error("تلميح: تأكد أن برنامج VPN يعمل على دولة (USA) أو (Germany).")
