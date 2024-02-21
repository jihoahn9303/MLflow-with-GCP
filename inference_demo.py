import os

import mlflow
import mlflow.pyfunc
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

MLFLOW_SERVER_PORT = os.environ["MLFLOW_SERVER_PORT"]


if __name__ == "__main__":
    model = mlflow.pyfunc.load_model(
        model_uri="gs://sentiment-analysis-prac/1/811e19ddd9c1438bad841647f0999b34/artifacts/model"
    )
    unwrapped_model = model.unwrap_python_model()  
    df = pd.DataFrame(
        data=[["Hi! How are you?"], ["You are so stupid!"], ["Story for this movie is really amazing!"]],
        columns=["review"]
    )
    
    # predictions = model.predict(data=df)
    predictions = unwrapped_model.custom_predict(input_df=df)
    predictions = list(map(lambda x: 'positive' if x == 0 else 'negative', predictions))

    print(predictions)