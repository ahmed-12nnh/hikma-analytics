import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from io import StringIO
import time
import re

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
    page_title="منصة التحليل الاستراتيجي",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 🎨 CSS للواجهة
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    * { box-sizing: border-box; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001f3f 0%, #000d1a 90%);
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
    }

    [data-testid="stSidebar"], header, #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

    .hero-section {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.95), rgba(10, 46, 92, 0.9));
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        margin: 20px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 40px rgba(0, 31, 63, 0.8);
        position: relative;
        animation: fadeIn 1s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer { 0%, 100% { opacity: 0.7; } 50% { opacity: 1; } }

    .main-title {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(180deg, #FFD700 0%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }

    .sub-title {
        color: #e0e0e0;
        font-size: 18px;
        letter-spacing: 2px;
        font-weight: 500;
    }

    .section-header {
        text-align: center;
        margin: 30px 20px;
        color: #FFD700;
        font-size: 1.4rem;
        font-weight: bold;
    }

    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        gap: 15px !important;
        flex-wrap: wrap !important;
        background: rgba(0, 0, 0, 0.3) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 0 20px 30px 20px !important;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 20, 40, 0.95)) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        padding: 15px 25px !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    div[role="radiogroup"] label:hover {
        border-color: #FFD700 !important;
        transform: translateY(-5px) !important;
    }

    .input-card {
        background: linear-gradient(135deg, rgba(0, 31, 63, 0.9), rgba(0, 15, 30, 0.95));
        border-radius: 20px;
        padding: 30px;
        margin: 10px;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }

    .input-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
    }

    .input-icon {
        width: 50px; height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #FFD700, #B8860B);
        border-radius: 12px;
        font-size: 1.5rem;
    }

    .input-title { color: #FFD700; font-size: 1.2rem; font-weight: 700; }
    .input-subtitle { color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-top: 5px; }

    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        padding: 20px !important;
        direction: rtl !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px dashed rgba(255, 215, 0, 0.3) !important;
        border-radius: 15px !important;
        padding: 25px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #DAA520) !important;
        color: #001f3f !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        border-radius: 15px !important;
        width: 100% !important;
        padding: 18px 40px !important;
        border: none !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 15px 40px !important;
        border-radius: 12px !important;
    }

    .success-banner {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 20px;
    }
    
    .success-banner span { color: #22c55e; font-size: 1.2rem; font-weight: 700; }

    .stTextArea > label, .stFileUploader > label, .stRadio > label { display: none !important; }

    iframe { border-radius: 15px !important; border: 2px solid rgba(255, 215, 0, 0.3) !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🎨 القوالب المحسنة
# ---------------------------------------------------------

STYLE_OFFICIAL = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&family=Amiri:wght@400;700&display=swap');
    
    :root {
        --navy: #001f3f;
        --navy-dark: #00152a;
        --gold: #D4AF37;
        --gold-light: #F4E4BC;
        --white: #ffffff;
        --gray-100: #f5f5f5;
        --gray-200: #e5e5e5;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        color: #262626;
        line-height: 1.8;
        direction: rtl;
        padding: 40px 20px;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        background: var(--white);
        border-radius: 24px;
        box-shadow: 0 25px 80px rgba(0, 31, 63, 0.15);
        overflow: hidden;
    }
    
    .container::before {
        content: '';
        display: block;
        height: 8px;
        background: linear-gradient(90deg, var(--gold), var(--gold-light), var(--gold));
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    header {
        background: linear-gradient(135deg, var(--navy), var(--navy-dark));
        padding: 60px 50px;
        text-align: center;
    }
    
    header h1 {
        font-family: 'Amiri', serif;
        font-size: 2.8rem;
        color: var(--gold);
        margin-bottom: 15px;
        text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
    }
    
    header h2 {
        font-size: 1.2rem;
        color: var(--gold-light);
        font-weight: 400;
    }
    
    .header-meta {
        margin-top: 25px;
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .meta-tag {
        background: rgba(212, 175, 55, 0.15);
        border: 1px solid rgba(212, 175, 55, 0.3);
        color: var(--gold-light);
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.9rem;
    }
    
    .content { padding: 50px; }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 25px;
        margin-bottom: 50px;
    }
    
    .stat-card {
        background: linear-gradient(145deg, var(--white), var(--gray-100));
        border-radius: 20px;
        padding: 30px;
        border: 1px solid var(--gray-200);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 80px; height: 80px;
        background: var(--accent-color, var(--gold));
        opacity: 0.1;
        border-radius: 0 20px 0 80px;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0, 31, 63, 0.15);
    }
    
    .stat-card .icon {
        width: 60px; height: 60px;
        background: linear-gradient(135deg, var(--accent-color, var(--gold)), #B8860B);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        margin-bottom: 20px;
    }
    
    .stat-card .label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .stat-card .value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--navy);
    }
    
    .stat-card.blue { --accent-color: #3b82f6; }
    .stat-card.green { --accent-color: #22c55e; }
    .stat-card.amber { --accent-color: #f59e0b; }
    .stat-card.red { --accent-color: #ef4444; }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--navy);
        margin: 50px 0 30px;
        padding-bottom: 15px;
        border-bottom: 3px solid var(--gray-200);
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -3px; right: 0;
        width: 80px; height: 3px;
        background: var(--gold);
    }
    
    .table-container {
        background: var(--white);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin: 30px 0;
        border: 1px solid var(--gray-200);
    }
    
    table { width: 100%; border-collapse: collapse; }
    
    thead { background: linear-gradient(135deg, var(--navy), var(--navy-dark)); }
    
    th {
        padding: 20px;
        color: var(--gold-light);
        font-weight: 700;
        text-align: center;
    }
    
    td {
        padding: 18px 20px;
        text-align: center;
        border-bottom: 1px solid var(--gray-100);
    }
    
    tbody tr:hover { background: rgba(212, 175, 55, 0.05); }
    
    .highlight-gold { background: #fef3c7 !important; color: #92400e; font-weight: 700; }
    .highlight-blue { background: #dbeafe !important; color: #1e40af; font-weight: 700; }
    .highlight-green { background: #dcfce7 !important; color: #166534; font-weight: 700; }
    .highlight-red { background: #fee2e2 !important; color: #991b1b; font-weight: 700; }
    
    .analysis-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 25px;
        margin: 30px 0;
    }
    
    .analysis-card {
        background: linear-gradient(145deg, var(--white), var(--gray-100));
        border-radius: 20px;
        padding: 30px;
        border: 1px solid var(--gray-200);
        transition: all 0.4s ease;
        border-top: 5px solid var(--card-color, var(--gold));
    }
    
    .analysis-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0, 31, 63, 0.12);
    }
    
    .analysis-card h4 {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--navy);
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px dashed var(--gray-200);
    }
    
    .analysis-card p { color: #475569; line-height: 1.9; }
    
    .analysis-card.red { --card-color: #ef4444; }
    .analysis-card.blue { --card-color: #3b82f6; }
    .analysis-card.green { --card-color: #22c55e; }
    
    .recommendations-section {
        background: var(--gray-100);
        border-radius: 24px;
        padding: 40px;
        margin-top: 50px;
        border: 2px solid var(--navy);
    }
    
    .recommendations-section h2 {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--navy);
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 3px solid var(--gold);
    }
    
    .recommendations-list {
        list-style: none;
        counter-reset: rec;
        padding: 0;
    }
    
    .recommendations-list li {
        position: relative;
        padding: 20px 30px 20px 80px;
        margin-bottom: 15px;
        background: var(--white);
        border-radius: 16px;
        border: 1px solid var(--gray-200);
        counter-increment: rec;
        transition: all 0.3s ease;
    }
    
    .recommendations-list li::before {
        content: counter(rec);
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        width: 45px; height: 45px;
        background: var(--navy);
        color: var(--gold);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }
    
    .recommendations-list li:hover {
        transform: translateX(-10px);
        border-color: var(--gold);
    }
    
    footer {
        background: linear-gradient(135deg, var(--navy), var(--navy-dark));
        padding: 40px;
        text-align: center;
    }
    
    footer::before {
        content: '';
        display: block;
        height: 4px;
        background: var(--gold);
        margin-bottom: 30px;
    }
    
    footer .org-name { font-size: 1.3rem; font-weight: 700; color: var(--gold); margin-bottom: 10px; }
    footer .dept-name { font-size: 1.1rem; color: var(--gold-light); }
    
    @media (max-width: 768px) {
        header { padding: 40px 25px; }
        header h1 { font-size: 2rem; }
        .content { padding: 30px 20px; }
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
'''

STYLE_DIGITAL = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary: #0ea5e9;
        --secondary: #8b5cf6;
        --accent: #f59e0b;
        --success: #22c55e;
        --danger: #ef4444;
        --dark: #0f172a;
        --white: #ffffff;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(180deg, var(--dark) 0%, #1a1a2e 100%);
        color: var(--white);
        direction: rtl;
        padding: 30px;
    }
    
    .dashboard { max-width: 1400px; margin: 0 auto; }
    
    .dashboard-header {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(139, 92, 246, 0.15));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 30px;
        backdrop-filter: blur(20px);
    }
    
    .dashboard-header h1 {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #7dd3fc, var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .dashboard-header .subtitle { color: #cbd5e1; font-size: 1.1rem; }
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
        transition: all 0.4s ease;
        border-top: 4px solid var(--kpi-color, var(--primary));
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card .icon {
        width: 55px; height: 55px;
        background: var(--kpi-color, var(--primary));
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 20px;
    }
    
    .kpi-card .label {
        color: #64748b;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .kpi-card .value {
        font-size: 2.8rem;
        font-weight: 900;
        color: var(--white);
    }
    
    .kpi-card.blue { --kpi-color: var(--primary); }
    .kpi-card.purple { --kpi-color: var(--secondary); }
    .kpi-card.amber { --kpi-color: var(--accent); }
    .kpi-card.green { --kpi-color: var(--success); }
    .kpi-card.red { --kpi-color: var(--danger); }
    
    .table-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 30px;
    }
    
    .table-card .card-header {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(139, 92, 246, 0.2));
        padding: 20px 25px;
    }
    
    .table-card .card-header h3 {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--white);
    }
    
    table { width: 100%; border-collapse: collapse; }
    
    thead { background: rgba(0, 0, 0, 0.3); }
    
    th {
        padding: 18px 20px;
        color: #7dd3fc;
        font-weight: 700;
        text-align: center;
    }
    
    td {
        padding: 16px 20px;
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #cbd5e1;
    }
    
    tbody tr:hover { background: rgba(14, 165, 233, 0.1); }
    
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    .badge.success { background: rgba(34, 197, 94, 0.2); color: var(--success); }
    .badge.danger { background: rgba(239, 68, 68, 0.2); color: var(--danger); }
    .badge.warning { background: rgba(245, 158, 11, 0.2); color: var(--accent); }
    
    .analysis-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 25px;
        margin-bottom: 30px;
    }
    
    .analysis-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        transition: all 0.4s ease;
    }
    
    .analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    .analysis-card h4 {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--white);
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .analysis-card p { color: #cbd5e1; line-height: 1.9; }
    
    .recommendations-card {
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 24px;
        padding: 40px;
    }
    
    .recommendations-card h2 {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--accent);
        margin-bottom: 30px;
    }
    
    .rec-list { list-style: none; padding: 0; counter-reset: rec; }
    
    .rec-list li {
        position: relative;
        padding: 20px 25px 20px 70px;
        margin-bottom: 15px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 14px;
        color: #cbd5e1;
        counter-increment: rec;
        transition: all 0.3s ease;
    }
    
    .rec-list li::before {
        content: counter(rec);
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        width: 40px; height: 40px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }
    
    .rec-list li:hover {
        background: rgba(14, 165, 233, 0.1);
        transform: translateX(-10px);
    }
    
    footer {
        text-align: center;
        padding: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    footer .org {
        font-size: 1.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #7dd3fc, var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    footer .dept { color: #64748b; margin-top: 5px; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
'''

STYLE_ANALYTICAL = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary: #4f46e5;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #111827;
        --white: #ffffff;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: #f3f4f6;
        color: var(--dark);
        direction: rtl;
        padding: 40px 30px;
    }
    
    .report { max-width: 1300px; margin: 0 auto; }
    
    .report-header {
        background: linear-gradient(135deg, var(--primary), #3730a3);
        border-radius: 24px;
        padding: 50px;
        margin-bottom: 35px;
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.3);
    }
    
    .report-header h1 {
        font-size: 2.6rem;
        font-weight: 900;
        color: var(--white);
        margin-bottom: 15px;
    }
    
    .report-header .subtitle { color: rgba(255, 255, 255, 0.8); font-size: 1.15rem; }
    
    .stats-overview {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 35px;
    }
    
    .stat-box {
        background: var(--white);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border-top: 4px solid var(--stat-color, var(--primary));
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
    }
    
    .stat-box .value {
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--stat-color, var(--primary));
    }
    
    .stat-box .label { color: #6b7280; font-size: 0.9rem; }
    
    .stat-box.primary { --stat-color: var(--primary); }
    .stat-box.accent { --stat-color: var(--accent); }
    .stat-box.success { --stat-color: var(--success); }
    .stat-box.warning { --stat-color: var(--warning); }
    .stat-box.danger { --stat-color: var(--danger); }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--dark);
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .section-title .icon {
        width: 45px; height: 45px;
        background: var(--primary);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--white);
    }
    
    .tier-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 35px;
    }
    
    .tier-card {
        background: var(--white);
        border-radius: 16px;
        padding: 25px;
        border-top: 6px solid var(--tier-color, var(--primary));
        transition: all 0.3s ease;
    }
    
    .tier-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
    }
    
    .tier-card h4 {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .tier-card .tier-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        background: var(--tier-color, var(--primary));
        color: var(--white);
    }
    
    .tier-card .stats-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .tier-card .progress-bar {
        height: 10px;
        background: #e5e7eb;
        border-radius: 10px;
        margin-top: 15px;
        overflow: hidden;
    }
    
    .tier-card .progress-fill {
        height: 100%;
        background: var(--tier-color, var(--primary));
        border-radius: 10px;
    }
    
    .tier-card.elite { --tier-color: #ef4444; }
    .tier-card.high { --tier-color: #f59e0b; }
    .tier-card.medium { --tier-color: #3b82f6; }
    .tier-card.low { --tier-color: #6b7280; }
    
    .data-table-container {
        background: var(--white);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin-bottom: 35px;
    }
    
    .table-header {
        background: linear-gradient(135deg, var(--primary), #3730a3);
        padding: 20px 25px;
    }
    
    .table-header h3 { color: var(--white); font-size: 1.2rem; font-weight: 700; }
    
    table { width: 100%; border-collapse: collapse; }
    
    th {
        padding: 16px 20px;
        color: #374151;
        font-weight: 700;
        background: #f9fafb;
        border-bottom: 2px solid #e5e7eb;
    }
    
    td {
        padding: 14px 20px;
        text-align: center;
        border-bottom: 1px solid #f3f4f6;
    }
    
    tbody tr:hover { background: #f9fafb; }
    
    .recommendations {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(6, 182, 212, 0.05));
        border: 2px solid var(--primary);
        border-radius: 24px;
        padding: 40px;
    }
    
    .recommendations h2 {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--primary);
        margin-bottom: 25px;
    }
    
    .rec-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 15px;
    }
    
    .rec-item {
        background: var(--white);
        border-radius: 14px;
        padding: 20px;
        display: flex;
        gap: 15px;
        transition: all 0.3s ease;
    }
    
    .rec-item:hover {
        transform: translateX(-5px);
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.1);
    }
    
    .rec-item .num {
        width: 40px; height: 40px;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--white);
        font-weight: 800;
        flex-shrink: 0;
    }
    
    .rec-item .text { color: #374151; line-height: 1.6; }
    
    footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 30px;
        border-top: 2px solid #e5e7eb;
    }
    
    footer .org { font-size: 1.2rem; font-weight: 700; color: var(--primary); }
    footer .dept { color: #6b7280; margin-top: 5px; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
'''

STYLE_PRESENTATION = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800;900&display=swap');
    
    :root {
        --navy: #0a1628;
        --gold: #d4af37;
        --gold-light: #f0d875;
        --white: #ffffff;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Cairo', sans-serif;
        background: var(--navy);
        overflow: hidden;
        height: 100vh;
        width: 100vw;
        direction: rtl;
    }
    
    .presentation {
        width: 100%; height: 100%;
        background: radial-gradient(ellipse at top, #162033, var(--navy));
    }
    
    .slide {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        opacity: 0;
        visibility: hidden;
        transform: scale(0.95);
        transition: all 0.6s ease;
        display: flex;
        flex-direction: column;
        padding: 50px 70px;
    }
    
    .slide.active {
        opacity: 1;
        visibility: visible;
        transform: scale(1);
        z-index: 10;
    }
    
    .slide.cover {
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    .cover-content {
        padding: 80px 100px;
        border: 3px solid var(--gold);
        background: rgba(0, 0, 0, 0.4);
    }
    
    .cover-content h1 {
        font-size: 3.5rem;
        font-weight: 900;
        color: var(--white);
        margin-bottom: 20px;
    }
    
    .cover-content h2 {
        font-size: 1.8rem;
        color: var(--gold);
        margin-bottom: 40px;
    }
    
    .slide-header {
        display: flex;
        justify-content: space-between;
        padding-bottom: 20px;
        border-bottom: 2px solid rgba(212, 175, 55, 0.3);
        margin-bottom: 30px;
    }
    
    .slide-header h2 { font-size: 2rem; font-weight: 800; color: var(--gold); }
    
    .slide-content {
        flex: 1;
        display: flex;
        gap: 40px;
    }
    
    .text-panel {
        flex: 3;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 35px;
        color: var(--navy);
        overflow-y: auto;
        border-right: 6px solid var(--gold);
    }
    
    .text-panel h3 {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        border-bottom: 2px dashed #e5e7eb;
        padding-bottom: 10px;
    }
    
    .text-panel p { font-size: 1.15rem; line-height: 2; margin-bottom: 20px; }
    
    .visual-panel {
        flex: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: var(--white);
    }
    
    .visual-panel .icon-box {
        font-size: 6rem;
        color: var(--gold);
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    .nav-controls {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 15px;
    }
    
    .nav-btn {
        width: 55px; height: 55px;
        border: 2px solid var(--gold);
        background: transparent;
        color: var(--gold);
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .nav-btn:hover {
        background: var(--gold);
        color: var(--navy);
    }
    
    .page-number {
        position: absolute;
        bottom: 40px; right: 70px;
        color: var(--gold);
        font-weight: 700;
    }
    
    .signature-box {
        margin-top: auto;
        padding-top: 20px;
        border-top: 1px solid rgba(212, 175, 55, 0.3);
        text-align: center;
    }
    
    .signature-box .org { color: var(--gold); font-weight: 700; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
'''

STYLE_EXECUTIVE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    :root {
        --black: #000000;
        --white: #ffffff;
        --gold: #c9a227;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Tajawal', sans-serif;
        background: var(--white);
        color: #111;
        direction: rtl;
    }
    
    .executive-report {
        max-width: 900px;
        margin: 0 auto;
        padding: 60px 50px;
    }
    
    .report-header {
        display: flex;
        justify-content: space-between;
        padding-bottom: 30px;
        border-bottom: 4px solid var(--black);
        margin-bottom: 50px;
    }
    
    .brand {
        font-size: 1.1rem;
        font-weight: 800;
        color: var(--gold);
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .title-section h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 800;
        color: var(--black);
        margin-bottom: 20px;
    }
    
    .title-section .subtitle {
        font-size: 1.3rem;
        color: #666;
    }
    
    .exec-summary {
        background: #f5f5f5;
        padding: 40px;
        margin-bottom: 50px;
        border-right: 6px solid var(--gold);
    }
    
    .exec-summary p {
        font-size: 1.25rem;
        line-height: 2;
        color: #333;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        margin-bottom: 50px;
    }
    
    .metric-box {
        padding: 30px;
        border: 1px solid #f5f5f5;
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        border-color: var(--gold);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
    }
    
    .metric-box .value {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 800;
        color: var(--black);
    }
    
    .metric-box .label {
        font-size: 0.95rem;
        color: #666;
        text-transform: uppercase;
    }
    
    .section-title {
        font-size: 0.9rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: var(--gold);
        margin-bottom: 20px;
        border-bottom: 1px solid #f5f5f5;
        padding-bottom: 10px;
    }
    
    .key-points { list-style: none; padding: 0; }
    
    .key-points li {
        padding: 20px 0;
        border-bottom: 1px solid #f5f5f5;
        display: flex;
        gap: 20px;
    }
    
    .key-points .num {
        width: 35px; height: 35px;
        background: var(--black);
        color: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }
    
    .key-points .text { color: #333; line-height: 1.8; }
    
    .highlight-box {
        background: var(--black);
        color: var(--white);
        padding: 40px;
        margin: 40px 0;
    }
    
    .highlight-box::before {
        content: '';
        display: block;
        width: 6px;
        height: 100%;
        background: var(--gold);
        position: absolute;
        right: 0;
    }
    
    .highlight-box h4 {
        color: var(--gold);
        margin-bottom: 15px;
    }
    
    footer {
        margin-top: 80px;
        padding-top: 30px;
        border-top: 4px solid var(--black);
        display: flex;
        justify-content: space-between;
    }
    
    footer .org-info .name { font-weight: 700; }
    footer .org-info .dept { color: #666; font-size: 0.9rem; }
</style>
'''

SCRIPT_PRESENTATION = '''
<script>
    let currentSlideIndex = 1;
    function updateSlide() {
        const slides = document.querySelectorAll('.slide');
        slides.forEach(slide => slide.classList.remove('active'));
        const activeSlide = document.getElementById('slide-' + currentSlideIndex);
        if(activeSlide) activeSlide.classList.add('active');
        const pageNum = document.getElementById('page-num');
        if(pageNum) pageNum.innerText = currentSlideIndex + ' / ' + slides.length;
    }
    function nextSlide() { 
        const total = document.querySelectorAll('.slide').length;
        if (currentSlideIndex < total) { currentSlideIndex++; updateSlide(); } 
    }
    function prevSlide() { 
        if (currentSlideIndex > 1) { currentSlideIndex--; updateSlide(); } 
    }
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') nextSlide();
        else if (e.key === 'ArrowRight') prevSlide();
    });
    setTimeout(updateSlide, 100);
</script>
'''

# ---------------------------------------------------------
# 🛠️ دوال المساعدة
# ---------------------------------------------------------

def extract_text_from_file(uploaded_file):
    text_content = ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
        elif "spreadsheet" in uploaded_file.type:
            df = pd.read_excel(uploaded_file)
            text_content = df.to_string()
        else:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text_content = stringio.read()
    except Exception as e:
        return f"خطأ: {e}"
    return text_content

def clean_html_response(text):
    return text.replace("```html", "").replace("```", "").strip()

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and "flash" in m.name:
                return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

def analyze_content_type(text):
    """تحليل نوع المحتوى لتحديد التصميم المناسب"""
    analysis = {'type': 'general', 'has_numbers': False, 'has_percentages': False}
    
    numbers = re.findall(r'\d{1,3}(?:,\d{3})*', text)
    analysis['has_numbers'] = len(numbers) > 5
    
    percentages = re.findall(r'\d+(?:\.\d+)?%', text)
    analysis['has_percentages'] = len(percentages) > 3
    
    if analysis['has_numbers'] and analysis['has_percentages']:
        analysis['type'] = 'statistical'
    elif bool(re.search(r'(توصية|توصيات|يوصى|يجب)', text)):
        analysis['type'] = 'recommendations'
    elif bool(re.search(r'(مقارنة|مقابل|ضد)', text)):
        analysis['type'] = 'comparison'
    
    return analysis

def get_dynamic_instructions(analysis):
    """تعليمات ديناميكية حسب نوع المحتوى"""
    if analysis['type'] == 'statistical':
        return """
        DYNAMIC: Use animated progress bars for percentages.
        Add gradient colors based on values (green=high, red=low).
        Create stat cards with large numbers and trend indicators.
        """
    elif analysis['type'] == 'recommendations':
        return """
        DYNAMIC: Use numbered cards with icons.
        Add priority indicators (high/medium/low).
        Create expandable sections.
        """
    elif analysis['type'] == 'comparison':
        return """
        DYNAMIC: Use side-by-side comparison layout.
        Add VS dividers between items.
        Use contrasting colors for each side.
        """
    return ""

# ---------------------------------------------------------
# 🏗️ الواجهة
# ---------------------------------------------------------

st.markdown('''
<div class="hero-section">
    <div class="main-title">تيار الحكمة الوطني</div>
    <div class="sub-title">الجهاز المركزي للجودة الشاملة | وحدة التخطيط الاستراتيجي</div>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="section-header">🎨 اختر نمط الإخراج</div>', unsafe_allow_html=True)

report_type = st.radio(
    "",
    ("🏛️ نمط الكتاب الرسمي", "📱 نمط الداشبورد الرقمي", "📊 نمط التحليل العميق", "📽️ عرض تقديمي تفاعلي", "✨ ملخص تنفيذي"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📝</div>
            <div>
                <div class="input-title">البيانات / الملاحظات</div>
                <div class="input-subtitle">أدخل النص أو الصق محتوى التقرير</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    user_text = st.text_area("", height=200, placeholder="اكتب هنا...", label_visibility="collapsed")

with col2:
    st.markdown('''
    <div class="input-card">
        <div class="input-header">
            <div class="input-icon">📎</div>
            <div>
                <div class="input-title">رفع الملفات</div>
                <div class="input-subtitle">PDF, XLSX, TXT</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['pdf', 'xlsx', 'txt'], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 بدء المعالجة وإنشاء التقرير"):
    
    if not API_KEY:
        st.error("⚠️ لم يتم العثور على مفتاح API")
        st.stop()
    
    full_text = user_text
    if uploaded_file:
        full_text += f"\n\n{extract_text_from_file(uploaded_file)}"

    if not full_text.strip():
        st.warning("⚠️ الرجاء إدخال بيانات")
    else:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(get_working_model())
            
            # تحليل المحتوى
            analysis = analyze_content_type(full_text)
            dynamic_inst = get_dynamic_instructions(analysis)

            # تحديد القالب
            if "الرسمي" in report_type:
                css = STYLE_OFFICIAL
                label = "Official_Report"
                struct = """Use: container > header(h1,h2) > content > stats-grid(stat-card) > section-title > table-container > analysis-grid(analysis-card) > recommendations-section > footer"""
            elif "الرقمي" in report_type:
                css = STYLE_DIGITAL
                label = "Digital_Dashboard"
                struct = """Use: dashboard > dashboard-header(h1,subtitle) > kpi-grid(kpi-card blue/purple/green) > table-card > analysis-grid > recommendations-card(rec-list) > footer"""
            elif "التحليل" in report_type:
                css = STYLE_ANALYTICAL
                label = "Deep_Analysis"
                struct = """Use: report > report-header > stats-overview(stat-box) > tier-grid(tier-card elite/high/medium) > data-table-container > recommendations(rec-grid > rec-item) > footer"""
            elif "عرض" in report_type:
                css = STYLE_PRESENTATION
                label = "Presentation"
                struct = """Use: presentation > slide.cover.active#slide-1 > slide#slide-2,3... Each has slide-header + slide-content(text-panel + visual-panel). Add nav-controls and page-number."""
            else:
                css = STYLE_EXECUTIVE
                label = "Executive_Summary"
                struct = """Use: executive-report > report-header(brand) > title-section(h1,subtitle) > exec-summary > metrics-grid(metric-box) > key-points > highlight-box > footer"""

            # البرومبت
            prompt = f"""
            أنت خبير تصميم تقارير HTML احترافية.
            
            المطلوب: إنشاء تقرير HTML كامل ومفصل من البيانات التالية.
            
            التعليمات:
            1. استخدم كل البيانات بالتفصيل - لا تختصر
            2. {dynamic_inst}
            3. البنية: {struct}
            4. أخرج HTML فقط (بدون ```html)
            5. استخدم أيقونات Font Awesome
            6. أضف classes الألوان المناسبة (blue, green, red, amber, purple)
            7. التوقيع: الجهاز المركزي للجودة الشاملة - وحدة التخطيط الاستراتيجي
            
            البيانات:
            {full_text}
            """

            # شريط التقدم
            progress = st.empty()
            for i in range(0, 101, 10):
                progress.markdown(f'''
                <div style="background:rgba(0,31,63,0.9);border-radius:15px;padding:30px;margin:20px;text-align:center;border:1px solid rgba(255,215,0,0.3);">
                    <div style="font-size:2rem;margin-bottom:15px;">🤖</div>
                    <div style="background:rgba(255,255,255,0.1);border-radius:10px;height:12px;overflow:hidden;margin:20px 0;">
                        <div style="height:100%;width:{i}%;background:linear-gradient(90deg,#FFD700,#FFA500);border-radius:10px;"></div>
                    </div>
                    <div style="color:rgba(255,255,255,0.8);">جاري التحليل... {i}%</div>
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(0.05)
            
            response = model.generate_content(prompt)
            html_body = clean_html_response(response.text)
            
            progress.empty()
            
            # بناء HTML النهائي
            wrapper = "presentation" if "عرض" in report_type else "container"
            script = SCRIPT_PRESENTATION if "عرض" in report_type else ""
            
            final_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير {label}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;800&family=Tajawal:wght@400;700;900&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
    {css}
</head>
<body>
    {html_body}
    {script}
</body>
</html>"""

            st.markdown('<div class="success-banner"><span>✅ تم إنشاء التقرير بنجاح!</span></div>', unsafe_allow_html=True)
            
            st.components.v1.html(final_html, height=850, scrolling=True)
            
            st.download_button(
                label="📥 تحميل التقرير (HTML)",
                data=final_html,
                file_name=f"{label}.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ خطأ: {e}")

# الفوتر
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''
<div style="background:linear-gradient(135deg,rgba(0,31,63,0.95),rgba(10,46,92,0.9));border-radius:15px;padding:30px;margin:20px;text-align:center;border:1px solid rgba(255,215,0,0.3);">
    <p style="color:#FFD700;font-size:1.1rem;font-weight:700;margin-bottom:8px;">الجهاز المركزي للجودة الشاملة</p>
    <p style="color:rgba(255,255,255,0.8);font-size:1rem;">وحدة التخطيط الاستراتيجي والتطوير</p>
    <p style="color:rgba(255,255,255,0.5);font-size:0.85rem;margin-top:15px;">جميع الحقوق محفوظة © 2026</p>
</div>
''', unsafe_allow_html=True)
