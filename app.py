# app.py
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import shap

# Load the Random Forest model
with open('models/RFC_best_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define feature names
feature_names = [
    "sfh", "popupwidnow", "sslfinal_state", "request_url", "url_of_anchor",
    "web_traffic", "url_length", "age_of_domain", "having_ip_address"
]

# Load background data for SHAP
background_data = pd.read_csv('models/background_sample.csv')

# Initialize SHAP TreeExplainer with background
explainer = shap.TreeExplainer(model, background_data)

# Create FastAPI app
app = FastAPI(
    title="Phishing Detection API",
    description="API for detecting phishing websites based on URL features",
    version="1.0.0"
)

# Define the input schema using Pydantic
class URLFeatures(BaseModel):
    sfh: int  
    popupwidnow: int  
    sslfinal_state: int  
    request_url: int 
    url_of_anchor: int  
    web_traffic: int  
    url_length: int  
    age_of_domain: int  
    having_ip_address: int  
    
    class Config:
        schema_extra = {
            "example": {
                "sfh": -1,
                "popupwidnow": 0,
                "sslfinal_state": -1,
                "request_url": -1,
                "url_of_anchor": -1,
                "web_traffic": 0,
                "url_length": -1,
                "age_of_domain": -1,
                "having_ip_address": 1
            }
        }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phishing Detection API. Use /docs to view the API documentation."}

@app.post("/predict/")
async def predict_url(features: URLFeatures):
    try:
        df = pd.DataFrame([features.model_dump()])
        prediction = model.predict(df)[0]

        # Get prediction probabilities safely
        probabilities = model.predict_proba(df)[0]
        if len(probabilities) == 2:
            probability = probabilities[prediction]
        else:
            probability = float(probabilities[0])

        # SHAP explanation
        shap_values = explainer.shap_values(df)

        if isinstance(shap_values, list):
            shap_value = shap_values[prediction][0].tolist()  # For binary classification
        else:
            shap_value = shap_values[0].tolist()  # If SHAP returns just a single array

        return {
            "prediction": int(prediction),
            "prediction_text": "Legitimate" if prediction == 1 else "Phishing",
            "probability": float(probability),
            "shap_values": shap_value,
            "feature_names": df.columns.tolist()
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)