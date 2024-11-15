import os
import sys
import json
import hashlib
import requests
import subprocess
from datetime import datetime
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from collections import Counter

class DevToolkit:
    @staticmethod
    def analyze_code_complexity(file_path: str) -> Dict[str, Any]:
        """Analyze the complexity of a Python file."""
        try:
            import radon.complexity as cc
            with open(file_path, 'r') as file:
                code = file.read()
            complexity = cc.cc_visit(code)
            return {func.name: func.complexity for func in complexity}
        except ImportError:
            print("Please install radon: pip install radon")
            return {}

    @staticmethod
    def generate_requirements(directory: str) -> List[str]:
        """Generate requirements.txt for a Python project."""
        try:
            import pipreqs
            pipreqs.pipreqs.get_all_imports(directory, encoding='utf-8')
            with open('requirements.txt', 'r') as f:
                return f.read().splitlines()
        except ImportError:
            print("Please install pipreqs: pip install pipreqs")
            return []

    @staticmethod
    def create_gitignore(project_type: str) -> None:
        """Create a .gitignore file based on project type."""
        url = f"https://www.toptal.com/developers/gitignore/api/{project_type}"
        response = requests.get(url)
        if response.status_code == 200:
            with open('.gitignore', 'w') as f:
                f.write(response.text)
            print(".gitignore created successfully.")
        else:
            print("Failed to create .gitignore")

    @staticmethod
    def analyze_json(json_str: str) -> Dict[str, Any]:
        """Analyze and provide insights about a JSON string."""
        try:
            data = json.loads(json_str)
            return {
                "type": type(data).__name__,
                "length": len(data) if isinstance(data, (list, dict)) else 1,
                "keys": list(data.keys()) if isinstance(data, dict) else None,
                "nested_types": {k: type(v).__name__ for k, v in data.items()} if isinstance(data, dict) else None
            }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON"}

    @staticmethod
    def monitor_file_changes(directory: str, interval: int = 5) -> None:
        """Monitor file changes in a directory."""
        import time
        previous = {}
        while True:
            current = {}
            for root, _, files in os.walk(directory):
                for file in files:
                    path = os.path.join(root, file)
                    try:
                        current[path] = os.path.getmtime(path)
                    except OSError:
                        pass
            
            if previous:
                for path, mtime in current.items():
                    if path not in previous:
                        print(f"New file: {path}")
                    elif mtime != previous[path]:
                        print(f"Modified: {path}")
                for path in previous.keys() - current.keys():
                    print(f"Deleted: {path}")
            
            previous = current
            time.sleep(interval)

    @staticmethod
    def create_data_backup(source: str, destination: str) -> None:
        """Create a data backup with versioning."""
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(destination, f"backup_{timestamp}")
        shutil.copytree(source, backup_dir)
        print(f"Backup created at {backup_dir}")

    @staticmethod
    def analyze_log_file(log_file: str) -> Dict[str, Any]:
        """Analyze a log file and provide insights."""
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        error_count = sum(1 for line in lines if 'ERROR' in line)
        warning_count = sum(1 for line in lines if 'WARNING' in line)
        
        return {
            "total_lines": len(lines),
            "error_count": error_count,
            "warning_count": warning_count,
            "error_percentage": (error_count / len(lines)) * 100,
            "warning_percentage": (warning_count / len(lines)) * 100
        }

    @staticmethod
    def generate_test_data(schema: Dict[str, str], num_records: int) -> List[Dict[str, Any]]:
        """Generate test data based on a given schema."""
        import random
        import string

        def generate_value(type_str):
            if type_str == 'int':
                return random.randint(1, 1000)
            elif type_str == 'float':
                return random.uniform(1, 1000)
            elif type_str == 'string':
                return ''.join(random.choices(string.ascii_letters, k=10))
            elif type_str == 'bool':
                return random.choice([True, False])
            else:
                return None

        return [{key: generate_value(value) for key, value in schema.items()} for _ in range(num_records)]

    @staticmethod
    def analyze_dependencies(requirements_file: str) -> Dict[str, Any]:
        """Analyze dependencies in a requirements.txt file."""
        with open(requirements_file, 'r') as f:
            requirements = f.read().splitlines()
        
        dependencies = {}
        for req in requirements:
            parts = req.split('==')
            if len(parts) == 2:
                dependencies[parts[0]] = parts[1]
            else:
                dependencies[req] = "Not specified"
        
        return {
            "total_dependencies": len(dependencies),
            "dependencies_with_versions": sum(1 for v in dependencies.values() if v != "Not specified"),
            "dependencies": dependencies
        }

    @staticmethod
    def generate_directory_tree(directory: str) -> str:
        """Generate a directory tree structure."""
        tree = ""
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            tree += f"{indent}{os.path.basename(root)}/\n"
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                tree += f"{sub_indent}{file}\n"
        return tree

    @staticmethod
    def analyze_code_duplication(directory: str) -> Dict[str, List[str]]:
        """Analyze code duplication in a directory."""
        duplicates = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                    hash_object = hashlib.md5(content.encode())
                    file_hash = hash_object.hexdigest()
                    if file_hash in duplicates:
                        duplicates[file_hash].append(os.path.join(root, file))
                    else:
                        duplicates[file_hash] = [os.path.join(root, file)]
        return {k: v for k, v in duplicates.items() if len(v) > 1}

    @staticmethod
    def visualize_data(data: List[float], title: str, xlabel: str, ylabel: str) -> None:
        """Visualize data using matplotlib."""
        plt.figure(figsize=(10, 6))
        plt.plot(data)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    @staticmethod
    def analyze_api_response(url: str) -> Dict[str, Any]:
        """Analyze an API response."""
        response = requests.get(url)
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content_type": response.headers.get('Content-Type'),
            "response_time": response.elapsed.total_seconds(),
            "content_length": len(response.content)
        }

    @staticmethod
    def generate_random_data(data_type: str, length: int) -> Any:
        """Generate random data of specified type and length."""
        import random
        import string

        if data_type == 'string':
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        elif data_type == 'int':
            return [random.randint(1, 100) for _ in range(length)]
        elif data_type == 'float':
            return [random.uniform(0, 1) for _ in range(length)]
        elif data_type == 'bool':
            return [random.choice([True, False]) for _ in range(length)]
        else:
            raise ValueError("Unsupported data type")

    @staticmethod
    def analyze_performance(func, *args, **kwargs) -> Dict[str, float]:
        """Analyze the performance of a function."""
        import time
        import cProfile
        import pstats
        from io import StringIO

        # Time execution
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()

        # Profile execution
        pr = cProfile.Profile()
        pr.enable()
        func(*args, **kwargs)
        pr.disable()
        s = StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()

        return {
            "execution_time": end_time - start_time,
            "profile": s.getvalue()
        }

    @staticmethod
    def generate_documentation(module_name: str) -> str:
        """Generate documentation for a Python module."""
        import importlib
        import inspect

        module = importlib.import_module(module_name)
        doc = f"# {module_name} Documentation\n\n"

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                doc += f"## Class: {name}\n\n"
                doc += f"{inspect.getdoc(obj)}\n\n"
                for method_name, method in inspect.getmembers(obj):
                    if inspect.isfunction(method):
                        doc += f"### Method: {method_name}\n\n"
                        doc += f"{inspect.getdoc(method)}\n\n"
            elif inspect.isfunction(obj):
                doc += f"## Function: {name}\n\n"
                doc += f"{inspect.getdoc(obj)}\n\n"

        return doc

    @staticmethod
    def analyze_text(text: str) -> Dict[str, Any]:
        """Analyze text and provide insights."""
        words = text.split()
        return {
            "word_count": len(words),
            "char_count": len(text),
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "most_common_words": Counter(words).most_common(5)
        }

    @staticmethod
    def execute_shell_command(command: str) -> Dict[str, Any]:
        """Execute a shell command and return the result."""
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                "error": str(e),
                "stdout": e.stdout,
                "stderr": e.stderr,
                "return_code": e.returncode
            }

    @staticmethod
    def analyze_image(image_path: str) -> Dict[str, Any]:
        """Analyze an image and provide insights."""
        try:
            from PIL import Image
            import numpy as np

            with Image.open(image_path) as img:
                img_array = np.array(img)
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "mean_color": img_array.mean(axis=(0,1)).tolist(),
                    "std_color": 
