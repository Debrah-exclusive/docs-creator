import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class PitchDeckGenerator(DocumentTemplate):
    """Generator for Pitch Deck documents."""
    
    def generate_pitch_deck(self, custom_data=None):
        """Generate a pitch deck document using template system and custom_data."""
        template_content = self.get_template_content('pitch_deck', custom_data)
        if template_content is None:
            print("❌ No template found for pitch_deck")
            return None
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
        filename = "pitch_deck_presentation.pdf"
        return self.generate_document(filename, content, "pitch_deck")

if __name__ == "__main__":
    generator = PitchDeckGenerator()
    filename = generator.generate_pitch_deck()
    if filename:
        print(f"Pitch deck generated: {filename}")