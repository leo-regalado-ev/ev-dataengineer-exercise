import os
import boto3


class S3Helper():
    """
    An S3 helper class with various methods for getting or putting objects onto S3.
    """

    def __init__(self):
        self.s3_bucket = os.environ.get("S3_BUCKET")
        self.client = boto3.client('s3')

    def get_csv(self, key):
        """
            Method that gets S3 object as CSV string.
            Parameters:
            key - S3 Key of the object to download
        """
        csv_obj = self.client.get_object(Bucket=self.s3_bucket, Key=key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')

        return csv_string
