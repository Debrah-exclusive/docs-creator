import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class EmploymentContractGenerator(DocumentTemplate):
    """Generator for Casual Worker Engagement documents."""
    
    def generate_employment_contract(self, custom_data=None):
        """Generate a casual engagement document using custom_data."""
        if custom_data is None:
            custom_data = {}
            
        # Ensure default keys exist if not provided via CLI
        custom_data.setdefault('[Date]', custom_data.get('date', datetime.now().strftime("%d %B %Y")))
        
        template_content = self.get_template_content('employment_contract', custom_data)
        if template_content is None:
            print("❌ No template found for employment_contract")
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
        
        # Filename based on worker name
        worker_name = custom_data.get('worker_name', '').strip().replace(' ', '').replace('_', '').lower()
        if worker_name:
            filename = f"EmploymentContract-{worker_name}.pdf"
        else:
            filename = "EmploymentContract.pdf"
        return self.generate_document(filename, content, "employment_contract")

if __name__ == "__main__":
    generator = EmploymentContractGenerator()
    generator.generate_employment_contract()