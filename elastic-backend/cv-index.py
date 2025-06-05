import argparse
import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

load_dotenv()

es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")),
    verify_certs=False,
)


def index_records(records_path: str, index_name: str):
    """Index records from a CSV file into Elasticsearch.

    This function reads records from a CSV file, performs data cleaning,
    and bulk indexes the records into an Elasticsearch index.

    Args:
        records_path (str): Path to the CSV file containing records to be indexed.
        index_name (str): The name of the index in the elastic search cluster.
    """

    # Verify index exists and get mappings
    if not es.indices.exists(index=index_name):
        raise ValueError(f"Index '{index_name}' does not exist")

    mappings = es.indices.get_mapping(index=index_name)[index_name]["mappings"]
    records_df = pd.read_csv(records_path)

    missing_fields = set(mappings["properties"].keys()) - set(records_df.columns)
    if missing_fields:
        raise ValueError(
            f"Records dataframe is missing required fields defined in index mapping: {missing_fields}"
        )

    # Cleaning of records data before indexing
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "records_path",
        type=str,
        help="Path to the CSV file containing records to be indexed",
    )
    parser.add_argument(
        "--index-name",
        type=str,
        default=os.getenv("INDEX_NAME", "cv-transcriptions"),
        help="The name of the existing index in the Elasticsearch cluster. Defaults to INDEX_NAME env variable or 'cv-transcriptions'.",
    )
    args = parser.parse_args()
    index_records(
        records_path=args.records_path,
        index_name=args.index_name,
    )
