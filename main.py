import pandas as pd
from google.cloud import bigquery
import logging
import functions_framework

logger = logging.getLogger(__name__)

# Example Request
# {
#     "input": "gs://na_data_internal/sample_file/sample_data.csv",
#     "project_id": "tw-rd-de-finn",
#     "dataset": "data_ingestion_demo",
#     "table": "csv_output",
#     "overwrite": true
# }


def read_data(filepath):
    # read data
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".json") or filepath.endswith(".txt"):
        df = pd.read_json(filepath, lines=True)
    elif filepath.endswith(".parquet"):
        df = pd.read_parquet(filepath)
    else:
        logging.warning("No corresponding input types!")
    logging.info(f"Successfully Read data from {filepath}.")

    # transform data into string
    df.astype("str")
    return df


def load_data(df, table_id, job_config):
    # write dataframe to bigquery
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, destination=table_id, job_config=job_config)
    job.result()  # Wait for the job to complete.
    logging.info("Successfully loaded {df.shape[0]} rows of data into {table_id}.")


@functions_framework.http
def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object with ingestion details.
    """
    request_json = request.get_json(silent=True)

    # parse requests
    if request_json:
        filepath = request_json["input"]
        project_id = request_json["project_id"]
        dataset = request_json["dataset"]
        table = request_json["table"]
        overwrite = request_json["overwrite"]
    else:
        logger.error("No valid json request!")

    # read data
    df = read_data(filepath)

    # load data
    table_id = f"{project_id}.{dataset}.{table}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE" if overwrite == True else "WRITE_APPEND",
    )
    load_data(df, table_id, job_config)

    return "Finished the data ingestion function job."
