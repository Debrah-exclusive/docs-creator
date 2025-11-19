import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class PartnershipProposalGenerator(DocumentTemplate):
    """Generator for Partnership Proposal documents."""
    
    def generate_partnership_proposal(self, custom_data=None):
        """Generate a partnership proposal document using template system and custom_data."""
        template_content = self.get_template_content('partnership_proposal', custom_data)
        if template_content is None:
            print("❌ No template found for partnership_proposal")
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
        partner = custom_data.get('partner', '').strip().replace(' ', '_').lower() if custom_data.get('partner') else None
        company = custom_data.get('company', '').strip().replace(' ', '_').lower() if custom_data.get('company') else None
        if partner:
            filename = f"partnership_proposal_{partner}.pdf"
        elif company:
            filename = f"partnership_proposal_{company}.pdf"
        else:
            filename = "partnership_proposal_document.pdf"
        return self.generate_document(filename, content, "partnership_proposal")

if __name__ == "__main__":
    generator = PartnershipProposalGenerator()
    filename = generator.generate_partnership_proposal()
    if filename:
        print(f"Partnership proposal generated: {filename}")