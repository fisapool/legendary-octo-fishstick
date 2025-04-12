"""
Test suite for Web Scraping & AI Analysis System.

This package contains all test cases for verifying the functionality
of the browser automation, AI processing, and utility components.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path for testing
sys.path.append(str(Path(__file__).parent.parent / 'src'))

# Configure pytest
pytest.register_assert_rewrite('tests.test_system')
