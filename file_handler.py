"""
File handling utilities for the Legacy Code Documentation Agent.
Reads code files and detects their language.
"""

import os

# Map file extensions to language names
EXTENSION_MAP = {
    ".sql": "SQL",
    ".py": "Python",
    ".cpp": "C++",
    ".h": "C++",
    ".dax": "DAX",
    ".m": "DAX",  # Power BI measure files sometimes use .m
}


def get_language_from_extension(filepath: str) -> str:
    """
    Determine the programming language based on file extension.

    Args:
        filepath: Path to the code file

    Returns:
        Language name as a string (e.g., "SQL", "Python")
    """
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    return EXTENSION_MAP.get(extension, "Unknown")


def read_code_file(filepath: str) -> dict:
    """
    Read a code file and return its contents with metadata.

    Args:
        filepath: Path to the code file

    Returns:
        Dictionary with keys: 'filename', 'language', 'content', 'success', 'error'
    """
    result = {
        "filename": os.path.basename(filepath),
        "language": None,
        "content": None,
        "success": False,
        "error": None
    }

    # Check if file exists
    if not os.path.exists(filepath):
        result["error"] = f"File not found: {filepath}"
        return result

    # Get the language
    result["language"] = get_language_from_extension(filepath)

    # Read the file contents
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            result["content"] = f.read()
        result["success"] = True
    except Exception as e:
        result["error"] = f"Error reading file: {str(e)}"

    return result


def get_code_files_from_folder(folder_path: str) -> list:
    """
    Scan a folder and return a list of supported code files.

    Args:
        folder_path: Path to the folder to scan

    Returns:
        List of file paths for supported code files
    """
    supported_files = []

    # Check if folder exists
    if not os.path.isdir(folder_path):
        return supported_files

    # Walk through the folder
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            language = get_language_from_extension(filepath)

            # Only include files we know how to handle
            if language != "Unknown":
                supported_files.append(filepath)

    return supported_files