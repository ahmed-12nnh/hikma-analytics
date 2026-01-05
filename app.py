import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ المفتاح غير موجود في Secrets.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ المحرك (الدوال)
# ---------------------------------------------------------
def extract_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages: text += page.extract_text() + "\n"
        elif "sheet" in uploaded_file.type:
            df = pd.read_excel(uploaded_file)
            text = df.to_string()
        else:
            text = uploaded_file.getvalue().decode("utf-8")
    except Exception as e: return f"Error: {e}"
    return text

def get_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                return m.name
        return "gemini-1.5-flash"
    except: return "gemini-1.5-flash"

# ---------------------------------------------------------
# 🎨 التصميم الجديد (نظام البطاقات الزجاجية)
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');

    /* الخلفية العامة */
    .stApp {
        background: radial-gradient(circle at center, #003366 0%, #001f3f 60%, #000a12 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }
    
    .block-container { padding-top: 2rem !important; }
    header, footer { visibility: hidden; }

    /* --- الهيدر الفخم --- */
    .hero {
        background: rgba(0, 31, 63, 0.6);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 40px rgba(0,0,0,0.5);
        backdrop-filter: blur(10px);
        margin-bottom: 40px;
        animation: fadeIn 1s ease;
    }
    .hero h1 {
        background: linear-gradient(to bottom, #FFD700, #DAA520);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3.5rem;
        margin: 0;
        text-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .hero p { color: #ccc; font-size: 1.2rem; margin-top: 10px; }

    /* --- نظام البطاقات (الجديد) --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .glass-card:hover { border-color: rgba(255, 215, 0, 0.3); transform: translateY(-2px); }
    
    /* عناوين الأقسام داخل البطاقات */
    .card-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        padding-bottom: 10px;
        display: flex; align-items: center; gap: 10px;
    }

    /* تحسين الحقول لتكون داخل البطاقة */
    .stTextArea textarea {
        background: rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; }

    /* تحسين صندوق الرفع */
    .stFileUploader {
        background: rgba(0,0,0,0.2);
        padding: 10px; border-radius: 10px;
        border: 1px dashed rgba(255,255,255,0.2);
    }

    /* --- الزر الاحترافي --- */
    .stButton button {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        color: #001f3f !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        padding: 15px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
        width: 100%;
        transition: all 0.3s;
    }
    .stButton button:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(255, 215, 0, 0.5); }

    /* أنيميشن */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الهيكلية (نظام الأعمدة داخل البطاقات)
# ---------------------------------------------------------

# 1. الهيدر
st.markdown("""
    <div class="hero">
        <h1>تيار الحكمة الوطني</h1>
        <p>الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</p>
    </div>
""", unsafe_allow_html=True)

# 2. منطقة العمل (نظام الأعمدة)
col_right, col_left = st.columns([2, 1])

# العمود الأيمن: النص
with col_right:
    # نفتح بطاقة زجاجية يدوياً عبر HTML للحاوية
    st.markdown('<div class="glass-card"><div class="card-title">📝 محتوى التقرير الاستراتيجي</div>', unsafe_allow_html=True)
    report_text = st.text_area("input", height=300, placeholder="اكتب مسودة التقرير هنا...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True) # إغلاق البطاقة

# العمود الأيسر: الملفات
with col_left:
    st.markdown('<div class="glass-card"><div class="card-title">📎 البيانات والمصادر</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.caption("يدعم النظام ملفات PDF و Excel الكبيرة.")
    st.markdown('</div>', unsafe_allow_html=True)

    # بطاقة معلومات صغيرة
    st.markdown("""
    <div class="glass-card" style="background: rgba(0, 31, 63, 0.4);">
        <div style="color: #FFD700; font-weight: bold; margin-bottom: 5px;">💡 ملاحظة:</div>
        <div style="font-size: 0.9rem; color: #ddd;">سيقوم الذكاء الاصطناعي بدمج النص المكتوب مع الملف المرفق في تقرير واحد شامل.</div>
    </div>
    """, unsafe_allow_html=True)

# 3. زر التشغيل (في المنتصف)
st.markdown("<br>", unsafe_allow_html=True)
col_spacer1, col_btn, col_spacer2 = st.columns([1, 2, 1])

with col_btn:
    run_btn = st.button("🚀 بدء التحليل وإنشاء الموقع التفاعلي")

# ---------------------------------------------------------
# ⚙️ المنطق البرمجي (بدون دوائر غريبة)
# ---------------------------------------------------------
if run_btn:
    final_input = report_text
    
    # واجهة تحميل أنيقة (Status Container)
    status = st.status("جاري معالجة البيانات...", expanded=True)
    
    try:
        # 1. معالجة الملف
        if uploaded_file:
            status.write("📂 جاري استخراج البيانات من الملف المرفق...")
            file_text = extract_text_from_file(uploaded_file)
            final_input += f"\n\n--- بيانات الملف ---\n{file_text}"
        
        # 2. التحقق
        if not final_input.strip():
            status.update(label="⚠️ خطأ: لا توجد بيانات!", state="error")
            st.warning("يرجى كتابة نص أو رفع ملف.")
        else:
            # 3. الاتصال بالذكاء الاصطناعي
            status.write("🤖 جاري الاتصال بمحرك التحليل (Gemini AI)...")
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_model())
            
            # 4. التوليد
            status.write("🏗️ جاري هندسة وتصميم الموقع...")
            prompt = f"""
            Act as a Senior Data Analyst & UI Developer for 'Al-Hikma National Movement'.
            **Goal:** Create a high-end HTML Dashboard from this data.
            **Rules:** 1. NO Summarization (Include ALL details).
            2. Theme: Navy Blue (#001f3f) & Gold (#FFD700). 
            3. RTL Arabic Layout.
            
            **Data:** {final_input}
            
            **Output:** ONLY raw HTML code.
            """
            
            response = model.generate_content(prompt)
            html_code = response.text.replace("```html", "").replace("```", "")
            
            # 5. النجاح
            status.update(label="✅ تم الانتهاء بنجاح!", state="complete", expanded=False)
            st.balloons()
            
            # عرض النتائج
            st.markdown("---")
            st.components.v1.html(html_code, height=1000, scrolling=True)
            
            # زر التحميل
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                st.download_button("📥 تحميل التقرير (HTML)", html_code, "Report.html", "text/html")
                
    except Exception as e:
        status.update(label="❌ حدث خطأ", state="error")
        st.error(f"تفاصيل الخطأ: {e}")
