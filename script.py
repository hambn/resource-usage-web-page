#!/usr/bin/env python3
import os
import sys
import re
import time
import subprocess

# ANSI color codes
GREEN = '\033[0;32m'
BOLDGREEN = '\033[1;32m'
RED = '\033[0;31m'
BOLDRED = '\033[1;31m'
YELLOW = '\033[1;33m'
BOLDYELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
BOLDBLUE = '\033[1;34m'
NC = '\033[0m'  # No Color

def version_lt(v1, v2):
    """Return True if version string v1 is less than v2."""
    def normalize(v):
        return [int(x) for x in v.split('.')]
    return normalize(v1) < normalize(v2)

def check_docker():
    """Check Docker and Compose installation and versions."""
    # Check for Docker
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{BOLDRED}Error: Docker is not installed. Please install Docker.{NC}")
        sys.exit(1)

    docker_version_str = result.stdout.strip()
    if not docker_version_str:
        print(f"{BOLDRED}Error: Could not determine Docker version.{NC}")
        sys.exit(1)

    # Parse Docker version (expects format like "Docker version 20.10.7, build abcdef")
    tokens = docker_version_str.split()
    if len(tokens) < 3:
        print(f"{BOLDRED}Error: Unexpected Docker version string format.{NC}")
        sys.exit(1)
    current_docker_version = tokens[2].rstrip(',')
    minimum_docker_version = "20.10.0"

    if version_lt(current_docker_version, minimum_docker_version):
        docker_warning = f"\n{YELLOW}WARNING: Your Docker version is outdated! Recommended: {minimum_docker_version} or higher.{NC}"
    else:
        docker_warning = ""

    print(f"{BOLDGREEN}Using Docker (version: {docker_version_str}).{NC}")

    # Determine Compose command and extract version robustly
    compose_cmd = None
    compose_version = None
    # Try Docker Compose plugin first
    try:
        result = subprocess.run(["docker", "compose", "version", "--short"],
                                capture_output=True, text=True, check=True)
        compose_version = result.stdout.strip()
        compose_cmd = ["docker", "compose"]
        print(f"{BOLDGREEN}Using Docker Compose plugin (version: {compose_version}).{NC}")
    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(["docker", "compose", "version"],
                                    capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            m = re.search(r'v?(\d+\.\d+\.\d+)', output)
            compose_version = m.group(1) if m else "N/A"
            compose_cmd = ["docker", "compose"]
            print(f"{BOLDGREEN}Using Docker Compose plugin (version: {compose_version}).{NC}")
        except subprocess.CalledProcessError:
            # Fallback to docker-compose executable
            try:
                result = subprocess.run(["docker-compose", "version", "--short"],
                                        capture_output=True, text=True, check=True)
                compose_version = result.stdout.strip()
                compose_cmd = ["docker-compose"]
                print(f"{BOLDGREEN}Using docker-compose executable (version: {compose_version}).{NC}")
            except subprocess.CalledProcessError:
                try:
                    result = subprocess.run(["docker-compose", "version"],
                                            capture_output=True, text=True, check=True)
                    output = result.stdout.strip()
                    m = re.search(r'v?(\d+\.\d+\.\d+)', output)
                    compose_version = m.group(1) if m else "N/A"
                    compose_cmd = ["docker-compose"]
                    print(f"{BOLDGREEN}Using docker-compose executable (version: {compose_version}).{NC}")
                except subprocess.CalledProcessError:
                    print(f"{BOLDRED}Error: Docker Compose is not installed. Please install Docker Compose.{NC}")
                    sys.exit(1)
    return docker_version_str, docker_warning, compose_cmd, compose_version

# Run initial Docker/Compose check
docker_version_str, docker_warning, COMPOSE_CMD, compose_version = check_docker()
time.sleep(1)

while True:
    os.system("clear")
    # Determine container status based on current project directory
    project_name = os.path.basename(os.getcwd())
    try:
        result_running = subprocess.run(
            ["docker", "ps", "--filter", f"label=com.docker.compose.project={project_name}",
             "--format", "{{.ID}}"], capture_output=True, text=True)
        running_containers = result_running.stdout.strip()

        result_all = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"label=com.docker.compose.project={project_name}",
             "--format", "{{.ID}}"], capture_output=True, text=True)
        all_containers = result_all.stdout.strip()
    except Exception as e:
        print(f"{BOLDRED}Error checking container status: {e}{NC}")
        time.sleep(2)
        continue

    if running_containers:
        status = f"{BOLDGREEN}Running{NC}"
        is_running = True
    elif all_containers:
        status = f"{YELLOW}Stopped{NC}"
        is_running = False
    else:
        status = f"{RED}Not Started{NC}"
        is_running = False

    # Display the control panel header
    print("")
    print(f"   {BLUE}┌────────────────── Docker Control Panel ───────────────────┐{NC}")
    print(f"   {BLUE}│{NC} {GREEN}Docker version:{NC} {docker_version_str}{docker_warning}")
    print(f"   {BLUE}│{NC} {GREEN}Compose version:{NC} {compose_version}")
    print(f"   {BLUE}│{NC} Compose status: {status}")
    print(f"   {BLUE}└───────────────────────────────────────────────────────────┘{NC}")
    print("")
    print(f"   {BOLDBLUE}┌────────────────────── Menu Options ───────────────────────┐{NC}")
    if is_running:
        print(f"   {BOLDBLUE}│{NC} {BOLDGREEN}1{NC}. Tail logs (logs -f)")
        print(f"   {BOLDBLUE}│{NC} {BOLDGREEN}2{NC}. Reset container (down and up)")
        print(f"   {BOLDBLUE}│{NC} {BOLDGREEN}3{NC}. {YELLOW}Restart{NC} container (restart)")
        print(f"   {BOLDBLUE}│{NC} {BOLDGREEN}4{NC}. {BOLDYELLOW}Stop{NC} container (stop)")
        print(f"   {BOLDBLUE}│{NC} {BOLDGREEN}5{NC}. {BOLDRED}Down{NC} container (stop and remove)")
    else:
        print(f"   {BOLDBLUE}│{NC} {BOLDGREEN}1{NC}. Start container ({GREEN}up{NC} -d)")
    print(f"   {BOLDBLUE}└───────────────────────────────────────────────────────────┘{NC}")
    print("")
    print(f"   {BOLDRED}┌──────────────────────────{NC} {RED}Exit{NC} {BOLDRED}───────────────────────────┐{NC}")
    print(f"   {BOLDRED}│{NC} type {BOLDGREEN}0{NC} or simply use {BOLDGREEN}Ctrl + C{NC} for {RED}exit{NC}")
    print(f"   {BOLDRED}└───────────────────────────────────────────────────────────┘{NC}")
    print("")
    choice = input("  Enter your choice: ")
    print("")

    # Process user input based on the current state of containers
    if is_running:
        if choice == "1":
            try:
                subprocess.run(COMPOSE_CMD + ["logs", "-f"])
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Log tailing interrupted. Returning to menu...{NC}")
                time.sleep(1)
        elif choice == "2":
            subprocess.run(COMPOSE_CMD + ["down", "--remove-orphans"])
            subprocess.run(COMPOSE_CMD + ["up", "-d"])
        elif choice == "3":
            subprocess.run(COMPOSE_CMD + ["restart"])
        elif choice == "4":
            subprocess.run(COMPOSE_CMD + ["stop"])
        elif choice == "5":
            subprocess.run(COMPOSE_CMD + ["down"])
        elif choice == "0":
            print(f"{YELLOW}Exiting...{NC}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid choice. Please try again.{NC}")
            time.sleep(1)
    else:
        if choice == "1":
            subprocess.run(COMPOSE_CMD + ["up", "-d"])
        elif choice == "0":
            print(f"{YELLOW}Exiting...{NC}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid choice. Please try again.{NC}")
            time.sleep(1)
    time.sleep(1)
