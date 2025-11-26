import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class PartnershipProposalGenerator(DocumentTemplate):
    """Generator for Partnership Proposal documents."""
    
    def generate_partnership_proposal(self, custom_data=None):
        """Generate a partnership proposal document."""
        if custom_data is None:
            custom_data = {}

        custom_data.setdefault('[Date]', custom_data.get('date', datetime.now().strftime("%d %B %Y")))

        template_content = self.get_template_content('partnership_proposal', custom_data)
        if template_content is None:
            print("❌ No template found for partnership_proposal")
            return None
            
        content = {
            "date": custom_data['[Date]'],
            "recipient": template_content.get('recipient', {}).get('default', []),
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        
        pharmacy = custom_data.get('pharmacy_name', '').strip().replace(' ', '').replace('_', '').lower()
        if pharmacy:
            filename = f"PartnershipProposal-{pharmacy}.pdf"
        else:
            filename = "PartnershipProposal.pdf"
        return self.generate_document(filename, content, "partnership_proposal")

if __name__ == "__main__":
    generator = PartnershipProposalGenerator()
    generator.generate_partnership_proposal()