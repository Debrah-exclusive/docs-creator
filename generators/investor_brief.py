import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class InvestorBriefGenerator(DocumentTemplate):
    """Generator for Investor Brief documents."""
    
    def generate_investor_brief(self, custom_data=None):
        """Generate an investor brief document."""
        if custom_data is None:
            custom_data = {}

        # Ensure date is present
        custom_data.setdefault('[Date]', custom_data.get('date', datetime.now().strftime("%d %B %Y")))
        
        # This line relies on custom_data having '[Investment Amount]' key from the CLI mapping
        template_content = self.get_template_content('investor_brief', custom_data)
        if template_content is None:
            print("❌ No template found for investor_brief")
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
        
        investor = custom_data.get('investor_name', '').strip().replace(' ', '_').lower()
        firm = custom_data.get('investment_firm', '').strip().replace(' ', '_').lower()
        
        if firm:
            filename = f"investor_brief_{firm}.pdf"
        elif investor:
            filename = f"investor_brief_{investor}.pdf"
        else:
            filename = "investor_brief_template.pdf"
            
        return self.generate_document(filename, content, "investor_brief")
    
if __name__ == "__main__":
    generator = InvestorBriefGenerator()
    generator.generate_investor_brief()