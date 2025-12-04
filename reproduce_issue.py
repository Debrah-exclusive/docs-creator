import os
import sys
import traceback
from generate_documents import DocumentSuite

def reproduce():
    print("Starting reproduction...")
    try:
        suite = DocumentSuite(output_dir=os.path.join(os.getcwd(), 'output'))
        print("Suite initialized.")
        
        gen = suite.generators.get('invitation_to_the_circle')
        if not gen:
            print("Generator for invitation_to_the_circle not found!")
            return

        print(f"Generator class: {type(gen)}")
        
        if 'invitation_to_the_circle' in gen.templates:
            print("Template 'invitation_to_the_circle' FOUND in templates.")
        else:
            print("Template 'invitation_to_the_circle' NOT FOUND in templates.")
            print("Available keys:", list(gen.templates.keys()))
        
        # Test with empty data
        print("Testing with empty data...")
        path = suite.generate_document('invitation_to_the_circle', {})
        print(f"Result with empty data: {path}")

        # Test with None data
        print("Testing with None data...")
        path = suite.generate_document('invitation_to_the_circle', None)
        print(f"Result with None data: {path}")

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
