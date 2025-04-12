import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.append(str(src_path))

from ai.processor import AIProcessor

async def main():
    # Initialize the processor
    processor = AIProcessor()
    
    # Process the test data
    data_path = Path(__file__).parent.parent / 'downloads' / 'test_data.txt'
    result = await processor.process_data(str(data_path))
    
    if result:
        print("Processing successful!")
        print("Result:")
        print(result)
        
        # Validate the response
        is_valid = await processor.validate_response(result)
        print(f"\nResponse validation: {'Success' if is_valid else 'Failed'}")
    else:
        print("Processing failed!")

if __name__ == "__main__":
    asyncio.run(main()) 