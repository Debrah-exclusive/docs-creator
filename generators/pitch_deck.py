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
        # Transform slides structure into body paragraphs for renderer
        slides = template_content.get('slides', [])
        body = []
        for slide in slides:
            stitle = slide.get('title', '').strip()
            headline = slide.get('headline', '').strip()
            if stitle:
                body.append(f"<b>{stitle}</b>")
            if headline:
                body.append(f"<i>{headline}</i>")
            for line in slide.get('body', []):
                body.append(line)
            body.append("")  # spacer paragraph
        content = {
            "date": custom_data.get('date', datetime.now().strftime("%d %B %Y")),
            "recipient": [],
            "title": template_content.get('title', ''),
            "salutation": '',
            "body": body,
            "closing": '',
            "signature": template_content.get('signature', [])
        }
        filename = "PitchDeck.pdf"
        return self.generate_document(filename, content, "pitch_deck")

if __name__ == "__main__":
    generator = PitchDeckGenerator()
    filename = generator.generate_pitch_deck()
    if filename:
        print(f"Pitch deck generated: {filename}")