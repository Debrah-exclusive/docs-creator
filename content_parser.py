from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, KeepTogether
from reportlab.lib import colors
from reportlab.lib.units import inch, mm

class ContentParser:
    """
    Dedicated logic layer that reads plain text/JSON and converts it into 
    rich PDF elements (Tables, ListFlowables, Paragraphs).
    """
    def __init__(self, styles):
        self.styles = styles

    def parse_recipient(self, recipient_data):
        """
        Parses recipient data into a Table for alignment.
        Expects a list of strings.
        """
        if not recipient_data or not isinstance(recipient_data, list):
            return []

        # Convert strings to Paragraphs for styling
        data = [[Paragraph(line, self.styles.get_style("Recipient"))] for line in recipient_data]
        
        # Create table
        t = Table(data, colWidths=[6 * inch])
        t.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        return [t, Spacer(1, 0.25 * inch)]

    def parse_body(self, body_data):
        """
        Parses body text. Renders as Paragraphs to maintain original visual style.
        Expects a list of strings.
        """
        if not body_data or not isinstance(body_data, list):
            return []

        story = []
        for item in body_data:
            if not isinstance(item, str):
                continue
            
            # Use Body style for everything, allowing inline XML tags like <b>
            style = self.styles.get_style("Body")
            story.append(Paragraph(item, style))

        return story

    def parse_signature(self, signature_data):
        """
        Parses signature block. Keeps lines together.
        Expects a list of strings.
        """
        if not signature_data or not isinstance(signature_data, list):
            return []

        elements = []
        for line in signature_data:
            elements.append(Paragraph(line, self.styles.get_style("Signature")))
        
        return [KeepTogether(elements)]
