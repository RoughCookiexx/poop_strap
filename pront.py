COLOR_MAP = {
    "success": "\033[92m",
    "error": "\033[91m",
    "warning": "\033[93m",
    "running": "\033[92m",
    "stopped": "\033[91m",
    "info": "\033[94m",
}

RESET = "\033[0m"

def pront(status, text):
    color = COLOR_MAP.get(status.lower(), "")
    print(f"{color}{text}{RESET}")