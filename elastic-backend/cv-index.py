import os
import sys

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

load_dotenv()

es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    verify_certs=False,
)


def index_records(records_path: str):
    """Index records from a CSV file into Elasticsearch.

    This function reads records from a CSV file, performs data cleaning,
    and bulk indexes the records into an Elasticsearch index.

    Args:
        records_path (str): Path to the CSV file containing records to be indexed.
    """

    index_name = os.getenv("INDEX_NAME", "cv-transcriptions")

    # Cleaning of records data before indexing
    records_df = pd.read_csv(records_path)
    for column in records_df.columns:
        records_df[column] = records_df[column].apply(
            lambda x: None if isinstance(x, float) and np.isnan(x) else x
        )

    actions = []
    for _, row in records_df.iterrows():
        action = {"_index": index_name, "_source": row.to_dict()}
        actions.append(action)

    try:
        print(f"Indexing {len(actions)} documents...")
        success, failed = bulk(es, actions)

        print(
            f"Indexing results:\nSuccess: {success} documents\nFailed: {failed} documents"
        )

    except Exception as e:
        print(f"Error bulk indexing {len(actions)} documents: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python elastic-backend/cv-index.py <records_path>")
        sys.exit(1)
    index_records(sys.argv[1])
