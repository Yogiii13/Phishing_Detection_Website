# Phishing_Detection_Website

A web application that uses machine learning to analyze URLs and detect potential phishing websites.

## Features

- URL analysis for phishing detection
- Web interface for easy interaction
- API endpoints for integration with other applications
- Classification into three categories: Phishing, Benign, and Defacement
- Confidence level display for predictions

## Project Structure

```
phishing-detector/
├── app.py                         # Flask application entry point
├── phishing_detection/
│   ├── __init__.py
│   ├── model.py                   # Model loading and prediction logic
│   └── phishing_model.pkl         # Pre-trained Random Forest model
└── templates/
    ├── index.html                 # Home page with URL input form
    └── result.html                # Results page showing prediction
```

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install flask numpy scikit-learn joblib
```

3. Run the application:

```bash
python app.py
```

## Usage

### Web Interface

1. Navigate to `http://localhost:5000` in your web browser
2. Enter a URL to analyze
3. View the detailed analysis results

### API

The application offers two API endpoints:

#### Standard Prediction Endpoint

```
POST /predict
Content-Type: application/json
```

Request body:
```json
{
  "url": "https://example.com"
}
```

Response:
```json
{
  "url": "https://example.com",
  "prediction": "Benign",
  "probabilities": [0.05, 0.92, 0.03],
  "is_safe": true,
  "success": true
}
```

#### Dedicated API Endpoint

```
POST /api/predict
Content-Type: application/json
```

Request body:
```json
{
  "url": "https://example.com"
}
```

Response:
```json
{
  "url": "https://example.com",
  "prediction": "Benign",
  "probabilities": [0.05, 0.92, 0.03],
  "is_safe": true,
  "message": "This URL appears safe to visit.",
  "success": true
}
```

## How It Works

The application uses a Random Forest model trained to identify phishing URLs based on 18 features extracted from each URL:

- URL length
- Type ratio (digits to total characters)
- Special character counts (@, ?, -, =, ., $, !, *, ,, //)
- Presence of abnormal URL patterns
- HTTPS usage
- Digit and letter counts
- Text encoding usage

## Deployment

The application is configured to work with cloud platforms that use the PORT environment variable. To deploy:

1. Set the PORT environment variable if needed
2. Ensure the phishing_model.pkl file is included in your deployment
3. Configure the web server to point to app.py

## Limitations

- No prediction is 100% guaranteed
- The model effectiveness depends on the training data
- New phishing techniques may not be detected
- Always exercise caution when visiting unknown websites
