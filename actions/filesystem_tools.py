import os

def list_files(path="."):
    """Lists files in the specified directory."""
    try:
        return os.listdir(path)
    except Exception as e:
        return str(e)

def read_file(path):
    """Reads the content of a file."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)

def write_file(path, content):
    """Writes content to a file."""
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return str(e)
