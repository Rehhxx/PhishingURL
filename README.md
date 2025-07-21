# Phishing Detection Project

This project provides a complete solution for detecting phishing websites using machine learning. It includes:
- A FastAPI backend for prediction and explainability
- A Streamlit web UI for user-friendly interaction
- Scripts for model training and testing

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the FastAPI Backend](#running-the-fastapi-backend)
- [Running the Streamlit UI](#running-the-streamlit-ui)
- [API Usage](#api-usage)
- [Model Training & Testing](#model-training--testing)
- [Notes](#notes)
- [License](#license)

---

## Features
- **Phishing Detection API**: Predicts if a website is legitimate or phishing based on URL features.
- **Explainability**: Uses SHAP to provide feature importance for each prediction.
- **Streamlit UI**: User-friendly web interface for entering URLs and visualizing results.
- **Model Training & Testing Scripts**: Easily retrain or evaluate the model with your own data.

## Project Structure
```
app.py                # FastAPI backend (main API)
appUI.py              # Streamlit web UI
models/
  RFC_best_model.pkl  # Pre-trained Random Forest model
  background_sample.csv # Background data for SHAP
  model_training.py   # Model training script
  model_test.py       # Model testing script
data/
  Website Phishing.csv # Dataset
requirments.txt        # Python dependencies
start_app.bat          # Batch file to start the app
```

## Setup Instructions
1. **Clone the repository** and navigate to the project directory.
2. **Create and activate a virtual environment** (recommended):
   ```powershell
   python -m venv myenv
   .\myenv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirments.txt
   ```

---

## Running the FastAPI Backend
Start the API server:
```powershell
python app.py
```
The API will be available at [http://localhost:8000](http://localhost:8000).
Visit `/docs` for interactive API documentation.

## Running the Streamlit UI
Launch the web interface:
```powershell
streamlit run appUI.py
```
This opens a browser window for user-friendly phishing detection and SHAP visualizations.

---

## API Usage
### Predict Endpoint
- **POST** `/predict/`
- **Request Body Example:**
  ```json
  {
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
  ```
- **Response Example:**
  ```json
  {
    "prediction": 0,
    "prediction_text": "Phishing",
    "probability": 0.95,
    "shap_values": [...],
    "feature_names": ["sfh", "popupwidnow", ...]
  }
  ```

### Health Check
- **GET** `/health`
- **Response:** `{ "status": "healthy" }`

---

## Model Training & Testing

### Training the Model
Edit and run `models/model_training.py` to retrain the Random Forest model on your data. The script loads the dataset, preprocesses it, performs train/test split, and saves the trained model as `RFC_best_model.pkl`.

### Testing the Model
Use `models/model_test.py` to analyze the dataset, print statistics, and check class balance.

---

## Notes
- The model and background data must be present in the `models/` directory for both API and UI to work.
- Use `/docs` for interactive API documentation and testing.
- The Streamlit UI (`appUI.py`) extracts features from URLs and communicates with the FastAPI backend for predictions and SHAP explanations.

## License
This project is for educational purposes.
