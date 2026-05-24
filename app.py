import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import shap
import matplotlib.pyplot as plt

# 1. Web Page Layout Configurations
st.set_page_config(page_title="Commercial XAI Concrete Engine", page_icon="🏗️", layout="wide")

# Apply custom styling themes
st.markdown("""
<style>
    .reportview-container { background: #f5f7f9; }
    .stButton>button { color: white; background: #1E3A8A; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background: #1D4ED8; }
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Open-Access Intelligent Concrete Informatics Engine")
st.markdown("### **2026 Structural Engineering Paradigm: Monetized Explainable AI (XAI) for Field Inspections**")
st.write("An auditable material verification engine built to predict concrete strength with complete physics transparency.")
st.markdown("---")

# 2. Safely Load the Trained XGBoost Weights
@st.cache_resource
def load_ai_brain():
    return joblib.load('concrete_xgboost_model.pkl')

try:
    model = load_ai_brain()
except:
    st.error("🚨 System Error: 'concrete_xgboost_model.pkl' not detected inside this repository folder.")
    st.stop()

# Track authentication states
if 'payment_verified' not in st.session_state:
    st.session_state.payment_verified = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Create two clean main user dashboard columns
col_inputs, col_payment = st.columns([1, 1.1])

# 3. Left Panel: Input Sliders for Concrete Mix Matrix
with col_inputs:
    st.subheader("📋 1. Enter On-Site Structural Mix Proportions")
    val_1 = st.slider("Cement Content (kg/m³)", 100.0, 550.0, 320.0, step=5.0)
    val_2 = st.slider("Blast Furnace Slag Addition (kg/m³)", 0.0, 350.0, 0.0, step=5.0)
    val_3 = st.slider("Fly Ash Supplementary Substitution (kg/m³)", 0.0, 200.0, 50.0, step=5.0)
    val_4 = st.slider("Water Mass Volume (kg/m³)", 120.0, 250.0, 175.0, step=2.0)
    val_5 = st.slider("Superplasticizer Admixture Dosage (kg/m³)", 0.0, 35.0, 6.0, step=0.5)
    val_6 = st.slider("Coarse Aggregate Frame (kg/m³)", 700.0, 1200.0, 960.0, step=10.0)
    val_7 = st.slider("Fine Aggregate Matrix (kg/m³)", 500.0, 1000.0, 740.0, step=10.0)
    val_8 = st.slider("Target Structure Curing Horizon (Days)", 1, 365, 28)

    # Convert sliders directly into a structured DataFrame matching your XGBoost features
    live_inputs = pd.DataFrame([[val_1, val_2, val_3, val_4, val_5, val_6, val_7, val_8]],
                              columns=['Cement', 'Blast_Furnace_Slag', 'Fly_Ash', 'Water', 'Superplasticizer', 'Coarse_Aggregate', 'Fine_Aggregate', 'Age'])

# 4. Right Panel: Monetization and XAI Analytics Engine
with col_payment:
    st.subheader("💳 2. Commercial License & Payment Gateway")
    
    st.markdown("""
    <div style='background-color:#FEF3C7; padding:12px; border-radius:8px; border-left: 5px solid #D97706; margin-bottom:15px;'>
        <p style='color:#92400E; margin:0; font-weight:bold;'>🎉 INITIAL LAUNCH PROMOTION ACTIVE!</p>
        <p style='color:#B45309; margin:0; font-size:13px;'>Use Promo Code <b>FREE2026</b> below to bypass payment during the launch phase.</p>
    </div>
    """, unsafe_allow_html=True)
    
    promo_code = st.text_input("🔑 Enter Promotional Access Code (Optional):").strip()
    
    if promo_code == "FREE2026":
        st.session_state.payment_verified = True
        st.session_state.user_type = "Promotional Free User"

    if not st.session_state.payment_verified:
        st.warning("🔒 Access Locked: Choose your user profile and clear your access token charge to unlock the report.")
        profile_tab = st.radio("Select Your Professional Profile:", 
                               ["Industry Professional (Contractor, Site Engineer)", 
                                "Academic Student (Valid Institutional ID)"])
        
        if "Industry Professional" in profile_tab:
            st.info("💰 **Rate:** ₹2,000 INR per query.")
            if st.button("💳 Pay ₹2000 & Unlock"):
                st.session_state.payment_verified = True
                st.session_state.user_type = "Professional"
                st.rerun()
        else:
            st.info("🎓 **Subsidy Rate:** ₹50 INR per student query.")
            college_name = st.text_input("College Name:")
            roll_number = st.text_input("Roll Number:")
            uploaded_id = st.file_uploader("Upload ID Card Photo", type=['jpg','jpeg','png'])
            if college_name and roll_number and uploaded_id:
                if st.button("💳 Pay Subsidized ₹50 & Unlock"):
                    st.session_state.payment_verified = True
                    st.session_state.user_type = "Student"
                    st.rerun()
    else:
        st.success(f"🔓 Access Granted! Mode: {st.session_state.user_type}")
        if st.button("🔄 Reset / Lock Session"):
            st.session_state.payment_verified = False
            st.session_state.user_type = None
            st.rerun()
            
        st.markdown("---")
        
        # 5. Core Machine Learning Calculations
        st.subheader("🔮 3. Core Structural Engineering Report")
        
        computed_strength = model.predict(live_inputs)[0]
        theme_color = "green" if computed_strength >= 40 else "blue" if computed_strength >= 20 else "orange"
        
        st.markdown(f"""
        <div style='background-color:rgba(0,0,0,0.03); padding:20px; border-radius:12px; border-left: 9px solid {theme_color};'>
            <h4 style='margin:0;'>PREDICTED 28-DAY CHARACTERISTIC STRENGTH:</h4>
            <h1 style='color:{theme_color}; margin:10px 0; font-size:40px;'>{computed_strength:.2f} MPa</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 6. High-Performance Transparency Audit (Fixed Rendering Pipeline)
        st.subheader("🧠 4. Transparency Audit: Detailed Physics Explanation")
        
        # Build SHAP TreeExplainer from the live inputs
        live_explainer = shap.TreeExplainer(model)
        calculated_shap_values = live_explainer(live_inputs)
        
        # Give neat professional names to data variables for the chart display
        calculated_shap_values.feature_names = [
            'Cement Content', 'Blast Furnace Slag', 'Fly Ash Substitution', 
            'Water Volume', 'Superplasticizer Admixture', 
            'Coarse Aggregate', 'Fine Aggregate', 'Curing Age (Days)'
        ]
        
        # Explicitly configure the Matplotlib figure canvas mapping to prevent blank outputs
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Generate the waterfall chart bound directly onto our custom plot axes
        shap.plots.waterfall(calculated_shap_values[0], max_display=8, show=False)
        
        # Format layout boundaries to prevent clipping errors on small screens
        plt.tight_layout()
        
        # Direct the fully rendered graphic object into Streamlit safely
        st.pyplot(fig)
        
        # Close the plot down to conserve system memory
        plt.close(fig)
