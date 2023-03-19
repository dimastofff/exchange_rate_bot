import psutil
from datetime import datetime
from . import desired_timezone

def generate_server_usage_text():
    network_counters = psutil.net_io_counters()
    text = "Server loading:\n"
    text += f"    Server booted: {datetime.fromtimestamp(psutil.boot_time(), desired_timezone).strftime('%d-%m-%Y %H:%M:%S')}\n"
    text += f"    CPU: {psutil.cpu_percent(interval=None)} %\n"
    text += f"    Memory: {psutil.virtual_memory().percent} %\n"
    text += f"    Disk: {psutil.disk_usage('/').percent} %\n"
    text += f"    Network: sent {network_counters.bytes_sent / 1048576:.2f} MB / received {network_counters.bytes_recv / 1048576:.2f} MB\n\n"
    return text
