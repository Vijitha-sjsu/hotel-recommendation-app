from flask_cors import CORS
from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the trained model
model = load('hotel_recommendation_model.joblib')

# Function to preprocess input data
def preprocess_input(data):
    df = pd.DataFrame([data])
    # No need for date_time and PCA-transformed destination data
    # Assuming these are the only features used in training
    return df

@app.route('/recommend', methods=['POST'])
def recommend_hotels():
    try:
        data = request.json
        print("Received data:", data)  # Log the received data
        # Preprocess the input data
        processed_data = preprocess_input(data)

        # Get the top N predictions
        top_n = 5  # Change this to get more or fewer recommendations
        probabilities = model.predict_proba(processed_data)[0]
        top_n_predictions = probabilities.argsort()[-top_n:][::-1]
        
        # Return the response with top N hotel recommendations
        response = jsonify({'hotel_recommendations': top_n_predictions.tolist()})

        print("Predictions:", response)  # Log the predictions

        return response
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
