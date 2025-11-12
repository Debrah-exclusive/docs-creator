import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class InvestorBriefGenerator(DocumentTemplate):
    """Generator for Investor Brief documents."""
    
    def generate_investor_brief(self, custom_data=None):
        """Generate an investor brief document using template system."""
        # Get template content
        template_content = self.get_template_content('investor_brief', custom_data)
        
        if template_content is None:
            print("❌ No template found for investor_brief")
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
        filename = f"investor_brief_{timestamp}.pdf"
        
        # Generate document with organized output
        return self.generate_document(filename, content, "investor_brief")
    
if __name__ == "__main__":
    generator = InvestorBriefGenerator()
    filename = generator.generate_investor_brief()
    if filename:
        print(f"Investor brief generated: {filename}")