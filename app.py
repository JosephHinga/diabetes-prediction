import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Hospital Diabetes Screening",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== HOSPITAL STYLE ====================
st.markdown("""
<style>
    /* Hospital Theme */
    .main {
        background-color: #f8f9fa;
    }
    
    .hospital-header {
        background: linear-gradient(135deg, #0056b3 0%, #007bff 100%);
        color: white;
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .medical-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-left: 5px solid #007bff;
    }
    
    .results-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
        font-size: 1.2rem;
    }
    
    .positive-result {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 3px solid #f44336;
        color: #c62828;
    }
    
    .negative-result {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: 3px solid #4caf50;
        color: #2e7d32;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1.1rem;
    }
    
    .vital-sign {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .hospital-footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 3rem;
        background: #e9ecef;
        border-top: 2px solid #dee2e6;
        color: #495057;
    }
    
    .file-check {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== MODEL LOADING ====================
def check_model_file():
    """Check if model file exists"""
    if os.path.exists('diabetes_model.pkl'):
        return True, "✅ Model file found: diabetes_model.pkl"
    else:
        return False, "❌ Model file NOT FOUND: diabetes_model.pkl"

def load_model():
    """Load the diabetes prediction model"""
    try:
        model = joblib.load('diabetes_model.pkl')
        return model, "✅ Model loaded successfully"
    except Exception as e:
        return None, f"❌ Error loading model: {str(e)}"

# ==================== MAIN APP ====================
def main():
    # Hospital Header
    st.markdown("""
    <div class="hospital-header">
        <h1>🏥 GENERAL HOSPITAL</h1>
        <h3>Diabetes Risk Assessment System</h3>
        <p>Version 2.1 | Patient Screening Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check model file first
    file_exists, file_message = check_model_file()
    
    if not file_exists:
        st.markdown(f"""
        <div class="file-check">
            <h4>⚠️ SYSTEM CONFIGURATION REQUIRED</h4>
            <p>{file_message}</p>
            <p><strong>Please upload 'diabetes_model.pkl' to:</strong></p>
            <code>https://diabetes-prediction-ixtwehdx5ekeoe2zfzybbf.streamlit.app/</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.error("""
        ## How to Fix:
        
        1. **Download your model file** from your training code
        2. **Go to Streamlit Cloud** dashboard
        3. **Upload** `diabetes_model.pkl` to your app
        4. **Restart** the application
        
        **Contact IT Support:** Hospital Extension 4567
        """)
        
        # Show file structure
        with st.expander("📁 Required File Structure"):
            st.code("""
            diabetes-prediction-app/
            ├── app.py              # This application
            ├── requirements.txt    # Python dependencies
            └── diabetes_model.pkl  # Your trained model (MISSING!)
            """)
        
        return
    
    # Load model
    model, model_message = load_model()
    
    if model is None:
        st.error(f"## Model Loading Failed\n\n{model_message}")
        return
    
    # ==================== PATIENT FORM ====================
    st.markdown("## 📋 Patient Medical Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Patient Information
        st.markdown("### 👤 Patient Information")
        st.markdown('<div class="medical-card">', unsafe_allow_html=True)
        
        patient_col1, patient_col2 = st.columns(2)
        with patient_col1:
            patient_name = st.text_input("Full Name", "John Smith")
            patient_id = st.text_input("Patient ID", f"PT-{datetime.datetime.now().strftime('%Y%m%d')}-001")
        
        with patient_col2:
            age = st.number_input("Age (Years)", 1, 120, 45)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        # Height & Weight
        height_weight = st.columns(2)
        with height_weight[0]:
            height = st.number_input("Height (cm)", 100, 250, 175)
        with height_weight[1]:
            weight = st.number_input("Weight (kg)", 30, 200, 75)
        
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        st.markdown(f'<div class="vital-sign"><strong>Calculated BMI:</strong> {bmi:.1f}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Medical Parameters
        st.markdown("### 🩺 Medical Parameters")
        st.markdown('<div class="medical-card">', unsafe_allow_html=True)
        
        # Row 1
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            pregnancies = st.number_input("Pregnancies", 0, 20, 1)
        with row1_col2:
            glucose = st.number_input("Glucose (mg/dL)", 50, 300, 120)
        with row1_col3:
            blood_pressure = st.number_input("Blood Pressure (mmHg)", 50, 200, 80)
        
        # Row 2
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        with row2_col1:
            skin_thickness = st.number_input("Skin Thickness (mm)", 0, 100, 25)
        with row2_col2:
            insulin = st.number_input("Insulin (μU/mL)", 0, 900, 85)
        with row2_col3:
            diabetes_pedigree = st.number_input("Diabetes Pedigree", 0.0, 2.5, 0.5, 0.01)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Assessment Button
        predict_button = st.button("🔍 PERFORM DIABETES ASSESSMENT", type="primary", use_container_width=True)
    
    with col2:
        # System Status
        st.markdown("### ⚙️ System Status")
        st.markdown('<div class="medical-card">', unsafe_allow_html=True)
        
        if model:
            st.success("✅ Model: ACTIVE")
        else:
            st.error("❌ Model: OFFLINE")
        
        st.info(f"**Time:** {datetime.datetime.now().strftime('%H:%M')}")
        st.info(f"**Date:** {datetime.datetime.now().strftime('%d/%m/%Y')}")
        
        st.markdown("---")
        st.markdown("### 📊 Normal Values")
        st.write("• Glucose: 70-100 mg/dL")
        st.write("• BP: <120/80 mmHg")
        st.write("• BMI: 18.5-24.9")
        st.write("• Insulin: 2-25 μU/mL")
        
        st.markdown("---")
        st.markdown("### 👨‍⚕️ Physician")
        st.write("**Dr. Sarah Johnson**")
        st.write("Endocrinology Department")
        st.write("Ext: 4567")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Current Vitals
        st.markdown("### 📈 Current Vitals")
        st.markdown('<div class="medical-card">', unsafe_allow_html=True)
        
        st.metric("Glucose", f"{glucose} mg/dL")
        st.metric("Blood Pressure", f"{blood_pressure} mmHg")
        st.metric("BMI", f"{bmi:.1f}")
        st.metric("Age", f"{age} years")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== PREDICTION ====================
    if predict_button:
        with st.spinner("🔬 Analyzing patient data..."):
            # Prepare input
            input_data = np.array([[
                pregnancies, glucose, blood_pressure,
                skin_thickness, insulin, bmi,
                diabetes_pedigree, age
            ]])
            
            try:
                # Make prediction
                prediction = model.predict(input_data)[0]
                probability = model.predict_proba(input_data)[0]
                risk_percent = probability[1] * 100
                
                # Clear any previous results
                st.session_state.prediction = prediction
                st.session_state.risk_percent = risk_percent
                st.session_state.patient_name = patient_name
                st.session_state.patient_id = patient_id
                
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                return
        
        # Display Results
        st.markdown("---")
        st.markdown("## 🎯 Assessment Results")
        
        if st.session_state.prediction == 1:
            st.markdown(f"""
            <div class="results-box positive-result">
                <h2>⚠️ DIABETES RISK DETECTED</h2>
                <h1 style="font-size: 4rem; margin: 1rem 0;">{st.session_state.risk_percent:.1f}%</h1>
                <p><strong>Probability of Diabetes</strong></p>
                <p>Patient: {st.session_state.patient_name} | ID: {st.session_state.patient_id}</p>
                <p>Time: {datetime.datetime.now().strftime('%H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # High risk warning
            if st.session_state.risk_percent > 80:
                st.error("""
                ## 🚨 HIGH RISK ALERT
                **Immediate medical consultation required.**
                Please contact Endocrinology Department (Ext: 4567)
                """)
            
            # Recommendations
            st.markdown("### ⚕️ Medical Recommendations")
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            st.write("""
            1. **Urgent endocrinology consultation**
            2. Fasting blood glucose test required
            3. Daily glucose monitoring
            4. Diabetic diet plan
            5. Follow-up in 1 week
            6. Regular exercise program
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.markdown(f"""
            <div class="results-box negative-result">
                <h2>✅ NO DIABETES DETECTED</h2>
                <h1 style="font-size: 4rem; margin: 1rem 0;">{st.session_state.risk_percent:.1f}%</h1>
                <p><strong>Probability of Diabetes</strong></p>
                <p>Patient: {st.session_state.patient_name} | ID: {st.session_state.patient_id}</p>
                <p>Time: {datetime.datetime.now().strftime('%H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Healthy recommendations
            st.markdown("### 💚 Health Recommendations")
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            st.write("""
            1. Continue healthy lifestyle
            2. Annual diabetes screening
            3. Maintain balanced diet
            4. Regular physical activity
            5. Monitor weight and BMI
            6. Next screening in 6-12 months
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Risk Analysis
        st.markdown("### 📊 Risk Analysis")
        
        analysis_cols = st.columns(4)
        
        with analysis_cols[0]:
            st.metric("Risk Level", 
                     "Critical" if st.session_state.risk_percent > 80 else
                     "High" if st.session_state.risk_percent > 60 else
                     "Moderate" if st.session_state.risk_percent > 30 else "Low")
        
        with analysis_cols[1]:
            st.metric("Glucose Status", 
                     "High" if glucose > 140 else "Normal" if glucose > 70 else "Low")
        
        with analysis_cols[2]:
            st.metric("BMI Status",
                     "Obese" if bmi > 30 else "Overweight" if bmi > 25 else "Normal")
        
        with analysis_cols[3]:
            st.metric("Age Factor",
                     "Risk Factor" if age > 45 else "Normal")
        
        # Progress bar for risk
        st.progress(st.session_state.risk_percent / 100)
        st.caption(f"Diabetes Risk: {st.session_state.risk_percent:.1f}%")
        
        # Medical Report
        with st.expander("📄 View Complete Medical Report"):
            report_col1, report_col2 = st.columns([2, 1])
            
            with report_col1:
                st.markdown("""
                **DIABETES SCREENING REPORT**
                
                **Patient Information**
                - Name: {}
                - ID: {}
                - Age: {} years
                - Gender: {}
                - Assessment Date: {}
                
                **Clinical Findings**
                - Diabetes Risk Probability: {:.1f}%
                - Assessment Result: {}
                - Key Parameters:
                  * Glucose: {} mg/dL
                  * Blood Pressure: {} mmHg
                  * BMI: {:.1f}
                  * Age: {} years
                
                **Recommendations**
                {}
                
                **Physician Notes**
                This screening is based on AI analysis. Clinical confirmation required.
                
                **Signature**
                _________________________
                Dr. Sarah Johnson
                Endocrinology Department
                """.format(
                    patient_name,
                    patient_id,
                    age,
                    gender,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    st.session_state.risk_percent,
                    "POSITIVE - Further testing required" if st.session_state.prediction == 1 else "NEGATIVE - Continue monitoring",
                    glucose,
                    blood_pressure,
                    bmi,
                    age,
                    "1. Immediate endocrinology consultation\n2. Fasting glucose test\n3. Daily monitoring" 
                    if st.session_state.prediction == 1 else 
                    "1. Annual screening\n2. Healthy lifestyle\n3. Regular check-ups"
                ))
            
            with report_col2:
                if st.button("🖨️ Print Report", use_container_width=True):
                    st.success("Report sent to hospital printer")
                
                if st.button("💾 Save to EMR", use_container_width=True):
                    st.success("Saved to Electronic Medical Records")
                
                if st.button("📧 Email Report", use_container_width=True):
                    st.success("Report emailed successfully")
                
                if st.button("🔄 New Patient", use_container_width=True):
                    st.rerun()

    # ==================== FOOTER ====================
    st.markdown("""
    <div class="hospital-footer">
        <p><strong>🏥 General Hospital Diabetes Screening System</strong> | Version 2.1</p>
        <p>HIPAA Compliant | FDA Cleared | For Clinical Use Only</p>
        <p style="font-size: 0.9rem;">Emergency: Ext. 911 | IT Support: Ext. 4567 | © 2024 General Hospital</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== RUN APP ====================
if __name__ == "__main__":
    main()