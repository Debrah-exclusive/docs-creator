import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class DocumentStyles:
    """
    Centralizes all typography, colors, and spacing rules.
    Enforces the visual hierarchy (H1 > H2 > Body).
    """
    
    # --- Colors ---
    COLOR_CYAN_TURQUOISE = colors.HexColor("#11534a")
    COLOR_INDIGO = colors.HexColor("#14213d")
    COLOR_AZTEC_GOLD = colors.HexColor("#8c6a2f")
    COLOR_METALLIC_YELLOW = colors.HexColor("#bfa100")
    COLOR_LIGHT_SILVER = colors.HexColor("#8a8d91")
    COLOR_BLACK = colors.HexColor("#111111")
    COLOR_HEADING = colors.HexColor("#0a2540")

    def __init__(self, assets_dir):
        self.assets_dir = assets_dir
        self.font_regular_name = "Helvetica"
        self.font_bold_name = "Helvetica-Bold"
        self._register_fonts()
        self.styles = self._create_stylesheet()

    def _register_fonts(self):
        """Registers custom fonts if available, otherwise falls back to defaults."""
        font_regular_path = os.path.join(self.assets_dir, "Satoshi-Regular.ttf")
        font_bold_path = os.path.join(self.assets_dir, "Satoshi-Bold.ttf")

        if os.path.exists(font_regular_path):
            try:
                pdfmetrics.registerFont(TTFont("Satoshi", font_regular_path))
                self.font_regular_name = "Satoshi"
            except Exception:
                pass
        
        if os.path.exists(font_bold_path):
            try:
                pdfmetrics.registerFont(TTFont("Satoshi-Bold", font_bold_path))
                self.font_bold_name = "Satoshi-Bold"
            except Exception:
                pass

    def _add_or_update_style(self, styles, name, parent_name="Normal", **props):
        """Helper to add or update a style in the stylesheet."""
        if name in styles:
            s = styles[name]
            for k, v in props.items():
                setattr(s, k, v)
        else:
            parent = styles[parent_name] if parent_name in styles else styles["Normal"]
            ps = ParagraphStyle(name=name, parent=parent, **props)
            styles.add(ps)

    def _create_stylesheet(self):
        """Creates and returns the complete stylesheet."""
        styles = getSampleStyleSheet()

        # --- Base Normal Style ---
        styles["Normal"].fontName = self.font_regular_name
        styles["Normal"].fontSize = 11  # Slightly smaller for professional look
        styles["Normal"].leading = 16   # Good readability
        styles["Normal"].textColor = self.COLOR_BLACK
        styles["Normal"].alignment = TA_LEFT

        # --- Specific Styles ---
        
        # Recipient (Address block) - Tighter
        self._add_or_update_style(styles, "Recipient", 
                                  spaceBefore=12, 
                                  fontSize=11, 
                                  leading=15, 
                                  textColor=self.COLOR_BLACK)

        # Date (Right aligned)
        self._add_or_update_style(styles, "Date", 
                                  alignment=TA_RIGHT, 
                                  fontSize=11, 
                                  leading=15, 
                                  textColor=self.COLOR_BLACK)

        # Heading 1 (Document Title) - Big and bold, lots of space after
        self._add_or_update_style(styles, "Heading1",
                                  fontName=self.font_bold_name,
                                  fontSize=24,  # Much larger
                                  leading=30,
                                  textColor=self.COLOR_HEADING,
                                  spaceBefore=24,
                                  spaceAfter=30,  # Clear separation from content
                                  alignment=TA_CENTER)

        # Heading 2 (Section Headers) - Distinct, space before, tight after
        self._add_or_update_style(styles, "Heading2",
                                  fontName=self.font_bold_name,
                                  fontSize=14,
                                  leading=18,
                                  textColor=self.COLOR_HEADING,
                                  spaceBefore=20,  # Widen: Push away from previous section
                                  spaceAfter=8)    # Tighten: Keep close to own content
        
        # Body Text - Readable, professional
        self._add_or_update_style(styles, "Body", 
                                  spaceAfter=12,   # Paragraph separation
                                  fontSize=11, 
                                  leading=17,      # Airy line height
                                  textColor=self.COLOR_BLACK)

        # Signature - Tight
        self._add_or_update_style(styles, "Signature",
                                  fontName=self.font_regular_name,
                                  fontSize=11,
                                  leading=15,
                                  textColor=self.COLOR_BLACK,
                                  spaceAfter=4) 

        # Footer
        self._add_or_update_style(styles, "Footer",
                                  fontName=self.font_regular_name,
                                  fontSize=8,
                                  leading=10,
                                  textColor=self.COLOR_LIGHT_SILVER)
        
        # Bullet Points
        self._add_or_update_style(styles, "Bullet",
                                  parent_name="Body",
                                  leftIndent=20,
                                  firstLineIndent=0,
                                  spaceAfter=6)

        return styles

    def get_style(self, name):
        """Retrieve a style by name."""
        return self.styles[name]
