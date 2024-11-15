import yaml
import logging
import logging.config
import os

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

    # ... (rest of the methods)

    def analyze_code_complexity(self, file_path):
        """
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
