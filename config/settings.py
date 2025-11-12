# DiscreetKit Document Generator Configuration
# ============================================

import os
from datetime import datetime

# --- Company Information ---
COMPANY_NAME = "ACCESS DISCREETKIT LTD"
COMPANY_TAGLINE = "Skip the Awkward"
COMPANY_ADDRESS = "House No. 57, Kofi Annan East Avenue, Madina, Accra, Ghana"
COMPANY_EMAIL = "discreetkit@gmail.com"
COMPANY_PHONE = "+233 20 300 1107"
COMPANY_TWITTER = "@discreetkit"
COMPANY_LINKEDIN = "/company/discreetkit"

# --- Default Signatories ---
DEFAULT_DIRECTOR = "Naeem Abdul-Aziz"
DEFAULT_DIRECTOR_TITLE = "Director"

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# --- Document Settings ---
DEFAULT_PAGE_SIZE = "A4"
DEFAULT_FONT_SIZE = 11
DEFAULT_HEADER_FONT_SIZE = 14

# --- Date Formats ---
DATE_FORMAT_LONG = "%d %B %Y"  # e.g., "11 November 2025"
DATE_FORMAT_SHORT = "%Y%m%d"   # e.g., "20251111"

# --- Color Scheme ---
COLORS = {
    'cyan_turquoise': "#187f76",
    'indigo': "#1e3a5f", 
    'aztec_gold': "#c48c52",
    'metallic_yellow': "#ffce07",
    'light_silver': "#d7d9db"
}

# --- Output Organization ---
OUTPUT_FOLDERS = {
    'board_resolutions': 'Board_Resolutions',
    'contracts': 'Contracts',
    'employment_contracts': 'Employment_Contracts', 
    'partnerships': 'Partnership_Proposals',
    'legal': 'Legal_Documents',
    'investor_relations': 'Investor_Relations',
    'general': 'General_Documents'
}

# --- Document Categories ---
DOCUMENT_CATEGORIES = {
    'board_resolution': 'board_resolutions',
    'employment_contract': 'employment_contracts',
    'partnership_proposal': 'partnerships',
    'nda': 'legal',
    'investor_brief': 'investor_relations',
    'contract': 'contracts',
    'letterhead': 'general'
}

def get_output_path(document_type):
    """Get the appropriate output path for a document type."""
    category = DOCUMENT_CATEGORIES.get(document_type, 'general')
    folder_name = OUTPUT_FOLDERS[category]
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    
    # Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    return folder_path

def get_timestamp():
    """Get current timestamp for file naming."""
    return datetime.now().strftime(DATE_FORMAT_SHORT)

def get_formatted_date():
    """Get current date in long format."""
    return datetime.now().strftime(DATE_FORMAT_LONG)