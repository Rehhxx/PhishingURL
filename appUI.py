# appUI.py
import streamlit as st
import requests
import re
from urllib.parse import urlparse
import pandas as pd
import shap
import matplotlib.pyplot as plt
import numpy as np

# Set page config
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🛡️",
    layout="centered"
)

# Function to extract features from URL
def extract_features_from_url(url):
    features = {}
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Feature 1: sfh - assume phishing if url contains 'data:' or empty
    features["sfh"] = -1 if "data:" in url or url.strip() == "" else 1

    # Feature 2: popupwidnow - very basic check for 'popup'
    features["popupwidnow"] = -1 if "popup" in url.lower() else 1

    # Feature 3: sslfinal_state
    features["sslfinal_state"] = 1 if url.startswith("https") else -1

    # Feature 4: request_url - assume phishing if domain not in path
    features["request_url"] = 1 if domain in url else -1

    # Feature 5: url_of_anchor - assume safe if no suspicious anchor
    features["url_of_anchor"] = 1 if "#" not in url and "@" not in url else -1

    # Feature 6: web_traffic - assume safe for well-known domains
    popular_sites = ["google", "youtube", "facebook", "microsoft", "amazon"]
    features["web_traffic"] = 1 if any(site in domain for site in popular_sites) else -1

    # Feature 7: url_length
    length = len(url)
    if length < 54:
        features["url_length"] = 1
    elif 54 <= length <= 75:
        features["url_length"] = 0
    else:
        features["url_length"] = -1

    # Feature 8: age_of_domain – assume old if domain doesn't contain digits
    features["age_of_domain"] = 1 if not re.search(r'\d', domain) else -1

    # Feature 9: having_ip_address
    ip_pattern = r'(([0-9]{1,3}\.){3}[0-9]{1,3})'
    features["having_ip_address"] = 1 if re.search(ip_pattern, domain) else -1

    print("Extracted Features:", features)  # Debug output
    return features

# Function to predict using the API
def predict_url(url_features):
    try:
        response = requests.post(
            "http://localhost:8000/predict/",
            json=url_features
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure the FastAPI backend is running.")
        return None

# Header
st.title("🛡️ Phishing URL Detector")
st.write("Enter a URL to check if it's legitimate or a phishing attempt.")

# URL Input
url = st.text_input("Enter URL:", placeholder="https://example.com")

# Check button
if st.button("Check URL"):
    if url:
        with st.spinner("Analyzing URL..."):
            # Extract features from URL
            features = extract_features_from_url(url)
            
            # Call API for prediction
            result = predict_url(features)
            
            if result and isinstance(result, dict) and "prediction" in result:
                # Display results
                if result["prediction"] == 1:
                    st.success(f"**Result: {result['prediction_text']}**")
                else:
                    st.error(f"**Result: {result['prediction_text']}**")
    
                # Display probability
                st.write(f"Confidence: {result['probability']*100:.2f}%")

                # Display extracted features
                with st.expander("🔍 View Extracted URL Features"):
                    st.write("Features extracted from URL:")
                    df = pd.DataFrame([features])
                    st.dataframe(df)

                
                # Show SHAP explanation if available
                # Show SHAP explanation if available
                if "shap_values" in result and "feature_names" in result:
                    if len(result["shap_values"]) == len(result["feature_names"]):
                        st.subheader("SHAP Explanation")

                        shap_values = result["shap_values"]

                        # Handle multi-class SHAP values (e.g., binary classification: [[val1, val2], ...])
                        if isinstance(shap_values[0], list):
                            # Option 1: Use the mean of both classes (neutral perspective)
                            shap_values = [np.mean(val) for val in shap_values]
                            # Option 2: Use class 0 values: shap_values = [val[0] for val in shap_values]
                            # Option 3: Use class 1 values: shap_values = [val[1] for val in shap_values]

                        # Create SHAP DataFrame
                        shap_df = pd.DataFrame({
                            "Feature": result["feature_names"],
                            "SHAP Value": shap_values
                        })

                        # Sort by absolute SHAP value for better visual impact
                        shap_df["abs_val"] = np.abs(shap_df["SHAP Value"])
                        shap_df = shap_df.sort_values(by="abs_val", ascending=False)
                        shap_df.drop(columns="abs_val", inplace=True)

                        # Plot SHAP values
                        fig, ax = plt.subplots(figsize=(8, 4))
                        ax.barh(shap_df["Feature"], shap_df["SHAP Value"], color="skyblue")
                        ax.set_xlabel("SHAP Value (Impact on Prediction)")
                        ax.set_title("Top Feature Contributions")
                        ax.invert_yaxis()
                        st.pyplot(fig)

                    else:
                        st.warning("Mismatch between number of SHAP values and feature names.")



    else:
        st.warning("Please enter a URL to check.")

# Information about the app
with st.expander("About this app"):
    st.write("""
    This application uses machine learning to detect phishing URLs. 
    The model analyzes several features of the provided URL to determine if it's legitimate or a phishing attempt.
    
    **How it works:**
    1. Enter a complete URL including http:// or https://
    2. Click "Check URL"
    3. The app will extract features from the URL and send them to the prediction API
    4. Results will show whether the URL is legitimate or potentially malicious
    """)

# Footer
st.markdown("---")
st.markdown("Developed with Streamlit, FastAPI and Machine Learning")