import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time
import base64

# ---------------------------------------------------------
# 🔑 إعدادات المفتاح
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = None

# ---------------------------------------------------------
# 🎨 إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة الحكمة | التحليل الاستراتيجي",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 🌟 CSS الثوري - تصميم Cyberpunk + Luxury Arabic
# ---------------------------------------------------------
REVOLUTIONARY_CSS = """
<style>
    /* ===== استيراد الخطوط الفاخرة ===== */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@200;300;400;500;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@400;500;600;700&display=swap');
    
    /* ===== المتغيرات الأساسية ===== */
    :root {
        --void-black: #030014;
        --deep-space: #0a0a1f;
        --cyber-blue: #00f0ff;
        --neon-gold: #ffd700;
        --royal-gold: #c9a227;
        --plasma-purple: #8b5cf6;
        --hot-pink: #ec4899;
        --matrix-green: #22c55e;
        --glass-white: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
    }
    
    /* ===== إعادة تعيين وإعدادات عامة ===== */
    *, *::before, *::after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    /* ===== إخفاء عناصر Streamlit ===== */
    #MainMenu, footer, header, [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"],
    .stDeployButton, [data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* ===== الخلفية الكونية ===== */
    .stApp {
        background: var(--void-black) !important;
        background-image: 
            radial-gradient(ellipse at 10% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(0, 240, 255, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(255, 215, 0, 0.05) 0%, transparent 70%),
            linear-gradient(180deg, var(--void-black) 0%, var(--deep-space) 100%) !important;
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
        min-height: 100vh;
        overflow-x: hidden;
    }
    
    /* ===== شبكة الخلفية المتحركة ===== */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
        background-size: 100px 100px;
        animation: gridMove 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes gridMove {
        0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
        100% { transform: perspective(500px) rotateX(60deg) translateY(100px); }
    }
    
    /* ===== الجزيئات العائمة ===== */
    .particles-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: var(--cyber-blue);
        border-radius: 50%;
        animation: float-particle 15s infinite ease-in-out;
        box-shadow: 0 0 10px var(--cyber-blue), 0 0 20px var(--cyber-blue);
    }
    
    .particle:nth-child(odd) {
        background: var(--neon-gold);
        box-shadow: 0 0 10px var(--neon-gold), 0 0 20px var(--neon-gold);
    }
    
    .particle:nth-child(3n) {
        background: var(--plasma-purple);
        box-shadow: 0 0 10px var(--plasma-purple), 0 0 20px var(--plasma-purple);
    }
    
    @keyframes float-particle {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }
    
    /* ===== الهيدر الملكي ===== */
    .royal-header {
        position: relative;
        padding: 60px 40px;
        margin: 20px;
        border-radius: 30px;
        background: linear-gradient(135deg, 
            rgba(10, 10, 31, 0.9) 0%, 
            rgba(3, 0, 20, 0.95) 100%);
        border: 1px solid var(--glass-border);
        overflow: hidden;
        z-index: 10;
    }
    
    /* الإطار الذهبي المتوهج */
    .royal-header::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            var(--neon-gold), 
            var(--cyber-blue), 
            var(--plasma-purple), 
            var(--hot-pink),
            var(--neon-gold));
        background-size: 400% 400%;
        border-radius: 32px;
        z-index: -1;
        animation: borderGlow 8s ease infinite;
        filter: blur(3px);
        opacity: 0.7;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* الزخرفة العربية */
    .arabic-ornament {
        position: absolute;
        font-size: 200px;
        color: rgba(255, 215, 0, 0.03);
        font-family: 'Amiri', serif;
        pointer-events: none;
        user-select: none;
    }
    
    .arabic-ornament.top-right {
        top: -50px;
        right: -30px;
        transform: rotate(15deg);
    }
    
    .arabic-ornament.bottom-left {
        bottom: -50px;
        left: -30px;
        transform: rotate(-15deg);
    }
    
    /* العنوان الرئيسي مع تأثير Glitch */
    .glitch-title {
        font-family: 'Reem Kufi', sans-serif;
        font-size: clamp(2.5rem, 6vw, 4.5rem);
        font-weight: 700;
        text-align: center;
        position: relative;
        color: var(--text-primary);
        text-shadow: 
            0 0 10px rgba(255, 215, 0, 0.5),
            0 0 20px rgba(255, 215, 0, 0.3),
            0 0 40px rgba(255, 215, 0, 0.2);
        animation: textGlow 3s ease-in-out infinite alternate;
    }
    
    .glitch-title::before,
    .glitch-title::after {
        content: attr(data-text);
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    
    .glitch-title::before {
        color: var(--cyber-blue);
        animation: glitch-1 2s infinite linear alternate-reverse;
        clip-path: polygon(0 0, 100% 0, 100% 35%, 0 35%);
    }
    
    .glitch-title::after {
        color: var(--hot-pink);
        animation: glitch-2 3s infinite linear alternate-reverse;
        clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);
    }
    
    @keyframes glitch-1 {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-3px); }
        40% { transform: translateX(3px); }
        60% { transform: translateX(-1px); }
        80% { transform: translateX(1px); }
    }
    
    @keyframes glitch-2 {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(3px); }
        40% { transform: translateX(-3px); }
        60% { transform: translateX(1px); }
        80% { transform: translateX(-1px); }
    }
    
    @keyframes textGlow {
        from { text-shadow: 0 0 10px rgba(255, 215, 0, 0.5), 0 0 20px rgba(255, 215, 0, 0.3); }
        to { text-shadow: 0 0 20px rgba(255, 215, 0, 0.8), 0 0 40px rgba(255, 215, 0, 0.5), 0 0 60px rgba(255, 215, 0, 0.3); }
    }
    
    /* العنوان الفرعي */
    .cyber-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: var(--text-secondary);
        margin-top: 20px;
        letter-spacing: 3px;
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .cyber-subtitle::before,
    .cyber-subtitle::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 100px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-gold), transparent);
    }
    
    .cyber-subtitle::before { right: calc(50% + 250px); }
    .cyber-subtitle::after { left: calc(50% + 250px); }
    
    /* ===== شريط الحالة المتحرك ===== */
    .status-bar {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 40px;
        flex-wrap: wrap;
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 25px;
        background: var(--glass-white);
        border: 1px solid var(--glass-border);
        border-radius: 50px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .status-item:hover {
        transform: translateY(-3px);
        border-color: var(--cyber-blue);
        box-shadow: 0 10px 30px rgba(0, 240, 255, 0.2);
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--matrix-green);
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px var(--matrix-green);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
    }
    
    .status-text {
        color: var(--text-secondary);
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* ===== قسم اختيار النمط ===== */
    .style-selector-container {
        margin: 40px 20px;
        padding: 40px;
        background: linear-gradient(135deg, rgba(10, 10, 31, 0.8), rgba(3, 0, 20, 0.9));
        border-radius: 25px;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    
    .section-title {
        text-align: center;
        font-size: 1.5rem;
        color: var(--neon-gold);
        margin-bottom: 30px;
        font-weight: 700;
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--neon-gold), transparent);
        border-radius: 2px;
    }
    
    /* أزرار الاختيار المحسنة */
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row-reverse !important;
        justify-content: center !important;
        gap: 20px !important;
        flex-wrap: wrap !important;
        background: transparent !important;
        padding: 20px 0 !important;
    }
    
    div[role="radiogroup"] > label {
        position: relative !important;
        background: linear-gradient(135deg, rgba(20, 20, 50, 0.9), rgba(10, 10, 30, 0.95)) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        padding: 20px 30px !important;
        border-radius: 20px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-align: center !important;
        min-width: 180px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        overflow: hidden !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div[role="radiogroup"] > label::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.2), transparent) !important;
        transition: left 0.5s ease !important;
    }
    
    div[role="radiogroup"] > label:hover::before {
        left: 100% !important;
    }
    
    div[role="radiogroup"] > label:hover {
        transform: translateY(-8px) scale(1.02) !important;
        border-color: var(--neon-gold) !important;
        box-shadow: 
            0 20px 40px rgba(255, 215, 0, 0.15),
            0 0 30px rgba(255, 215, 0, 0.1),
            inset 0 0 20px rgba(255, 215, 0, 0.05) !important;
    }
    
    div[role="radiogroup"] > label[data-checked="true"],
    div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(201, 162, 39, 0.1)) !important;
        border-color: var(--neon-gold) !important;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.3),
            inset 0 0 30px rgba(255, 215, 0, 0.1) !important;
    }
    
    /* ===== منطقة الإدخال ===== */
    .input-section {
        margin: 40px 20px;
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 30px;
    }
    
    @media (max-width: 900px) {
        .input-section {
            grid-template-columns: 1fr;
        }
    }
    
    .input-card {
        background: linear-gradient(135deg, rgba(10, 10, 31, 0.9), rgba(3, 0, 20, 0.95));
        border-radius: 25px;
        padding: 35px;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .input-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--cyber-blue), var(--neon-gold), var(--plasma-purple));
    }
    
    .input-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 215, 0, 0.3);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }
    
    .input-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .input-icon {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, var(--neon-gold), var(--royal-gold));
        border-radius: 15px;
        font-size: 1.5rem;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
    }
    
    .input-title {
        color: var(--text-primary);
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .input-subtitle {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* تخصيص حقل النص */
    .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: var(--text-primary) !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1.05rem !important;
        padding: 20px !important;
        direction: rtl !important;
        text-align: right !important;
        transition: all 0.3s ease !important;
        min-height: 200px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--cyber-blue) !important;
        box-shadow: 
            0 0 20px rgba(0, 240, 255, 0.2),
            inset 0 0 20px rgba(0, 240, 255, 0.05) !important;
        outline: none !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* تخصيص رفع الملفات */
    [data-testid="stFileUploader"] {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 2px dashed rgba(255, 215, 0, 0.3) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--neon-gold) !important;
        background: rgba(255, 215, 0, 0.05) !important;
    }
    
    [data-testid="stFileUploader"] > div {
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, var(--neon-gold), var(--royal-gold)) !important;
        color: var(--void-black) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px 25px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* ===== زر المعالجة الرئيسي ===== */
    .main-action-container {
        margin: 50px 20px;
        text-align: center;
    }
    
    .stButton > button {
        position: relative !important;
        background: linear-gradient(135deg, #ffd700 0%, #c9a227 50%, #ffd700 100%) !important;
        background-size: 200% auto !important;
        color: var(--void-black) !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        padding: 20px 60px !important;
        border: none !important;
        border-radius: 20px !important;
        cursor: pointer !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 
            0 10px 40px rgba(255, 215, 0, 0.4),
            0 0 0 0 rgba(255, 215, 0, 0.5) !important;
        animation: buttonShine 3s ease infinite !important;
    }
    
    @keyframes buttonShine {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 200% center; }
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.3) 50%,
            transparent 70%
        ) !important;
        transform: rotate(45deg) translateY(-100%) !important;
        transition: transform 0.6s ease !important;
    }
    
    .stButton > button:hover::before {
        transform: rotate(45deg) translateY(100%) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 
            0 20px 60px rgba(255, 215, 0, 0.5),
            0 0 50px rgba(255, 215, 0, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    /* ===== شريط التقدم المخصص ===== */
    .progress-container {
        margin: 40px auto;
        max-width: 600px;
        padding: 30px;
        background: var(--glass-white);
        border-radius: 20px;
        border: 1px solid var(--glass-border);
    }
    
    .progress-bar-wrapper {
        height: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--cyber-blue), var(--neon-gold), var(--plasma-purple));
        background-size: 200% 100%;
        border-radius: 10px;
        animation: progressGlow 2s ease infinite;
        transition: width 0.5s ease;
    }
    
    @keyframes progressGlow {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
    
    .progress-text {
        text-align: center;
        margin-top: 15px;
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    /* ===== منطقة النتائج ===== */
    .result-section {
        margin: 40px 20px;
        padding: 40px;
        background: linear-gradient(135deg, rgba(10, 10, 31, 0.95), rgba(3, 0, 20, 0.98));
        border-radius: 30px;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }
    
    .result-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--matrix-green), var(--cyber-blue), var(--neon-gold));
    }
    
    .success-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
        border: 1px solid var(--matrix-green);
        padding: 15px 30px;
        border-radius: 50px;
        margin-bottom: 30px;
        animation: successPulse 2s ease infinite;
    }
    
    @keyframes successPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(34, 197, 94, 0.3); }
        50% { box-shadow: 0 0 40px rgba(34, 197, 94, 0.5); }
    }
    
    .success-icon {
        font-size: 1.5rem;
    }
    
    .success-text {
        color: var(--matrix-green);
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* ===== زر التحميل ===== */
    .download-btn-container {
        text-align: center;
        margin-top: 30px;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--plasma-purple), #6d28d9) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 18px 50px !important;
        border-radius: 15px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.6) !important;
    }
    
    /* ===== تنبيهات مخصصة ===== */
    .stAlert {
        background: rgba(255, 215, 0, 0.1) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 15px !important;
        color: var(--text-primary) !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
    }
    
    /* ===== Spinner مخصص ===== */
    .stSpinner > div {
        border-color: var(--neon-gold) transparent transparent transparent !important;
    }
    
    /* ===== الفوتر ===== */
    .cyber-footer {
        text-align: center;
        padding: 40px 20px;
        margin-top: 60px;
        border-top: 1px solid var(--glass-border);
        color: var(--text-secondary);
    }
    
    .footer-logo {
        font-family: 'Reem Kufi', sans-serif;
        font-size: 1.5rem;
        color: var(--neon-gold);
        margin-bottom: 15px;
    }
    
    .footer-text {
        font-size: 0.9rem;
        opacity: 0.7;
    }
    
    /* ===== تأثيرات إضافية ===== */
    .floating-shapes {
        position: fixed;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .shape {
        position: absolute;
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 50%;
        animation: floatShape 20s infinite linear;
    }
    
    .shape:nth-child(1) {
        width: 300px;
        height: 300px;
        top: 10%;
        right: -150px;
        animation-delay: 0s;
    }
    
    .shape:nth-child(2) {
        width: 200px;
        height: 200px;
        top: 60%;
        left: -100px;
        animation-delay: -5s;
    }
    
    .shape:nth-child(3) {
        width: 150px;
        height: 150px;
        bottom: 20%;
        right: 20%;
        animation-delay: -10s;
    }
    
    @keyframes floatShape {
        0% { transform: rotate(0deg) translateX(0); }
        50% { transform: rotate(180deg) translateX(50px); }
        100% { transform: rotate(360deg) translateX(0); }
    }
    
    /* ===== تخصيص المعاينة ===== */
    iframe {
        border-radius: 20px !important;
        border: 2px solid var(--glass-border) !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* ===== إخفاء عناصر Streamlit الافتراضية ===== */
    .stTextInput > label,
    .stTextArea > label,
    .stFileUploader > label,
    .stRadio > label {
        display: none !important;
    }
    
    /* ===== تحسينات الاستجابة ===== */
    @media (max-width: 768px) {
        .royal-header {
            padding: 40px 20px;
            margin: 10px;
        }
        
        .glitch-title {
            font-size: 2rem;
        }
        
        .cyber-subtitle::before,
        .cyber-subtitle::after {
            display: none;
        }
        
        .status-bar {
            gap: 15px;
        }
        
        .input-section {
            margin: 20px 10px;
            gap: 20px;
        }
        
        .input-card {
            padding: 25px;
        }
        
        div[role="radiogroup"] > label {
            min-width: 140px !important;
            padding: 15px 20px !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* ===== تأثير الماوس التفاعلي ===== */
    .cursor-glow {
        position: fixed;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.3), transparent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transition: transform 0.1s ease;
    }
</style>
"""

# ---------------------------------------------------------
# 🎨 القوالب المحسنة
# ---------------------------------------------------------

STYLE_OFFICIAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    
    :root {
        --navy-primary: #001f3f;
        --navy-dark: #00152a;
        --gold-primary: #c9a227;
        --gold-light: #ffd700;
        --white: #ffffff;
        --gray-100: #f8f9fa;
        --gray-200: #e9ecef;
        --text-dark: #1a1a2e;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-200) 100%);
        color: var(--text-dark);
        line-height: 1.8;
        direction: rtl;
        min-height: 100vh;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px 30px;
    }
    
    header {
        background: linear-gradient(135deg, var(--navy-primary) 0%, var(--navy-dark) 100%);
        color: var(--gold-light);
        padding: 50px 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 31, 63, 0.3);
    }
    
    header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--gold-primary), var(--gold-light), var(--gold-primary));
    }
    
    header h1 {
        font-family: 'Amiri', serif;
        font-size: 2.8em;
        margin-bottom: 10px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    header h2 {
        font-size: 1.3em;
        color: rgba(255, 215, 0, 0.8);
        font-weight: 400;
    }
    
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 30px;
    }
    
    .card {
        background: var(--white);
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, var(--gold-light), var(--gold-primary));
    }
    
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    }
    
    .card h3 {
        color: var(--navy-primary);
        font-size: 1.6em;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid var(--gold-light);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 20px 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
    }
    
    table th {
        background: linear-gradient(135deg, var(--navy-primary), var(--navy-dark));
        color: var(--gold-light);
        padding: 18px 20px;
        font-weight: 600;
        font-size: 1.05em;
    }
    
    table td {
        padding: 16px 20px;
        border-bottom: 1px solid var(--gray-200);
        background: var(--white);
    }
    
    table tr:last-child td { border-bottom: none; }
    
    table tr:hover td {
        background: rgba(201, 162, 39, 0.05);
    }
    
    ul {
        list-style: none;
        padding: 0;
    }
    
    ul li {
        padding: 18px 20px;
        margin-bottom: 12px;
        background: var(--gray-100);
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
        border-right: 4px solid transparent;
    }
    
    ul li:hover {
        background: var(--white);
        border-right-color: var(--gold-primary);
        transform: translateX(-5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    }
    
    ul li span.value {
        background: linear-gradient(135deg, var(--navy-primary), var(--navy-dark));
        color: var(--gold-light);
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.1em;
        min-width: 80px;
        text-align: center;
    }
    
    footer {
        grid-column: 1 / -1;
        text-align: center;
        padding: 40px;
        margin-top: 50px;
        background: var(--white);
        border-radius: 20px;
        border-top: 4px solid var(--navy-primary);
    }
    
    footer p {
        color: var(--navy-primary);
        font-size: 1.1em;
    }
    
    footer strong {
        color: var(--gold-primary);
    }
</style>
"""

STYLE_DIGITAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');
    
    :root {
        --primary-blue: #0066ff;
        --primary-dark: #0052cc;
        --accent-cyan: #00d4ff;
        --bg-light: #f0f4f8;
        --bg-white: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --success: #10b981;
        --warning: #f59e0b;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--bg-light);
        color: var(--text-primary);
        line-height: 1.8;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 30px auto;
        padding: 40px;
        background: var(--bg-white);
        border-radius: 30px;
        box-shadow: 0 25px 80px rgba(0, 102, 255, 0.1);
    }
    
    header {
        text-align: center;
        padding-bottom: 40px;
        margin-bottom: 50px;
        border-bottom: 3px solid var(--primary-blue);
        position: relative;
    }
    
    header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 6px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--primary-blue));
        border-radius: 3px;
    }
    
    h1 {
        font-size: 2.8em;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-cyan));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    h2 {
        font-size: 2em;
        color: var(--primary-blue);
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px dashed var(--bg-light);
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    h2::before {
        content: '';
        width: 5px;
        height: 30px;
        background: linear-gradient(180deg, var(--primary-blue), var(--accent-cyan));
        border-radius: 3px;
    }
    
    .card {
        background: var(--bg-white);
        border: 2px solid var(--bg-light);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 30px;
        transition: all 0.4s ease;
        position: relative;
    }
    
    .card:hover {
        border-color: var(--accent-cyan);
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0, 212, 255, 0.15);
    }
    
    .goal {
        background: linear-gradient(135deg, #e0f2fe, #e0e7ff);
        border: 2px solid var(--accent-cyan);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-size: 1.3em;
        font-weight: 700;
        color: var(--primary-dark);
        margin: 30px 0;
        position: relative;
        overflow: hidden;
    }
    
    .goal::before {
        content: '🎯';
        position: absolute;
        top: 50%;
        right: 30px;
        transform: translateY(-50%);
        font-size: 2em;
        opacity: 0.3;
    }
    
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 15px;
        overflow: hidden;
        margin: 25px 0;
        box-shadow: 0 5px 30px rgba(0, 0, 0, 0.08);
    }
    
    thead th {
        background: linear-gradient(135deg, var(--primary-blue), var(--primary-dark));
        color: white;
        padding: 20px;
        font-weight: 700;
    }
    
    td {
        padding: 18px 20px;
        border-bottom: 1px solid var(--bg-light);
        text-align: center;
    }
    
    tr:hover td {
        background: rgba(0, 212, 255, 0.05);
    }
    
    ul li {
        position: relative;
        padding: 15px 35px 15px 15px;
        margin-bottom: 15px;
        background: var(--bg-light);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    ul li::before {
        content: '◆';
        position: absolute;
        right: 12px;
        color: var(--primary-blue);
        font-size: 0.8em;
    }
    
    ul li:hover {
        background: var(--bg-white);
        box-shadow: 0 5px 20px rgba(0, 102, 255, 0.1);
        transform: translateX(-5px);
    }
    
    footer {
        text-align: center;
        padding-top: 40px;
        margin-top: 50px;
        border-top: 2px solid var(--bg-light);
        color: var(--text-secondary);
    }
</style>
"""

STYLE_ANALYTICAL = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    :root {
        --deep-blue: #004a99;
        --royal-blue: #0056b3;
        --accent-orange: #ff6b35;
        --accent-red: #d90429;
        --accent-yellow: #f7b801;
        --accent-green: #2ec4b6;
        --bg-gray: #f4f7f6;
        --bg-white: #ffffff;
        --text-dark: #2d3436;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--bg-gray);
        color: var(--text-dark);
        line-height: 1.8;
        direction: rtl;
    }
    
    .container {
        max-width: 1200px;
        margin: 30px auto;
        padding: 20px;
    }
    
    header {
        background: linear-gradient(135deg, var(--deep-blue) 0%, var(--royal-blue) 100%);
        color: white;
        padding: 50px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(0, 74, 153, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    header h1 {
        font-size: 2.5em;
        font-weight: 900;
        margin-bottom: 10px;
        position: relative;
    }
    
    .report-section {
        background: var(--bg-white);
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 35px;
        padding: 40px;
        position: relative;
        overflow: hidden;
    }
    
    .report-section::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, var(--deep-blue), var(--accent-orange));
    }
    
    .report-section h2 {
        color: var(--deep-blue);
        font-size: 1.8em;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 3px solid var(--accent-orange);
        display: inline-block;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 25px;
        margin: 30px 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #eef5ff, #f8faff);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 2px solid #d0e3ff;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 74, 153, 0.2);
        border-color: var(--deep-blue);
    }
    
    .stat-card .value {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--deep-blue), var(--royal-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .stat-card .label {
        color: var(--text-dark);
        font-size: 1.1em;
        font-weight: 600;
    }
    
    .pyramid-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 25px;
    }
    
    .tier-card {
        border-radius: 20px;
        padding: 30px;
        background: var(--bg-white);
        border: 2px solid #e0e0e0;
        position: relative;
        overflow: hidden;
    }
    
    .tier-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
    }
    
    .tier-upper::before { background: linear-gradient(90deg, var(--accent-red), #ff6b6b); }
    .tier-middle::before { background: linear-gradient(90deg, var(--accent-yellow), #ffd93d); }
    .tier-lower::before { background: linear-gradient(90deg, var(--accent-green), #4ecdc4); }
    
    .tier-card h4 {
        font-size: 1.3em;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .bar-container {
        background: #e0e0e0;
        border-radius: 10px;
        height: 16px;
        margin-top: 15px;
        overflow: hidden;
    }
    
    .bar {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    .tier-upper .bar { background: linear-gradient(90deg, var(--accent-red), #ff6b6b); }
    .tier-middle .bar { background: linear-gradient(90deg, var(--accent-yellow), #ffd93d); }
    .tier-lower .bar { background: linear-gradient(90deg, var(--accent-green), #4ecdc4); }
    
    footer {
        text-align: center;
        padding: 40px;
        margin-top: 40px;
        background: var(--bg-white);
        border-radius: 20px;
        border-top: 4px solid var(--deep-blue);
    }
</style>
"""

STYLE_PRESENTATION = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
    
    :root {
        --primary-navy: #002b49;
        --primary-blue: #004e89;
        --gold-main: #c5a059;
        --gold-light: #e6c885;
        --white: #ffffff;
        --grey-light: #f8f9fa;
        --text-dark: #333333;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--primary-navy);
        overflow: hidden;
        height: 100vh;
        width: 100vw;
        direction: rtl;
    }
    
    .presentation-container {
        width: 100%;
        height: 100%;
        position: relative;
        background: radial-gradient(ellipse at center, #003865 0%, #001a2c 100%);
    }
    
    .slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        visibility: hidden;
        transform: scale(0.95) translateX(50px);
        transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
        display: flex;
        flex-direction: column;
        padding: 50px 70px;
    }
    
    .slide.active {
        opacity: 1;
        visibility: visible;
        transform: scale(1) translateX(0);
        z-index: 10;
    }
    
    .slide.cover {
        align-items: center;
        justify-content: center;
        text-align: center;
        background: linear-gradient(135deg, var(--primary-navy) 30%, #001a2c 100%);
    }
    
    .cover-content {
        border: 3px solid var(--gold-main);
        padding: 80px 100px;
        position: relative;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 20px;
    }
    
    .main-title {
        font-family: 'Tajawal', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        color: var(--white);
        margin-bottom: 20px;
        text-shadow: 0 5px 30px rgba(0, 0, 0, 0.5);
    }
    
    .sub-title {
        font-size: 1.8rem;
        color: var(--gold-main);
        font-weight: 300;
    }
    
    .slide-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid var(--gold-main);
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    
    .header-title h2 {
        color: var(--gold-main);
        font-size: 2.2rem;
        font-weight: 800;
    }
    
    .header-logo {
        font-family: 'Tajawal', sans-serif;
        color: var(--white);
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .slide-content {
        flex-grow: 1;
        display: flex;
        gap: 50px;
        height: 100%;
        overflow: hidden;
    }
    
    .text-panel {
        flex: 3;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 40px;
        color: var(--text-dark);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        overflow-y: auto;
        border-right: 6px solid var(--gold-main);
    }
    
    .visual-panel {
        flex: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: var(--white);
        text-align: center;
    }
    
    .icon-box {
        font-size: 6rem;
        color: var(--gold-main);
        margin-bottom: 25px;
        text-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    h3 {
        color: var(--primary-blue);
        font-size: 1.7rem;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px dashed #e0e0e0;
    }
    
    p {
        font-size: 1.25rem;
        line-height: 2;
        margin-bottom: 25px;
        text-align: justify;
    }
    
    li {
        font-size: 1.2rem;
        margin-bottom: 15px;
        line-height: 1.8;
        padding-right: 25px;
        position: relative;
    }
    
    li::before {
        content: '◆';
        position: absolute;
        right: 0;
        color: var(--gold-main);
    }
    
    .nav-controls {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 20px;
        z-index: 100;
    }
    
    .nav-btn {
        background: transparent;
        border: 2px solid var(--gold-main);
        color: var(--gold-main);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.4rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .nav-btn:hover {
        background: var(--gold-main);
        color: var(--primary-navy);
        transform: scale(1.1);
        box-shadow: 0 10px 30px rgba(197, 160, 89, 0.4);
    }
    
    .page-number {
        position: absolute;
        bottom: 40px;
        right: 70px;
        color: var(--gold-main);
        font-size: 1.3rem;
        font-weight: bold;
    }
    
    .signature-box {
        margin-top: 60px;
        padding-top: 30px;
        border-top: 2px solid var(--gold-main);
        text-align: center;
    }
    
    .signature-title {
        font-size: 1rem;
        color: #aaa;
        margin-bottom: 15px;
    }
    
    .signature-name {
        font-size: 1.5rem;
        color: var(--gold-main);
        font-weight: bold;
        font-family: 'Tajawal', sans-serif;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

STYLE_EXECUTIVE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@200;300;400;500;700;800;900&display=swap');
    
    :root {
        --navy-deep: #002b49;
        --gold-accent: #c5a059;
        --gold-light: #e6c885;
        --white: #ffffff;
        --gray-50: #fafafa;
        --gray-100: #f5f5f5;
        --text-primary: #1a1a1a;
        --text-secondary: #666666;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background: var(--white);
        color: var(--text-primary);
        direction: rtl;
        line-height: 1.8;
    }
    
    .container {
        max-width: 900px;
        margin: 50px auto;
        padding: 60px;
        border: 1px solid #eee;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.08);
    }
    
    header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 30px;
        margin-bottom: 50px;
        border-bottom: 5px solid var(--navy-deep);
    }
    
    .brand {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--navy-deep);
        letter-spacing: -1px;
    }
    
    .date {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    h1 {
        font-size: 3.2rem;
        font-weight: 900;
        line-height: 1.2;
        margin-bottom: 15px;
        color: var(--navy-deep);
    }
    
    .executive-summary {
        font-size: 1.4rem;
        line-height: 1.9;
        color: var(--text-secondary);
        margin: 40px 0;
        padding: 30px;
        background: var(--gray-50);
        border-right: 6px solid var(--gold-accent);
    }
    
    .grid-2 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 30px;
        margin: 40px 0;
    }
    
    .metric-box {
        padding: 30px;
        background: var(--gray-100);
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .metric-box:hover {
        border-color: var(--gold-accent);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .metric-val {
        font-size: 3rem;
        font-weight: 900;
        color: var(--navy-deep);
        margin-bottom: 10px;
    }
    
    .metric-lbl {
        font-size: 1.1rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 800;
        text-transform: uppercase;
        margin: 50px 0 25px;
        color: var(--gold-accent);
        border-bottom: 3px solid var(--gray-100);
        padding-bottom: 10px;
        display: inline-block;
    }
    
    p {
        font-size: 1.15rem;
        margin-bottom: 20px;
    }
    
    ul {
        list-style: none;
    }
    
    ul li {
        padding: 15px 25px 15px 0;
        margin-bottom: 10px;
        border-bottom: 1px solid var(--gray-100);
        position: relative;
    }
    
    ul li::before {
        content: '●';
        position: absolute;
        right: 0;
        color: var(--gold-accent);
    }
    
    footer {
        margin-top: 80px;
        padding-top: 30px;
        border-top: 2px solid var(--gray-100);
        text-align: center;
        color: var(--text-secondary);
    }
    
    footer strong {
        color: var(--gold-accent);
    }
</style>
"""

SCRIPT_PRESENTATION = """
<script>
    let currentSlideIndex = 1;
    
    function updateSlide() {
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        if(totalSlides === 0) return;
        
        slides.forEach((slide, index) => {
            slide.classList.remove('active');
            slide.style.transform = 'scale(0.95) translateX(50px)';
        });
        
        const activeSlide = document.getElementById(`slide-${currentSlideIndex}`);
        if(activeSlide) {
            activeSlide.classList.add('active');
            activeSlide.style.transform = 'scale(1) translateX(0)';
        }
        
        const pageNum = document.getElementById('page-num');
        if(pageNum) pageNum.innerText = `${currentSlideIndex} / ${totalSlides}`;
    }
    
    function nextSlide() {
        const totalSlides = document.querySelectorAll('.slide').length;
        if (currentSlideIndex < totalSlides) {
            currentSlideIndex++;
            updateSlide();
        }
    }
    
    function prevSlide() {
        if (currentSlideIndex > 1) {
            currentSlideIndex--;
            updateSlide();
        }
    }
    
    document.addEventListener('keydown', function(event) {
        if (event.key === "ArrowLeft" || event.key === " ") nextSlide();
        else if (event.key === "ArrowRight") prevSlide();
    });
    
    setTimeout(updateSlide, 100);
</script>
"""

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    """استخراج النص من الملفات المرفوعة"""
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

def clean_html_response(text):
    """تنظيف رد الذكاء الاصطناعي"""
    text = text.replace("```html", "").replace("```", "")
    return text.strip()

def get_working_model():
    """الحصول على نموذج Gemini المتاح"""
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name:
                    return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

def generate_particles_html():
    """توليد HTML للجزيئات المتحركة"""
    particles = ""
    for i in range(20):
        left = (i * 5) % 100
        delay = i * 0.5
        duration = 10 + (i % 5) * 2
        particles += f'<div class="particle" style="left: {left}%; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'
    return f'<div class="particles-container">{particles}</div>'

def generate_floating_shapes():
    """توليد الأشكال العائمة"""
    return """
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    """

# ---------------------------------------------------------
# 🏗️ بناء الواجهة الرئيسية
# ---------------------------------------------------------

# حقن CSS
st.markdown(REVOLUTIONARY_CSS, unsafe_allow_html=True)

# الجزيئات المتحركة
particles_html = generate_particles_html()
st.markdown(particles_html, unsafe_allow_html=True)

# الأشكال العائمة
shapes_html = generate_floating_shapes()
st.markdown(shapes_html, unsafe_allow_html=True)

# الهيدر الملكي
header_html = '''
<div class="royal-header">
    <div class="arabic-ornament top-right">۞</div>
    <div class="arabic-ornament bottom-left">۞</div>
    <h1 class="glitch-title" data-text="تيار الحكمة الوطني">تيار الحكمة الوطني</h1>
    <p class="cyber-subtitle">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</p>
    <div class="status-bar">
        <div class="status-item">
            <div class="status-dot"></div>
            <span class="status-text">النظام نشط</span>
        </div>
        <div class="status-item">
            <div class="status-dot" style="background: #ffd700; box-shadow: 0 0 10px #ffd700;"></div>
            <span class="status-text">الذكاء الاصطناعي متصل</span>
        </div>
        <div class="status-item">
            <div class="status-dot" style="background: #8b5cf6; box-shadow: 0 0 10px #8b5cf6;"></div>
            <span class="status-text">جاهز للمعالجة</span>
        </div>
    </div>
</div>
'''
st.markdown(header_html, unsafe_allow_html=True)

# قسم اختيار النمط
style_section = '''
<div class="style-selector-container">
    <h2 class="section-title">🎨 اختر نمط الإخراج المطلوب</h2>
</div>
'''
st.markdown(style_section, unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي", "✨ ملخص تنفيذي حديث"),
    horizontal=True,
    label_visibility="collapsed"
)

# قسم الإدخال
col_input, col_upload = st.columns([1.5, 1])

with col_input:
    input_card_html = '''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📝</div>
            <div>
                <div class="input-title">البيانات والملاحظات</div>
                <div class="input-subtitle">أدخل النص أو الصق محتوى التقرير</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(input_card_html, unsafe_allow_html=True)
    user_text = st.text_area("", height=250, placeholder="اكتب الملاحظات أو الصق نص التقرير هنا...", label_visibility="collapsed")

with col_upload:
    upload_card_html = '''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📎</div>
            <div>
                <div class="input-title">رفع الملفات</div>
                <div class="input-subtitle">PDF, XLSX, TXT - حتى 200MB</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(upload_card_html, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    
    if uploaded_file:
        success_html = f'''
        <div style="
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
            border: 1px solid #22c55e;
            border-radius: 12px;
            padding: 15px 20px;
            margin-top: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span style="font-size: 1.5rem;">✅</span>
            <span style="color: #22c55e; font-weight: 600;">تم إرفاق: {uploaded_file.name}</span>
        </div>
        '''
        st.markdown(success_html, unsafe_allow_html=True)

# زر المعالجة
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 بدء المعالجة وإنشاء التقرير الكامل"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API. يرجى إضافته في Secrets.")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        with st.spinner('📂 جاري قراءة الملف...'):
            file_content = extract_text_from_file(uploaded_file)
            full_text += f"\n\n[محتوى الملف]:\n{file_content}"
    
    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات أو رفع ملف للمعالجة.")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())
            
            # تحديد النمط والقواعد
            target_css = ""
            design_rules = ""
            file_label = "Report"
            
            unified_signature = """
            <div style="margin-top: 60px; text-align: center; padding-top: 30px; border-top: 3px solid #c9a227; font-family: 'Tajawal';">
                <p style="color: #666; margin-bottom: 10px; font-size: 1rem;">صادر من</p>
                <p style="color: #002b49; font-size: 1.3em; font-weight: 800; margin-bottom: 5px;">الجهاز المركزي للجودة الشاملة</p>
                <p style="color: #c9a227; font-size: 1.1em; font-weight: 600;">وحدة التخطيط الاستراتيجي والتطوير</p>
            </div>
            """
            
            if "الرسمي" in report_type:
                target_css = STYLE_OFFICIAL
                file_label = "Official_Report"
                design_rules = """
                Style: Official Corporate Report with Royal Theme.
                - Use <div class="card-grid"> as container for cards.
                - Wrap sections in <div class="card"> with <h3> titles.
                - Use HTML <table> for tabular data.
                - Use <ul> with <li><span>Label</span> <span class="value">Value</span></li> for lists.
                """
            
            elif "الرقمي" in report_type:
                target_css = STYLE_DIGITAL
                file_label = "Digital_Dashboard"
                design_rules = """
                Style: Modern Digital Dashboard with Blue Theme.
                - Use <section class="card"> for main sections.
                - Use <div class="goal"> for key highlights.
                - Use clean tables with proper thead/tbody.
                """
            
            elif "التحليل" in report_type:
                target_css = STYLE_ANALYTICAL
                file_label = "Deep_Analysis"
                design_rules = """
                Style: Statistical Deep Analysis.
                - Use <div class="report-section"> for main sections.
                - Use <div class="stats-grid"> with <div class="stat-card"> for statistics.
                - Use <div class="pyramid-grid"> with tier-card classes (tier-upper, tier-middle, tier-lower).
                - Include progress bars with <div class="bar-container"><div class="bar" style="width: XX%;"></div></div>.
                """
            
            elif "ملخص" in report_type:
                target_css = STYLE_EXECUTIVE
                file_label = "Executive_Summary"
                design_rules = """
                Style: Modern Executive Summary - Clean & Minimal.
                - Use <div class="executive-summary"> for the main summary paragraph.
                - Use <div class="grid-2"> with <div class="metric-box"> for metrics.
                - Use <h2 class="section-title"> for section headers.
                """
            
            elif "عرض تقديمي" in report_type:
                target_css = STYLE_PRESENTATION
                file_label = "Presentation_Slides"
                design_rules = """
                Style: Interactive Presentation Slides.
                Structure:
                1. First slide: <div class="slide cover active" id="slide-1"> with cover-content, main-title, sub-title.
                2. Content slides: <div class="slide" id="slide-N"> with slide-header, slide-content (text-panel + visual-panel).
                3. Use FontAwesome icons in visual-panel: <div class="icon-box"><i class="fas fa-icon"></i></div>.
                4. Last slide must have signature-box.
                5. Output ONLY HTML body content, no CSS/JS.
                """
                unified_signature = """
                <div class="nav-controls">
                    <button class="nav-btn" onclick="prevSlide()"><i class="fas fa-chevron-right"></i></button>
                    <button class="nav-btn" onclick="nextSlide()"><i class="fas fa-chevron-left"></i></button>
                </div>
                <div class="page-number" id="page-num">1 / 1</div>
                """
            
            # بناء الـ Prompt
            prompt = f"""
            You are an expert Data Analyst & Document Designer for 'Al-Hikma National Movement'.
            
            **CRITICAL INSTRUCTIONS:**
            1. **FULL CONTENT:** Do NOT summarize. Include EVERY detail, number, name from the input.
            2. **DATE:** Detect date from input. If not found, use generic or current context.
            3. **FORMAT:** Output ONLY valid HTML (body content). No markdown or ```html markers.
            4. **DESIGN RULES:** {design_rules}
            5. **LANGUAGE:** Professional Arabic.
            
            **INPUT DATA:**
            {full_text}
            """
            
            # شريط التقدم المخصص
            progress_placeholder = st.empty()
            
            with st.spinner(''):
                # عرض تقدم مخصص
                for i in range(0, 101, 10):
                    progress_html = f'''
                    <div class="progress-container">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <span style="font-size: 2rem;">🤖</span>
                        </div>
                        <div class="progress-bar-wrapper">
                            <div class="progress-bar-fill" style="width: {i}%;"></div>
                        </div>
                        <p class="progress-text">جاري تحليل البيانات وتوليد التقرير... {i}%</p>
                    </div>
                    '''
                    progress_placeholder.markdown(progress_html, unsafe_allow_html=True)
                    time.sleep(0.1)
                
                # توليد المحتوى
                response = model.generate_content(prompt)
                html_body = clean_html_response(response.text)
                
                progress_placeholder.empty()
            
            # تجميع الملف النهائي
            container_class = 'presentation-container' if 'عرض تقديمي' in report_type else 'container'
            
            final_html = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>تقرير {file_label} - تيار الحكمة</title>
                <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&family=Tajawal:wght@300;400;500;700;800&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
                {target_css}
            </head>
            <body>
                <div class="{container_class}">
                    {html_body}
                    {unified_signature}
                </div>
                {SCRIPT_PRESENTATION if 'عرض تقديمي' in report_type else ''}
            </body>
            </html>
            """
            
            # عرض النتيجة
            result_html = '''
            <div class="result-section">
                <div class="success-badge">
                    <span class="success-icon">✅</span>
                    <span class="success-text">تم إنشاء التقرير بنجاح!</span>
                </div>
            </div>
            '''
            st.markdown(result_html, unsafe_allow_html=True)
            
            # المعاينة
            st.components.v1.html(final_html, height=900, scrolling=True)
            
            # زر التحميل
            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=final_html,
                file_name=f"{file_label}.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")

# الفوتر
footer_html = '''
<div class="cyber-footer">
    <div class="footer-logo">⚡ تيار الحكمة الوطني</div>
    <p class="footer-text">منصة التحليل الاستراتيجي المدعومة بالذكاء الاصطناعي</p>
    <p class="footer-text" style="margin-top: 10px; opacity: 0.5;">جميع الحقوق محفوظة © 2025</p>
</div>
'''
st.markdown(footer_html, unsafe_allow_html=True)
