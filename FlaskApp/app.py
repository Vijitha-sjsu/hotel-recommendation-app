from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
import logging
import traceback

app = Flask(__name__)

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')
logging.info("Model Path" + str(model_path))
# model_path = ''

model = joblib.load(os.path.join(model_path, 'tuned_ensemble_model.joblib'))
preprocessor = joblib.load(os.path.join(model_path, 'preprocessor.joblib'))
logging.info("tuned_ensemble Model: " + str(model))


@app.route('/ping', methods=['GET'])
def ping():
    try:
        health = model is not None
        status = 200 if health else 404
        return jsonify({'status': 'ok'}), status
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/invocations', methods=['POST'])
def predict():
    try:
        # Log the request
        # print("Received request: ", request.get_json())

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
    app.run(debug=False, host='0.0.0.0', port=8080)