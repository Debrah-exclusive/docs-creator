import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_template import DocumentTemplate
from datetime import datetime

class EmploymentContractGenerator(DocumentTemplate):
    """Generator for Employment Contract documents."""
    
    def generate_employment_contract(self, custom_data=None):
        """Generate an employment contract document using custom_data."""
        if custom_data is None:
            custom_data = {}
        template_content = self.get_template_content('employment_contract', custom_data)
        if template_content is None:
            print("❌ No template found for employment_contract")
            return None
        content = {
            "date": custom_data.get('date', datetime.now().strftime("%d %B %Y")),
            "recipient": [custom_data.get('employee_name', r) for r in template_content.get('recipient', {}).get('default', [])],
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        employee_name = custom_data.get('employee_name', '').strip().replace(' ', '_').lower() if custom_data.get('employee_name') else None
        if employee_name:
            filename = f"employment_contract_{employee_name}.pdf"
        else:
            filename = "employment_contract_document.pdf"
        return self.generate_document(filename, content, "employment_contract")
    
    def get_default_contract_data(self):
        """Default employment contract content."""
        return {
            "date": datetime.now().strftime("%d %B %Y"),
            "recipient": [
                "[Employee Name]",
                "[Employee Address]",
                "Accra, Ghana"
            ],
            "title": "EMPLOYMENT CONTRACT",
            "salutation": "Dear [Employee Name],",
            "body": [
                "We are pleased to offer you employment with Access DiscreetKit Ltd under the following terms and conditions:",
                "<b>1. Position and Duties:</b> You will be employed as [Job Title] and will report to [Supervisor Title]. Your duties will include [Job Description].",
                "<b>2. Commencement:</b> Your employment will commence on [Start Date] and will continue until terminated by either party in accordance with the terms of this contract.",
                "<b>3. Remuneration:</b> Your gross monthly salary will be GHS [Amount] payable monthly in arrears by bank transfer.",
                "<b>4. Working Hours:</b> Normal working hours are Monday to Friday, 8:00 AM to 5:00 PM with a one-hour lunch break.",
                "<b>5. Annual Leave:</b> You are entitled to 21 working days of annual leave per calendar year, plus public holidays as declared by the Government of Ghana.",
                "<b>6. Probationary Period:</b> Your employment will be subject to a probationary period of [X] months from your commencement date.",
                "<b>7. Confidentiality:</b> You agree to maintain strict confidentiality regarding all company information and client matters.",
                "<b>8. Termination:</b> Either party may terminate this employment by giving [Notice Period] written notice to the other party.",
                "Please confirm your acceptance by signing and returning a copy of this letter."
            ],
            "closing": "We look forward to welcoming you to our team.",
            "signature": [
                "",
                "Yours sincerely,",
                "",
                "",
                "______________________________",
                "Naeem Abdul-Aziz",
                "Director",
                "Access DiscreetKit Ltd",
                "",
                "I accept the terms and conditions of employment:",
                "",
                "______________________________",
                "[Employee Name]",
                "",
                "Date: _______________"
            ]
        }

if __name__ == "__main__":
    generator = EmploymentContractGenerator()
    filename = generator.generate_employment_contract()
    print(f"Employment contract generated: {filename}")