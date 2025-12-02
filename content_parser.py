from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, KeepTogether, Image
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
import os
SVG_ENABLED = True
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
except Exception:
    SVG_ENABLED = False

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
        Supports [SIGNATURE:filename] marker for SVG signatures.
        """
        if not signature_data or not isinstance(signature_data, list):
            return []

        elements = []
        for line in signature_data:
            if line.startswith("[SIGNATURE:") and line.endswith("]"):
                # Extract filename
                filename = line[11:-1]
                # Assume assets dir is relative to this file or passed in styles? 
                # Styles has assets_dir, let's try to use that if possible, or just assume standard location
                # But ContentParser doesn't know about assets_dir directly unless we pass it.
                # doc_styles has it.
                assets_dir = getattr(self.styles, 'assets_dir', os.path.join(os.path.dirname(__file__), 'assets'))
                svg_path = os.path.join(assets_dir, filename)
                
                if os.path.exists(svg_path) and SVG_ENABLED:
                    try:
                        drawing = svg2rlg(svg_path)
                        target_width = 1.5 * inch
                        scale_factor = target_width / drawing.width
                        drawing.width *= scale_factor
                        drawing.height *= scale_factor
                        drawing.scale(scale_factor, scale_factor)
                        elements.append(drawing)
                        elements.append(Spacer(1, 5*mm))
                    except Exception as e:
                        elements.append(Paragraph(f"[Error loading signature: {filename}]", self.styles.get_style("Signature")))
                else:
                    msg = f"[Signature file not available: {filename}]" if SVG_ENABLED else f"[SVG support unavailable: {filename}]"
                    elements.append(Paragraph(msg, self.styles.get_style("Signature")))
            else:
                elements.append(Paragraph(line, self.styles.get_style("Signature")))
        
        return [KeepTogether(elements)]
