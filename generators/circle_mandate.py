import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class CircleMandateGenerator(DocumentTemplate):
    """Generator for Circle Mandate (Internal Memorandum) documents."""
    
    def generate_circle_mandate(self, custom_data=None):
        """Generate a Circle Mandate document."""
        if custom_data is None:
            custom_data = {}

        # Ensure date is present but DO NOT pass 'date' as a raw key to get_template_content
        # because DocumentTemplate blindly replaces all custom_data keys in the text.
        # If we pass 'date', it replaces the word "date" inside words like "accommodate".
        doc_date = custom_data.get('date', datetime.now().strftime("%d %B %Y"))
        
        # Create a safe copy for template replacement that doesn't include common words as keys
        safe_data = custom_data.copy()
        if 'date' in safe_data:
            del safe_data['date']
        
        template_content = self.get_template_content('circle_mandate', safe_data)
        if template_content is None:
            print("[ERROR] No template found for circle_mandate")
            return None
            
        content = {
            "date": doc_date,
            "recipient": template_content.get('recipient', {}).get('default', []),
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        
        filename = "CircleMandate.pdf"
        return self.generate_document(filename, content, "circle_mandate")
    
if __name__ == "__main__":
    generator = CircleMandateGenerator()
    filename = generator.generate_circle_mandate()
    if filename:
        print(f"Circle Mandate generated: {filename}")
