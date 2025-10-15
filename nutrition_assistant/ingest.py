import pandas as pd
import numpy as np
import minsearch



def load_index(data_path='../data/data.csv'):
    df=pd.read_csv('../data/data.csv')
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

