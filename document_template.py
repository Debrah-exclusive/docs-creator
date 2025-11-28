import os
import sys
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Import new components
from document_styles import DocumentStyles
from content_parser import ContentParser

# --- Configuration Loading ---
try:
    from config import settings as cfg
except ImportError:
    class FallbackCfg:
        COMPANY_NAME = "YOUR COMPANY LTD"
        COMPANY_TAGLINE = "Your Tagline"
        DEFAULT_DIRECTOR = "Jane Doe"
        DEFAULT_DIRECTOR_TITLE = "Director"
        # Assets/Templates dir relative to this file
        ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        COMPANY_ADDRESS = 'House No. 57, Kofi Annan East Avenue,<br/>Madina, Accra, Ghana<br/>P.O. Box LG 918, Legon'
        COMPANY_EMAIL = 'dscreetkit@gmail.com'
        COMPANY_PHONE = '+233 20 300 1107'
    cfg = FallbackCfg()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = getattr(cfg, 'ASSETS_DIR', os.path.join(BASE_DIR, "assets"))
TEMPLATES_DIR = getattr(cfg, 'TEMPLATES_DIR', os.path.join(BASE_DIR, "templates"))
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
COMPANY_NAME = getattr(cfg, 'COMPANY_NAME', 'YOUR COMPANY LTD')
COMPANY_TAGLINE = getattr(cfg, 'COMPANY_TAGLINE', 'Your Tagline')
DEFAULT_DIRECTOR = getattr(cfg, 'DEFAULT_DIRECTOR', 'Jane Doe')
DEFAULT_DIRECTOR_TITLE = getattr(cfg, 'DEFAULT_DIRECTOR_TITLE', 'Director')

CATEGORY_MAP = {
    "board_resolution": "Board_Resolutions",
    "partnership_proposal": "Partnership_Proposals",
    "nda": "Legal_Documents",
    "employment_contract": "Employment_Contracts",
    "investor_brief": "Investor_Relations",
    "invitation_to_the_circle": "Legal_Documents",
    "pitch_deck": "Pitch_Decks",
    "company_profile": "General_Documents",
    "brand_and_model_bible": "Brand_Guidelines",
    "circle_mandate": "Internal_Memos"
}

def format_name_title(name):
    """Convert a name string to title case, handling None and trimming whitespace."""
    if not name or not isinstance(name, str):
        return name
    return ' '.join([w.capitalize() for w in name.strip().split()])

def get_output_path(document_type: str) -> str:
    """Resolve the output folder for a given document type, creating it if needed."""
    category = CATEGORY_MAP.get(document_type, "General_Documents")
    folder_path = os.path.join(OUTPUT_DIR, category)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

class DocumentTemplate:
    """
    Layout Engine & Orchestrator.
    Assembles the final PDF using DocumentStyles and ContentParser.
    """
    
    def __init__(self):
        self.doc_styles = DocumentStyles(ASSETS_DIR)
        self.parser = ContentParser(self.doc_styles)
        self.load_templates()
    
    def load_templates(self):
        """Load document templates from JSON file."""
        templates_file = os.path.join(TEMPLATES_DIR, "document_templates.json")
        try:
            with open(templates_file, 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            self.templates = {}
            print(f"Warning: Template file not found at {templates_file}")

    def get_template_content(self, document_type, custom_data=None):
        """Get template content for a specific document type with placeholder replacement."""
        if document_type not in self.templates:
            return None

        template = self.templates[document_type].copy()

        # Placeholders
        NAME_PLACEHOLDERS = [
            '[Contributor Name]', '[Worker Name]', '[Investor Name]', '[Recipient Name]', '[CEO Name]', '[Director Name]', '[Circle Name]',
            '{{CONTRIBUTOR_NAME}}', '{{WORKER_NAME}}', '{{INVESTOR_NAME}}', '{{RECIPIENT_NAME}}', '{{CEO_NAME}}', '{{DIRECTOR_NAME}}', '{{CIRCLE_NAME}}', '{{NAME}}'
        ]

        replacements = {
            '{{COMPANY_NAME}}': COMPANY_NAME,
            '{{COMPANY_TAGLINE}}': COMPANY_TAGLINE,
            '{{DIRECTOR_NAME}}': format_name_title(DEFAULT_DIRECTOR),
            '{{DIRECTOR_TITLE}}': DEFAULT_DIRECTOR_TITLE,
            '{{DATE}}': datetime.now().strftime("%d %B %Y")
        }

        if custom_data:
            for k, v in custom_data.items():
                if k in NAME_PLACEHOLDERS:
                    replacements[k] = format_name_title(v)
                else:
                    replacements[k] = v

        def replace_and_format(text):
            if not isinstance(text, str): return text
            for placeholder, value in replacements.items():
                if placeholder in NAME_PLACEHOLDERS:
                    text = text.replace(placeholder, format_name_title(str(value)))
                else:
                    text = text.replace(placeholder, str(value))
            return text

        # Recursive replacement helper
        def process_node(node):
            if isinstance(node, str):
                return replace_and_format(node)
            elif isinstance(node, list):
                return [process_node(item) for item in node]
            elif isinstance(node, dict):
                return {k: process_node(v) for k, v in node.items()}
            return node

        return process_node(template)

    def draw_header_footer(self, canv, doc):
        """Draw header and footer using DocumentStyles."""
        canv.saveState()
        width, height = doc.pagesize
        styles = self.doc_styles

        # --- Header ---
        header_height = 32 * mm
        
        # Cyan Sidebar
        canv.setFillColor(styles.COLOR_CYAN_TURQUOISE)
        canv.rect(0, height - header_height, 8 * mm, header_height, stroke=0, fill=1)

        # Logo
        if os.path.exists(LOGO_PATH):
            try:
                logo = ImageReader(LOGO_PATH)
                logo_w, logo_h = logo.getSize()
                aspect = logo_h / float(logo_w)
                draw_w = 1.4 * inch
                draw_h = draw_w * aspect
                logo_y = height - (header_height / 2) - (draw_h / 2)
                logo_x_offset = doc.leftMargin + 3 * mm
                canv.drawImage(logo, logo_x_offset, logo_y, width=draw_w, height=draw_h, mask='auto')
            except Exception:
                pass

        # Company Name & Tagline
        right_margin_x = width - doc.rightMargin
        company_name_y = height - (header_height / 2) + (4 * mm)
        
        canv.setFont(styles.font_bold_name, 12)
        canv.setFillColor(styles.COLOR_INDIGO)
        canv.drawRightString(right_margin_x, company_name_y, COMPANY_NAME)
        
        tagline_y = company_name_y - (6 * mm)
        canv.setFont(styles.font_regular_name, 10)
        canv.setFillColor(styles.COLOR_AZTEC_GOLD)
        canv.drawRightString(right_margin_x, tagline_y, COMPANY_TAGLINE)

        # Separator Line
        header_bottom = height - header_height - (2 * mm)
        canv.setStrokeColor(styles.COLOR_LIGHT_SILVER)
        canv.setLineWidth(1)
        canv.line(doc.leftMargin, header_bottom, width - doc.rightMargin, header_bottom)

        # --- Footer ---
        footer_line_y = doc.bottomMargin - (6 * mm)
        if footer_line_y < 12 * mm: footer_line_y = 12 * mm

        canv.setStrokeColor(styles.COLOR_LIGHT_SILVER)
        canv.setLineWidth(1)
        canv.line(doc.leftMargin, footer_line_y, width - doc.rightMargin, footer_line_y)

        # Footer Content
        address = getattr(cfg, 'COMPANY_ADDRESS', '')
        email = getattr(cfg, 'COMPANY_EMAIL', '')
        phone = getattr(cfg, 'COMPANY_PHONE', '')
        instagram = '@discreetkit'
        tiktok = '@discreetkit'

        cols = [
            f"<b>Address</b><br/>{address}",
            f"<b>Contact</b><br/>Email: {email}<br/>Phone: {phone}",
            f"<b>Follow Us</b><br/>Instagram: {instagram}<br/>TikTok: {tiktok}",
        ]

        usable_width = width - doc.leftMargin - doc.rightMargin
        col_width = usable_width / 3.0
        footer_style = styles.get_style('Footer')

        for i, txt in enumerate(cols):
            p = Paragraph(txt, footer_style)
            w, h = p.wrap(col_width, doc.bottomMargin)
            draw_x = doc.leftMargin + (i * col_width)
            draw_y = footer_line_y - (3 * mm) - h
            if draw_y < 6 * mm: draw_y = 6 * mm
            p.drawOn(canv, draw_x, draw_y)

        canv.restoreState()

    def generate_document(self, filename: str, content: dict, document_type: str = ""):
        """Generate the PDF document."""
        if document_type:
            output_path = get_output_path(document_type)
            full_filename = os.path.join(output_path, filename)
            print(f"Saving to: {os.path.relpath(output_path)}/{filename}")
        else:
            full_filename = filename
            print(f"Saving to: {filename}")
        
        doc = SimpleDocTemplate(
            full_filename,
            pagesize=A4,
            topMargin=1.6 * inch,
            bottomMargin=1.25 * inch,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
        )

        story = []
        
        # Spacer
        story.append(Spacer(1, 0.2 * inch))

        # Date
        if content.get('date'):
            story.append(Paragraph(str(content['date']), self.doc_styles.get_style('Date')))
            story.append(Spacer(1, 0.4 * inch))  # Widen: More space after date

        # Recipient
        story.extend(self.parser.parse_recipient(content.get('recipient')))

        # Title
        if content.get('title'):
            story.append(Paragraph(str(content['title']), self.doc_styles.get_style('Heading1')))
            # Spacer removed; Heading1 style has spaceAfter=30

        # Salutation
        if content.get('salutation'):
            story.append(Paragraph(str(content['salutation']), self.doc_styles.get_style('Normal')))
            story.append(Spacer(1, 0.2 * inch))  # Widen: More space after salutation

        # Body
        story.extend(self.parser.parse_body(content.get('body')))

        # Closing
        if content.get('closing'):
            story.append(Paragraph(str(content['closing']), self.doc_styles.get_style('Normal')))
            story.append(Spacer(1, 0.25 * inch))

        # Signature
        story.extend(self.parser.parse_signature(content.get('signature')))

        try:
            doc.build(story, onFirstPage=self.draw_header_footer, onLaterPages=self.draw_header_footer)
            print(f"Successfully generated: {os.path.relpath(full_filename)}")
            return full_filename
        except Exception as e:
            print(f"Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            return None