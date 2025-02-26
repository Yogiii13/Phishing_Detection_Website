from flask import Flask, request, render_template, jsonify
from phishing_detection.model import load_model, predict_url
import os

# Initialize Flask app
app = Flask(__name__)

# Load the model when the app starts
model = load_model()

@app.route('/')
def home():
    """Render the home page with the prediction form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Process the URL and return prediction result.
    Accepts both form submissions and JSON requests.
    """
    if request.is_json:
        # Handle API request
        data = request.get_json()
        url = data.get('url', '')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        result_data = predict_url(model, url)
        return jsonify({
            'url': url,
            'prediction': result_data['result'],
            'probabilities': result_data['probabilities'],
            'is_safe': result_data['result'] == 'Benign',
            'success': True
        })
    else:
        # Handle form submission
        url = request.form.get('url', '')
        if not url:
            return render_template('index.html', error='Please enter a URL')
        
        result_data = predict_url(model, url)
        is_safe = result_data['result'] == 'Benign'
        
        # Calculate percentage confidence for the prediction
        max_probability = max(result_data['probabilities']) * 100
        
        return render_template('result.html', 
                               url=url, 
                               prediction=result_data['result'],
                               is_safe=is_safe,
                               confidence=round(max_probability, 1),
                               probabilities=result_data['probabilities'])

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Dedicated endpoint for API calls."""
    data = request.get_json()
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    result_data = predict_url(model, url)
    is_safe = result_data['result'] == 'Benign'
    
    return jsonify({
        'url': url,
        'prediction': result_data['result'],
        'probabilities': result_data['probabilities'],
        'is_safe': is_safe,
        'message': 'This URL appears safe to visit.' if is_safe else 'This URL may be dangerous. Proceed with caution.',
        'success': True
    })

if __name__ == '__main__':
    # Get port from environment variable for cloud deployment compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)