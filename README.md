# Data Ingestion by Cloud Run Functions
## Description
Using Cloud Run Functions to deploy data ingestion service. 
The function supports three types of input files: CSV, Parquet, and JSON Lines (TXT).

## Scenarios and limitations
The function with specific gcs path can be tiggered with HTTP request, and ingesting data into the destination of BigQuery dataset.

You can use cloud run functions to implement data ingestion as the scenarios are much simpler with one managed machine:
1. Resource Limits: 32 GiB memory per function, and so on.
2. Time Limits: 60 minutes for HTTP functions, and 9 minutes for event-driven functions.

[More information about quota and limitation](https://cloud.google.com/functions/quotas)

## Architecture
![arch](image/data_ingestion_function_architecture.jpg)

## Permission
- service account of Cloud Run Functions need to be granted `storage.object.list`

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
1. Manual deployment
    ```
    gcloud functions deploy data_ingestion_function --region asia-east1 \
        --runtime python311 \
        --trigger-http \
        --allow-unauthenticated \
        --entry-point main \
        --gen2 
    ```
2. Continuous deployment
As pushing new commit to remote repository, there is trigger to continuous deployment with via Cloud Build. More setting please refer to `cloudbuild.yaml`

## Demo with postman
1. Sent ingestion request by postman.
    ![header](image/data_ingestion_function_postman_header.png)
    ![body](image/data_ingestion_function_postman_body.png)
2. Checked the output table after the ingestion was done.
    ![output](image/data_ingestion_function_output.png)
