import unittest
import os
import json

class TestBrowserExtension(unittest.TestCase):
    def setUp(self):
        # Load manifest.json
        with open('manifest.json', 'r') as f:
            self.manifest = json.load(f)
        
        # Verify required files exist
        self.required_files = [
            'background.js',
            'popup.html',
            'popup.js',
            'onload.js',
            'onload.css',
            'popup.css'
        ]

    def test_manifest_structure(self):
        """Test if manifest.json has required fields"""
        required_fields = ['manifest_version', 'name', 'version']
        for field in required_fields:
            self.assertIn(field, self.manifest, f"Missing required field: {field}")

    def test_required_files_exist(self):
        """Test if all required files are present"""
        for file in self.required_files:
            self.assertTrue(os.path.exists(file), f"Missing required file: {file}")

    def test_background_script(self):
        """Test if background.js exists and is readable"""
        self.assertTrue(os.path.exists('background.js'))
        with open('background.js', 'r') as f:
            content = f.read()
            self.assertIsInstance(content, str)
            self.assertTrue(len(content) > 0)

    def test_popup_files(self):
        """Test if popup related files exist and are readable"""
        popup_files = ['popup.html', 'popup.js', 'popup.css']
        for file in popup_files:
            self.assertTrue(os.path.exists(file))
            with open(file, 'r') as f:
                content = f.read()
                self.assertIsInstance(content, str)
                self.assertTrue(len(content) > 0)

if __name__ == '__main__':
    unittest.main() 