import json
from datetime import datetime
from pathlib import Path

# Define the base directory for the logs
BASE_LOG_DIR = Path("project/data/log")


def get_log_file_path() -> Path:
    """
    Creates the necessary directories if they don't exist and
    returns the file path for today's log file.
    """
    # Ensure the directory structure exists (project/data/log)
    BASE_LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Generate today's date string (e.g., 2026-03-08)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create and return the full file path
    return BASE_LOG_DIR / f"log_{current_date}.json"


def read_existing_logs(file_path: Path) -> list:
    """
    Reads existing logs from the JSON file.
    Returns an empty list if the file doesn't exist or is empty.
    """
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If the file exists but is empty or corrupted, start fresh
            return []
    return []


def write_logs(file_path: Path, logs: list):
    """
    Writes the updated list of logs back to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(logs, file, indent=4, ensure_ascii=False)


def log_error(message: str):
    """
    Main function to log an error message. It retrieves the current log file,
    appends the new error, and saves the file.
    """
    file_path = get_log_file_path()
    logs = read_existing_logs(file_path)

    # Create the new log entry
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": "ERROR",
        "message": message
    }

    # Append and save
    logs.append(new_entry)
    write_logs(file_path, logs)

    print(f"Logged error to {file_path}")