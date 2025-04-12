#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Chrome with remote debugging...${NC}"

# Kill any existing Chrome processes using port 9222
echo -e "\n${BLUE}Checking for existing Chrome instances...${NC}"
if lsof -i :9222 > /dev/null; then
    echo -e "${RED}Port 9222 is in use. Closing existing Chrome instances...${NC}"
    pkill -f "chrome.*remote-debugging-port=9222"
    sleep 2
fi

# Detect OS and start Chrome with appropriate command
case "$(uname -s)" in
    Linux*)
        echo -e "${BLUE}Starting Chrome on Linux...${NC}"
        google-chrome \
            --remote-debugging-port=9222 \
            --profile-directory="Default" \
            --disable-features=BlockInsecurePrivateNetworkRequests \
            --no-first-run \
            --no-default-browser-check \
            --user-data-dir="$(pwd)/chrome-data" &
        ;;
    Darwin*)
        echo -e "${BLUE}Starting Chrome on macOS...${NC}"
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
            --remote-debugging-port=9222 \
            --profile-directory="Default" \
            --disable-features=BlockInsecurePrivateNetworkRequests \
            --no-first-run \
            --no-default-browser-check \
            --user-data-dir="$(pwd)/chrome-data" &
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo -e "${BLUE}Starting Chrome on Windows...${NC}"
        "C:\Program Files\Google\Chrome\Application\chrome.exe" \
            --remote-debugging-port=9222 \
            --profile-directory="Default" \
            --disable-features=BlockInsecurePrivateNetworkRequests \
            --no-first-run \
            --no-default-browser-check \
            --user-data-dir="$(pwd)/chrome-data" &
        ;;
    *)
        echo -e "${RED}Unsupported operating system${NC}"
        exit 1
        ;;
esac

# Wait for Chrome to start
echo -e "\n${BLUE}Waiting for Chrome to start...${NC}"
max_attempts=30
attempt=0

while ! curl -s http://localhost:9222/json/version > /dev/null; do
    attempt=$((attempt + 1))
    if [ $attempt -eq $max_attempts ]; then
        echo -e "${RED}Failed to start Chrome after $max_attempts attempts${NC}"
        exit 1
    fi
    echo -e "${BLUE}Waiting for Chrome to become available (attempt $attempt/$max_attempts)...${NC}"
    sleep 1
done

echo -e "\n${GREEN}Chrome is running with remote debugging enabled on port 9222${NC}"
echo -e "${BLUE}Debug URL: http://localhost:9222${NC}"
echo -e "${BLUE}You can now start the Python server with: python src/main.py${NC}"

# Keep the script running to maintain the Chrome process
wait
