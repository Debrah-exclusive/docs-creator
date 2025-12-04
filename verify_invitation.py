import os
from document_template import DocumentTemplate

def test_invitation():
    print("Testing Invitation Generation...")
    doc_template = DocumentTemplate()
    
    data = {
        'contributor_name': 'Test Contributor',
        'circle_name': 'Test Circle',
        'date': '2023-12-04'
    }
    
    # This mimics what app.py does: it calls generate_document with the template key
    output_path = doc_template.generate_document('test_invitation.pdf', 
                                               doc_template.get_template_content('invitation_to_the_circle', data), 
                                               document_type='invitation_to_the_circle')
    
    if output_path:
        print(f"Generated: {output_path}")
    else:
        print("Generation failed.")

if __name__ == "__main__":
    test_invitation()
