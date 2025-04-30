"""

Author: Petrou Dimitrios 
Organization: Athena Research Center
Project Name:  STELAR EU 
Project Info: https://stelar-project.eu/

"""

from minio import Minio
import streamlit as st
import os
from utils.profile_functions import read_json_profile

class MinioClient:
    def __init__(self, 
                 endpoint, 
                 access_key, 
                 secret_key, 
                 secure=True, 
                 session_token=None):
        """
        Initialize a new instance of the MinIO client.
        Parameters:
            endpoint (str): The MinIO server endpoint, including host and port (e.g., "minio.stelar.gr").
            access_key (str): The access key for authenticating with the MinIO server.
            secret_key (str): The secret key associated with the provided access key for authentication.
            secure (bool, optional): Indicates whether to use HTTPS (True) or HTTP (False). Defaults to True.
            session_token (str, optional): An optional session token for temporary credentials. Defaults to None.
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            session_token=session_token
        )

    def _parse_s3_path(self, s3_path):
        """
        Parse an S3 path.

        Accepts:
         - "s3://bucket/object/name"
         - "bucket/object/name"
        
        :param s3_path: The S3 path to parse.
        :return: A tuple (bucket, object_name).
        """
        if s3_path.startswith("s3://"):
            path = s3_path[5:]
        else:
            path = s3_path
        parts = path.split("/", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("Invalid path. Expected format 's3://bucket/object/name' or 'bucket/object/name'.")
        return parts[0], parts[1]

    @st.cache_data
    def get_object(_self, bucket_name=None, object_name=None, s3_path=None, local_path=None):
        """
        Retrieve an object.
        Usage: Either pass bucket_name and object_name or s3_path.
        If local_path is provided, the object will be saved to that file.
        
        :param bucket_name: Name of the bucket.
        :param object_name: Name of the object.
        :param s3_path: S3-style path (e.g., "s3://bucket/object/name" or "bucket/object/name").
        :param local_path: Optional local file path to save the object.
        :return: The object data in bytes (if local_path is not provided)
                 or a success message (if saved to file).
        """
        if s3_path:
            bucket_name, object_name = _self._parse_s3_path(s3_path)
        elif not (bucket_name and object_name):
            raise ValueError("Bucket name and object name must be provided if s3_path is not used.")

        response = _self.client.get_object(bucket_name, object_name)
        try:
            if local_path:
                with open(local_path, 'wb') as file_data:
                    for d in response.stream(32 * 1024):
                        file_data.write(d)
                return read_json_profile(local_path)
            else:
                return response.read()
        finally:
            response.close()
            response.release_conn()

    