import json
import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    print("Received event:", event)

    allowed_extensions = ['png', 'jpg', 'jpeg']
    topic_arn = os.environ.get("SNS_TOPIC_ARN")

    try:
        # Simulated input
        filename = event.get("queryStringParameters", {}).get("filename", "")

        if not filename or '.' not in filename:
            raise ValueError("Filename is missing or invalid.")

        ext = filename.split('.')[-1].lower()
        if ext not in allowed_extensions:
            error_msg = f"Invalid file type: {ext}"
            print(error_msg)

            # ✅ Publish to SNS
            sns.publish(
                TopicArn=topic_arn,
                Subject="Image Upload Failed",
                Message=f"Error: {error_msg}"
            )

            return {
                "statusCode": 400,
                "body": json.dumps({"error": error_msg})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Valid file type"})
        }

    except Exception as e:
        print("Exception:", str(e))
        sns.publish(
            TopicArn=topic_arn,
            Subject="Lambda Error",
            Message=f"Unexpected error: {str(e)}"
        )
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
