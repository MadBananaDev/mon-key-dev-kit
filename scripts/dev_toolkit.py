import yaml
import logging
import logging.config
import os
import docker
import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient

class DevToolkit:
    def __init__(self):
        self.config = self.load_config()
        self.setup_logging()

    def load_config(self):
        config = {}
        config_files = ['general.yaml', 'logging.yaml', 'cloud.yaml']
        for file in config_files:
            with open(os.path.join('config', file), 'r') as f:
                config.update(yaml.safe_load(f))
        return config

    def setup_logging(self):
        logging.config.dictConfig(self.config['logging'])
        self.logger = logging.getLogger('devtoolkit')

    @staticmethod
    def create_docker_container(image_name: str, container_name: str) -> None:
        client = docker.from_env()
        client.containers.run(image_name, name=container_name, detach=True)

    @staticmethod
    def run_security_scan(directory: str) -> Dict[str, Any]:
        import bandit
        return bandit.run(directory)

    @staticmethod
    def profile_code(func, *args, **kwargs) -> Dict[str, Any]:
        import py_spy
        return py_spy.record(func, *args, **kwargs)

    @staticmethod
    def upload_to_cloud(file_path: str, cloud_provider: str, bucket_name: str) -> None:
        if cloud_provider == 'aws':
            s3 = boto3.client('s3')
            s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
        elif cloud_provider == 'gcp':
            client = storage.Client()
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(os.path.basename(file_path))
            blob.upload_from_filename(file_path)
        elif cloud_provider == 'azure':
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)
            blob_client = blob_service_client.get_blob_client(container=bucket_name, blob=os.path.basename(file_path))
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)

    def analyze_code_complexity(self, file_path):
        Analyze the complexity of a Python file.

        Usage:
            toolkit = DevToolkit()
            complexity = toolkit.analyze_code_complexity('path/to/your/file.py')
            print(complexity)

        Args:
            file_path (str): Path to the Python file to analyze.

        Returns:
            dict: A dictionary containing function names as keys and their complexity as values.

        Configuration:
            This method uses the 'max_file_size' parameter from the general configuration.
            You can update this in the config/general.yaml file.
        """
        max_file_size = self.config['general']['max_file_size'] * 1024 * 1024  # Convert to bytes
        if os.path.getsize(file_path) > max_file_size:
            self.logger.warning(f"File size exceeds the maximum allowed size of {max_file_size} bytes")
            return {}

        # ... (rest of the method implementation)

    # ... (update other methods similarly)

if __name__ == "__main__":
    toolkit = DevToolkit()
    # Add example usage here
