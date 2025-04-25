"""
# MLog Viewer
This is a program that takes logs as input and spits out another two logs that contain commands & players
"""
from datetime import datetime, timedelta
from colorama import Fore as F
from colorama import init
from time import sleep
import ctypes
import yaml
import gzip
import sys
import os

init(strip=False, convert=True)
ctypes.windll.kernel32.SetConsoleTitleW("MLog Viewer")

CONFIG_PATH: str = "./config.yml"
LOGS_PATH: str = "./logs/"
VERSION: str = "0.1_d1"
NAMESPACE: str = "MLogV"

def printer(text: str) -> None: print(F.BLACK + "[" + F.GREEN + NAMESPACE + F.BLACK + "]" + F.RED + " > " + F.WHITE + text + F.RESET)
def printerwarn(text: str) -> None: print(F.BLACK + "[" + F.GREEN + NAMESPACE + F.BLACK + "]" + F.RED + " > " + F.YELLOW + text + F.RESET)

# Default Config Stuff
DEFAULT_COMMAND_MATCH = [
    "/give",
    "/gamemode",
    "/msg",
    "/tell",
    "/restart",
    "/stop",
    "/op",
    "/deop"
]
DEFAULT_PLAYER_MATCH = []

# Logs the time of the program starting
start_time = datetime.now()

if not os.path.exists(CONFIG_PATH):
    config_data = {
        "version": VERSION,
        "command_match": DEFAULT_COMMAND_MATCH,
        "player_match": DEFAULT_PLAYER_MATCH
    }

    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config_data, f)

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[:ERROR:] > Failed to load config: {e}")
        return None

config = load_config()

if config is None:
    printer("Unable to continue, missing or broken config.yml")
    sleep(4)
    sys.exit(1)

if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH)
    printer("Log directory created. Place your logs in there.")
    sleep(4)
    sys.exit(0)

printer("Loading Log files... Please wait...")

files = []
log_files = [f for f in os.listdir(LOGS_PATH) if os.path.isfile(os.path.join(LOGS_PATH, f))]

printer(f"{len(log_files)} log files found.")

for log in log_files:
    path = os.path.join(LOGS_PATH, log)
    try:
        if log.endswith(".gz"):
            with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
                files.extend(f.readlines())
        elif log.endswith(".log"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                files.extend(f.readlines())
        else:
            printerwarn(f"Skipping unsupported file: {log}")
    except Exception as e:
        printerwarn(f"Failed to read {log}: {e}")

if not files:
    printerwarn("No valid logs to search.")
    sleep(4)
    sys.exit(0)

printer("Starting Log Search Process...")

command_results = []
player_results = []

for line in files:
    if any(cmd in line for cmd in config.get("command_match", [])):
        command_results.append(line)

    if any(player in line for player in config.get("player_match", [])):
        player_results.append(line)

printer("Saving results...")

with open("command_results.log", "w", encoding="utf-8") as f:
    f.writelines(command_results)

with open("player_results.log", "w", encoding="utf-8") as f:
    f.writelines(player_results)

end_time = datetime.now()
delta: timedelta = end_time - start_time

printer(f"Task completed in {delta.total_seconds():.2f}s")
printer(f"Found {len(command_results)} command entries and {len(player_results)} player entries.")
sleep(4)