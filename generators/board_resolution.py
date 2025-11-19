import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class BoardResolutionGenerator(DocumentTemplate):
    """Generator for Board Resolution documents."""
    
    def generate_board_resolution(self, custom_data=None):
        """Generate a board resolution document using template system and custom_data."""
        template_content = self.get_template_content('board_resolution', custom_data)
        if template_content is None:
            print("❌ No template found for board_resolution")
            return None
        # Ensure custom_data is a dict
        if custom_data is None:
            custom_data = {}
        content = {
            "date": custom_data.get('date', datetime.now().strftime("%d %B %Y")),
            "recipient": [custom_data.get('recipient', r) for r in template_content.get('recipient', {}).get('default', [])],
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"board_resolution_{timestamp}.pdf"
        return self.generate_document(filename, content, "board_resolution")

if __name__ == "__main__":
    generator = BoardResolutionGenerator()
    filename = generator.generate_board_resolution()
    if filename:
        print(f"Board resolution generated: {filename}")