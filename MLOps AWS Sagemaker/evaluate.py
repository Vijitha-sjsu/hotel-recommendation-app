"""Evaluation script for measuring mean squared error."""
import json
import logging
import pathlib
import pickle
import tarfile

import numpy as np
import pandas as pd
import xgboost

from sklearn.metrics import mean_squared_error

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())



if __name__ == "__main__":
    logger.debug("Starting evaluation.")
    model_path = "/opt/ml/processing/model/model.tar.gz"
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")

    logger.debug("Calculating mean squared error.")
    train_path = "/opt/ml/processing/train/train.csv"
    rmse_train = pd.read_csv(train_path, header=None)
    report_dict = {
        "regression_metrics": {
            "mse": {
                "value": rmse_train
            },
        },
    }

    output_dir = "/opt/ml/processing/evaluation"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    logger.info("Writing out evaluation report with mse: %f", mse)
    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        f.write(json.dumps(report_dict))
