import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class PartnershipProposalGenerator(DocumentTemplate):
    """Generator for Partnership Proposal documents."""
    
    def generate_partnership_proposal(self, custom_data=None):
        """Generate a partnership proposal document using template system."""
        # Get template content
        template_content = self.get_template_content('partnership_proposal', custom_data)
        
        if template_content is None:
            print("❌ No template found for partnership_proposal")
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
        filename = f"partnership_proposal_{timestamp}.pdf"
        
        # Generate document with organized output
        return self.generate_document(filename, content, "partnership_proposal")

if __name__ == "__main__":
    generator = PartnershipProposalGenerator()
    filename = generator.generate_partnership_proposal()
    if filename:
        print(f"Partnership proposal generated: {filename}")