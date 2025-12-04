import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class ContributorCharterGenerator(DocumentTemplate):
    """Generator for Contributor Engagement Charter & NDA documents."""
    
    def generate_charter(self, contributor_name="[Contributor Name]", circle_name="[Circle Name]", custom_data=None):
        """Generate an Invitation to the Circle document with dynamic date and custom_data."""
        if custom_data is None:
            custom_data = {}
        # Fill custom_data with CLI or defaults
        custom_data.setdefault("[Contributor Name]", contributor_name)
        custom_data.setdefault("[Circle Name]", circle_name)
        # Use the date provided by the user, or generate the current date if not provided
        date_value = custom_data.get('date')
        if not date_value or not str(date_value).strip():
            date_value = datetime.now().strftime("%d %B %Y")
        custom_data['date'] = date_value
        custom_data['{{DATE}}'] = date_value
        template_content = self.get_template_content('invitation_to_the_circle', custom_data)
        if template_content is None:
            raise ValueError("No template found for invitation_to_the_circle")
        content = {
            "date": date_value,
            "recipient": template_content.get('recipient', {}).get('default', []),
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_contributor = contributor_name.strip().replace('[', '').replace(']', '').replace('_', '').replace('  ', ' ').replace(' ', '').lower()
        safe_circle = circle_name.strip().replace('[', '').replace(']', '').replace('_', '').replace('  ', ' ').replace(' ', '').lower()
        if safe_contributor and safe_circle:
            filename = f"InvitationToTheCircle-{safe_contributor}-{safe_circle}.pdf"
        elif safe_contributor:
            filename = f"InvitationToTheCircle-{safe_contributor}.pdf"
        else:
            filename = "InvitationToTheCircle.pdf"
        return self.generate_document(filename, content, "invitation_to_the_circle")
    
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
