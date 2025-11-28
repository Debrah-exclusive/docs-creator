import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class PharmacyLOIGenerator(DocumentTemplate):
    """Generator for Pharmacy LOI documents."""
    
    def generate_pharmacy_loi(self, custom_data=None):
        """Generate a pharmacy LOI document."""
        if custom_data is None:
            custom_data = {}

        custom_data.setdefault('[Date]', custom_data.get('date', datetime.now().strftime("%d %B %Y")))

        template_content = self.get_template_content('pharmacy_loi', custom_data)
        if template_content is None:
            print("❌ No template found for pharmacy_loi")
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
            filename = f"PharmacyLOI-{pharmacy}.pdf"
        else:
            filename = "PharmacyLOI.pdf"
        return self.generate_document(filename, content, "pharmacy_loi")

if __name__ == "__main__":
    generator = PharmacyLOIGenerator()
    generator.generate_pharmacy_loi()
