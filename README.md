# file-uploader (WIP)

Simple file uploader made with Flask
- files are saved to Amazon S3
- additional information are saved to Amazon DynamoDB
- use instance IAM Role

## docker-compose
You can use `docker-compose.yml` to deploy.
- Prepare AWS resources in advance. They should be in the same region.
  - S3 bucket: to store uploaded files.
  - DynamoDB Table: to store information for files.
    - Partition Key: `file_id` (String)

- Set environment variables in `docker-compose.yml` .
  ```yml
    environment:
      - AWS_REGION=us-east-1
      - S3_BUCKET=<YOUR AMAZON S3 BUCKET>
      - DYNAMODB_TABLE=<YOUR AMAZON DYNAMODB TABLE>
  ```