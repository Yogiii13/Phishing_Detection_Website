import joblib
import numpy as np
from urllib.parse import urlparse

# Function to load the pre-trained model
def load_model():
    """
    Load the trained Random Forest model.
    """
    return joblib.load('phishing_detection/phishing_model.pkl')

# Function to extract features from a URL
def extract_features(url):
    """
    Extract features from a URL for prediction, matching the training data format.
    Args:
        url (str): The URL to analyze.
    Returns:
        numpy.ndarray: Array of extracted features.
    """
    parsed_url = urlparse(url)
    
    # Calculate type ratio
    total_chars = len(url)
    digit_count = sum(char.isdigit() for char in url)
    letter_count = sum(char.isalpha() for char in url)
    type_ratio = digit_count / total_chars if total_chars > 0 else 0
    
    # Check for abnormal URL
    abnormal_url = 0
    if parsed_url.netloc and ('.' not in parsed_url.netloc or '@' in parsed_url.netloc):
        abnormal_url = 1
    
    # Check for text encoding
    has_text_encoding = 0
    if '%' in url and any(f'%{h}' in url.lower() for h in '0123456789abcdef'):
        has_text_encoding = 1
    
    # Extract 18 features exactly as expected by the model
    features = [
        len(url),                          # URL_Length
        type_ratio,                        # type_ratio
        url.count('@'),                    # @ count
        url.count('?'),                    # ? count
        url.count('-'),                    # - count
        url.count('='),                    # = count
        url.count('.'),                    # . count
        url.count('$'),                    # $ count
        url.count('!'),                    # ! count
        url.count('*'),                    # * count
        url.count(','),                    # , count
        url.count('//'),                   # // count
        abnormal_url,                      # Abnormal_URL
        int(parsed_url.scheme == 'https'), # Has_HTTPS
        digit_count,                       # Digit_Count
        letter_count,                      # Letter_Count
        has_text_encoding,                 # Has_Text_Encoding
        0,                                 # Placeholder for the 18th feature (adjust if needed)
    ]
    
    return np.array(features)

# Function to predict phishing status
def predict_url(model, url):
    """
    Predict if the given URL is phishing, benign, or defacement.
    Args:
        model: The loaded machine learning model.
        url (str): The URL to analyze.
    Returns:
        dict: Classification result and probabilities
    """
    features = extract_features(url)  # Extract features
    
    # Get prediction and probabilities
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    
    # Map numeric prediction to category (fixed mapping)
    if prediction == 0:
        result = 'Phishing'
    elif prediction == 1:
        result = 'Benign'
    else:  # prediction == 2
        result = 'Defacement'
    
    # Return both the result and the probabilities
    return {
        'result': result,
        'probabilities': probabilities.tolist(),
        'raw_prediction': int(prediction),
        'extracted_features': features.tolist(),
        'feature_count': len(features)
    }