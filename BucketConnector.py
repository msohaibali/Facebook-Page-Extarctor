import os
import json
import boto3
import botocore
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class BucketConnector:
    @staticmethod
    def get_client(minio: bool = False):
        session = boto3.session.Session()
        if not minio:
            client = session.client(
                "s3",
                config=botocore.config.Config(s3={"addressing_style": "virtual"}),
                region_name="sfo3",
                endpoint_url="https://sfo3.digitaloceanspaces.com",
                aws_access_key_id=os.getenv("SPACES_KEY"),
                aws_secret_access_key=os.getenv("SPACES_SECRET"),
            )
        else:
            client = session.client(
                "s3",
                endpoint_url=os.getenv("ENDPOINT"),
                aws_access_key_id=os.getenv("SPACES_KEY"),
                aws_secret_access_key=os.getenv("SPACES_SECRET"),
                config=boto3.session.Config(signature_version="s3v4"),
            )

        return client

    @staticmethod
    def store_data(
        data: dict,
        bucket_name: str,
        category_name: str,
        folder_name: str,
        about_data: bool = False,
    ):
        file_name = str(datetime.now().date()) + ".json"
        client = BucketConnector.get_client(minio=True)
        try:
            if not about_data:
                client.put_object(
                    Body=json.dumps(data),
                    Bucket=bucket_name,
                    Key=f"{folder_name}/{category_name}/{file_name}",
                )
            else:
                client.put_object(
                    Body=json.dumps(data),
                    Bucket=bucket_name,
                    Key=f"{folder_name}/{file_name}",
                )
        except Exception as ex:
            print(
                "[!]  Issue  Page({} | {}) & File({})  ::  {}".format(
                    folder_name, category_name, file_name, str(ex)
                )
            )
