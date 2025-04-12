import os
import sys
import pytest
import json
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from browser.controller import BrowserController
from ai.processor import AIProcessor
from utils.logger import setup_logger

@pytest.fixture
def browser_controller():
    return BrowserController()

@pytest.fixture
def ai_processor():
    return AIProcessor(model="phi3")

@pytest.fixture
def logger():
    return setup_logger("test_logger", log_file=None)

def test_browser_config_loading(browser_controller):
    """Test that browser configuration loads correctly."""
    assert browser_controller.config is not None
    assert 'remote_debugging' in browser_controller.config
    assert 'port' in browser_controller.config['remote_debugging']
    assert browser_controller.config['remote_debugging']['port'] == 9222

@pytest.mark.asyncio
async def test_browser_navigation(browser_controller):
    """Test browser navigation."""
    result = await browser_controller.navigate("https://example.com")
    assert result is True

@pytest.mark.asyncio
async def test_scraping_trigger(browser_controller):
    """Test scraping trigger."""
    result = await browser_controller.trigger_scrape()
    assert result is True

@pytest.mark.asyncio
async def test_download_monitoring(browser_controller):
    """Test download monitoring."""
    result = await browser_controller.wait_for_download()
    assert result is not None
    assert isinstance(result, str)
    assert result.endswith('.json')

def test_ai_processor_initialization(ai_processor):
    """Test AI processor initialization."""
    assert ai_processor.model == "phi3"

@pytest.mark.asyncio
async def test_ai_processing(ai_processor, tmp_path):
    """Test AI data processing."""
    # Create a temporary test data file
    test_data = {
        "products": [
            {"name": "Test Product", "price": "$9.99", "available": True}
        ]
    }
    test_file = tmp_path / "test_data.json"
    test_file.write_text(json.dumps(test_data))
    
    # Process the test data
    result = await ai_processor.process_data(str(test_file))
    assert result is not None
    assert "products" in result
    assert isinstance(result["products"], list)

@pytest.mark.asyncio
async def test_ai_response_validation(ai_processor):
    """Test AI response validation."""
    valid_response = {
        "products": [
            {
                "name": "Test Product",
                "price": "$9.99",
                "availability": True
            }
        ]
    }
    assert await ai_processor.validate_response(valid_response) is True

    invalid_response = {
        "products": [
            {
                "name": "Test Product"
                # Missing required fields
            }
        ]
    }
    assert await ai_processor.validate_response(invalid_response) is False

def test_logger_setup(logger):
    """Test logger setup."""
    assert logger.level == 20  # INFO level
    assert len(logger.handlers) > 0

def test_environment_variables():
    """Test that required environment variables are set."""
    required_vars = [
        'AI_PROVIDER',
        'OLLAMA_BASE_URL',
        'DEFAULT_MODEL'
    ]
    
    # Load .env file if it exists
    env_path = Path(__file__).parent.parent / 'config' / '.env'
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
    
    for var in required_vars:
        assert os.getenv(var) is not None, f"Missing environment variable: {var}"

if __name__ == '__main__':
    pytest.main([__file__])
