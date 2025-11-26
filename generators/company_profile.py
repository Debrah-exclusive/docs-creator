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
        sections = template_content.get('sections', [])
        body = []
        for section in sections:
            heading = section.get('heading', '').strip()
            content_text = section.get('content', '').strip()
            if heading:
                body.append(f"<b>{heading}</b>")
            if content_text:
                # Preserve line breaks using <br/>
                body.append(content_text.replace('\n', '<br/>'))
            body.append("")
        content = {
            "date": custom_data.get('date', datetime.now().strftime("%d %B %Y")),
            "recipient": [],
            "title": template_content.get('title', ''),
            "salutation": '',
            "body": body,
            "closing": '',
            "signature": template_content.get('signature', [])
        }
        filename = "CompanyProfile.pdf"
        return self.generate_document(filename, content, "company_profile")

if __name__ == "__main__":
    generator = CompanyProfileGenerator()
    filename = generator.generate_company_profile()
    if filename:
        print(f"Company profile generated: {filename}")