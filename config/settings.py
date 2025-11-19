# DiscreetKit Document Generator Configuration
# ============================================

import os

from datetime import datetime

# --- Business Information ---
BUSINESS_INFO = {
    "business_name": "Access Discreetkit Ltd",
    "house_number": "57",
    "landmark": "Agrimat Irrigation",
    "street_name": "Kofi Annan East Ave",
    "town": "Accra",
    "gps_address": "GM-033-9072",
    "principal_activity": "To engage in the importation, distribution, supply, and redistribution of health kits, medical consumables, and related sanitary products.",
    "post_office": "LG 918, Legon",
    "email": "dscreetkit@gmail.com",
    "office_phone": "0203001107",
    "stated_capital": ""
}

# --- Directors ---
DIRECTORS = [
    {
        "first_name": "NAEEM",
        "middle_name": "_",
        "last_name": "ABDUL-AZIZ",
        "tin_number": "N/A",
        "dob": "27/07/2005",
        "place_of_birth": "TEMA",
        "house_number": "GK 64, DUBLIN ST",
        "landmark": "MICHEL CAMP",
        "street_name": "DUBLIN ST",
        "town": "TEMA",
        "email": "naeemabdulaziz202@gmail.com",
        "gps_address": "GK-0305-2694",
        "post_office_box": "",
        "occupation": "STUDENT",
        "nationality": "GHANAIAN",
        "phone": "0203001107",
        "share_percentage": "40%"
    },
    {
        "first_name": "Derrick",
        "middle_name": "Kwadjo",
        "last_name": "Debrah",
        "tin_number": "P0065544242",
        "dob": "12 September 2005",
        "place_of_birth": "Accra",
        "house_number": "57",
        "landmark": "Agrimat Irrigation",
        "street_name": "Kofi Annan East Ave",
        "town": "Accra",
        "email": "dk.debrah747@gmail.com",
        "gps_address": "GM-033-9072",
        "post_office_box": "P.O. Box LG 25, Legon Accra, Ghana",
        "occupation": "Student",
        "nationality": "Ghanaian",
        "phone": "0535407104",
        "share_percentage": "30%"
    }
]

# --- Additional Shareholders ---
SHAREHOLDERS = [
    {
        "first_name": "Benedict",
        "middle_name": "Dela",
        "last_name": "Tordzro",
        "tin_number": "N/A",
        "dob": "02-10-2005",
        "place_of_birth": "Hohoe (Hohoe District)",
        "house_number": "5 Yellowwood",
        "landmark": "UPSA",
        "street_name": "Yellowwood Street",
        "town": "Accra",
        "email": "dt.benedict@icloud.com",
        "gps_address": "GA-517-8422",
        "post_office_box": "LG 918, Legon .",
        "occupation": "Student",
        "nationality": "Ghanaian",
        "phone": "0200811683",
        "share_percentage": "30%"
    }
]

# --- Secretary ---
SECRETARY = {
    "first_name": "NAEEM",
    "middle_name": "_",
    "last_name": "ABDUL-AZIZ",
    "tin_number": "N/A",
    "dob": "25/07/2005",
    "place_of_birth": "TEMA",
    "house_number": "GK 64, DUBLIN ST",
    "landmark": "MICHEL CAMP",
    "street_name": "DUBLIN ST",
    "town": "TEMA",
    "gps_address": "GK-0305-2694",
    "post_office_box": "",
    "occupation": "STUDENT",
    "nationality": "GHANAIAN",
    "email": "naeemabdulaziz202@gmail.com",
    "phone": "0203001107"
}


# --- Company Information (for templates) ---
COMPANY_NAME = BUSINESS_INFO["business_name"]
COMPANY_TAGLINE = "Skip the Awkward"
COMPANY_ADDRESS = f"House No. {BUSINESS_INFO['house_number']}, {BUSINESS_INFO['street_name']}, {BUSINESS_INFO['town']}"
COMPANY_EMAIL = BUSINESS_INFO["email"]
COMPANY_PHONE = BUSINESS_INFO["office_phone"]
COMPANY_TWITTER = "@discreetkit"
COMPANY_LINKEDIN = "/company/discreetkit"
DEFAULT_DIRECTOR = DIRECTORS[0]["first_name"] + " " + DIRECTORS[0]["last_name"]
DEFAULT_DIRECTOR_TITLE = "CEO"

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