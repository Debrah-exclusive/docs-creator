import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class CompanyProfileGenerator(DocumentTemplate):
    """Generator for Company Profile documents."""
    
    def generate_company_profile(self, custom_data=None):
        """Generate a company profile document using template system and custom_data."""
        template_content = self.get_template_content('company_profile', custom_data)
        if template_content is None:
            print("❌ No template found for company_profile")
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
        filename = "company_profile_document.pdf"
        return self.generate_document(filename, content, "company_profile")

if __name__ == "__main__":
    generator = CompanyProfileGenerator()
    filename = generator.generate_company_profile()
    if filename:
        print(f"Company profile generated: {filename}")