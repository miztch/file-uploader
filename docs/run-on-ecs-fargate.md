# Running with docker-compose: on ECS/Fargate
- First, prepare following AWS resources in advance.
  - VPC and Subnet
  - ECS Cluster
    - ECS Task Role
    - ECS Task Execution Role

 With [CloudFormation template](../cloudformation/ecs-cluster-fargate.yml), You can create ECS Cluster into existing VPC.

- Download [Amazon ECS CLI](https://github.com/aws/amazon-ecs-cli) and configure.
```shell-session
$ sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
$ sudo chmod +x /usr/local/bin/ecs-cli

$ ecs-cli configure --region <AWS_REGION> --cluster <ECS_CLUSTER_NAME>
```

- Modify `ecs-params-fargate.yml` .
  - You can require some values from CloudFormation stack outputs.
```yml
  task_role_arn: <ECS_TASK_ROLE_ARN>
  task_execution_role: <ECS_TASK_EXECUTION_ROLE_NAME>
```

```yml
    awsvpc_configuration:
      subnets:
        - <SUBNET_ID>        
      security_groups:
        - <FARGATE_TASK_SECURITY_GROUP_ID>
```

- Run `ecs-cli compose up`.
  - For further options, see [README.md of aws/amazon-ecs-cli](https://github.com/aws/amazon-ecs-cli/blob/mainline/README.md)
```shell-session
$ mv ecs-params-fargate.yml ecs-params.yml
$ ecs-cli compose up --launch-type FARGATE
```

- Check status.
```shell-session
$ ecs-cli compose ps
Name                                               State    Ports               TaskDefinition   Health
fileuploader/0123456789aaaabbbbccccddddeeeeff/app  RUNNING                      file-uploader:1  UNKNOWN
fileuploader/0123456789aaaabbbbccccddddeeeeff/web  RUNNING  x.x.x.x:80->80/tcp  file-uploader:1  UNKNOWN
```

- View Application on browser.
  - You can see your endpoint(public IP of the Fargate task) on the following URL.

> https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/<CLUSTER_NAME>/tasks

## tips
### scaling tasks
```shell-session
$ ecs-cli compose scale 2
$ ecs-cli compose ps
Name                                               State    Ports               TaskDefinition   Health
fileuploader/0123456789aaaabbbbccccddddeeeeff/app  RUNNING                      file-uploader:1  UNKNOWN
fileuploader/0123456789aaaabbbbccccddddeeeeff/web  RUNNING  x.x.x.x:80->80/tcp  file-uploader:1  UNKNOWN
fileuploader/0123456789aaaabbbbccccddddeeeeff/web  RUNNING  y.y.y.y:80->80/tcp  file-uploader:1  UNKNOWN
fileuploader/0123456789aaaabbbbccccddddeeeeff/app  RUNNING                      file-uploader:1  UNKNOWN
```

### container logging
- you can put logs into CloudWatch Logs with modifying `ecs-params-fargate.yml`
  - see: https://github.com/aws/amazon-ecs-cli/blob/mainline/README.md#viewing-container-logs
