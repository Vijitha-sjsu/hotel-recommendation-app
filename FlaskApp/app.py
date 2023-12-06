from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Load the model and preprocessor
model = joblib.load('tuned_ensemble_model.joblib')
preprocessor = joblib.load('preprocessor.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Log the request
        print("Received request: ", request.get_json())

        data = request.get_json()
        input_df = pd.DataFrame([data])
        preprocessed_input = preprocessor.transform(input_df)

        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(preprocessed_input)
            top5_indices = np.argsort(probabilities, axis=1)[:, -5:]
            top5_indices = np.fliplr(top5_indices)
            top5_labels = [model.classes_[indices] for indices in top5_indices][0]
            return jsonify({'top5_recommendations': top5_labels.tolist()})
        else:
            prediction = model.predict(preprocessed_input)
            return jsonify({'prediction': prediction.tolist()})

    except Exception as e:
        print("An error occurred: ", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
