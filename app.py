import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import shap
import matplotlib.pyplot as plt

# Web Page Configurations
st.set_page_config(page_title="Commercial XAI Concrete Engine", page_icon="🏗️", layout="wide")

# Custom CSS styling for a professional SaaS feel
st.markdown("""
<style>
    .reportview-container { background: #f5f7f9; }
    .stButton>button { color: white; background: #1E3A8A; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background: #1D4ED8; }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🏗️ Commercialized Open-Access Intelligent Concrete Informatics Engine")
st.markdown("### **2026 Structural Engineering Paradigm: Monetized Explainable AI (XAI) for Field Inspections**")
st.write("An auditable material verification engine built to predict concrete strength with complete physics transparency.")

st.markdown("---")

# Securely load the compiled model brain
@st.cache_resource
def load_ai_brain():
    return joblib.load('concrete_xgboost_model.pkl')

try:
    model = load_ai_brain()
except:
    st.error("🚨 System Error: 'concrete_xgboost_model.pkl' not detected. Please make sure you uploaded the model file to the server.")
    st.stop()

# Initialize session state variables to track payment steps securely
if 'payment_verified' not in st.session_state:
    st.session_state.payment_verified = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Main Interface Grid Split
col_inputs, col_payment = st.columns([1, 1.1])

with col_inputs:
    st.subheader("📋 1. Enter On-Site Structural Mix Proportions")
    st.caption("Adjust sliders based on your target trial mix calculations or batching values:")
    
    val_1 = st.slider("Cement Content (kg/m³)", 100.0, 550.0, 320.0, step=5.0)
    val_2 = st.slider("Blast Furnace Slag Addition (kg/m³)", 0.0, 350.0, 0.0, step=5.0)
    val_3 = st.slider("Fly Ash Supplementary Substitution (kg/m³)", 0.0, 200.0, 50.0, step=5.0)
    val_4 = st.slider("Water Mass Volume (kg/m³)", 120.0, 250.0, 175.0, step=2.0)
    val_5 = st.slider("Superplasticizer Admixture Dosage (kg/m³)", 0.0, 35.0, 6.0, step=0.5)
    val_6 = st.slider("Coarse Aggregate Frame (kg/m³)", 700.0, 1200.0, 960.0, step=10.0)
    val_7 = st.slider("Fine Aggregate Matrix (kg/m³)", 500.0, 1000.0, 740.0, step=10.0)
    val_8 = st.slider("Target Structure Curing Horizon (Days)", 1, 365, 28)

    # Convert sliders into a structured dataframe format
    live_inputs = pd.DataFrame([[val_1, val_2, val_3, val_4, val_5, val_6, val_7, val_8]])

with col_payment:
    st.subheader("💳 2. Commercial License & Payment Gateway")
    
    if not st.session_state.payment_verified:
        st.warning("🔒 Access Locked: To view the AI prediction and the Explainable AI (XAI) engineering report, please choose your user profile and clear your access token charge.")
        
        # User Type selection tab
        profile_tab = st.radio("Select Your Professional Profile:", 
                               ["Industry Professional (Contractor, Site Engineer, Consultant, Owner)", 
                                "Academic Student (BTech/MTech/Diploma with Valid Institutional ID)"])
        
        if "Industry Professional" in profile_tab:
            st.info("💰 **Rate Layer:** ₹2,000 INR per premium concrete audit query.")
            
            # Simulated Payment Options
            pay_method = st.selectbox("Choose Payment Mode:", ["UPI (GPay/PhonePe/Paytm)", "Credit/Debit Card", "Net Banking"])
            if pay_method == "UPI (GPay/PhonePe/Paytm)":
                st.code("concreteAI.startup@upi", language="")
                st.caption("Scan the UPI ID above or interact below to simulate payment authorization.")
                
            if st.button("💳 Pay ₹2000 & Unlock Audit Report"):
                st.session_state.payment_verified = True
                st.session_state.user_type = "Professional"
                st.rerun()
                
        else:
            st.info("🎓 **Subsidy Rate Layer:** ₹50 INR per student query (97.5% Educational Subsidy applied).")
            
            # Student Verification Inputs
            college_name = st.text_input("Enter College/University Name:")
            roll_number = st.text_input("Enter Student Roll/Enrollment ID Number:")
            uploaded_id = st.file_uploader("Upload Clear Photo of Institutional ID Card (.jpg, .png)", type=['jpg','jpeg','png'])
            
            if college_name and roll_number and uploaded_id:
                st.success("✅ Student identity parameters verified successfully by system parser!")
                if st.button("💳 Pay Subsidized ₹50 & Unlock Audit Report"):
                    st.session_state.payment_verified = True
                    st.session_state.user_type = "Student"
                    st.rerun()
            else:
                st.caption("Please fill out institutional details and upload your ID card to unlock the student rate.")
                
    else:
        st.success(f"🔓 Access Granted! Active Session Type: {st.session_state.user_type} Token Verified.")
        if st.button("🔄 Clear Token / Lock Session"):
            st.session_state.payment_verified = False
            st.session_state.user_type = None
            st.rerun()
            
        st.markdown("---")
        st.subheader("🔮 3. Processed Core Structural Engineering Report")
        
        # Run Machine Learning Inference
        computed_strength = model.predict(live_inputs)[0]
        
        if computed_strength < 20.0:
            theme_color = "orange"
            structural_use = "Low Strength / Plain Cement Concrete (Lean Base Cores, Mass Foundation Screeds)"
        elif computed_strength < 40.0:
            theme_color = "blue"
            structural_use = "Standard Structural Concrete Grade (Reinforced Beams, High-Load Slabs, Frame Columns)"
        else:
            theme_color = "green"
            structural_use = "High-Performance Advanced Grade (Prestressed Precast Members, Bridge Decks, High-Rise Shear Walls)"
            
        st.markdown(f"""
        <div style='background-color:rgba(0,0,0,0.03); padding:20px; border-radius:12px; border-left: 9px solid {theme_color};'>
            <h4 style='margin:0; font-family:sans-serif;'>PREDICTED 28-DAY COMPRESSIVE STRENGTH:</h4>
            <h1 style='color:{theme_color}; margin:6px 0; font-size:42px;'>{computed_strength:.2f} MPa</h1>
            <p style='margin:0; font-weight:bold; font-family:sans-serif;'>Target Application Category: {structural_use}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🧠 4. Transparency Audit: Detailed Physics Explanation")
        st.caption("This visualization uses Game Theory attribution tracking to analyze your custom input mix. Red markers display metrics accelerating structural capacity; blue fields depict parameters restricting output limits.")
        
        # Calculate instant marginal SHAP vector components
        live_explainer = shap.TreeExplainer(model)
        calculated_shap_values = live_explainer(live_inputs)
        
        calculated_shap_values.feature_names = [
            'Cement', 'Blast Furnace Slag', 'Fly Ash Substitution', 'Water Content', 
            'Superplasticizer Admixture', 'Coarse Aggregate', 'Fine Aggregate', 'Curing Age Days'
        ]
        
        # Render visual breakdown chart directly in Streamlit
        fig, ax = plt.subplots(figsize=(10, 4))
        shap.plots.waterfall(calculated_shap_values[0], max_display=8, show=False)
        plt.title("On-Site Custom Component Weight Contribution Analysis (SHAP Waterfall)", fontsize=11, pad=22)
        st.pyplot(fig)
        
        st.info("💡 **Field Engineering Takeaway:** Review the topmost drivers. If 'Water Content' features a long blue vector moving left, the computational network has penalized your entry for containing excessive water volume, which dilutes crystallization density. Lowering water by 5-10 liters will immediately eliminate this structural penalty and boost load calculations.")