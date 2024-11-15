import logging
import logging.config
import os
from typing import Dict, Any, Optional

class DevToolkit:
    def __init__(self):
        self.config = self.load_config()
        self.setup_logging()

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from multiple YAML files.
        """
        config = {}
        config_files = ['general.yaml', 'logging.yaml', 'cloud.yaml']
        for file in config_files:
            try:
                with open(os.path.join('config', file), 'r') as f:
                    config.update(yaml.safe_load(f))
            except FileNotFoundError:
                print(f"Configuration file not found: {file}. Skipping...")
        return config

    def setup_logging(self):
        """
        Setup logging based on the logging configuration.
        """
        if 'logging' in self.config:
            logging.config.dictConfig(self.config['logging'])
        self.logger = logging.getLogger('devtoolkit')

    @staticmethod
    def create_docker_container(image_name: str, container_name: str) -> None:
        """
        Create and run a Docker container.
        """
        try:
            client = docker.from_env()
            client.containers.run(image_name, name=container_name, detach=True)
            print(f"Container {container_name} created from image {image_name}.")
        except docker.errors.DockerException as e:
            print(f"Failed to create Docker container: {e}")

    @staticmethod
    def run_security_scan(directory: str) -> Optional[Dict[str, Any]]:
        """
        Run a security scan on the given directory using Bandit.
        """
        try:
            from bandit.core.manager import BanditManager
            from bandit.core.config import BanditConfig
            from bandit.core.constants import EXAMPLES_DIR

            b_config = BanditConfig()
            manager = BanditManager(b_config, [EXAMPLES_DIR])
            manager.run_tests()
            results = manager.get_issue_list()
            return results
        except ImportError:
            print("Bandit is not installed. Please install it with `pip install bandit`.")
            return None

    @staticmethod
    def upload_to_cloud(file_path: str, cloud_provider: str, bucket_name: str) -> None:
        """
        Upload a file to a specified cloud provider's storage bucket.
        """
        try:
            if cloud_provider == 'aws':
                s3 = boto3.client('s3')
                s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
                print(f"Uploaded {file_path} to AWS bucket {bucket_name}.")
            elif cloud_provider == 'gcp':
                client = storage.Client()
                bucket = client.get_bucket(bucket_name)
                blob = bucket.blob(os.path.basename(file_path))
                blob.upload_from_filename(file_path)
                print(f"Uploaded {file_path} to GCP bucket {bucket_name}.")
            elif cloud_provider == 'azure':
                connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
                if not connect_str:
                    raise ValueError("Azure storage connection string not set.")
                blob_service_client = BlobServiceClient.from_connection_string(connect_str)
                blob_client = blob_service_client.get_blob_client(container=bucket_name, blob=os.path.basename(file_path))
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data)
                print(f"Uploaded {file_path} to Azure container {bucket_name}.")
            else:
                print(f"Unsupported cloud provider: {cloud_provider}")
        except Exception as e:
            print(f"Error uploading to cloud: {e}")

    def analyze_code_complexity(self, file_path: str) -> Dict[str, int]:
        """
        Analyze the complexity of a Python file.

        Args:
            file_path (str): Path to the Python file to analyze.

        Returns:
            Dict[str, int]: Function names and their complexity.
        """
        try:
            import radon.complexity as rc
            with open(file_path, 'r') as f:
                code = f.read()
            blocks = rc.cc_visit(code)
            complexity = {block.name: block.complexity for block in blocks}
            return complexity
        except ImportError:
            print("Radon is not installed. Please install it with `pip install radon`.")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to analyze code complexity: {e}")
            return {}

if __name__ == "__main__":
    toolkit = DevToolkit()

    # Example usage:
    # toolkit.create_docker_container("nginx", "my_nginx")
    # toolkit.upload_to_cloud("example.txt", "aws", "my_bucket")
    # complexity = toolkit.analyze_code_complexity("example.py")
    # print(complexity)