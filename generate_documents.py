"""
DiscreetKit Document Generator Suite
====================================

Enhanced modular document generator with organized output structure.
This CLI tool bridges the gap between user input and the PDF templates.

Features:
- ✅ Organized output folders by document category
- ✅ Template-based content system 
- ✅ Timestamped file naming
- ✅ Consistent branding across all documents
- ✅ Smart placeholder mapping
- ✅ Automatic Currency Formatting (GHS)

Usage:
    python generate_documents.py [document_type] [arguments]
"""

import os
import sys
from datetime import datetime
import argparse

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all generators
from generators.board_resolution import BoardResolutionGenerator
from generators.partnership_proposal import PartnershipProposalGenerator
from generators.nda import NDAGenerator
from generators.employment_contract import EmploymentContractGenerator
from generators.investor_brief import InvestorBriefGenerator
from generators.contributor_charter import ContributorCharterGenerator
from generators.pitch_deck import PitchDeckGenerator
from generators.company_profile import CompanyProfileGenerator

# --- CONFIGURATION: CLI TO TEMPLATE MAPPING ---
# This maps the variable name in this script to the [Placeholder] in your JSON template.
PLACEHOLDER_MAP = {
    # General
    'date': '[Date]',
    'branch': '[Branch Name]',
    
    # Partnership
    'pharmacy_name': '[Pharmacy Name]',
    'partner_address': '[Partner Address]', 
    
    # NDA
    'recipient_name': '[Recipient Name]',
    'recipient_company': '[Recipient Company]',
    'recipient_address': '[Company Address]',
    
    # Casual Worker / Employment
    'worker_name': '[Worker Name]',
    'worker_address': '[Worker Address]',
    'role': '[Role]',
    'start_date': '[Start Date]',
    'rate': '[Rate]',
    'unit': '[Unit]', 
    'basis': '[Commission/Task Basis]', 
    'payment_frequency': '[Payment Frequency]',
    'notice_period': '[Notice Period]',
    
    # Investor
    'investor_name': '[Investor Name]',
    'investment_firm': '[Investment Firm]',
    'investment_amount': '[Investment Amount]',
    
    # Contributor
    'contributor_name': '[Contributor Name]',
    'circle_name': '[Circle Name]'
}

# Fields that should be auto-formatted as currency
CURRENCY_FIELDS = ['rate', 'amount', 'investment_amount']

def format_currency(value):
    """Format a string/number into GHS currency format (e.g. 70000 -> GHS 70,000.00)."""
    if not value:
        return value
    
    # Clean the input (remove existing GHS, commas, spaces)
    clean_val = str(value).upper().replace('GHS', '').replace(',', '').strip()
    
    try:
        num_val = float(clean_val)
        # Format with commas and 2 decimal places
        return f"GHS {num_val:,.2f}"
    except ValueError:
        # If it's not a clean number (e.g. "5% equity"), return as is
        return value

def get_placeholders_for_type(doc_type):
    """Define required CLI inputs for each document type."""
    mapping = {
        'board_resolution': ['branch', 'date'],
        'partnership_proposal': ['pharmacy_name', 'partner_address', 'date'],
        'nda': ['recipient_name', 'recipient_company', 'recipient_address', 'date'],
        'employment_contract': ['worker_name', 'worker_address', 'role', 'start_date', 'rate', 'unit', 'basis', 'payment_frequency', 'notice_period', 'date'],
        'investor_brief': ['investor_name', 'investment_firm', 'investment_amount', 'date'],
        'contributor_charter': ['contributor_name', 'circle_name', 'date'],
        'pitch_deck': ['date'],
        'company_profile': ['date'],
    }
    return mapping.get(doc_type, [])

class DocumentSuite:
    """Enhanced document generation suite with organized output."""
    
    def __init__(self):
        self.generators = {
            'board_resolution': BoardResolutionGenerator(),
            'partnership_proposal': PartnershipProposalGenerator(),
            'nda': NDAGenerator(),
            'employment_contract': EmploymentContractGenerator(),
            'investor_brief': InvestorBriefGenerator(),
            'contributor_charter': ContributorCharterGenerator(),
            'pitch_deck': PitchDeckGenerator(),
            'company_profile': CompanyProfileGenerator()
        }
        self.setup_output_directories()
    
    def setup_output_directories(self):
        """Create organized output directory structure."""
        base_output = os.path.join(os.path.dirname(__file__), 'output')
        directories = [
            'Board_Resolutions',
            'Partnership_Proposals', 
            'Legal_Documents',
            'Employment_Contracts',
            'Investor_Relations',
            'General_Documents',
            'Pitch_Decks'
        ]
        for directory in directories:
            dir_path = os.path.join(base_output, directory)
            os.makedirs(dir_path, exist_ok=True)
    
    def generate_document(self, doc_type, custom_data=None):
        """Generate a specific document type with passed data."""
        if doc_type not in self.generators:
            print(f"❌ Unknown document type: {doc_type}")
            return None
        
        print(f"🔄 Generating {doc_type.replace('_', ' ').title()}...")
        
        try:
            # Pass custom_data to all generators
            if doc_type == 'board_resolution':
                filename = self.generators[doc_type].generate_board_resolution(custom_data)
            elif doc_type == 'partnership_proposal':
                filename = self.generators[doc_type].generate_partnership_proposal(custom_data)
            elif doc_type == 'nda':
                filename = self.generators[doc_type].generate_nda(custom_data)
            elif doc_type == 'employment_contract':
                filename = self.generators[doc_type].generate_employment_contract(custom_data)
            elif doc_type == 'investor_brief':
                filename = self.generators[doc_type].generate_investor_brief(custom_data)
            elif doc_type == 'contributor_charter':
                c_name = custom_data.get('contributor_name', '[Contributor Name]') if custom_data else '[Contributor Name]'
                c_circle = custom_data.get('circle_name', '[Circle Name]') if custom_data else '[Circle Name]'
                filename = self.generators[doc_type].generate_charter(c_name, c_circle, custom_data)
            elif doc_type == 'pitch_deck':
                filename = self.generators[doc_type].generate_pitch_deck(custom_data)
            elif doc_type == 'company_profile':
                filename = self.generators[doc_type].generate_company_profile(custom_data)
            
            if filename:
                display_name = os.path.basename(filename)
                folder_name = os.path.basename(os.path.dirname(filename))
                print(f"✅ Generated: {folder_name}/{display_name}")
                return filename
            else:
                print(f"❌ Failed to generate {doc_type}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating {doc_type}: {e}")
            # Debugging: un-comment next line to see full stack trace
            # import traceback; traceback.print_exc()
            return None
    
    def generate_all(self):
        """Generate all available document types using defaults."""
        print("🚀 DiscreetKit Document Suite - Generating All Documents")
        generated_files = []
        for doc_type in self.generators.keys():
            filename = self.generate_document(doc_type, {})
            if filename:
                generated_files.append(filename)
            print()
        
        print(f"📊 Summary: Generated {len(generated_files)} of {len(self.generators)} documents")
        return generated_files

    def list_available(self):
        """List available document types."""
        print("📋 Available Document Types:")
        types = {
            'board_resolution': 'Bank/Admin Resolutions',
            'partnership_proposal': 'Pharmacy/Lab Proposals',
            'nda': 'Standard NDA',
            'employment_contract': 'Casual Worker Agreements',
            'investor_brief': 'Seed Round Brief',
            'contributor_charter': 'Contributor Onboarding',
            'pitch_deck': 'Investment Pitch Deck',
            'company_profile': 'Company Profile Document'
        }
        for dt, desc in types.items():
            print(f"  • {dt:<22} - {desc}")

def main():
    """Main entry point."""
    suite = DocumentSuite()
    parser = argparse.ArgumentParser(description="DiscreetKit Document Generator")
    parser.add_argument('doc_type', type=str, help='Type of document to generate (or "all")')
    parser.add_argument('--all', action='store_true', help='Generate all documents')
    parser.add_argument('--list', action='store_true', help='List available types')

    # --- Dynamic Arguments for Custom Data ---
    # General
    parser.add_argument('--date', type=str, help="Date of document")
    parser.add_argument('--branch', type=str, help="Bank Branch Name")
    
    # Partnership
    parser.add_argument('--pharmacy-name', dest='pharmacy_name', type=str)
    parser.add_argument('--partner-address', dest='partner_address', type=str)
    
    # NDA
    parser.add_argument('--recipient-name', dest='recipient_name', type=str)
    parser.add_argument('--recipient-company', dest='recipient_company', type=str)
    parser.add_argument('--recipient-address', dest='recipient_address', type=str)
    
    # Worker / Employment
    parser.add_argument('--worker-name', dest='worker_name', type=str)
    parser.add_argument('--worker-address', dest='worker_address', type=str)
    parser.add_argument('--role', type=str, help="Job Role e.g. 'Delivery Rider'")
    parser.add_argument('--start-date', dest='start_date', type=str)
    parser.add_argument('--rate', type=str, help="Pay rate e.g. '20'")
    parser.add_argument('--unit', type=str, help="Pay unit e.g. 'per delivery'")
    parser.add_argument('--basis', type=str, help="e.g. 'Task-Based'")
    parser.add_argument('--frequency', dest='payment_frequency', type=str, help="e.g. 'Weekly'")
    parser.add_argument('--notice', dest='notice_period', type=str, help="e.g. '24 hours'")

    # Investor
    parser.add_argument('--investor-name', dest='investor_name', type=str)
    parser.add_argument('--investment-firm', dest='investment_firm', type=str)
    parser.add_argument('--amount', dest='investment_amount', type=str, help="Ask amount e.g. '50000'")

    # Contributor
    parser.add_argument('--contributor-name', dest='contributor_name', type=str)
    parser.add_argument('--circle-name', dest='circle_name', type=str)

    args = parser.parse_args()
    doc_type = args.doc_type.lower()

    if args.all or doc_type == 'all':
        suite.generate_all()
        return
    if args.list or doc_type in ['help', '-h']:
        suite.list_available()
        return

    # 1. Identify required fields for the requested doc type
    required_fields = get_placeholders_for_type(doc_type)
    
    # 2. Build custom_data dictionary
    custom_data = {}
    
    # If user didn't provide arguments via flags, ask interactively
    if doc_type in suite.generators:
        print(f"📝 Enter details for {doc_type.replace('_', ' ').title()}:")
        for field in required_fields:
            # Check if provided via CLI flag
            val = getattr(args, field, None)
            if not val:
                prompt_text = field.replace('_', ' ').title()
                if field in CURRENCY_FIELDS:
                    prompt_text += " (Numeric)"
                val = input(f"  > {prompt_text}: ")
            
            # --- AUTO CURRENCY FORMATTING ---
            if field in CURRENCY_FIELDS:
                val = format_currency(val)
            
            # Map to the template key (e.g. worker_name -> [Worker Name])
            template_key = PLACEHOLDER_MAP.get(field, field)
            custom_data[template_key] = val
            
            # Also keep original key for filename logic in generators
            custom_data[field] = val 
            
        # 3. Generate
        suite.generate_document(doc_type, custom_data)
    else:
        print(f"❌ Error: '{doc_type}' is not a valid document type.")
        suite.list_available()

if __name__ == "__main__":
    main()