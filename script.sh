#!/bin/bash
# ANSI color codes
GREEN='\033[0;32m'
BOLDGREEN='\033[1;32m'
RED='\033[0;31m'
BOLDRED='\033[1;31m'
YELLOW='\033[1;33m'
BOLDYELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLDBLUE='\033[1;34m'
NC='\033[0m' # No Color

# Function to check Docker and Compose installation and version
check_docker() {
    # Check for Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${BOLDRED}Error: Docker is not installed. Please install Docker.${NC}"
        exit 1
    fi

    # Get Docker version
    DOCKER_VERSION=$(docker --version 2>/dev/null)
    if [[ -z "$DOCKER_VERSION" ]]; then
        echo -e "${BOLDRED}Error: Could not determine Docker version.${NC}"
        exit 1
    fi

    current_docker_version=$(echo "$DOCKER_VERSION" | awk '{print $3}' | cut -d',' -f1)
    minimum_docker_version="20.10.0"

    # Version comparison using dpkg (Debian) or rpm (Redhat) if available
    if dpkg --compare-versions "$current_docker_version" "lt" "$minimum_docker_version" 2>/dev/null; then
        DOCKER_WARNING="\n${YELLOW}WARNING: Your Docker version is outdated! Recommended: $minimum_docker_version or higher.${NC}"
    elif command -v rpm &> /dev/null; then
        if rpm -q --queryformat "%{VERSION}" docker | grep -q "$minimum_docker_version"; then
            DOCKER_WARNING=""
        else
            DOCKER_WARNING="\n${YELLOW}WARNING: Your Docker version is outdated! Recommended: $minimum_docker_version or higher.${NC}"
        fi
    else
        if [[ "$current_docker_version" < "$minimum_docker_version" ]]; then
            DOCKER_WARNING="\n${YELLOW}WARNING: Your Docker version is outdated! Recommended: $minimum_docker_version or higher.${NC}"
        else
            DOCKER_WARNING=""
        fi
    fi

    # Determine Compose command and extract version robustly
    if docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
        if docker compose version --short &> /dev/null; then
            COMPOSE_VERSION=$(docker compose version --short 2>/dev/null)
        else
            COMPOSE_VERSION=$(docker compose version 2>/dev/null | grep -Eo 'v[0-9]+\.[0-9]+\.[0-9]+' || echo "N/A")
        fi
        echo -e "${BOLDGREEN}Using Docker Compose plugin (version: $COMPOSE_VERSION).${NC}"
    elif command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
        if docker-compose version --short &> /dev/null; then
            COMPOSE_VERSION=$(docker-compose version --short 2>/dev/null)
        else
            COMPOSE_VERSION=$(docker-compose version 2>/dev/null | grep -Eo 'v[0-9]+\.[0-9]+\.[0-9]+' || echo "N/A")
        fi
        echo -e "${BOLDGREEN}Using docker-compose executable (version: $COMPOSE_VERSION).${NC}"
    else
        echo -e "${BOLDRED}Error: Docker Compose is not installed. Please install Docker Compose.${NC}"
        exit 1
    fi
}

# Initial Docker/Compose check
check_docker
sleep 1

# Main loop for the control menu
while true; do
    clear

    # Determine container status based on the current project directory
    project_name=$(basename "$(pwd)")
    running_containers=$(docker ps --filter "label=com.docker.compose.project=$project_name" --format "{{.ID}}")
    all_containers=$(docker ps -a --filter "label=com.docker.compose.project=$project_name" --format "{{.ID}}")

    if [ -n "$running_containers" ]; then
        STATUS="${BOLDGREEN}Running${NC}"
        IS_RUNNING=1
    elif [ -n "$all_containers" ]; then
        STATUS="${YELLOW}Stopped${NC}"
        IS_RUNNING=0
    else
        STATUS="${RED}Not Started${NC}"
        IS_RUNNING=0
    fi

    echo ""
    echo -e "   ${BLUE}┌────────────────── Docker Control Panel ───────────────────┐${NC}"
    echo -e "   ${BLUE}│${NC} ${GREEN}Docker version:${NC} $DOCKER_VERSION$DOCKER_WARNING"
    echo -e "   ${BLUE}│${NC} ${GREEN}Compose version:${NC} $COMPOSE_VERSION"
    echo -e "   ${BLUE}│${NC} Compose status: $STATUS"
    echo -e "   ${BLUE}└───────────────────────────────────────────────────────────┘${NC}"

    echo -e "   ${BOLDBLUE}┌────────────────────── Menu Options ───────────────────────┐${NC}"
    # Show the appropriate menu based on container status
    if [ "$IS_RUNNING" -eq 1 ]; then
        echo -e "   ${BOLDBLUE}│${NC} ${BOLDGREEN}1${NC}. Tail logs (logs -f)"
        echo -e "   ${BOLDBLUE}│${NC} ${BOLDGREEN}2${NC}. Reset container (down and up)"
        echo -e "   ${BOLDBLUE}│${NC} ${BOLDGREEN}3${NC}. ${YELLOW}Restart${NC} container (restart)"
        echo -e "   ${BOLDBLUE}│${NC} ${BOLDGREEN}4${NC}. ${BOLDYELLOW}Stop${NC} container (stop)"
        echo -e "   ${BOLDBLUE}│${NC} ${BOLDGREEN}5${NC}. ${BOLDRED}Down${NC} container (stop and remove)"
    else
        echo -e "   ${BOLDBLUE}│${NC} ${BOLDGREEN}1${NC}. Start container (${GREEN}up${NC} -d)"
    fi
    echo -e "   ${BOLDBLUE}└───────────────────────────────────────────────────────────┘${NC}"

    echo -e "   ${BOLDRED}┌──────────────────────────${NC} ${RED}Exit${NC} ${BOLDRED}───────────────────────────┐${NC}"
    echo -e "   ${BOLDRED}│${NC} type ${BOLDGREEN}0${NC} or simply use ${BOLDGREEN}Ctrl + C${NC} for ${RED}exit${NC}"
    echo -e "   ${BOLDRED}└───────────────────────────────────────────────────────────┘${NC}"

    echo ""
    read -p "  Enter your choice: " choice
    echo ""

    # Process user input based on the current state of containers
    if [ "$IS_RUNNING" -eq 1 ]; then
        case $choice in
            1) $COMPOSE_CMD logs -f ;;
            2) $COMPOSE_CMD down --remove-orphans && $COMPOSE_CMD up -d ;;
            3) $COMPOSE_CMD restart ;;
            4) $COMPOSE_CMD stop ;;
            5) $COMPOSE_CMD down ;;
            0) echo -e "${YELLOW}Exiting...${NC}" && exit 0 ;;
            *) echo -e "${RED}Invalid choice. Please try again.${NC}" && sleep 1 ;;
        esac
    else
        case $choice in
            1) $COMPOSE_CMD up -d ;;
            0) echo -e "${YELLOW}Exiting...${NC}" && exit 0 ;;
            *) echo -e "${RED}Invalid choice. Please try again.${NC}" && sleep 1 ;;
        esac
    fi
    sleep 1
done