import json
import boto3
from secret_keys import SecretKeys
from urllib.parse import unquote_plus

secret_keys = SecretKeys()
sqs_client = boto3.client(
    "sqs",
    region_name=secret_keys.AWS_REGION,
)

ecs_client = boto3.client(
    "ecs",
    region_name=secret_keys.AWS_REGION,
)


def poll_sqs():
    while True:
        response = sqs_client.receive_message(
            QueueUrl=secret_keys.RAW_VIDEO_PROCESSING_QUEUE,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )
        for message in response.get("Messages", []):
            message_body = json.loads(message.get("Body"))
            if (
                "Service" in message_body
                and "Event" in message_body
                and message_body.get("Event") == "s3:TestEvent"
            ):
                sqs_client.delete_message(
                    QueueUrl=secret_keys.RAW_VIDEO_PROCESSING_QUEUE,
                    RecieptHandle=message["RecieptHandle"],
                )
                continue
            if "Records" in message_body:
                s3_record = message_body["Records"][0]["s3"]
                bucket_name = s3_record["bucket"]["name"]
                s3_key = s3_record["object"]["key"]
                decoded_key = unquote_plus(s3_key)

                print()
                print("===========================LOGS=================================")
                print(bucket_name)
                print(s3_key)


                response = ecs_client.run_task(
                    cluster="arn:aws:ecs:ap-south-1:829730167354:cluster/video-transcoder-bytecry-cluster3",
                    launchType="FARGATE",
                    taskDefinition="arn:aws:ecs:ap-south-1:829730167354:task-definition/video-transcoder-task-definition2:1",
                    overrides={
                        "containerOverrides": [
                            {
                                "name": "video-transcoder",
                                "environment": [
                                    {"name": "S3_BUCKET", "value": bucket_name},
                                    {"name": "S3_KEY", "value": decoded_key},
                                ],
                            }
                        ]
                    },
                    networkConfiguration={
                        "awsvpcConfiguration": {
                            "subnets": [
                                "subnet-072be244abbef9d09",
                                "subnet-08b01ab911e11125b",
                                "subnet-0bb00f48eebe6b43a",
                            ],
                            "assignPublicIp": "ENABLED",
                            "securityGroups": ["sg-0a395793ec3570600"],
                        }
                    },
                )
                
                sqs_client.delete_message(
                    QueueUrl=secret_keys.RAW_VIDEO_PROCESSING_QUEUE,
                    ReceiptHandle=message["ReceiptHandle"],
                )


poll_sqs()
