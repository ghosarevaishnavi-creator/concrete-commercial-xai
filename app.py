import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import shap
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_pdf import PdfPages

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

# 2. Safely Load and Cache the Trained XGBoost Model Weights
@st.cache_resource
def load_ai_brain():
    return joblib.load('concrete_xgboost_model.pkl')

# 3. Cache the SHAP Explainer Engine to Stop Page Freezing
@st.cache_resource
def get_shap_explainer(_trained_model):
    return shap.TreeExplainer(_trained_model)

try:
    model = load_ai_brain()
    explainer = get_shap_explainer(model)
except:
    st.error("🚨 System Error: Critical files not detected inside this repository folder.")
    st.stop()

# Track authentication states
if 'payment_verified' not in st.session_state:
    st.session_state.payment_verified = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Create two clean main user dashboard columns
col_inputs, col_payment = st.columns([1, 1.1])

# 4. Left Panel: Input Sliders for Concrete Mix Matrix
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

    # Build the DataFrame with the exact feature names the model expects.
    # This keeps the UI slider labels user-friendly while feeding the model its original training names.
    training_feature_names = [
        'Cement (component 1)(kg in a m^3 mixture)',
        'Blast Furnace Slag (component 2)(kg in a m^3 mixture)',
        'Fly Ash (component 3)(kg in a m^3 mixture)',
        'Water  (component 4)(kg in a m^3 mixture)',
        'Superplasticizer (component 5)(kg in a m^3 mixture)',
        'Coarse Aggregate  (component 6)(kg in a m^3 mixture)',
        'Fine Aggregate (component 7)(kg in a m^3 mixture)',
        'Age (day)'
    ]

    values = [val_1, val_2, val_3, val_4, val_5, val_6, val_7, val_8]
    live_inputs = pd.DataFrame([values], columns=training_feature_names)

# 5. Right Panel: Monetization and XAI Analytics Engine
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
        
        # 6. Core Machine Learning Calculations
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
        
        # 7. High-Performance Transparency Audit (Fixed Rendering Pipeline)
        st.subheader("🧠 4. Transparency Audit: Detailed Physics Explanation")
        
        # Run pre-cached explainer calculation instantly
        calculated_shap_values = explainer(live_inputs)
        
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

        # ---- Prepare PDF buffer for download (include waterfall + contribution chart) ----
        pdf_buffer = io.BytesIO()
        # Save the waterfall figure first into the PDF
        with PdfPages(pdf_buffer) as pdf:
            pdf.savefig(fig)
            plt.close(fig)

        # ---- Additional XAI Reporting: textual explanation + contribution bar chart ----
        shap_vals = np.array(calculated_shap_values.values[0])
        feat_names = list(calculated_shap_values.feature_names)

        df_shap = pd.DataFrame({
            'feature': feat_names,
            'shap_value': shap_vals,
        })
        df_shap['abs_shap'] = df_shap['shap_value'].abs()
        df_shap['pct_contrib'] = 100.0 * df_shap['abs_shap'] / df_shap['abs_shap'].sum()
        df_shap.sort_values('abs_shap', ascending=False, inplace=True)

        # Natural-language explanation: top positive and negative contributors
        pos = df_shap[df_shap['shap_value'] > 0].head(3)
        neg = df_shap[df_shap['shap_value'] < 0].head(3)

        why_lines = []
        if not pos.empty:
            why_lines.append("Primary positive contributors (increase predicted strength): " +
                             ", ".join([f"{r.feature} (+{r.shap_value:.2f}, {r.pct_contrib:.1f}%)" for r in pos.itertuples()]))
        if not neg.empty:
            why_lines.append("Primary negative contributors (decrease predicted strength): " +
                             ", ".join([f"{r.feature} ({r.shap_value:.2f}, {r.pct_contrib:.1f}%)" for r in neg.itertuples()]))
        why_text = "\n".join(why_lines) if why_lines else "No strong contributors identified."

        st.subheader("🔎 Why (Feature Contributions)")
        st.write(why_text)

        # ---- Detailed, educational SHAP explanation (for students/researchers/contractors) ----
        base_value = None
        if hasattr(calculated_shap_values, 'base_values'):
            bv = calculated_shap_values.base_values
            try:
                base_value = float(bv[0])
            except Exception:
                try:
                    base_value = float(bv)
                except Exception:
                    base_value = None

        predicted = float(computed_strength)
        net_effect = None
        if base_value is not None:
            net_effect = predicted - base_value

        # Domain guidance templates per feature
        guidance = {
            'Cement Content': 'Cement is the primary binder — increasing cement generally raises early-age strength but also increases cost and CO2 footprint. Optimize mix for required strength.',
            'Water Volume': 'Water increases workability but a higher water-to-cement ratio lowers strength. Reducing water while using superplasticizer improves strength.',
            'Superplasticizer Admixture': 'Superplasticizers reduce water demand for the same workability, enabling lower w/c ratios and higher strength when used correctly.',
            'Age (Curing Days)': 'Strength develops with curing time — adequate curing (moisture and temperature control) significantly improves final strength.',
            'Fly Ash Substitution': 'Fly ash can reduce early strength but improves long-term strength and durability; monitor replacement percentage carefully for early-age requirements.',
            'Blast Furnace Slag': 'Slag behaves similarly to fly ash: beneficial for long-term strength and durability but may reduce early-age strength at high replacement levels.',
            'Coarse Aggregate': 'Aggregate quality and grading affect packing density and strength — check grading, cleanliness, and particle shape.',
            'Fine Aggregate': 'Fine aggregate proportions affect workability and finishing; excessive fines can increase water demand and reduce strength.'
        }

        # Build per-feature detailed lines
        detailed_lines = []
        detailed_lines.append(f"Executive summary: predicted = {predicted:.2f} MPa" + (f", model base = {base_value:.2f} MPa, net effect = {net_effect:.2f} MPa" if net_effect is not None else ""))
        detailed_lines.append("\nTop contributors and interpretations:")
        for r in df_shap.head(8).itertuples():
            feat = r.feature
            val = live_inputs.iloc[0][feat] if feat in live_inputs.columns else 'N/A'
            sign = 'increases' if r.shap_value > 0 else 'decreases'
            pct = r.pct_contrib
            interp = guidance.get(feat, '')
            detailed_lines.append(f"- {feat}: value={val} -> {sign} prediction by {r.shap_value:.2f} MPa ({pct:.1f}%). {interp}")

        # Actionable recommendations (top 3)
        detailed_lines.append("\nActionable recommendations:")
        for r in pos.itertuples():
            feat = r.feature
            interp = guidance.get(feat, '')
            detailed_lines.append(f"- Increase/maintain {feat}: {interp}")
        for r in neg.itertuples():
            feat = r.feature
            interp = guidance.get(feat, '')
            detailed_lines.append(f"- Reduce/adjust {feat}: {interp}")

        # Lesson and conclusion
        detailed_lines.append("\nLessons and conclusion:")
        detailed_lines.append("- The water-to-cement ratio and proper curing are often the single biggest drivers of early-age compressive strength.")
        detailed_lines.append("- Supplementary materials (fly ash, slag) improve long-term performance but require balancing for early-age requirements.")
        detailed_lines.append("- Use the contribution table and recommendations to iteratively adjust mix design and validate with field tests.")

        detailed_text = "\n".join(detailed_lines)
        st.subheader("📘 Detailed Explanation & Recommendations")
        st.write(detailed_text)

        # ---- Results Section (concise, specific) ----
        result_lines = []
        result_lines.append(f"Predicted 28-day compressive strength: {predicted:.2f} MPa")
        if base_value is not None:
            result_lines.append(f"Model baseline (expected average): {base_value:.2f} MPa")
            result_lines.append(f"Net effect (prediction - baseline): {net_effect:.2f} MPa")

        # top contributors list (ordered)
        top_list = [f"{r.feature}: {r.shap_value:.2f} MPa ({r.pct_contrib:.1f}%)" for r in df_shap.head(5).itertuples()]
        result_lines.append("Top feature contributions:")
        result_lines.extend([f"- {t}" for t in top_list])

        st.subheader("✅ Results")
        for line in result_lines:
            st.write(line)

        # ---- Conclusion Section (actionable, short) ----
        conclusion_lines = []
        conclusion_lines.append("Conclusion:")
        conclusion_lines.append("- The predicted mix meets/does not meet common benchmark targets depending on project spec; check required strength thresholds.")
        conclusion_lines.append("- If early-age strength is critical, prioritize lowering water content and ensuring proper curing.")
        conclusion_lines.append("- For long-term durability, consider supplementary cementitious materials (fly ash/slag) while validating early-age performance.")
        conclusion_text = "\n".join(conclusion_lines)
        st.subheader("📌 Conclusion")
        st.write(conclusion_text)

        # Contribution bar chart
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        plot_df = df_shap.copy()
        plot_df = plot_df[::-1]  # reverse for horizontal bar order
        colors = ['green' if v > 0 else 'red' for v in plot_df['shap_value']]
        ax2.barh(plot_df['feature'], plot_df['shap_value'], color=colors)
        ax2.set_xlabel('SHAP value (contribution to prediction)')
        ax2.set_title('Feature contributions (positive = increase prediction)')
        plt.tight_layout()
        st.pyplot(fig2)
        # Save the contribution chart into the same PDF
        with PdfPages(pdf_buffer) as pdf:
            pdf.savefig(fig2)
            plt.close(fig2)

        # Add a final page with textual summary
        summary_fig = plt.figure(figsize=(8.5, 11))
        summary_fig.clf()
        # include the rich detailed text in the PDF summary page
        summary_text = f"Predicted 28-day strength: {computed_strength:.2f} MPa\n\n{detailed_text}"
        summary_fig.text(0.01, 0.99, summary_text, va='top', wrap=True, fontsize=10)
        with PdfPages(pdf_buffer) as pdf:
            pdf.savefig(summary_fig)
            plt.close(summary_fig)

        pdf_buffer.seek(0)
        st.download_button("📥 Download SHAP Report (PDF)", data=pdf_buffer.getvalue(), file_name="shap_report.pdf", mime="application/pdf")

        # Show a small table summarizing contributions
        st.subheader("📊 SHAP Contribution Summary")
        st.table(df_shap[['feature', 'shap_value', 'pct_contrib']].reset_index(drop=True))
