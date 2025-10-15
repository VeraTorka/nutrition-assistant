import os
import pandas as pd
import numpy as np
import minsearch

DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")

def load_index(data_path=DATA_PATH):
    df=pd.read_csv(data_path)
    documents=df.to_dict(orient='records')
    index = minsearch.Index(
        text_fields=[
            "food", 
            "allergens"
            ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index

