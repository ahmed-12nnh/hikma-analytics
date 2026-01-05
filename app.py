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
    st.error("⚠️ المفتاح غير موجود في Secrets.")
    st.stop()

# ---------------------------------------------------------
# 🛠️ المحرك والدوال المساعدة
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
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(page_title="منصة التحليل الاستراتيجي", page_icon="🦅", layout="wide")

# ---------------------------------------------------------
# 🖌️ القائمة الجانبية (اختيار التصميم) - الإضافة الجديدة
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("🎨 استوديو التصميم")
    st.markdown("---")
    
    design_mode = st.radio(
        "اختر نمط التقرير:",
        ("النمط الرسمي (تيار الحكمة)", "النمط الحديث (Clean Modern)", "النمط المستقبلي (Dark Neon)")
    )
    
    st.info(f"✨ النمط المختار: **{design_mode}**\n\nسيقوم الذكاء الاصطناعي بإعادة كتابة كود HTML/CSS بالكامل ليتناسب مع هذا النمط.")

# ---------------------------------------------------------
# 💎 CSS الواجهة الرئيسية (تصميم الزجاج)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #003366 0%, #001f3f 60%, #000a12 100%);
        font-family: 'Tajawal', sans-serif;
        color: white;
        direction: rtl;
    }
    .block-container { padding-top: 1rem !important; }
    header, footer { visibility: hidden; }

    /* الهيدر */
    .hero {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px; padding: 30px; text-align: center;
        backdrop-filter: blur(10px); margin-bottom: 30px;
        animation: fadeIn 1s ease;
    }
    .hero h1 {
        background: linear-gradient(to bottom, #FFD700, #DAA520);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 900; margin: 0;
    }

    /* البطاقات الزجاجية */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
    }
    .card-title {
        color: #FFD700; font-size: 1.2rem; font-weight: 700;
        margin-bottom: 10px; border-bottom: 1px solid rgba(255, 215, 0, 0.1);
        padding-bottom: 5px;
    }

    /* تحسين المدخلات */
    .stTextArea textarea {
        background: rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important; border-radius: 10px !important;
    }
    .stTextArea textarea:focus { border-color: #FFD700 !important; }
    
    .stFileUploader {
        background: rgba(0,0,0,0.2); padding: 10px; border-radius: 10px;
        border: 1px dashed rgba(255,255,255,0.2);
    }

    /* الزر */
    .stButton button {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        color: #001f3f !important; font-weight: 900 !important;
        border-radius: 50px !important; border: none !important;
        padding: 10px 30px !important; width: 100%; transition: 0.3s;
    }
    .stButton button:hover { transform: scale(1.02); box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4); }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🏗️ الواجهة
# ---------------------------------------------------------
st.markdown("""
    <div class="hero">
        <h1>تيار الحكمة الوطني</h1>
        <p>نظام التحليل الاستراتيجي وتوليد التقارير الذكية</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="glass-card"><div class="card-title">📝 البيانات النصية</div>', unsafe_allow_html=True)
    report_text = st.text_area("input", height=300, placeholder="اكتب هنا...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card"><div class="card-title">📎 الملفات المرفقة</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("file", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # الزر
    run_btn = st.button("🚀 توليد التقرير")

# ---------------------------------------------------------
# 🧠 المنطق البرمجي (هندسة الأوامر المتغيرة)
# ---------------------------------------------------------
if run_btn:
    final_input = report_text
    
    # تحضير التصميم المختار (Prompt Styling)
    design_prompt = ""
    if design_mode == "النمط الرسمي (تيار الحكمة)":
        design_prompt = """
        **Design Style: Official Corporate**
        - Colors: Deep Navy Blue (#001f3f), Gold (#FFD700), White Card Backgrounds.
        - Typography: 'Tajawal', Formal, Bold Headers.
        - Components: Stat Cards with Gold borders, Data Tables, Official Footer.
        - Vibe: Prestigious, Serious, Governmental.
        """
    elif design_mode == "النمط الحديث (Clean Modern)":
        design_prompt = """
        **Design Style: Modern Minimalist (SaaS Style)**
        - Colors: White Background (#F3F4F6), Dark Text (#1F2937), Accent Blue (#3B82F6).
        - Typography: 'Cairo', Clean, Airy, High Readability.
        - Components: Soft Shadow Cards (Neomorphism hints), Rounded Corners (12px), Clean Grids.
        - Vibe: Clean, Professional, Easy to read, Silicon Valley style.
        """
    else: # النمط المستقبلي
        design_prompt = """
        **Design Style: Dark Futuristic (Cyberpunk/Tech)**
        - Colors: Dark Background (#0f172a), Neon Accents (Cyan #06b6d4, Purple #8b5cf6).
        - Typography: 'IBM Plex Sans Arabic', Tech-oriented.
        - Components: Glowing Borders, Glassmorphism Cards, Dark Mode Tables.
        - Vibe: High-Tech, Innovation, Future-ready.
        """

    # الحاوية التفاعلية
    status = st.status("جاري العمل...", expanded=True)
    
    try:
        if uploaded_file:
            status.write("📂 قراءة الملف...")
            final_input += f"\n\n--- FILE DATA ---\n{extract_text_from_file(uploaded_file)}"
        
        if not final_input.strip():
            status.update(label="⚠️ تنبيه", state="error")
            st.warning("أدخل نصاً أو ملفاً.")
        else:
            status.write("🎨 استدعاء خبير التصميم...")
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_model())
            
            prompt = f"""
            You are an expert Frontend Developer & UI/UX Designer.
            
            **Objective:** Convert this data into a STUNNING HTML Dashboard/Report.
            
            **CRITICAL DESIGN INSTRUCTIONS:**
            {design_prompt}
            
            **General Rules:**
            1. **NO SUMMARIZATION:** Include ALL details from input.
            2. **Layout:** Responsive Grid Layout (Use Flexbox/Grid).
            3. **Language:** Arabic (RTL).
            4. **Styling:** Embed ALL CSS inside <style> tags. Make it look like a real website, not a Word doc.
            
            **Input Data:** {final_input}
            
            **Output:** ONLY raw HTML code.
            """
            
            response = model.generate_content(prompt)
            html_code = response.text.replace("```html", "").replace("```", "")
            
            status.update(label="✅ تم الإنجاز!", state="complete", expanded=False)
            st.balloons()
            
            st.components.v1.html(html_code, height=1000, scrolling=True)
            
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                st.download_button("📥 تحميل التقرير (HTML)", html_code, "Report.html", "text/html")
                
    except Exception as e:
        status.update(label="❌ خطأ", state="error")
        st.error(str(e))
