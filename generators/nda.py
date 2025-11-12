import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class NDAGenerator(DocumentTemplate):
    """Generator for Non-Disclosure Agreement documents."""
    
    def generate_nda(self, custom_data=None):
        """Generate an NDA document using template system."""
        # Get template content
        template_content = self.get_template_content('nda', custom_data)
        
        if template_content is None:
            print("❌ No template found for nda")
            return None
        
        # Prepare document content
        content = {
            "date": datetime.now().strftime("%d %B %Y"),
            "recipient": template_content.get('recipient', {}).get('default', []),
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"nda_{timestamp}.pdf"
        
        # Generate document with organized output
        return self.generate_document(filename, content, "nda")
    
if __name__ == "__main__":
    generator = NDAGenerator()
    filename = generator.generate_nda()
    if filename:
        print(f"NDA generated: {filename}")