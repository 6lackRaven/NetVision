# utils/format.py

import datetime

# Terminal color codes
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"


def colorize(text, color):
    return f"{color}{text}{Color.RESET}"


def format_timestamp(ts=None):
    """Return UTC timestamp in readable format"""
    if not ts:
        ts = datetime.datetime.utcnow()
    elif isinstance(ts, str):
        ts = datetime.datetime.fromisoformat(ts)

    return ts.strftime("%Y-%m-%d %H:%M:%S")


def format_bytes(size):
    """Convert bytes into human-readable format"""
    power = 2**10
    n = 0
    labels = ["B", "KB", "MB", "GB", "TB"]
    while size > power and n < len(labels)-1:
        size /= power
        n += 1
    return f"{round(size, 2)} {labels[n]}"


def shorten(text, max_length=30):
    """Shorten long text for cleaner output"""
    return text if len(text) <= max_length else text[:max_length - 3] + "..."


# Example use case:
if __name__ == "__main__":
    print(colorize("Scan started...", Color.GREEN))
    print("Timestamp:", format_timestamp())
    print("Data Size:", format_bytes(5432112))
    print("Short:", shorten("This is a very long text that needs trimming", 25))
