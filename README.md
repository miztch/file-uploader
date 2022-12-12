# file-uploader (WIP)

- Simple file uploader made with Flask
  - files are saved to Amazon S3
  - additional information are saved to Amazon DynamoDB
- prepare `instance/config.cfg`.
  - `AWS_ACCESS_KEY_ID` `AWS_SECRET_ACCESS_KEY` `AWS_REGION` are not needed if you use IAM Role.
  ```
  AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY ID>
  AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET ACCESS KEY>
  AWS_REGION=<YOUR AWS REGION>
  MAX_CONTENT_LENGTH=10 * 1024 * 1024
  ```
- set environment variables.
  ```
  export S3_BUCKET=<YOUR AMAZON S3 BUCKET>
  export DYNAMODB_TABLE=<YOUR AMAZON DYNAMODB TABLE>
  ```