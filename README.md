# file-uploader

- Simple file uploader made with Flask
  - files are saved to Amazon S3
  - additional information are saved to Amazon DynamoDB
- prepare `config.cfg` to set environment variables.
    ```
    AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY ID>
    AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET ACCESS KEY>
    AWS_REGION=<YOUR AWS REGION>
    S3_BUCKET=<YOUR AMAZON S3 BUCKET>
    DYNAMODB_TABLE=<YOUR AMAZON DYNAMODB TABLE>
    MAX_CONTENT_LENGTH=10 * 1024 * 1024
    ```
