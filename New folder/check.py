import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
# لقد وضعت المفتاح الذي أرسلته لك هنا جاهزاً
api_key_input = "AIzaSyDOq2fwJOR0br9VJ7AZxrBMruU_RH48sjs"
# ---------------------------------------------------------

st.set_page_config(page_title="منصة التحليل الاستراتيجي", layout="wide")

# إعداد التصميم (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    .stApp { background-color: #001f3f; color: white; font-family: 'Tajawal', sans-serif; direction: rtl; }
    .header-box { background: linear-gradient(90deg, #001f3f, #003366); padding: 30px; border-radius: 15px; border-bottom: 5px solid #FFD700; text-align: center; margin-bottom: 20px; }
    .main-title { font-size: 45px; font-weight: 900; color: #FFD700; }
    .stTextArea textarea { background-color: rgba(255,255,255,0.1); color: white; border: 1px solid #FFD700; }
</style>
""", unsafe_allow_html=True)

# الهيدر
st.markdown("""
    <div class="header-box">
        <div class="main-title">تيار الحكمة الوطني</div>
        <h3 style='color: white;'>وحدة التخطيط الاستراتيجي | نظام التحليل الذكي</h3>
    </div>
""", unsafe_allow_html=True)

# المدخلات
report_text = st.text_area("أدخل نص التقرير هنا:", height=150)

if st.button("🚀 إنشاء الموقع"):
    if not report_text:
        st.warning("أدخل النص أولاً")
    else:
        try:
            # تهيئة الذكاء الاصطناعي
            genai.configure(api_key=api_key_input)
            
            # -----------------------------------------------------
            # محاولة استخدام الموديل الأضمن (gemini-1.5-flash)
            # -----------------------------------------------------
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('جاري الاتصال بسيرفرات Google... (تأكد من تشغيل VPN)'):
                prompt = f"""
                Act as a web developer.
                Convert this text into a modern HTML report (RTL/Arabic).
                Use Blue/Gold theme.
                Text: {report_text}
                Output ONLY HTML code.
                """
                response = model.generate_content(prompt)
                
                html_code = response.text.replace("```html", "").replace("```", "")
                st.components.v1.html(html_code, height=600, scrolling=True)
                st.download_button("تحميل الملف", html_code, "report.html")

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
            st.error("🔴 نصيحة: إذا رأيت خطأ 404، يرجى تشغيل VPN على دولة أمريكا وإعادة المحاولة.")