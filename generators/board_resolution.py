import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class BoardResolutionGenerator(DocumentTemplate):
    """Generator for Board Resolution documents."""
    
    def generate_board_resolution(self, custom_data=None):
        """Generate a board resolution document using template system."""
        # Get template content
        template_content = self.get_template_content('board_resolution', custom_data)
        
        if template_content is None:
            print("❌ No template found for board_resolution")
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
        filename = f"board_resolution_{timestamp}.pdf"
        
        # Generate document with organized output
        return self.generate_document(filename, content, "board_resolution")

if __name__ == "__main__":
    generator = BoardResolutionGenerator()
    filename = generator.generate_board_resolution()
    if filename:
        print(f"Board resolution generated: {filename}")