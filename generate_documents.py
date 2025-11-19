"""
DiscreetKit Document Generator Suite
====================================

Enhanced modular document generator with organized output structure.
All documents use the exact same beautiful design template with professional organization.

Features:
- ✅ Organized output folders by document category
- ✅ Template-based content system 
- ✅ Timestamped file naming
- ✅ Consistent branding across all documents
- ✅ Easy customization through JSON templates

Usage:
    python generate_documents.py [document_type]
    
Available document types:
    - board_resolution
    - partnership_proposal  
    - nda
    - employment_contract
    - investor_brief
    - all (generates all documents)

Examples:
    python generate_documents.py board_resolution
    python generate_documents.py all

Output Structure:
    output/
    ├── Board_Resolutions/
    ├── Partnership_Proposals/
    ├── Legal_Documents/
    ├── Employment_Contracts/
    ├── Investor_Relations/
    └── General_Documents/
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

class DocumentSuite:
    """Enhanced document generation suite with organized output."""
    
    def __init__(self):
        self.generators = {
            'board_resolution': BoardResolutionGenerator(),
            'partnership_proposal': PartnershipProposalGenerator(),
            'nda': NDAGenerator(),
            'employment_contract': EmploymentContractGenerator(),
            'investor_brief': InvestorBriefGenerator(),
            'contributor_charter': ContributorCharterGenerator()
        }
        
        # Ensure output directory structure exists
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
            'Contracts'
        ]
        
        for directory in directories:
            dir_path = os.path.join(base_output, directory)
            os.makedirs(dir_path, exist_ok=True)
    
    def generate_document(self, doc_type):
        """Generate a specific document type with organized output."""
        if doc_type not in self.generators:
            print(f"❌ Unknown document type: {doc_type}")
            print(f"Available types: {', '.join(self.generators.keys())}")
            return None
        
        print(f"🔄 Generating {doc_type.replace('_', ' ').title()}...")
        
        try:
            if doc_type == 'board_resolution':
                filename = self.generators[doc_type].generate_board_resolution()
            elif doc_type == 'partnership_proposal':
                filename = self.generators[doc_type].generate_partnership_proposal()
            elif doc_type == 'nda':
                filename = self.generators[doc_type].generate_nda()
            elif doc_type == 'employment_contract':
                filename = self.generators[doc_type].generate_employment_contract()
            elif doc_type == 'investor_brief':
                filename = self.generators[doc_type].generate_investor_brief()
            elif doc_type == 'contributor_charter':
                # Default placeholders can be overridden by command-line args later
                filename = self.generators[doc_type].generate_charter()
            
            if filename:
                # Extract just the filename for display
                display_name = os.path.basename(filename)
                folder_name = os.path.basename(os.path.dirname(filename))
                print(f"✅ Generated: {folder_name}/{display_name}")
                return filename
            else:
                print(f"❌ Failed to generate {doc_type}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating {doc_type}: {e}")
            return None
    
    def generate_all(self):
        """Generate all available document types with organized output."""
        print("🚀 DiscreetKit Document Suite - Generating All Documents")
        print("=" * 65)
        print(f"📁 Output directory: ./output/")
        print(f"🕐 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)
        
        generated_files = []
        
        for doc_type in self.generators.keys():
            filename = self.generate_document(doc_type)
            if filename:
                generated_files.append(filename)
            print()  # Add space between documents
        
        print("=" * 65)
        print(f"📊 Summary: Generated {len(generated_files)} of {len(self.generators)} documents")
        print()
        print("📁 Output Structure:")
        self.show_output_structure()
        
        return generated_files
    
    def show_output_structure(self):
        """Display the organized output structure."""
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        if not os.path.exists(output_dir):
            print("   📁 output/ (not yet created)")
            return
        
        print("   📁 output/")
        for item in sorted(os.listdir(output_dir)):
            item_path = os.path.join(output_dir, item)
            if os.path.isdir(item_path):
                files = [f for f in os.listdir(item_path) if f.endswith('.pdf')]
                print(f"   ├── 📂 {item}/ ({len(files)} files)")
                for file in sorted(files)[:3]:  # Show first 3 files
                    print(f"   │   ├── 📄 {file}")
                if len(files) > 3:
                    print(f"   │   └── ... and {len(files) - 3} more files")
    
    def list_available(self):
        """List all available document types with descriptions."""
        print("📋 Available Document Types:")
        print("=" * 40)
        
        descriptions = {
            'board_resolution': 'Bank account opening resolutions',
            'partnership_proposal': 'Strategic partnership proposals',
            'nda': 'Non-disclosure agreements',
            'employment_contract': 'Staff employment contracts', 
            'investor_brief': 'Investment opportunity briefs',
            'contributor_charter': 'Contributor Engagement Charter & NDA'
        }
        
        for doc_type, description in descriptions.items():
            print(f"  � {doc_type:<20} - {description}")
        
        print()
        print("💡 Usage Examples:")
        print("  python generate_documents.py board_resolution")
        print("  python generate_documents.py all")
        print()
        print("📁 All files are organized in output/ folders by category")


def get_placeholders_for_type(doc_type):
    """Define required placeholders for each document type."""
    mapping = {
        'board_resolution': ['recipient', 'branch', 'date'],
        'partnership_proposal': ['partner', 'company', 'date'],
        'nda': ['recipient_name', 'recipient_company', 'date'],
        'employment_contract': ['employee_name', 'job_title', 'start_date', 'amount', 'supervisor_title', 'notice_period', 'date'],
        'investor_brief': ['investor_name', 'investment_firm', 'date'],
        'contributor_charter': ['contributor_name', 'circle_name', 'date'],
    }
    return mapping.get(doc_type, [])

def main():
    """Main function to handle command line arguments with argparse."""
    suite = DocumentSuite()
    parser = argparse.ArgumentParser(description="DiscreetKit Document Generator")
    parser.add_argument('doc_type', type=str, help='Type of document to generate')
    parser.add_argument('--all', action='store_true', help='Generate all documents')
    parser.add_argument('--structure', action='store_true', help='Show output structure')
    parser.add_argument('--list', action='store_true', help='List available document types')

    # Accept arbitrary placeholder arguments
    parser.add_argument('--recipient', type=str)
    parser.add_argument('--branch', type=str)
    parser.add_argument('--partner', type=str)
    parser.add_argument('--company', type=str)
    parser.add_argument('--recipient_name', type=str)
    parser.add_argument('--recipient_company', type=str)
    parser.add_argument('--employee_name', type=str)
    parser.add_argument('--job_title', type=str)
    parser.add_argument('--start_date', type=str)
    parser.add_argument('--amount', type=str)
    parser.add_argument('--supervisor_title', type=str)
    parser.add_argument('--notice_period', type=str)
    parser.add_argument('--investor_name', type=str)
    parser.add_argument('--investment_firm', type=str)
    parser.add_argument('--contributor_name', type=str)
    parser.add_argument('--circle_name', type=str)
    parser.add_argument('--date', type=str)

    args = parser.parse_args()

    doc_type = args.doc_type.lower()

    if args.all or doc_type == 'all':
        suite.generate_all()
        return
    if args.structure:
        print("📁 Current Output Structure:")
        print("=" * 35)
        suite.show_output_structure()
        return
    if args.list or doc_type in ['help', '-h', '--help']:
        print(__doc__)
        suite.list_available()
        return

    # Collect placeholders for this document type
    required_placeholders = get_placeholders_for_type(doc_type)
    custom_data = {}
    for placeholder in required_placeholders:
        value = getattr(args, placeholder, None)
        if not value:
            value = input(f"Enter value for '{placeholder}': ")
        custom_data[placeholder] = value

    # Pass custom_data to generator
    if doc_type in suite.generators:
        generator = suite.generators[doc_type]
        # Use correct method for each generator
        if doc_type == 'board_resolution':
            generator.generate_board_resolution(custom_data)
        elif doc_type == 'partnership_proposal':
            generator.generate_partnership_proposal(custom_data)
        elif doc_type == 'nda':
            generator.generate_nda(custom_data)
        elif doc_type == 'employment_contract':
            generator.generate_employment_contract(custom_data)
        elif doc_type == 'investor_brief':
            generator.generate_investor_brief(custom_data)
        elif doc_type == 'contributor_charter':
            generator.generate_charter(custom_data.get('contributor_name', '[Contributor Name]'), custom_data.get('circle_name', '[Circle Name]'))
    else:
        print(f"❌ Unknown document type: {doc_type}")
        suite.list_available()

if __name__ == "__main__":
    main()