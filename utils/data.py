from typing import Tuple
import joblib

import pandas as pd
from scipy.sparse import csr_matrix 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if 'sentiment' in df.columns:
        df["label"] = pd.factorize(df["sentiment"])[0]
        
    return df

def split_data(
    df: pd.DataFrame,
    test_size: float    
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=2024,
        stratify=df["sentiment"] if "sentiment" in df.columns else df["label"]
    )
    
    return train_df, test_df

def preprocess_data(
    train_df: pd.DataFrame, 
    test_df: pd.DataFrame
) -> Tuple[csr_matrix, csr_matrix, TfidfVectorizer]:
    vectorizer = TfidfVectorizer(stop_words="english")
    train_inputs = vectorizer.fit_transform(train_df["review"])
    test_inputs = vectorizer.transform(test_df["review"])
    
    return train_inputs, test_inputs, vectorizer
    