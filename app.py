import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO

# ---------------------------------------------------------
# 🔑 إعداد المفتاح من الخزنة السرية
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح في Secrets. يرجى إضافته في إعدادات الموقع.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ دوال مساعدة لقراءة الملفات (حل المشكلة الثانية)
# ---------------------------------------------------------
def extract_text_from_file(uploaded_file):
    """دالة ذكية لاستخراج النص من أي نوع ملف"""
    text = ""
    try:
        # 1. إذا كان ملف PDF
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        # 2. إذا كان ملف Excel
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            text = df.to_string() # تحويل الجدول لنص
            
        # 3. إذا كان ملف نصي TXT
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            
    except Exception as e:
        return f"خطأ في قراءة الملف: {e}"
    
    return text

# ---------------------------------------------------------
# 🎨 إعداد الصفحة والتصميم
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الذكي", layout="wide")

# قائمة جانبية لاختيار التصميم (حل المشكلة الأولى)
with st.sidebar:
    st.header("🎨 إعدادات التصميم")
    design_style = st.selectbox(
        "اختر نمط التقرير:",
        ["Al-Hikma Corporate (أزرق وذهبي)", "Modern Light (أبيض وعصري)", "Dark Future (أسود ونيون)"]
    )
    
    st.info("💡 ملاحظة: تغيير النمط سيجعل الذكاء الاصطناعي يعيد كتابة الكود بتصميم جديد كلياً.")

# ---------------------------------------------------------
# 🏠 الواجهة الرئيسية
# ---------------------------------------------------------
st.title("🦅 تيار الحكمة الوطني | نظام التحليل الاستراتيجي")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 البيانات المدخلة")
    text_input = st.text_area("اكتب تقريرك هنا:", height=150)

with col2:
    st.subheader("📂 رفع الملفات")
    uploaded_file = st.file_uploader("ارفع (PDF, Excel, TXT)", type=['pdf', 'xlsx', 'txt'])

# زر التشغيل
if st.button("🚀 تحليل البيانات وإنشاء الموقع"):
    
    # 1. تجميع البيانات (من النص أو الملف)
    final_content = text_input
    
    if uploaded_file:
        with st.spinner('جاري قراءة الملف واستخراج البيانات...'):
            file_text = extract_text_from_file(uploaded_file)
            final_content += f"\n\n--- بيانات من الملف المرفق ---\n{file_text}"
    
    # التأكد من وجود محتوى
    if not final_content.strip():
        st.warning("⚠️ الرجاء إدخال نص أو رفع ملف يحتوي على بيانات.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash') # موديل سريع وذكي
            
            # 2. تصميم الأمر (Prompt) بناءً على النمط المختار
            design_prompt = ""
            if "Corporate" in design_style:
                design_prompt = "Design Theme: Official Corporate. Colors: Deep Navy Blue (#001f3f) & Gold (#FFD700). Style: Professional, Boxed Layout."
            elif "Light" in design_style:
                design_prompt = "Design Theme: Modern Light. Colors: White, Light Gray, and Blue Accents. Style: Clean, Minimalist, Bootstrap 5 style."
            else:
                design_prompt = "Design Theme: Dark Future. Colors: Black background, Neon Cyan & Purple accents. Style: Cyberpunk, Glowing effects."

            full_prompt = f"""
            Act as a Senior Front-End Developer.
            Task: Convert the following DATA into a fully responsive HTML Dashboard Report.
            
            {design_prompt}
            
            Language: Arabic (RTL).
            Font: 'Cairo' or 'Tajawal'.
            
            Data to visualize:
            "{final_content[:15000]}"  # نأخذ أول 15 ألف حرف لتجنب تجاوز الحد
            
            Requirements:
            1. Extract key numbers from the data and show them as "Stat Cards".
            2. Organize text into clean sections.
            3. If there is tabular data, create a responsive HTML table.
            4. Output ONLY valid HTML code with embedded CSS.
            """
            
            with st.spinner('🤖 الذكاء الاصطناعي يقوم بتحليل البيانات وبناء الواجهة...'):
                response = model.generate_content(full_prompt)
                html_code = response.text.replace("```html", "").replace("```", "")
                
                # عرض النتيجة
                st.components.v1.html(html_code, height=800, scrolling=True)
                st.download_button("📥 تحميل التقرير (HTML)", html_code, "report.html")
                
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
