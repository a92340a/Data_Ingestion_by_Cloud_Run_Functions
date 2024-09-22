# Data Ingestion by Cloud Run Functions
## Description
Using Cloud Run Functions to deploy data ingestion service. 
The function supports three types of input files: CSV, Parquet, and JSON Lines (TXT).

## Scenario
The function with specific gcs path can be tiggered with HTTP request, and ingesting data into the destination of BigQuery dataset.

## Limitation


## Request Format
The HTTP request should be a JSON object with the following fields:

- `input`: The GCS path to the input file.
- `project_id`: The Google Cloud project ID.
- `dataset`: The BigQuery dataset name.
- `table`: The BigQuery table name.
- `overwrite`: A boolean indicating whether to overwrite the existing table or append to it.

Example Request:
```
{
    "input": "gs://na_data_internal/sample_file/sample_data.csv",
    "project_id": "tw-rd-de-finn",
    "dataset": "data_ingestion_demo",
    "table": "csv_output",
    "overwrite": true
}
```
```
{
    "input": "gs://na_data_internal/sample_file/sample_data.txt",
    "project_id": "tw-rd-de-finn",
    "dataset": "data_ingestion_demo",
    "table": "json_output",
    "overwrite": true
}
```
```
{
    "input": "gs://na_data_internal/sample_file/sample_data.parquet",
    "project_id": "tw-rd-de-finn",
    "dataset": "data_ingestion_demo",
    "table": "parquet_output",
    "overwrite": true
}
```

## Supported File Formats
1. CSV
If the input file is a CSV, the function reads the file using pandas.read_csv.
2. Parquet
If the input file is a Parquet file, the function reads the file using pandas.read_parquet.
3. JSON Lines (TXT)
If the input file is a JSON Lines file (with a .txt extension), the function reads the file using pandas.read_json with the lines=True parameter.

## Deployment
```
gcloud functions deploy data_ingestion_function --region asia-east1 \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point main \
    --gen2 
```