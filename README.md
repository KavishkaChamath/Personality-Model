# Personality Predictor — Introvert vs Extrovert

ML system that predicts whether a person is an **Introvert** or **Extrovert** from 7 behavioral traits. Trained with SVM (~91.7% accuracy), served via a FastAPI REST API, with a Streamlit UI as the frontend.

## Live Links

- **Frontend (UI):** https://personality-model.streamlit.app/
- **Backend API:** https://kavicham98-personality-predictor-api.hf.space

> Free hosting tiers sleep after inactivity — first request may take 10–20s to wake up.

## How It Works

```
Streamlit UI  --POST request-->  FastAPI API  -->  SVM Model  --> Prediction
(Streamlit Cloud)                (Hugging Face Spaces)
```

The API is the single source of truth for inference — it loads the model and returns predictions over HTTP. The UI is a pure frontend that calls the API.

## Test the API directly

```bash
curl -X POST https://kavicham98-personality-predictor-api.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"Time_spent_Alone":4,"Stage_fear":"No","Social_event_attendance":5,"Going_outside":4,"Drained_after_socializing":"No","Friends_circle_size":6,"Post_frequency":4}'
```

**Response:**
```json
{"prediction": "Introvert", "confidence": 87.3}
```

## Features Used

| Feature | Type |
|---|---|
| Time_spent_Alone | Numeric (hrs/day) |
| Stage_fear | Yes/No |
| Social_event_attendance | Numeric (per month) |
| Going_outside | Numeric (days/week) |
| Drained_after_socializing | Yes/No |
| Friends_circle_size | Numeric |
| Post_frequency | Numeric (per week) |

## Project Files

| File | Purpose |
|---|---|
| `personality_notebook.ipynb` | Data preprocessing, model training & evaluation |
| `api.py` | FastAPI backend (deployed on Hugging Face Spaces) |
| `app.py` | Streamlit frontend (deployed on Streamlit Cloud) |
| `personality_model.pkl` | Trained SVM model |
| `label_encoders.pkl` | Encoders for categorical features + target |
| `requirements-api.txt` | Dependencies for the API |
| `requirements.txt` | Dependencies for the UI |
| `Dockerfile` | Container build for Hugging Face Spaces |

## Model

8 algorithms were benchmarked with 5-fold cross-validation; **SVM** was selected as the best performer.

- **Accuracy:** ~91.7%
- **F1 Score:** ~0.92
