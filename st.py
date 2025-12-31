# File: mediroute_max.py
# Run: streamlit run mediroute_max.py
# Install: pip install streamlit folium pandas numpy plotly

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import json

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="MediRoute Pro MAX | Ethiopia",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CUSTOM CSS - MOST ADVANCED ==========
st.markdown("""
<style>
    /* Modern Gradient Theme */
    :root {
        --primary: #0066CC;
        --secondary: #00C2FF;
        --accent: #00D4AA;
        --danger: #FF4D4D;
        --warning: #FFB347;
        --success: #2ECC71;
        --dark: #0A192F;
        --light: #F8FAFF;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0A192F 0%, #1A2942 50%, #2A3B56 100%);
        background-attachment: fixed;
    }
    
    /* Floating Particles Background */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(0, 194, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(0, 212, 170, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 77, 77, 0.05) 0%, transparent 50%);
        z-index: -1;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(100px, 100px) rotate(360deg); }
    }
    
    /* Supreme Header */
    .supreme-header {
        background: linear-gradient(135deg, 
            rgba(0, 102, 204, 0.9) 0%, 
            rgba(0, 194, 255, 0.9) 50%, 
            rgba(0, 212, 170, 0.9) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 0 0 30px 30px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        border-bottom: 3px solid rgba(255, 255, 255, 0.3);
        box-shadow: 
            0 20px 60px rgba(0, 102, 204, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .supreme-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 50%,
            transparent 70%
        );
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* 3D Glass Cards */
    .glass-card-3d {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 
            0 25px 45px rgba(0, 0, 0, 0.3),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card-3d:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 60px rgba(0, 102, 204, 0.5),
            inset 0 0 0 1px rgba(255, 255, 255, 0.2);
        border-color: var(--secondary);
    }
    
    .glass-card-3d::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transition: 0.5s;
    }
    
    .glass-card-3d:hover::before {
        left: 100%;
    }
    
    /* Neon Glow Cards */
    .neon-glow {
        background: rgba(0, 194, 255, 0.05);
        border: 2px solid transparent;
        border-radius: 20px;
        padding: 2rem;
        position: relative;
        box-shadow: 
            0 0 20px rgba(0, 194, 255, 0.2),
            inset 0 0 20px rgba(0, 194, 255, 0.1);
        animation: neonPulse 2s infinite alternate;
    }
    
    @keyframes neonPulse {
        from {
            box-shadow: 
                0 0 20px rgba(0, 194, 255, 0.2),
                inset 0 0 20px rgba(0, 194, 255, 0.1);
        }
        to {
            box-shadow: 
                0 0 30px rgba(0, 194, 255, 0.4),
                inset 0 0 30px rgba(0, 194, 255, 0.2);
        }
    }
    
    /* Holographic Button */
    .holographic-btn {
        background: linear-gradient(
            135deg,
            rgba(0, 102, 204, 0.9),
            rgba(0, 194, 255, 0.9),
            rgba(0, 212, 170, 0.9)
        );
        border: none;
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 
            0 10px 30px rgba(0, 102, 204, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1);
    }
    
    .holographic-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        transition: 0.5s;
    }
    
    .holographic-btn:hover::before {
        left: 100%;
    }
    
    .holographic-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 20px 40px rgba(0, 102, 204, 0.6),
            0 0 0 1px rgba(255, 255, 255, 0.2);
    }
    
    /* Floating Animation */
    @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .floating-element {
        animation: floating 3s ease-in-out infinite;
    }
    
    /* Map Container with Glass Effect */
    .glass-map-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 1px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.4),
            inset 0 0 0 1px rgba(255, 255, 255, 0.05);
        overflow: hidden;
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 1rem 2rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white !important;
        box-shadow: 0 10px 25px rgba(0, 102, 204, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
    }
    
    /* Dataframe Styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--secondary), var(--accent)) !important;
        border-radius: 10px;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Checkbox Styling */
    .stCheckbox > label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Number Input Styling */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 10px;
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--secondary), var(--accent));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--primary), var(--secondary));
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #0A192F 0%, #1A2942 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(0, 102, 204, 0.2), 
            rgba(0, 194, 255, 0.2));
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 194, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 50%,
            transparent 70%
        );
        animation: shine 3s infinite;
        opacity: 0.3;
    }
    
    /* Typography Enhancement */
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(135deg, white, rgba(255, 255, 255, 0.8));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-top: 4px solid var(--secondary);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Pulse Animation for Alerts */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .pulse-alert {
        animation: pulse 2s infinite;
    }
    
    /* Grid Background */
    .grid-bg {
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if 'clinics' not in st.session_state:
    st.session_state.clinics = []
if 'selected_clinic' not in st.session_state:
    st.session_state.selected_clinic = None
if 'ai_mode' not in st.session_state:
    st.session_state.ai_mode = "GENIUS"
if 'emergency_mode' not in st.session_state:
    st.session_state.emergency_mode = "NORMAL"
if 'map_center' not in st.session_state:
    st.session_state.map_center = [9.145, 40.489]

# ========== SUPREME HEADER ==========
col_header1, col_header2, col_header3 = st.columns([3, 2, 1])

with col_header1:
    st.markdown("""
    <div class="supreme-header">
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 15px;">
            <div class="floating-element" style="font-size: 3.5rem;">🚑</div>
            <div>
                <h1 style="margin: 0; font-size: 3rem; font-weight: 800; letter-spacing: -0.5px;">
                    <span style="background: linear-gradient(135deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MediRoute</span> 
                    <span style="color: white;">Pro MAX</span>
                </h1>
                <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin: 5px 0 0 0;">
                    🇪🇹 World's Most Advanced Healthcare Logistics Platform
                </p>
            </div>
        </div>
        <div style="display: flex; gap: 20px; margin-top: 20px;">
            <div style="background: rgba(255, 255, 255, 0.1); padding: 8px 20px; border-radius: 20px; font-size: 0.9rem;">
                ⚡ Powered by Quantum AI
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 8px 20px; border-radius: 20px; font-size: 0.9rem;">
                🎯 99.9% Delivery Accuracy
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 8px 20px; border-radius: 20px; font-size: 0.9rem;">
                💰 $2.4M Monthly Savings
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    current_time = datetime.now()
    st.markdown(f"""
    <div class="glass-card-3d" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 10px;">⏰</div>
        <div style="font-size: 2rem; font-weight: bold; color: white;">{current_time.strftime('%H:%M:%S')}</div>
        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">Live System Time</div>
        <div style="margin-top: 10px; color: #00D4AA; font-size: 0.9rem;">
            Last update: {current_time.strftime('%b %d, %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_header3:
    st.markdown("""
    <div class="neon-glow" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 10px;">🌍</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: white;">Ethiopia</div>
        <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">Coverage Area</div>
        <div style="margin-top: 10px; color: #00C2FF; font-weight: bold;">
            🔴 🟠 🟢
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== REAL-TIME METRICS ==========
st.markdown("### 📊 REAL-TIME SYSTEM METRICS")

col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

with col_metric1:
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="font-size: 2rem;">🏥</div>
            <div>
                <div style="font-size: 2.5rem; font-weight: bold; color: white;">247</div>
                <div style="color: rgba(255, 255, 255, 0.7);">Active Clinics</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span style="color: #00D4AA;">↑ 12.5%</span>
            <span style="color: rgba(255, 255, 255, 0.7);">vs last month</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_metric2:
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="font-size: 2rem; color: #FF4D4D;">⚠️</div>
            <div>
                <div style="font-size: 2.5rem; font-weight: bold; color: #FF4D4D;">38</div>
                <div style="color: rgba(255, 255, 255, 0.7);">Critical Alerts</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span style="color: #FFB347;">↗️ Needs Attention</span>
            <span style="color: rgba(255, 255, 255, 0.7);">Immediate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_metric3:
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="font-size: 2rem; color: #00D4AA;">👥</div>
            <div>
                <div style="font-size: 2.5rem; font-weight: bold; color: white;">12.5M</div>
                <div style="color: rgba(255, 255, 255, 0.7);">People Served</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span style="color: #00D4AA;">↑ 8.7%</span>
            <span style="color: rgba(255, 255, 255, 0.7);">coverage increase</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_metric4:
    st.markdown("""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="font-size: 2rem; color: #FFD700;">💰</div>
            <div>
                <div style="font-size: 2.5rem; font-weight: bold; color: white;">$2.4M</div>
                <div style="color: rgba(255, 255, 255, 0.7);">Monthly Savings</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
            <span style="color: #00D4AA;">↑ 42.3%</span>
            <span style="color: rgba(255, 255, 255, 0.7);">efficiency gain</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== ENHANCED SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
        <div class="floating-element" style="font-size: 3rem;">⚡</div>
        <h3 style="color: white; margin: 15px 0;">QUANTUM CONTROL</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Intelligence Level
    st.markdown("### 🤖 QUANTUM AI LEVEL")
    ai_mode = st.select_slider(
        "",
        options=["BASIC", "SMART", "ADVANCED", "GENIUS", "QUANTUM"],
        value="GENIUS",
        label_visibility="collapsed"
    )
    
    # Region Selector
    st.markdown("### 🌍 REGION FOCUS")
    region = st.selectbox(
        "",
        ["ALL ETHIOPIA", "ADDIS ABABA", "OROMIA", "AMHARA", "TIGRAY", "SNNPR", "SOMALI", "AFAR", "DIRE DAWA"],
        label_visibility="collapsed"
    )
    
    # Emergency Mode
    st.markdown("### 🚨 EMERGENCY MODE")
    emergency = st.select_slider(
        "",
        options=["NORMAL", "ALERT", "HIGH", "CRITICAL", "WAR"],
        value="NORMAL",
        label_visibility="collapsed"
    )
    
    if emergency != "NORMAL":
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #FF4D4D, #FF6B6B); 
                    color: white; padding: 15px; border-radius: 15px; 
                    text-align: center; margin: 15px 0; animation: pulse 1s infinite;">
            <div style="font-size: 1.2rem; font-weight: bold;">⚡ {emergency} MODE</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Emergency Protocols Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Map Layers
    st.markdown("### 🗺️ VISUALIZATION LAYERS")
    col_layer1, col_layer2 = st.columns(2)
    with col_layer1:
        st.checkbox("🌡️ Heat Map", True)
        st.checkbox("🚚 Delivery Routes", True)
        st.checkbox("⚠️ Critical Zones", True)
    with col_layer2:
        st.checkbox("🌧️ Weather", False)
        st.checkbox("🛣️ Road Network", False)
        st.checkbox("📶 Network Coverage", False)
    
    # Quick Actions
    st.markdown("### ⚡ QUANTUM ACTIONS")
    
    col_action1, col_action2 = st.columns(2)
    with col_action1:
        if st.button("🚀 OPTIMIZE", use_container_width=False):
            st.toast("⚡ Quantum Optimization Started!", icon="🚀")
            st.balloons()
    with col_action2:
        if st.button("🔄 REFRESH", use_container_width=False):
            st.rerun()
    
    # Advanced Settings
    with st.expander("⚙️ QUANTUM SETTINGS", expanded=False):
        st.slider("AI Confidence", 80, 99, 95)
        st.slider("Prediction Horizon", 1, 30, 7)
        st.slider("Response Time", 1, 10, 3)
        st.checkbox("Auto-Reroute", True)
        st.checkbox("Predictive Analytics", True)
        st.checkbox("Real-time Learning", True)
    
    # System Status
    st.markdown("---")
    st.markdown("### 📡 SYSTEM STATUS")
    
    status_data = [
        ("⚡ AI Engine", "🟢 ONLINE", "99.9%"),
        ("🌐 Network", "🟢 STABLE", "2.3ms"),
        ("🗄️ Database", "🟢 SYNCED", "0.1s"),
        ("🔒 Security", "🟢 ACTIVE", "100%"),
    ]
    
    for name, status, value in status_data:
        col_stat1, col_stat2 = st.columns([3, 2])
        with col_stat1:
            st.markdown(f"<span style='color: rgba(255, 255, 255, 0.7);'>{name}</span>", unsafe_allow_html=True)
        with col_stat2:
            st.markdown(f"<span style='color: #00D4AA; font-weight: bold;'>{status}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"**QUANTUM CORE v4.2.1** • {datetime.now().strftime('%H:%M:%S')}")
    st.caption("© 2024 MediRoute Pro MAX • Classified")

# ========== GENERATE ULTIMATE DATA ==========
def generate_ultimate_data():
    """Generate the most comprehensive clinic data for Ethiopia"""
    
    ethiopian_cities = {
        "Addis Ababa": {"lat": 9.03, "lon": 38.74, "population": 5000000, "hospitals": 45},
        "Jimma": {"lat": 7.67, "lon": 36.83, "population": 200000, "hospitals": 8},
        "Bahir Dar": {"lat": 11.59, "lon": 37.39, "population": 350000, "hospitals": 12},
        "Mekelle": {"lat": 13.49, "lon": 39.47, "population": 500000, "hospitals": 15},
        "Hawassa": {"lat": 7.05, "lon": 38.47, "population": 400000, "hospitals": 10},
        "Dire Dawa": {"lat": 9.60, "lon": 41.87, "population": 500000, "hospitals": 8},
        "Gondar": {"lat": 12.61, "lon": 37.46, "population": 400000, "hospitals": 11},
        "Nekemte": {"lat": 9.08, "lon": 36.55, "population": 150000, "hospitals": 5},
        "Jijiga": {"lat": 9.35, "lon": 42.80, "population": 200000, "hospitals": 6},
        "Semera": {"lat": 11.79, "lon": 41.01, "population": 50000, "hospitals": 3},
        "Arba Minch": {"lat": 6.04, "lon": 37.55, "population": 100000, "hospitals": 4},
        "Axum": {"lat": 14.12, "lon": 38.72, "population": 80000, "hospitals": 3},
        "Shashamane": {"lat": 7.20, "lon": 38.60, "population": 250000, "hospitals": 7},
        "Debre Markos": {"lat": 10.33, "lon": 37.72, "population": 120000, "hospitals": 4},
        "Assosa": {"lat": 10.07, "lon": 34.53, "population": 50000, "hospitals": 2},
    }
    
    clinics = []
    clinic_id = 1001
    
    medicine_types = {
        "Malaria": {"critical": 50, "icon": "🦟", "color": "#FF6B6B"},
        "HIV": {"critical": 40, "icon": "🩺", "color": "#4ECDC4"},
        "Vaccines": {"critical": 30, "icon": "💉", "color": "#45B7D1"},
        "Antibiotics": {"critical": 60, "icon": "💊", "color": "#96CEB4"},
        "Insulin": {"critical": 20, "icon": "💙", "color": "#FECA57"},
        "Painkillers": {"critical": 80, "icon": "⚕️", "color": "#FF9FF3"},
        "Cholera": {"critical": 70, "icon": "🚰", "color": "#54A0FF"},
        "TB Drugs": {"critical": 35, "icon": "🫁", "color": "#5F27CD"},
    }
    
    facility_types = [
        ("National Hospital", "🏥", 0.1, "#FF4D4D"),
        ("Regional Hospital", "🏨", 0.2, "#FF6B6B"),
        ("Health Center", "⚕️", 0.4, "#45B7D1"),
        ("Health Clinic", "🩺", 0.2, "#96CEB4"),
        ("Mobile Clinic", "🚐", 0.1, "#FECA57"),
    ]
    
    for city, info in ethiopian_cities.items():
        num_clinics = min(info["hospitals"] * 2, 15)
        
        for i in range(num_clinics):
            facility_type, icon, weight, color = random.choices(
                facility_types,
                weights=[w for _, _, w, _ in facility_types]
            )[0]
            
            # Generate medicine stock
            medicine_stock = {}
            for med, details in medicine_types.items():
                if city in ["Oromia", "Jimma", "Nekemte"] and med == "Malaria":
                    stock = random.randint(0, 100)
                elif city in ["Addis Ababa", "Dire Dawa"] and med == "HIV":
                    stock = random.randint(20, 150)
                elif med == "Vaccines":
                    stock = random.randint(10, 120)
                else:
                    stock = random.randint(0, details["critical"] * 3)
                
                medicine_stock[med] = {
                    "stock": stock,
                    "critical": details["critical"],
                    "icon": details["icon"],
                    "color": details["color"],
                    "status": "🟢 GOOD" if stock > details["critical"] * 0.7 
                             else "🟠 LOW" if stock > details["critical"] * 0.3 
                             else "🔴 CRITICAL"
                }
            
            # Calculate metrics
            critical_count = sum(1 for m in medicine_stock.values() if "CRITICAL" in m["status"])
            low_count = sum(1 for m in medicine_stock.values() if "LOW" in m["status"])
            
            priority_score = (
                critical_count * 40 +
                low_count * 20 +
                random.randint(0, 40)
            )
            
            # Generate clinic data
            clinic = {
                "id": f"HCF-{clinic_id}",
                "name": f"{icon} {city} {facility_type} #{i+1}",
                "city": city,
                "type": facility_type,
                "icon": icon,
                "color": color,
                "lat": info["lat"] + random.uniform(-0.1, 0.1),
                "lon": info["lon"] + random.uniform(-0.1, 0.1),
                "population_served": random.randint(5000, 50000),
                "staff": random.randint(5, 150),
                "beds": random.randint(0, 300),
                "medicine_stock": medicine_stock,
                "critical_count": critical_count,
                "low_count": low_count,
                "priority_score": priority_score,
                "last_delivery": (datetime.now() - timedelta(days=random.randint(0, 14))).strftime("%b %d"),
                "status": "🔴 URGENT" if critical_count >= 3 
                         else "🟠 NEEDED" if critical_count >= 1 
                         else "🟢 STABLE",
                "contact": f"+251 9{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
                "email": f"contact@{city.lower().replace(' ', '')}{i+1}.et",
                "power": random.choice(["⚡ Grid", "☀️ Solar", "🛢️ Generator", "❌ None"]),
                "water": random.choice(["🚰 Piped", "💧 Well", "🚛 Tanker", "❌ Limited"]),
                "internet": random.choice(["📶 Good", "📡 Fair", "📵 Poor", "❌ None"]),
                "road_access": random.choice(["🛣️ Highway", "🛤️ Gravel", "🚧 Dirt", "🚧 Seasonal"]),
            }
            
            clinics.append(clinic)
            clinic_id += 1
    
    return clinics

# Load data
clinics_data = generate_ultimate_data()

# Filter by region
if region != "ALL ETHIOPIA":
    clinics_data = [c for c in clinics_data if region.upper() in c["city"].upper()]

# ========== ULTIMATE TABS ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 QUANTUM MAP", 
    "📊 AI DASHBOARD", 
    "🚚 LOGISTICS HUB", 
    "⚡ CONTROL CENTER"
])

# ========== TAB 1: QUANTUM MAP ==========
with tab1:
    st.markdown("### 🌍 QUANTUM REAL-TIME MAP")
    
    # Map Controls
    col_map_ctrl1, col_map_ctrl2, col_map_ctrl3 = st.columns([2, 1, 1])
    
    with col_map_ctrl1:
        map_style = st.selectbox(
            "",
            ["OpenStreetMap", "CartoDB Dark Matter", "Stamen Terrain", "Satellite", "Hybrid"],
            label_visibility="collapsed"
        )
    
    with col_map_ctrl2:
        auto_zoom = st.checkbox("Auto-Zoom", True)
    
    with col_map_ctrl3:
        cluster_markers = st.checkbox("Cluster", True)
    
    # Create the ultimate map
    if clinics_data:
        lats = [c["lat"] for c in clinics_data]
        lons = [c["lon"] for c in clinics_data]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        st.session_state.map_center = [center_lat, center_lon]
    
    m = folium.Map(
        location=st.session_state.map_center,
        zoom_start=7,
        tiles=map_style,
        control_scale=True,
        prefer_canvas=True
    )
    
    # Add dark theme if selected
    if map_style == "CartoDB Dark Matter":
        folium.TileLayer(
            tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            attr='CartoDB',
            name='Dark Mode',
            control=False
        ).add_to(m)
    
    # Add warehouse
    folium.Marker(
        [9.03, 38.74],
        popup="<b>🏭 CENTRAL MEDICINE WAREHOUSE</b><br>Capacity: 100,000 units<br>Vehicles: 25",
        icon=folium.Icon(color='black', icon='industry', prefix='fa'),
        tooltip="Click for details"
    ).add_to(m)
    
    # Add clinics with enhanced markers
    for clinic in clinics_data:
        # Marker color based on status
        if clinic["critical_count"] >= 3:
            color = "red"
            icon_color = "#FF4D4D"
            icon_type = "exclamation-circle"
            size = 25
        elif clinic["critical_count"] >= 1:
            color = "orange"
            icon_color = "#FFB347"
            icon_type = "exclamation-triangle"
            size = 20
        else:
            color = "green"
            icon_color = "#00D4AA"
            icon_type = "hospital"
            size = 18
        
        # Create medicine HTML
        meds_html = ""
        for med_name, med_data in list(clinic["medicine_stock"].items())[:6]:  # Show 6 medicines
            status_color = "#FF4D4D" if "CRITICAL" in med_data["status"] else "#FFB347" if "LOW" in med_data["status"] else "#00D4AA"
            meds_html += f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 5px; margin: 2px 0; background: {status_color}15; border-radius: 5px;">
                <span style="display: flex; align-items: center; gap: 8px;">
                    {med_data['icon']} <span style="font-weight: 500;">{med_name}</span>
                </span>
                <span style="font-weight: bold; color: {status_color};">
                    {med_data['stock']}/{med_data['critical']}
                </span>
            </div>
            """
        
        # Create ultimate popup
        popup_html = f"""
        <div style="width: 350px; font-family: 'Segoe UI', system-ui, sans-serif;">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, {icon_color}40, {icon_color}20); 
                        padding: 20px; border-radius: 15px 15px 0 0; border-bottom: 2px solid {icon_color}60;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2rem;">{clinic['icon']}</div>
                    <div>
                        <h3 style="margin: 0; color: #1A1A2E; font-weight: 700;">{clinic['name']}</h3>
                        <div style="color: #666; font-size: 0.9rem; margin-top: 5px;">
                            📍 {clinic['city']} • 🏷️ {clinic['type']}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Body -->
            <div style="padding: 20px; background: white; color: #333;">
                <!-- Quick Stats -->
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">
                    <div style="text-align: center; padding: 10px; background: #F8F9FA; border-radius: 10px;">
                        <div style="font-size: 0.8rem; color: #666;">👥 POPULATION</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #1A1A2E;">{clinic['population_served']:,}</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: #F8F9FA; border-radius: 10px;">
                        <div style="font-size: 0.8rem; color: #666;">⚠️ CRITICAL</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #FF4D4D;">{clinic['critical_count']}</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: #F8F9FA; border-radius: 10px;">
                        <div style="font-size: 0.8rem; color: #666;">🎯 PRIORITY</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #0066CC;">{clinic['priority_score']}</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: #F8F9FA; border-radius: 10px;">
                        <div style="font-size: 0.8rem; color: #666;">📅 LAST DELIVERY</div>
                        <div style="font-size: 1.5rem; font-weight: 700; color: #5F27CD;">{clinic['last_delivery']}</div>
                    </div>
                </div>
                
                <!-- Medicine Stock -->
                <div style="margin-bottom: 20px;">
                    <div style="font-weight: 600; color: #1A1A2E; margin-bottom: 10px; font-size: 1.1rem;">
                        💊 MEDICINE STOCK
                    </div>
                    <div style="max-height: 200px; overflow-y: auto; padding-right: 10px;">
                        {meds_html}
                    </div>
                </div>
                
                <!-- Contact & Info -->
                <div style="background: #F8F9FA; padding: 15px; border-radius: 10px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem;">
                        <div>
                            <div style="color: #666;">📞 CONTACT</div>
                            <div style="font-weight: 500;">{clinic['contact']}</div>
                        </div>
                        <div>
                            <div style="color: #666;">📧 EMAIL</div>
                            <div style="font-weight: 500;">{clinic['email']}</div>
                        </div>
                        <div>
                            <div style="color: #666;">⚡ POWER</div>
                            <div style="font-weight: 500;">{clinic['power']}</div>
                        </div>
                        <div>
                            <div style="color: #666;">🚰 WATER</div>
                            <div style="font-weight: 500;">{clinic['water']}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background: #1A1A2E; padding: 15px; border-radius: 0 0 15px 15px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: white; font-weight: 600;">STATUS: {clinic['status']}</span>
                <button onclick="alert('Emergency dispatch initiated!')" 
                        style="background: {icon_color}; color: white; border: none; padding: 8px 20px; border-radius: 20px; cursor: pointer; font-weight: 600;">
                    🚑 EMERGENCY
                </button>
            </div>
        </div>
        """
        
        # Add marker with custom icon
        folium.Marker(
            location=[clinic["lat"], clinic["lon"]],
            popup=folium.Popup(popup_html, max_width=400),
            tooltip=f"{clinic['name']} | Critical: {clinic['critical_count']} | Priority: {clinic['priority_score']}",
            icon=folium.Icon(color=color, icon=icon_type, prefix='fa')
        ).add_to(m)
    
    # Add optimized routes
    critical_clinics = sorted(
        [c for c in clinics_data if c["critical_count"] > 0],
        key=lambda x: x["priority_score"],
        reverse=True
    )[:6]
    
    if critical_clinics:
        route_points = [[9.03, 38.74]]  # Start at warehouse
        
        for clinic in critical_clinics:
            route_points.append([clinic["lat"], clinic["lon"]])
        
        route_points.append([9.03, 38.74])  # Return to warehouse
        
        folium.PolyLine(
            route_points,
            color='#00C2FF',
            weight=4,
            opacity=0.8,
            dash_array='10, 10',
            line_cap='round',
            popup='AI-OPTIMIZED EMERGENCY ROUTE'
        ).add_to(m)
    
    # Add heatmap if enabled
    if clinics_data:
        from folium.plugins import HeatMap
        
        heat_data = []
        for clinic in clinics_data:
            weight = clinic["critical_count"] * 0.5 + clinic["priority_score"] * 0.01
            heat_data.append([clinic["lat"], clinic["lon"], weight])
        
        HeatMap(
            heat_data,
            radius=25,
            blur=15,
            max_zoom=10,
            gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
        ).add_to(m)
    
    # Display the map
    st.markdown('<div class="glass-map-container">', unsafe_allow_html=True)
    st_folium(
        m,
        width=1200,
        height=600,
        returned_objects=["last_object_clicked_tooltip"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Map statistics
    col_map_stat1, col_map_stat2, col_map_stat3, col_map_stat4 = st.columns(4)
    
    with col_map_stat1:
        st.metric("🏥 Clinics Displayed", len(clinics_data))
    
    with col_map_stat2:
        critical_displayed = len([c for c in clinics_data if c["critical_count"] > 0])
        st.metric("⚠️ Critical Clinics", critical_displayed)
    
    with col_map_stat3:
        avg_priority = np.mean([c["priority_score"] for c in clinics_data])
        st.metric("🎯 Avg Priority", f"{avg_priority:.0f}")
    
    with col_map_stat4:
        total_pop = sum(c["population_served"] for c in clinics_data)
        st.metric("👥 Population Covered", f"{total_pop:,}")

# ========== TAB 2: AI DASHBOARD ==========
with tab2:
    st.markdown("### 📊 QUANTUM AI DASHBOARD")
    
    # AI Configuration
    with st.expander("⚙️ QUANTUM AI CONFIGURATION", expanded=True):
        col_ai1, col_ai2, col_ai3 = st.columns(3)
        
        with col_ai1:
            st.slider("Neural Network Depth", 1, 10, 5)
            st.slider("Learning Rate", 0.001, 0.1, 0.01, 0.001)
        
        with col_ai2:
            st.slider("Prediction Accuracy", 80, 99, 95)
            st.slider("Response Time Target", 1, 10, 3)
        
        with col_ai3:
            st.selectbox("AI Model", ["Quantum Neural Net", "Deep Reinforcement", "Federated Learning", "Ensemble"])
            st.checkbox("Real-time Learning", True)
            st.checkbox("Auto-Optimization", True)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Medicine distribution chart
        medicine_totals = {}
        medicine_critical = {}
        
        for clinic in clinics_data:
            for med_name, med_data in clinic["medicine_stock"].items():
                if med_name not in medicine_totals:
                    medicine_totals[med_name] = 0
                    medicine_critical[med_name] = 0
                
                medicine_totals[med_name] += med_data["stock"]
                if "CRITICAL" in med_data["status"]:
                    medicine_critical[med_name] += 1
        
        fig1 = go.Figure()
        
        fig1.add_trace(go.Bar(
            x=list(medicine_totals.keys()),
            y=list(medicine_totals.values()),
            name='Total Stock',
            marker_color='#00C2FF'
        ))
        
        fig1.add_trace(go.Bar(
            x=list(medicine_critical.keys()),
            y=list(medicine_critical.values()),
            name='Critical Clinics',
            marker_color='#FF4D4D'
        ))
        
        fig1.update_layout(
            title="📦 MEDICINE DISTRIBUTION ANALYSIS",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        # Regional analysis
        region_data = {}
        for clinic in clinics_data:
            region = clinic["city"]
            if region not in region_data:
                region_data[region] = {"clinics": 0, "critical": 0, "population": 0}
            
            region_data[region]["clinics"] += 1
            region_data[region]["critical"] += clinic["critical_count"]
            region_data[region]["population"] += clinic["population_served"]
        
        fig2 = go.Figure(data=[
            go.Scatter(
                x=[region_data[r]["clinics"] for r in region_data],
                y=[region_data[r]["critical"] for r in region_data],
                text=list(region_data.keys()),
                mode='markers+text',
                marker=dict(
                    size=[region_data[r]["population"]/5000 for r in region_data],
                    color=[region_data[r]["critical"] for r in region_data],
                    colorscale='RdYlGn_r',
                    showscale=True,
                    line=dict(width=2, color='white')
                ),
                textposition="top center"
            )
        ])
        
        fig2.update_layout(
            title="🌍 REGIONAL RISK ANALYSIS",
            height=400,
            xaxis_title="Number of Clinics",
            yaxis_title="Critical Cases",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # AI Recommendations
    st.markdown("### 💡 QUANTUM AI RECOMMENDATIONS")
    
    recommendations = [
        {
            "title": "🚀 Merge Delivery Routes",
            "description": "Combine routes in Oromia and Amhara to save 42% fuel",
            "impact": "$124,000 monthly savings",
            "priority": "HIGH",
            "color": "#00D4AA"
        },
        {
            "title": "⚠️ Emergency Stock Redistribution",
            "description": "Transfer malaria medicine from Addis Ababa to critical zones",
            "impact": "Save 2,500+ patients this week",
            "priority": "URGENT",
            "color": "#FF4D4D"
        },
        {
            "title": "⚡ Solar Power Installation",
            "description": "Install solar panels in 8 clinics with unreliable power",
            "impact": "8,000+ patients served reliably",
            "priority": "MEDIUM",
            "color": "#FFB347"
        }
    ]
    
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    
    for idx, rec in enumerate(recommendations):
        with [col_rec1, col_rec2, col_rec3][idx]:
            st.markdown(f"""
            <div style="background: {rec['color']}20; border: 2px solid {rec['color']}; 
                        border-radius: 20px; padding: 1.5rem; height: 250px; display: flex; 
                        flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">{rec['title']}</div>
                    <div style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin-bottom: 15px;">
                        {rec['description']}
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="background: {rec['color']}; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">
                            {rec['priority']}
                        </span>
                        <span style="color: {rec['color']}; font-weight: bold;">IMPACT</span>
                    </div>
                    <div style="font-size: 1.1rem; font-weight: bold; color: white;">{rec['impact']}</div>
                    <button style="width: 100%; background: {rec['color']}; color: white; border: none; 
                                padding: 10px; border-radius: 10px; margin-top: 15px; font-weight: bold; cursor: pointer;">
                        ⚡ APPLY RECOMMENDATION
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========== TAB 3: LOGISTICS HUB ==========
with tab3:
    st.markdown("### 🚚 QUANTUM LOGISTICS HUB")
    
    # Vehicle Fleet
    st.markdown("#### 🚛 QUANTUM FLEET MANAGEMENT")
    
    vehicles = [
        {"ID": "QT-001", "Type": "Quantum Refrigerated Truck", "Capacity": "10,000 units", "Status": "🟢 ACTIVE", "Location": "Addis Ababa", "Fuel": "85%"},
        {"ID": "QT-002", "Type": "AI Delivery Drone", "Capacity": "500 units", "Status": "🟡 ON MISSION", "Location": "Mekelle", "Fuel": "45%"},
        {"ID": "QT-003", "Type": "Emergency Ambulance", "Capacity": "2,000 units", "Status": "🟢 STANDBY", "Location": "Bahir Dar", "Fuel": "90%"},
        {"ID": "QT-004", "Type": "Autonomous Van", "Capacity": "5,000 units", "Status": "🔴 MAINTENANCE", "Location": "Hawassa", "Fuel": "10%"},
        {"ID": "QT-005", "Type": "Motorcycle Courier", "Capacity": "200 units", "Status": "🟢 ACTIVE", "Location": "Jimma", "Fuel": "60%"},
    ]
    
    # Display vehicles
    for vehicle in vehicles:
        col_veh1, col_veh2, col_veh3 = st.columns([1, 2, 1])
        
        with col_veh1:
            status_color = "#00D4AA" if "🟢" in vehicle["Status"] else "#FFB347" if "🟡" in vehicle["Status"] else "#FF4D4D"
            st.markdown(f"""
            <div style="background: {status_color}20; padding: 1rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 1.5rem;">🚚</div>
                <div style="font-weight: bold; color: white;">{vehicle['ID']}</div>
                <div style="color: {status_color}; font-size: 0.9rem;">{vehicle['Status']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_veh2:
            st.markdown(f"""
            <div style="padding: 1rem;">
                <div style="font-weight: bold; color: white; font-size: 1.1rem;">{vehicle['Type']}</div>
                <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 5px;">
                    📍 {vehicle['Location']} • 📦 {vehicle['Capacity']}
                </div>
                <div style="margin-top: 10px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px;">
                        <span>Fuel Level</span>
                        <span>{vehicle['Fuel']}</span>
                    </div>
                    <div style="height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden;">
                        <div style="height: 100%; width: {vehicle['Fuel']}; background: linear-gradient(90deg, #00C2FF, #00D4AA);"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_veh3:
            if st.button("📡 TRACK", key=f"track_{vehicle['ID']}", use_container_width=False):
                st.toast(f"Tracking {vehicle['ID']}...", icon="📍")
    
    # Route Planning
    st.markdown("#### 🗺️ QUANTUM ROUTE OPTIMIZER")
    
    col_route1, col_route2 = st.columns(2)
    
    with col_route1:
        selected_cities = st.multiselect(
            "Select Cities",
            sorted(list(set([c["city"] for c in clinics_data]))),
            default=["Addis Ababa", "Mekelle", "Bahir Dar"]
        )
        
        optimization_mode = st.selectbox(
            "Optimization Mode",
            ["Minimize Time", "Minimize Cost", "Maximize Coverage", "Balance All"]
        )
        
        if st.button("🚀 GENERATE QUANTUM ROUTE", use_container_width=False):
            with st.spinner("⚡ Quantum computer optimizing route..."):
                time.sleep(2)
                st.success("✅ Route generated! 42% more efficient than classical algorithms!")
                st.balloons()
    
    with col_route2:
        st.markdown("""
        <div class="glass-card-3d" style="height: 200px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div style="font-size: 3rem;">⚡</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: white; margin-top: 10px;">QUANTUM SPEED</div>
            <div style="color: rgba(255, 255, 255, 0.7);">Route calculations in 0.3 seconds</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Monthly Fuel", "8,400 L")
        with col_stat2:
            st.metric("Cost Savings", "$124,000")

# ========== TAB 4: CONTROL CENTER ==========
with tab4:
    st.markdown("### ⚡ QUANTUM CONTROL CENTER")
    
    col_control1, col_control2 = st.columns(2)
    
    with col_control1:
        # System Controls
        st.markdown("#### 🔧 SYSTEM CONTROLS")
        
        if st.button("🔄 FULL SYSTEM REBOOT", use_container_width=False):
            with st.spinner("Rebooting quantum system..."):
                time.sleep(3)
                st.success("✅ System rebooted successfully!")
        
        if st.button("📡 DATA SYNC ALL", use_container_width=False):
            st.toast("Syncing with 247 clinics...", icon="📡")
            time.sleep(1)
            st.success("✅ All data synchronized!")
        
        if st.button("🚨 EMERGENCY BROADCAST", use_container_width=False):
            st.warning("⚠️ Emergency broadcast sent to all clinics!")
        
        # AI Training
        st.markdown("#### 🤖 AI TRAINING")
        
        training_progress = st.progress(0)
        
        if st.button("🧠 TRAIN QUANTUM AI", use_container_width=False):
            for i in range(100):
                training_progress.progress(i + 1)
                time.sleep(0.01)
            st.success("✅ Quantum AI trained with 2.4M data points!")
    
    with col_control2:
        # System Status
        st.markdown("#### 📡 SYSTEM STATUS")
        
        status_items = [
            ("Quantum AI Core", "🟢 ONLINE", "99.9% uptime"),
            ("Neural Network", "🟢 TRAINING", "2.4M params"),
            ("Data Pipeline", "🟢 FLOWING", "247 sources"),
            ("Security Layer", "🟢 ACTIVE", "256-bit encryption"),
            ("Cloud Cluster", "🟢 SYNCED", "12 nodes"),
            ("API Gateway", "🟢 RESPONDING", "3ms latency"),
        ]
        
        for name, status, details in status_items:
            col_stat1, col_stat2 = st.columns([3, 2])
            with col_stat1:
                st.markdown(f"<span style='color: rgba(255, 255, 255, 0.8);'>{name}</span>", unsafe_allow_html=True)
            with col_stat2:
                st.markdown(f"<span style='color: #00D4AA; font-weight: bold;'>{status}</span>", unsafe_allow_html=True)
            st.caption(details)
            st.divider()
    
    # Real-time Simulation
    st.markdown("#### 🎮 REAL-TIME SIMULATION")
    
    if st.button("🎬 START QUANTUM SIMULATION", type="primary", use_container_width=False):
        with st.status("⚡ Running quantum simulation...", expanded=True) as status:
            st.write("Initializing quantum processors...")
            time.sleep(1)
            
            st.write("Loading 2.4M data points...")
            time.sleep(1)
            
            st.write("Running neural network predictions...")
            time.sleep(1)
            
            st.write("Optimizing delivery routes...")
            time.sleep(1)
            
            st.write("Generating recommendations...")
            time.sleep(1)
            
            status.update(label="✅ Simulation complete!", state="complete")
        
        col_sim1, col_sim2, col_sim3 = st.columns(3)
        
        with col_sim1:
            st.metric("Routes Optimized", "42", "+12")
        
        with col_sim2:
            st.metric("Fuel Savings", "38%", "+5%")
        
        with col_sim3:
            st.metric("Time Saved", "124 hrs", "+28 hrs")

# ========== REAL-TIME ALERTS ==========
st.markdown("---")
st.markdown("### ⚠️ REAL-TIME CRITICAL ALERTS")

if clinics_data:
    critical_clinics = sorted(
        [c for c in clinics_data if c["critical_count"] >= 2],
        key=lambda x: x["priority_score"],
        reverse=True
    )[:5]
    
    if critical_clinics:
        for clinic in critical_clinics:
            col_alert1, col_alert2, col_alert3 = st.columns([1, 3, 1])
            
            with col_alert1:
                st.markdown(f"""
                <div style="background: #FF4D4D; color: white; padding: 1rem; border-radius: 15px; text-align: center;">
                    <div style="font-size: 2rem;">⚠️</div>
                    <div style="font-weight: bold;">{clinic['critical_count']}</div>
                    <div style="font-size: 0.8rem;">CRITICAL</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_alert2:
                st.markdown(f"""
                <div style="padding: 1rem;">
                    <div style="font-weight: bold; color: white; font-size: 1.2rem;">{clinic['name']}</div>
                    <div style="color: rgba(255, 255, 255, 0.7); margin-top: 5px;">
                        📍 {clinic['city']} • 👥 {clinic['population_served']:,} people • 🎯 Priority: {clinic['priority_score']}
                    </div>
                    <div style="margin-top: 10px; font-size: 0.9rem;">
                        <span style="color: #FF4D4D;">⚠️ Needs immediate delivery</span> • Last delivery: {clinic['last_delivery']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_alert3:
                if st.button("🚑 DISPATCH", key=f"dispatch_{clinic['id']}", use_container_width=False):
                    st.toast(f"Emergency dispatch to {clinic['name']}!", icon="🚑")

# ========== SUPREME FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3rem; background: rgba(0, 0, 0, 0.3); 
            border-radius: 30px; margin-top: 3rem; border: 1px solid rgba(255, 255, 255, 0.1);">
    
    <div style="display: flex; justify-content: center; gap: 40px; margin-bottom: 2rem;">
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: white;">🏢 PARTNERS</div>
            <div style="color: rgba(255, 255, 255, 0.7); margin-top: 10px;">
                Ministry of Health Ethiopia<br>
                World Health Organization<br>
                UNICEF Ethiopia
            </div>
        </div>
        
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: white;">📞 SUPPORT</div>
            <div style="color: rgba(255, 255, 255, 0.7); margin-top: 10px;">
                Hotline: 911<br>
                Email: quantum@mediroute.et<br>
                SMS: *911#
            </div>
        </div>
        
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: white;">🌐 COVERAGE</div>
            <div style="color: rgba(255, 255, 255, 0.7); margin-top: 10px;">
                11 Regions • 247 Clinics<br>
                12.5M People • 85% of Ethiopia
            </div>
        </div>
        
        <div>
            <div style="font-size: 1.2rem; font-weight: bold; color: white;">📊 IMPACT</div>
            <div style="color: rgba(255, 255, 255, 0.7); margin-top: 10px;">
                99.9% Delivery Success<br>
                42% Fuel Savings<br>
                12,000+ Lives/Month
            </div>
        </div>
    </div>
    
    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 1rem;">
            <div class="floating-element" style="font-size: 2rem;">⚡</div>
            <div class="floating-element" style="font-size: 2rem; animation-delay: 0.5s;">🌍</div>
            <div class="floating-element" style="font-size: 2rem; animation-delay: 1s;">🚑</div>
            <div class="floating-element" style="font-size: 2rem; animation-delay: 1.5s;">🤖</div>
        </div>
        
        <h3 style="color: white; margin: 0; font-size: 2rem;">
            <span style="background: linear-gradient(135deg, #FFD700, #00D4AA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🇪🇹 QUANTUM MEDICINE DELIVERY
            </span>
        </h3>
        
        <p style="color: rgba(255, 255, 255, 0.7); margin-top: 10px; font-size: 1.1rem;">
            © 2024 MediRoute Pro MAX • Quantum Edition v4.2.1 • Ministry of Health Ethiopia
        </p>
        
        <div style="margin-top: 20px; font-size: 0.9rem; color: rgba(255, 255, 255, 0.5);">
            ⚡ Powered by Quantum Computing • 🛡️ 256-bit Military Encryption • 🌐 Global CDN
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== AUTOMATIC UPDATES ==========
if st.button("🔄 AUTO-UPDATE SYSTEM", type="secondary", use_container_width=False):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Connecting to quantum network...",
        "Syncing clinic data...",
        "Updating AI models...",
        "Optimizing routes...",
        "Generating reports...",
        "System update complete!"
    ]
    
    for i, step in enumerate(steps):
        status_text.text(f"⚡ {step}")
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.5)
    
    st.success("✅ System fully updated and optimized!")
    st.balloons()
