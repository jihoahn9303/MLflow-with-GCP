import os

import numpy as np
import mlflow
import joblib
import hydra
from sklearn.base import BaseEstimator
from mlflow.models.signature import infer_signature
from mlflow.pyfunc import log_model
from hydra.utils import instantiate
from dotenv import load_dotenv

from src.trainer import evaluate
from src.model import SentimentClassifier
from config.config_schema import Config, setup_config
from utils.data import (
    load_data,
    split_data,
    preprocess_data
)

# load environment variable in .env file
load_dotenv()
np.random.seed(2024)


def train_model_and_save_artifacts(configuration: Config):
    # instantiate model for sentiment analysis
    model: BaseEstimator = instantiate(configuration.model)
    
    # load data
    df = load_data(path='./data/imdb-dataset.csv')
    
    # split data
    train_df, test_df = split_data(df, test_size=0.3)
    
    # preprocess data & serialize vectorizer
    train_inputs, test_inputs, vectorizer = preprocess_data(train_df, test_df)
    joblib.dump(vectorizer, "vectorizer.joblib")
    
    # set tracking server
    MLFLOW_SERVER_PORT = os.environ["MLFLOW_SERVER_PORT"]
    mlflow.set_tracking_uri(f"http://localhost:{MLFLOW_SERVER_PORT}")
    mlflow.set_experiment("sentiment-analysis")
    
    # train & validate model + log artifacts
    with mlflow.start_run():
        # train and serialize model
        model.fit(train_inputs, train_df["label"].values)
        joblib.dump(model, "model.joblib")
        
        # evaluate model and make confusion matrix figure
        f1_score, figure = evaluate(
            model=model,
            test_inputs=test_inputs,
            test_labels=test_df["label"].values,
            class_names=test_df["sentiment"].unique().tolist()
        )
        figure.savefig("confusion_matrix.png")
        print("F1 score: ", f1_score)
        
        # log artifacts(including artifact)
        # https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html#mlflow.sklearn.log_model
        mlflow.log_figure(figure, "confusion_matrix.png")
        mlflow.log_metric(key='f1_score', value=f1_score)
        mlflow.log_params(model.get_params())
        
        signature = infer_signature(
            model_input={
                "review": test_inputs.toarray()
            },
            model_output=model.predict(test_inputs)
        )
        
        sentiment_classifier = SentimentClassifier()
        artifacts = {
            'vectorizer': "./vectorizer.joblib",
            'model': "./model.joblib",
        }
        
        log_model(
            artifact_path="model",
            python_model=sentiment_classifier,
            artifacts=artifacts,
            signature=signature,
            conda_env="./conda.yaml",
            registered_model_name="basic-sentiment-classifier"
        )
        
@hydra.main(config_name="config_schema", version_base="1.2")
def main(config: Config):
    train_model_and_save_artifacts(configuration=config)
    
    
if __name__ == "__main__":
    setup_config()
    main()