import os
import sys
from datetime import datetime
from typing import List, Dict
import json
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# --- Configuration ---
COLOR_CYAN_TURQUOISE = colors.HexColor("#187f76")
COLOR_INDIGO = colors.HexColor("#1e3a5f")
COLOR_AZTEC_GOLD = colors.HexColor("#c48c52")
COLOR_METALLIC_YELLOW = colors.HexColor("#ffce07")
COLOR_LIGHT_SILVER = colors.HexColor("#d7d9db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

FONT_REGULAR_PATH = os.path.join(ASSETS_DIR, "Satoshi-Regular.ttf")
FONT_BOLD_PATH = os.path.join(ASSETS_DIR, "Satoshi-Bold.ttf")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

# Company Information
COMPANY_NAME = "ACCESS DISCREETKIT LTD"
COMPANY_TAGLINE = "Skip the Awkward"
DEFAULT_DIRECTOR = "Naeem Abdul-Aziz"
DEFAULT_DIRECTOR_TITLE = "Director"

# Document Categories for Output Organization
DOCUMENT_CATEGORIES = {
    'board_resolution': 'Board_Resolutions',
    'employment_contract': 'Employment_Contracts',
    'partnership_proposal': 'Partnership_Proposals',
    'nda': 'Legal_Documents',
    'investor_brief': 'Investor_Relations',
    'contract': 'Contracts',
    'letterhead': 'General_Documents'
}

def get_output_path(document_type):
    """Get the appropriate output path for a document type."""
    category = DOCUMENT_CATEGORIES.get(document_type, 'General_Documents')
    folder_path = os.path.join(OUTPUT_DIR, category)
    
    # Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    return folder_path

# --- Font Registration with fallbacks ---
if os.path.exists(FONT_REGULAR_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Satoshi", FONT_REGULAR_PATH))
    except Exception:
        pass
if os.path.exists(FONT_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Satoshi-Bold", FONT_BOLD_PATH))
    except Exception:
        pass

# resolved font names (fall back to built-in fonts)
REGISTERED = set(pdfmetrics.getRegisteredFontNames())
FONT_REGULAR_NAME = "Satoshi" if "Satoshi" in REGISTERED else "Helvetica"
FONT_BOLD_NAME = "Satoshi-Bold" if "Satoshi-Bold" in REGISTERED else "Helvetica-Bold"


def add_or_update_style(styles, name: str, parent_name: str = "Normal", **props):
    """Add or update a ParagraphStyle in a stylesheet."""
    if name in styles:
        s = styles[name]
        for k, v in props.items():
            setattr(s, k, v)
    else:
        parent = styles[parent_name] if parent_name in styles else styles["Normal"]
        ps = ParagraphStyle(name=name, parent=parent, **props)
        styles.add(ps)


def get_document_styles():
    """Return a stylesheet with professional standards."""
    styles = getSampleStyleSheet()

    # Base Normal style
    styles["Normal"].fontName = FONT_REGULAR_NAME
    styles["Normal"].fontSize = 10
    styles["Normal"].leading = 14
    styles["Normal"].textColor = COLOR_INDIGO

    add_or_update_style(styles, "Recipient", spaceBefore=10)
    add_or_update_style(styles, "Date", alignment=TA_RIGHT)
    add_or_update_style(
        styles,
        "Heading1",
        fontName=FONT_BOLD_NAME,
        fontSize=14,  # Professional standard for subject lines
        textColor=COLOR_INDIGO,
        spaceBefore=16,
        spaceAfter=12,
        alignment=TA_CENTER,  # Center-aligned for formal documents
    )
    add_or_update_style(styles, "Body", spaceAfter=14, fontSize=11, leading=16)  # Standard body text
    add_or_update_style(
        styles,
        "Footer",
        fontName=FONT_REGULAR_NAME,
        fontSize=8,
        leading=10,
        textColor=COLOR_INDIGO,
    )

    return styles


def draw_header_footer(canv, doc):
    """Draw header and footer with the perfected balanced design."""
    canv.saveState()
    width, height = doc.pagesize

    # --- Header ---
    header_height = 32 * mm  # Accommodates balanced layout

    # Streamlined cyan sidebar - minimal accent only
    canv.setFillColor(COLOR_CYAN_TURQUOISE)
    canv.rect(0, height - header_height, 8 * mm, header_height, stroke=0, fill=1)

    # Logo - larger and proportionate to brand text block
    draw_w = 0
    draw_h = 0
    logo_x_offset = doc.leftMargin + 3 * mm
    if os.path.exists(LOGO_PATH):
        try:
            logo = ImageReader(LOGO_PATH)
            logo_w, logo_h = logo.getSize()
            aspect = logo_h / float(logo_w)
            # Increased logo size to be proportionate with text stack height
            draw_w = 1.4 * inch  # Larger for better proportion with text block
            draw_h = draw_w * aspect
            # Center logo vertically in header
            logo_y = height - (header_height / 2) - (draw_h / 2)
            canv.drawImage(logo, logo_x_offset, logo_y, width=draw_w, height=draw_h, mask='auto')
        except Exception:
            draw_w = 0
            draw_h = 0

    # Brand text positioned at right margin - balanced layout
    page_width = width
    right_margin_x = page_width - doc.rightMargin
    
    # Company Name - right-aligned at margin
    company_name_y = height - (header_height / 2) + (4 * mm)
    try:
        canv.setFont(FONT_BOLD_NAME, 12)
        company_name_width = canv.stringWidth("ACCESS DISCREETKIT LTD", FONT_BOLD_NAME, 12)
    except Exception:
        canv.setFont('Helvetica-Bold', 12)
        company_name_width = canv.stringWidth("ACCESS DISCREETKIT LTD", 'Helvetica-Bold', 12)
    
    company_name_x = right_margin_x - company_name_width
    canv.setFillColor(COLOR_INDIGO)
    canv.drawString(company_name_x, company_name_y, "ACCESS DISCREETKIT LTD")
    
    # Tagline - right-aligned below company name
    tagline_y = company_name_y - (6 * mm)
    try:
        canv.setFont(FONT_REGULAR_NAME, 10)
        tagline_width = canv.stringWidth("Skip the Awkward", FONT_REGULAR_NAME, 10)
    except Exception:
        canv.setFont('Helvetica', 10)
        tagline_width = canv.stringWidth("Skip the Awkward", 'Helvetica', 10)
    
    tagline_x = right_margin_x - tagline_width
    canv.setFillColor(COLOR_AZTEC_GOLD)
    canv.drawString(tagline_x, tagline_y, "Skip the Awkward")

    # Separator line beneath complete layout
    header_bottom = height - header_height - (2 * mm)
    canv.setStrokeColor(COLOR_LIGHT_SILVER)
    canv.setLineWidth(1)  # Clean, professional line
    canv.line(doc.leftMargin, header_bottom, width - doc.rightMargin, header_bottom)

    # --- Footer ---
    left = doc.leftMargin
    right = width - doc.rightMargin
    usable_width = right - left

    # Move footer lower to avoid overlap
    footer_line_y = doc.bottomMargin - (6 * mm)
    if footer_line_y < 12 * mm:
        footer_line_y = 12 * mm

    canv.setStrokeColor(COLOR_LIGHT_SILVER)
    canv.setLineWidth(1)
    canv.line(left, footer_line_y, left + usable_width, footer_line_y)

    styles = get_document_styles()
    footer_style = styles['Footer']

    cols = [
        "<b>Address</b><br/>House No. 57, Kofi Annan East Avenue,<br/>Madina, Accra, Ghana",
        "<b>Contact</b><br/>Email: discreetkit@gmail.com<br/>Phone: +233 20 300 1107",
        "<b>Follow Us</b><br/>Twitter: @discreetkit<br/>LinkedIn: /company/discreetkit",
    ]

    col_width = usable_width / 3.0
    x_positions = [left + i * col_width for i in range(3)]
    padding = 3 * mm

    for i, txt in enumerate(cols):
        p = Paragraph(txt, footer_style)
        w, h = p.wrap(col_width, doc.bottomMargin)
        draw_x = x_positions[i]
        draw_y = footer_line_y - padding - h
        if draw_y < 6 * mm:
            draw_y = 6 * mm
        p.drawOn(canv, draw_x, draw_y)

    canv.restoreState()


class DocumentTemplate:
    """Base template class for all DiscreetKit documents."""
    
    def __init__(self):
        self.styles = get_document_styles()
        self.load_templates()
    
    def load_templates(self):
        """Load document templates from JSON file."""
        templates_file = os.path.join(TEMPLATES_DIR, "document_templates.json")
        try:
            with open(templates_file, 'r') as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            self.templates = {}
            print(f"Warning: Template file not found at {templates_file}")
    
    def get_template_content(self, document_type, custom_data=None):
        """Get template content for a specific document type."""
        if document_type not in self.templates:
            return None
        
        template = self.templates[document_type].copy()
        
        # Replace placeholders with actual values
        replacements = {
            '{{COMPANY_NAME}}': COMPANY_NAME,
            '{{COMPANY_TAGLINE}}': COMPANY_TAGLINE,
            '{{DIRECTOR_NAME}}': DEFAULT_DIRECTOR,
            '{{DIRECTOR_TITLE}}': DEFAULT_DIRECTOR_TITLE,
            '{{DATE}}': datetime.now().strftime("%d %B %Y")
        }
        
        # Add custom replacements
        if custom_data:
            replacements.update(custom_data)
        
        # Replace placeholders in title
        if 'title' in template and isinstance(template['title'], str):
            for placeholder, value in replacements.items():
                template['title'] = template['title'].replace(placeholder, str(value))
        
        # Replace placeholders in salutation and closing
        for key in ['salutation', 'closing']:
            if key in template and isinstance(template[key], str):
                for placeholder, value in replacements.items():
                    template[key] = template[key].replace(placeholder, str(value))
        
        # Replace placeholders in body paragraphs
        if 'body' in template and isinstance(template['body'], list):
            for i, item in enumerate(template['body']):
                if isinstance(item, str):
                    updated_item = item
                    for placeholder, value in replacements.items():
                        updated_item = updated_item.replace(placeholder, str(value))
                    template['body'][i] = updated_item
        
        # Replace placeholders in signature lines
        if 'signature' in template and isinstance(template['signature'], list):
            for i, item in enumerate(template['signature']):
                if isinstance(item, str):
                    updated_item = item
                    for placeholder, value in replacements.items():
                        updated_item = updated_item.replace(placeholder, str(value))
                    template['signature'][i] = updated_item
        
        return template
    
    def generate_document(self, filename: str, content: dict, document_type: str = ""):
        """Generate a document with the standard DiscreetKit template."""
        # Determine output path based on document type
        if document_type:
            output_path = get_output_path(document_type)
            full_filename = os.path.join(output_path, filename)
            print(f"📁 Saving to: {os.path.relpath(output_path)}/{filename}")
        else:
            full_filename = filename
            print(f"📁 Saving to: {filename}")
        
        doc = SimpleDocTemplate(
            full_filename,
            pagesize=A4,
            topMargin=1.6 * inch,  # Adjusted for balanced header
            bottomMargin=1.25 * inch,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
        )

        story = []

        # Small spacer so content doesn't touch header
        story.append(Spacer(1, 0.2 * inch))

        # Date
        story.append(Paragraph(str(content.get('date', '')), self.styles['Date']))
        story.append(Spacer(1, 0.25 * inch))

        # Recipient
        recipient = content.get('recipient', [])
        if isinstance(recipient, list):
            for line in recipient:
                story.append(Paragraph(str(line), self.styles['Recipient']))

        story.append(Spacer(1, 0.25 * inch))

        # Title
        story.append(Paragraph(str(content.get('title', '')), self.styles['Heading1']))
        story.append(Spacer(1, 0.1 * inch))

        # Salutation
        story.append(Paragraph(str(content.get('salutation', '')), self.styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        # Body
        body = content.get('body', [])
        if isinstance(body, list):
            for para in body:
                story.append(Paragraph(str(para), self.styles['Body']))

        # Closing and signature
        story.append(Paragraph(str(content.get('closing', '')), self.styles['Normal']))
        story.append(Spacer(1, 0.25 * inch))
        signature = content.get('signature', [])
        if isinstance(signature, list):
            for line in signature:
                story.append(Paragraph(str(line), self.styles['Normal']))

        try:
            doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
            print(f"✅ Successfully generated: {os.path.relpath(full_filename)}")
            return full_filename
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return None