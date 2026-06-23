import psutil


def detect_mode():
    """
    Lightweight hardware-based mode detection.
    """

    ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    cpu_cores = psutil.cpu_count(logical=True)

    # conservative laptop threshold
    if ram_gb <= 10 or cpu_cores <= 6:
        return "laptop"

    return "desktop"