# This script runs on my little home server and runs my little programs.

import os
import time
from os.path import abspath, dirname

import git
import requests

PARENT_DIR = dirname(dirname(abspath(__file__)))


def start_fastapi():
    # see if the service is running
    # if not, start it

    path = "localhost:8000"

    # I don't have a health check endpoint but that's fine
    try:
        is_running = requests.get(path)
    except Exception:
        is_running = False

    if not is_running:
        os.system(f"fastapi run \"{PARENT_DIR}/Photo email scheduler/response_api.py\" &")
        return True
    return False


def start_scheduler():
    # os.system("python3 scheduler.py")
    return False


def update_repos():
    repos = ["Photo email scheduler", "server_manager"]
    for repo in repos:
        git.repo.Repo(f"{PARENT_DIR}/{repo}").remotes.origin.pull()


def main():
    counter = 0
    while True:
        counter += 1
        needed_restart = start_fastapi()
        needed_restart = needed_restart or start_scheduler()

        if needed_restart or counter % 60 == 0:
            update_repos()

        print(f"Running{'.' * counter % 3}", end="\r")
        time.sleep(60)


if __name__ == "__main__":
    main()
