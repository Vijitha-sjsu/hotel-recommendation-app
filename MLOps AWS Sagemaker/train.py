import argparse
import logging
import os
import pathlib
import requests
import tempfile

import boto3
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from io import StringIO
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    logger.debug("Starting training.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, required=True)
    args = parser.parse_args()
    
    train_path = "/opt/ml/processing/train/train.csv"
    X_train = pd.read_csv(train_path, header=None)
    test_path = "/opt/ml/processing/test/test.csv"
    X_test = pd.read_csv(test_path, header=None)
    
    
    # Using Truncated SVD for matrix factorization
    n_components = 20  # number of latent factors
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    svd.fit(X_train
            
    # Function to calculate Precision@k and Recall@k
    def precision_recall_at_k(predictions, k=10, threshold=0.5):
        user_est_true = defaultdict(list)
        for uid, user_ratings in predictions.items():
            for est, true_r in user_ratings:
                user_est_true[uid].append((est, true_r))
        precisions = dict()
        recalls = dict()
        for uid, user_ratings in user_est_true.items():
            user_ratings.sort(key=lambda x: x[0], reverse=True)
            n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
            n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
            n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold)) for (est, true_r) in user_ratings[:k])
            precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1
            recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1
        return precisions, recalls

    # Transforming the train and test sets
    X_train_svd = svd.transform(X_train)
    X_test_svd = svd.transform(X_test)
            
    # Reconstruct the test matrix
    X_test_reconstructed = np.dot(X_test_svd, svd.components_)

    # Generate predictions for each user
    predictions = {}
    for i, user_id in enumerate(X_test.index):
        actual_ratings = X_test.iloc[i].values
        predicted_ratings = X_test_reconstructed[i]
        predictions[user_id] = list(zip(predicted_ratings, actual_ratings))
    # Reconstructing the matrices from the factors
    X_train_reconstructed = np.dot(X_train_svd, svd.components_)
    X_test_reconstructed = np.dot(X_test_svd, svd.components_)

    # Calculating RMSE for the reconstructed matrices
    rmse_train = np.sqrt(mean_squared_error(X_train.values, X_train_reconstructed))
    rmse_test = np.sqrt(mean_squared_error(X_test.values, X_test_reconstructed))
            
    rmse_train.to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
