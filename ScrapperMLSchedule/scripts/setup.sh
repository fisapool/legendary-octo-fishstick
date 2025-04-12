#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Web Scraping & AI Analysis System...${NC}"

# Create necessary directories
echo -e "\n${BLUE}Creating directories...${NC}"
mkdir -p logs downloads

# Check Python version
echo -e "\n${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo -e "${GREEN}Python version $python_version is compatible${NC}"
else
    echo -e "${RED}Error: Python version $python_version is below required version $required_version${NC}"
    exit 1
fi

# Install Python dependencies
echo -e "\n${BLUE}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Check if Ollama is installed
echo -e "\n${BLUE}Checking Ollama installation...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}Ollama is not installed. Installing now...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo -e "${GREEN}Ollama is already installed${NC}"
fi

# Pull required Ollama models
echo -e "\n${BLUE}Pulling required Ollama models...${NC}"
ollama pull phi3
ollama pull tinyllama

# Create .env file if it doesn't exist
if [ ! -f "config/.env" ]; then
    echo -e "\n${BLUE}Creating .env file...${NC}"
    cp config/.env.example config/.env
    echo -e "${GREEN}Created .env file. Please edit config/.env with your settings${NC}"
fi

# Detect OS and provide appropriate Chrome startup command
echo -e "\n${BLUE}Detecting operating system...${NC}"
case "$(uname -s)" in
    Linux*)
        chrome_cmd="google-chrome --remote-debugging-port=9222 --profile-directory=Default"
        ;;
    Darwin*)
        chrome_cmd="/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --profile-directory=Default"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        chrome_cmd="\\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\\" --remote-debugging-port=9222 --profile-directory=Default"
        ;;
    *)
        echo -e "${RED}Unsupported operating system${NC}"
        exit 1
        ;;
esac

# Create start_browser.sh
echo -e "\n${BLUE}Creating browser startup script...${NC}"
cat > scripts/start_browser.sh << EOL
#!/bin/bash
$chrome_cmd
EOL
chmod +x scripts/start_browser.sh

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Edit config/.env with your settings"
echo "2. Run 'scripts/start_browser.sh' to start Chrome with remote debugging"
echo "3. Start the server with 'python src/main.py'"
echo -e "\n${BLUE}For more information, see the README.md file${NC}"
