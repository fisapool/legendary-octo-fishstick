# Web Scraping & AI Analysis System

A comprehensive system for automated web scraping and AI-powered data analysis using Ollama, A5-Browser-Use, and Chrome automation.

## Features

- Automated web navigation and data scraping
- Local AI processing with Ollama
- Modern web dashboard for control and monitoring
- Chrome extension integration
- Robust error handling and logging

## Prerequisites

- Python 3.11 or higher
- Google Chrome browser
- Ollama installed and running
- A5-Browser-Use extension

## Quick Start

1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Pull required models:
```bash
ollama pull qwen2.5:32b-instruct-q4_K_M
```

3. Start Ollama:
```bash
ollama serve
```

4. Configure Chrome for remote debugging:
```bash
# Linux
google-chrome --remote-debugging-port=9222 --profile-directory="Default"

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --profile-directory="Default"

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory="Default"
```

5. Install Python dependencies:
```bash
pip install -r requirements.txt
```

6. Start the server:
```bash
python src/main.py
```

## Project Structure

```
project/
├── config/
│   ├── .env
│   └── browser_config.json
├── scripts/
│   ├── setup.sh
│   └── start_browser.sh
├── src/
│   ├── browser/
│   ├── ai/
│   └── utils/
├── tests/
└── README.md
```

## Configuration

Create a `.env` file in the config directory with:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=phi3
```

## Usage

1. Start Chrome with remote debugging enabled
2. Launch the Ollama service
3. Start the Python server
4. Access the dashboard at http://localhost:8000
5. Use the Chrome extension to control scraping and processing

## Error Handling

The system includes comprehensive error handling:
- Network connectivity issues
- Browser automation failures
- AI processing errors
- File system operations

## Logging

Logs are stored in `logs/a5.log` with different severity levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: Critical failures
- DEBUG: Detailed debugging information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details
