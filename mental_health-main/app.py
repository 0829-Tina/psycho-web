import streamlit as st
import requests

st.set_page_config(
    page_title="Mental Health Outcome Predictor",
    page_icon="🧠",
    layout="wide",
)

st.title("🌱 心理健康小助手")
user_input = st.text_area("请描述你最近的心理困扰：", height=150)
if st.button("获取建议"):
    if not user_input.strip():
        st.warning("输入不能为空哦")
    else:
        with st.spinner("正在生成建议，请稍候..."):
            resp = requests.post(
                "http://localhost:5000/chat",
                json={"message": user_input},
                timeout=30
            )
        if resp.status_code == 200:
            st.success("已生成建议")
            st.write(resp.json()["reply"])
        else:
            st.error("后端调用失败，请检查终端日志")

import streamlit as st
import numpy as np
import pickle  

# Set Streamlit page configuration (move this to the very top)

# Load the trained model with error handling
def load_model():
    try:
        # Open the model file in binary mode and then load it
        with open('./random_forest_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None
    
rf_model = load_model()

# Maximum observed values in the dataset (used for scaling)
max_values = np.array([0.462045, 1.506730, 1.031688, 8.624634, 3.700000, 7.645899, 4.700000])

# Add a custom background color
def add_custom_style():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f8ff;
            color: #333;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_style()

def main():
    """
    Streamlit interface for predicting mental health outcomes.
    """
    # Title and description
    st.markdown("# 🧠 Mental Health Outcome Prediction")
    st.markdown(
        """
        ### 📊 Predict Disability-Adjusted Life Years (DALYs)
        This app predicts mental health outcomes based on the prevalence of disorders in the population. 
        Adjust the sliders to input your data and click **Predict** to see the results!
        """
    )

    # Sidebar for input sliders
    with st.sidebar:
        st.markdown("## 🎚️ Adjust Parameters")
        schizophrenia = st.slider("Schizophrenia disorders (%):", 0.0, 100.0, 10.0)
        bipolar = st.slider("Bipolar disorders (%):", 0.0, 100.0, 10.0)
        eating_disorders = st.slider("Eating disorders (%):", 0.0, 100.0, 10.0)
        anxiety = st.slider("Anxiety disorders (%):", 0.0, 100.0, 10.0)
        drug_use = st.slider("Drug use disorders (%):", 0.0, 100.0, 10.0)
        depression = st.slider("Depressive disorders (%):", 0.0, 100.0, 10.0)
        alcohol_use = st.slider("Alcohol use disorders (%):", 0.0, 100.0, 10.0)

    # Collect user inputs
    user_values = np.array([schizophrenia, bipolar, eating_disorders, anxiety, drug_use, depression, alcohol_use])

    # Scale the inputs to match the model's range
    features = (user_values / 100) * max_values

    # Predict button
    st.markdown("## 🎯 Results")
    if st.button("Predict"):
        if rf_model is not None:
            prediction = rf_model.predict([features])
            st.success(f"Predicted Disability-Adjusted Life Years (DALYs): {prediction[0]:.2f}%")
            st.markdown(
                f"""
                ### 📈 Prediction Breakdown
                - **Schizophrenia disorders:** {schizophrenia}%  
                - **Bipolar disorders:** {bipolar}%  
                - **Eating disorders:** {eating_disorders}%  
                - **Anxiety disorders:** {anxiety}%  
                - **Drug use disorders:** {drug_use}%  
                - **Depressive disorders:** {depression}%  
                - **Alcohol use disorders:** {alcohol_use}%  
                """
            )
        else:
            st.error("Model could not be loaded. Please try again later.")

if __name__ == "__main__":
    main()
