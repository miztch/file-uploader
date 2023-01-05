# file-uploader

Simple file uploader made with Flask
- files are saved to Amazon S3
- additional information are saved to Amazon DynamoDB
- use instance IAM Role

## How to deploy

- Prepare AWS resources in advance. They should be in the same region.
  - S3 bucket: to store uploaded files.
  - DynamoDB Table: to store information for files.
    - Partition Key: `file_id` (String)

- You can use `docker-compose.yml` to deploy.
  - Set environment variables in `docker-compose.yml` .
    ```yml
      environment:
        - AWS_REGION=<AWS_REGION>
        - S3_BUCKET=<YOUR AMAZON S3 BUCKET>
        - DYNAMODB_TABLE=<YOUR AMAZON DYNAMODB TABLE>
    ```

- You can also deploy on Amazon ECS. see the followings:
  - [Running on ECS/EC2](docs/run-on-ecs-ec2.md)
  - [Running on ECS/Fargate](docs/run-on-ecs-fargate.md)