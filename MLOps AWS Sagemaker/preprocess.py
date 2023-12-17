"""Feature engineers the abalone dataset."""
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
    logger.debug("Starting preprocessing.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, required=True)
    args = parser.parse_args()
    
    def download_s3_file(bucket_name, file_key):
        """Download a file from S3 and return its content."""
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        return response['Body'].read().decode('utf-8')
    
    def get_s3_bucket_and_key(s3_url):
        """Extract bucket name and file key from S3 URL."""
        s3_parts = s3_url.replace("s3://", "").split("/")
        bucket_name = s3_parts[0]
        file_key = "/".join(s3_parts[1:])
        return bucket_name, file_key
    
    def process_chunk(chunk):
        # Convert date columns to datetime
        chunk['date_time'] = pd.to_datetime(chunk['date_time'])
        chunk['srch_ci'] = pd.to_datetime(chunk['srch_ci'], errors='coerce')  # Coerce errors in case of invalid dates
        chunk['srch_co'] = pd.to_datetime(chunk['srch_co'], errors='coerce')

        # Example: Create a new column for the length of stay
        # Calculate the number of nights between check-in and check-out
        chunk['length_of_stay'] = (chunk['srch_co'] - chunk['srch_ci']).dt.days

        # Example: Filter rows where the country is a specific value (e.g., '66')
        filtered_chunk = chunk[chunk['user_location_country'] == 66]

        # You can add more processing steps here as needed

        return filtered_chunk

    input_data = f"s3://sagemaker-project-p-2vyfyyymovqz/ExpedisDataset/train.csv"
    # Extract bucket name and file key from the input_data parameter
    logger.info("Extracting bucket name and file key from the input_data parameter")
    bucket, key = get_s3_bucket_and_key(input_data)

    # Download the file content
    logger.info("Download the file content from bucket: %s, key: %s", bucket, key)
    file_content = download_s3_file(bucket, key)
    
    chunk_size = 100000  # Adjust chunk size based on your system's capability
    processed_chunks = []

    for chunk in pd.read_csv(StringIO(file_content), chunksize=chunk_size):
        processed_chunk = process_chunk(chunk)
        processed_chunks.append(processed_chunk)

    # Optionally, combine all processed chunks into one DataFrame
    combined_df = pd.concat(processed_chunks)
    
    train_data = combined_df
    
    train_data['date_time'] = pd.to_datetime(train_data['date_time'])

    # Filter the DataFrame for the year 2014
    train_data_2013 = train_data[train_data['date_time'].dt.year == 2013]
    train_data = train_data[pd.to_datetime(train_data['srch_co']) > pd.to_datetime(train_data['srch_ci'])]
    
    # Data Preprocessing for Collaborative Filtering

    # Selecting relevant columns for Collaborative Filtering
    # Typically, we need user_id, item_id (hotel_cluster in this case), and ratings (implicit or explicit)
    # For this dataset, we'll treat 'is_booking' as an implicit rating (1 for booking, 0 for click)
    cf_data = train_data[['user_id', 'hotel_cluster', 'is_booking']]

    # Checking for missing values
    missing_values = cf_data.isnull().sum()
    
    # Constructing the user-item interaction matrix
    interaction_matrix = cf_data.pivot_table(index='user_id', columns='hotel_cluster', values='is_booking').fillna(0)

    # Splitting the data into train and test sets
    X_train, X_test = train_test_split(interaction_matrix, test_size=0.2, random_state=42)
    
    X_train.to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    X_test.to_csv(f"{base_dir}/test/test.csv", header=False, index=False)
    
