import json
import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any
import ollama

class AIProcessor:
    def __init__(self, model: str = "phi3"):
        self.logger = logging.getLogger(__name__)
        self.model = model
        # Set logging level to DEBUG
        self.logger.setLevel(logging.DEBUG)
        # Configure root logger to show debug messages
        logging.basicConfig(level=logging.DEBUG)

    def _extract_json_from_markdown(self, text: str) -> Optional[str]:
        """Extract JSON from markdown-formatted text."""
        # Try to find JSON between ```json and ``` markers
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # If no markdown markers, try to find JSON between { and }
        json_match = re.search(r'(\{.*?\})', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        return None

    async def process_data(self, data_path: str) -> Optional[Dict[str, Any]]:
        """Process scraped data using Ollama."""
        try:
            self.logger.debug(f"Reading data from {data_path}")
            # Read the data file
            with open(data_path, 'r') as f:
                content = f.read().strip()
            
            # Try to parse as JSON first
            try:
                data = json.loads(content)
                self.logger.debug(f"Data read successfully as JSON: {data}")
            except json.JSONDecodeError:
                # If not JSON, treat as plain text
                self.logger.debug("Data is not JSON, treating as plain text")
                data = {"raw_text": content}

            # If data is already in the correct format, just return it
            if await self.validate_response(data):
                self.logger.debug("Data is already in the correct format")
                return data

            # Process with Ollama
            prompt = f"""
            Convert this product data into a structured JSON format. Each line contains a product name, price, and stock status.
            Input data:
            {content}

            Instructions:
            1. Parse each line into a product object
            2. Include exactly these fields for each product: "name", "price", "status"
            3. Return a valid JSON object with a "products" array
            4. Do not include any other text or markdown

            Example format:
            {{"products": [
                {{"name": "Example Product", "price": "$10.00", "status": "In Stock"}}
            ]}}
            """
            self.logger.debug(f"Sending prompt to Ollama: {prompt}")

            try:
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    options={"temperature": 0.1}  # Lower temperature for more consistent output
                )
                self.logger.debug(f"Received response from Ollama: {response}")

                # Extract JSON from response
                response_text = response['response'].strip()
                self.logger.debug(f"Response text: {response_text}")
                
                json_str = self._extract_json_from_markdown(response_text)
                if not json_str:
                    self.logger.error("Could not extract JSON from response")
                    return None

                self.logger.debug(f"Extracted JSON string: {json_str}")

                # Try to parse the response as JSON
                try:
                    result = json.loads(json_str)
                    self.logger.debug(f"Successfully parsed response as JSON: {result}")
                    
                    # Clean and validate the response
                    if 'products' in result and isinstance(result['products'], list):
                        cleaned_products = []
                        for product in result['products']:
                            # Skip invalid products
                            if not isinstance(product, dict):
                                continue
                                
                            # Clean up the product object
                            cleaned_product = {}
                            # Extract name from various possible fields
                            for name_field in ['name', 'nameiname', 'namein']:
                                if name_field in product:
                                    cleaned_product['name'] = product[name_field]
                                    break
                            # Copy other fields if they exist
                            if 'price' in product:
                                cleaned_product['price'] = product['price']
                            if 'status' in product:
                                cleaned_product['status'] = product['status']
                            
                            # Only add if we have all required fields
                            if all(k in cleaned_product for k in ('name', 'price', 'status')):
                                cleaned_products.append(cleaned_product)
                        
                        result['products'] = cleaned_products
                    
                    # Validate the result
                    if await self.validate_response(result):
                        return result
                    else:
                        self.logger.error("Generated response failed validation")
                        return None

                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse response as JSON: {e}")
                    self.logger.error(f"JSON string was: {json_str}")
                    return None

            except Exception as e:
                self.logger.error(f"Error generating response from Ollama: {e}")
                return None

        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    async def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate AI response format."""
        try:
            self.logger.debug(f"Validating response: {response}")
            if not isinstance(response.get('products'), list):
                self.logger.debug("Response does not contain a products list")
                return False
            
            for product in response['products']:
                if not all(k in product for k in ('name', 'price', 'status')):
                    self.logger.debug(f"Product missing required fields: {product}")
                    return False
            
            self.logger.debug("Response validation successful")
            return True
        except Exception as e:
            self.logger.error(f"Response validation failed: {e}")
            return False
