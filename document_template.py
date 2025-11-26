def format_name_title(name):
    """Convert a name string to title case, handling None and trimming whitespace."""
    if not name or not isinstance(name, str):
        return name
    return ' '.join([w.capitalize() for w in name.strip().split()])

import os
import sys
from datetime import datetime
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

# Load external settings (single source of truth for customization)
try:
    from config import settings as cfg
except ImportError:  # Fallback if settings not found
    class FallbackCfg:  # minimal defaults
        COMPANY_NAME = "YOUR COMPANY LTD"
        COMPANY_TAGLINE = "Your Tagline"
        DEFAULT_DIRECTOR = "Jane Doe"
        DEFAULT_DIRECTOR_TITLE = "Director"
        COLORS = {
            'cyan_turquoise': "#11534a",  # Darker cyan-turquoise
            'indigo': "#14213d",         # Darker indigo/navy
            'aztec_gold': "#8c6a2f",     # Deeper gold/bronze
            'metallic_yellow': "#bfa100", # Muted/darker yellow
            'light_silver': "#8a8d91"     # Darker silver/grey
        }
        ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    cfg = FallbackCfg()

# --- Configuration ---
COLOR_CYAN_TURQUOISE = colors.HexColor(cfg.COLORS.get('cyan_turquoise', "#11534a"))
COLOR_INDIGO = colors.HexColor(cfg.COLORS.get('indigo', "#14213d"))
COLOR_AZTEC_GOLD = colors.HexColor(cfg.COLORS.get('aztec_gold', "#8c6a2f"))
COLOR_METALLIC_YELLOW = colors.HexColor(cfg.COLORS.get('metallic_yellow', "#bfa100"))
COLOR_LIGHT_SILVER = colors.HexColor(cfg.COLORS.get('light_silver', "#8a8d91"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")  # Output stays internal; not user-configurable yet
ASSETS_DIR = getattr(cfg, 'ASSETS_DIR', os.path.join(BASE_DIR, "assets"))
TEMPLATES_DIR = getattr(cfg, 'TEMPLATES_DIR', os.path.join(BASE_DIR, "templates"))

FONT_REGULAR_PATH = os.path.join(ASSETS_DIR, "Satoshi-Regular.ttf")
FONT_BOLD_PATH = os.path.join(ASSETS_DIR, "Satoshi-Bold.ttf")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

# --- Company Defaults now sourced from settings ---
COMPANY_NAME = getattr(cfg, 'COMPANY_NAME', 'YOUR COMPANY LTD')
COMPANY_TAGLINE = getattr(cfg, 'COMPANY_TAGLINE', 'Your Tagline')
DEFAULT_DIRECTOR = getattr(cfg, 'DEFAULT_DIRECTOR', 'Jane Doe')
DEFAULT_DIRECTOR_TITLE = getattr(cfg, 'DEFAULT_DIRECTOR_TITLE', 'Director')

# Mapping document types to output subfolders
CATEGORY_MAP = {
    "board_resolution": "Board_Resolutions",
    "partnership_proposal": "Partnership_Proposals",
    "nda": "Legal_Documents",
    "employment_contract": "Employment_Contracts",
    "investor_brief": "Investor_Relations",
    "invitation_to_the_circle": "Legal_Documents",
    "pitch_deck": "Pitch_Decks",
    "company_profile": "General_Documents",
    "brand_and_model_bible": "Brand_Guidelines"
}

def get_output_path(document_type: str) -> str:
    """Resolve the output folder for a given document type, creating it if needed."""
    category = CATEGORY_MAP.get(document_type, "General_Documents")
    folder_path = os.path.join(OUTPUT_DIR, category)
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

    # --- Professional, Crisp, Mobile-Friendly Styles ---
    styles["Normal"].fontName = FONT_REGULAR_NAME
    styles["Normal"].fontSize = 13  # Larger for readability
    styles["Normal"].leading = 18   # More line spacing
    styles["Normal"].textColor = colors.HexColor("#111111")  # Near-black for max contrast

    add_or_update_style(styles, "Recipient", spaceBefore=10, fontSize=13, leading=18, textColor=colors.HexColor("#111111"))
    add_or_update_style(styles, "Date", alignment=TA_RIGHT, fontSize=13, leading=18, textColor=colors.HexColor("#111111"))
    add_or_update_style(
        styles,
        "Heading1",
        fontName=FONT_BOLD_NAME,
        fontSize=17,
        leading=22,
        textColor=colors.HexColor("#0a2540"),  # Deep blue for headings
        spaceBefore=16,
        spaceAfter=14,
        alignment=TA_CENTER,
    )
    add_or_update_style(
        styles,
        "Heading2",
        fontName=FONT_BOLD_NAME,
        fontSize=14,
        leading=19,
        textColor=colors.HexColor("#0a2540"),
        spaceAfter=12,
    )
    add_or_update_style(styles, "Body", spaceAfter=14, fontSize=13, leading=18, textColor=colors.HexColor("#111111"))
    add_or_update_style(
        styles,
        "Signature",
        fontName=FONT_REGULAR_NAME,
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#111111"),
        spaceAfter=18,
    )
    add_or_update_style(
        styles,
        "Footer",
        fontName=FONT_REGULAR_NAME,
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#8a8d91"),
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
        company_name_width = canv.stringWidth(COMPANY_NAME, FONT_BOLD_NAME, 12)
    except Exception:
        canv.setFont('Helvetica-Bold', 12)
        company_name_width = canv.stringWidth(COMPANY_NAME, 'Helvetica-Bold', 12)
    
    company_name_x = right_margin_x - company_name_width
    canv.setFillColor(COLOR_INDIGO)
    canv.drawString(company_name_x, company_name_y, COMPANY_NAME)
    
    # Tagline - right-aligned below company name
    tagline_y = company_name_y - (6 * mm)
    try:
        canv.setFont(FONT_REGULAR_NAME, 10)
        tagline_width = canv.stringWidth(COMPANY_TAGLINE, FONT_REGULAR_NAME, 10)
    except Exception:
        canv.setFont('Helvetica', 10)
        tagline_width = canv.stringWidth("Skip the Awkward", 'Helvetica', 10)
    
    tagline_x = right_margin_x - tagline_width
    canv.setFillColor(COLOR_AZTEC_GOLD)
    canv.drawString(tagline_x, tagline_y, COMPANY_TAGLINE)

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

    # Footer content derived from settings (with graceful fallbacks)
    address = getattr(cfg, 'COMPANY_ADDRESS', 'House No. 57, Kofi Annan East Avenue,<br/>Madina, Accra, Ghana<br/>P.O. Box LG 918, Legon')
    email = getattr(cfg, 'COMPANY_EMAIL', 'dscreetkit@gmail.com')
    phone = getattr(cfg, 'COMPANY_PHONE', '+233 20 300 1107')
    instagram = '@discreetkit'
    tiktok = '@discreetkit'

    cols = [
        f"<b>Address</b><br/>{address}",
        f"<b>Contact</b><br/>Email: {email}<br/>Phone: {phone}",
        f"<b>Follow Us</b><br/>Instagram: {instagram}<br/>TikTok: {tiktok}",
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
            # FIX: Added encoding='utf-8' to handle bullet points and special chars correctly
            with open(templates_file, 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            self.templates = {}
            print(f"Warning: Template file not found at {templates_file}")
    
    def get_template_content(self, document_type, custom_data=None):
        """Get template content for a specific document type."""
        if document_type not in self.templates:
            return None

        template = self.templates[document_type].copy()


        # Only these placeholders should be title-cased (actual person names)
        NAME_PLACEHOLDERS = [
            '[Contributor Name]', '[Worker Name]', '[Investor Name]', '[Recipient Name]', '[CEO Name]', '[Director Name]', '[Circle Name]',
            '{{CONTRIBUTOR_NAME}}', '{{WORKER_NAME}}', '{{INVESTOR_NAME}}', '{{RECIPIENT_NAME}}', '{{CEO_NAME}}', '{{DIRECTOR_NAME}}', '{{CIRCLE_NAME}}', '{{NAME}}'
        ]

        # Replace placeholders with actual values, enforcing title case for names only
        replacements = {
            '{{COMPANY_NAME}}': COMPANY_NAME,
            '{{COMPANY_TAGLINE}}': COMPANY_TAGLINE,
            '{{DIRECTOR_NAME}}': format_name_title(DEFAULT_DIRECTOR),
            '{{DIRECTOR_TITLE}}': DEFAULT_DIRECTOR_TITLE,
            '{{DATE}}': datetime.now().strftime("%d %B %Y")
        }

        # Add custom replacements, title-casing only if key is a name placeholder
        if custom_data:
            for k, v in custom_data.items():
                if k in NAME_PLACEHOLDERS:
                    replacements[k] = format_name_title(v)
                else:
                    replacements[k] = v


        # Helper to replace and enforce uppercase for name placeholders in a string
        def replace_and_format(text):
            for placeholder, value in replacements.items():
                if placeholder in NAME_PLACEHOLDERS:
                    text = text.replace(placeholder, format_name_title(value))
                else:
                    text = text.replace(placeholder, str(value))
            return text

        # Replace placeholders in title
        if 'title' in template and isinstance(template['title'], str):
            template['title'] = replace_and_format(template['title'])

        # Replace placeholders in recipient lines, skipping date lines if already present at top
        if 'recipient' in template and isinstance(template['recipient'], dict):
            for key, lines in template['recipient'].items():
                if isinstance(lines, list):
                    new_lines = []
                    for line in lines:
                        # Remove date lines if they duplicate the main date
                        if line.strip().lower().startswith('date:'):
                            continue
                        new_lines.append(replace_and_format(line))
                    template['recipient'][key] = new_lines

        # Replace placeholders in salutation and closing
        for key in ['salutation', 'closing']:
            if key in template and isinstance(template[key], str):
                template[key] = replace_and_format(template[key])

        # Replace placeholders in body paragraphs
        if 'body' in template and isinstance(template['body'], list):
            for i, item in enumerate(template['body']):
                if isinstance(item, str):
                    template['body'][i] = replace_and_format(item)

        # Replace placeholders in signature lines
        if 'signature' in template and isinstance(template['signature'], list):
            for i, item in enumerate(template['signature']):
                if isinstance(item, str):
                    template['signature'][i] = replace_and_format(item)

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