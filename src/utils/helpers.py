import os
import json
import yaml
import logging

def ensure_directory(path):
    """Ensure a directory exists, create it if it doesn't."""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def read_json(filepath):
    """Read a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def write_json(filepath, data):
    """Write data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def read_yaml(filepath):
    """Read a YAML file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def write_yaml(filepath, data):
    """Write data to a YAML file."""
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def clear_directory(directory_path):
    """Delete all files in a directory."""
    if os.path.exists(directory_path):
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
