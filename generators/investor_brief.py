import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class InvestorBriefGenerator(DocumentTemplate):
    """Generator for Investor Brief documents."""
    
    def generate_investor_brief(self, custom_data=None):
        """Generate an investor brief document using template system and custom_data."""
        template_content = self.get_template_content('investor_brief', custom_data)
        if template_content is None:
            print("❌ No template found for investor_brief")
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
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"investor_brief_{timestamp}.pdf"
        return self.generate_document(filename, content, "investor_brief")
    
if __name__ == "__main__":
    generator = InvestorBriefGenerator()
    filename = generator.generate_investor_brief()
    if filename:
        print(f"Investor brief generated: {filename}")