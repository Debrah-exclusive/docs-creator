import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class ContributorCharterGenerator(DocumentTemplate):
    """Generator for Contributor Engagement Charter & NDA documents."""
    
    def generate_charter(self, contributor_name="[Contributor Name]", circle_name="[Circle Name]"):
        """Generate a Contributor Charter document with dynamic date."""
        # Custom data to replace placeholders, including dynamic date
        custom_data = {
            "[Contributor Name]": contributor_name,
            "[Circle Name]": circle_name,
            "{{DATE}}": datetime.now().strftime("%d %B %Y")
        }

        # Get template content with dynamic date
        template_content = self.get_template_content('contributor_charter', custom_data)

        if template_content is None:
            print("❌ No template found for contributor_charter")
            return None

        # Prepare document content
        content = {
            "date": custom_data["{{DATE}}"],
            "recipient": template_content.get('recipient', {}).get('default', []),
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = contributor_name.replace(" ", "_").replace("[", "").replace("]", "")
        filename = f"contributor_charter_{safe_name}_{timestamp}.pdf"

        # Generate document
        return self.generate_document(filename, content, "contributor_charter")
    
if __name__ == "__main__":
    generator = ContributorCharterGenerator()
    
    # You can modify these values or accept user input
    contributor_name = "[Contributor Name]"
    circle_name = "[Circle Name]"
    
    if len(sys.argv) > 1:
        contributor_name = sys.argv[1]
    if len(sys.argv) > 2:
        circle_name = sys.argv[2]
        
    filename = generator.generate_charter(contributor_name, circle_name)
    if filename:
        print(f"Contributor Charter generated: {filename}")
