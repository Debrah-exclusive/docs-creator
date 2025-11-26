import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from document_template import DocumentTemplate  # type: ignore[attr-defined]
except Exception:
    # Fallback stub to satisfy editors/linters if DocumentTemplate isn't exported or import fails
    class DocumentTemplate:
        def get_template_content(self, *args, **kwargs):
            return {}
        def generate_document(self, filename, content, template_key):
            return filename
from datetime import datetime

class BrandBibleGenerator(DocumentTemplate):
    """Generator for Brand and Model Bible documents."""
    
    def generate_brand_bible(self, custom_data=None):
        """Generate a brand and model bible document using template system and custom_data."""
        template_content = self.get_template_content('brand_and_model_bible', custom_data)
        if template_content is None:
            print("❌ No template found for brand_and_model_bible")
            return None
        # Ensure custom_data is a dict
        if custom_data is None:
            custom_data = {}
        content = {
            "date": custom_data.get('date', datetime.now().strftime("%d %B %Y")),
            "recipient": template_content.get('recipient', {}).get('default', []),
            "title": template_content.get('title', ''),
            "salutation": template_content.get('salutation', ''),
            "body": template_content.get('body', []),
            "closing": template_content.get('closing', ''),
            "signature": template_content.get('signature', [])
        }
        filename = "BrandAndModelBible.pdf"
        return self.generate_document(filename, content, "brand_and_model_bible")

if __name__ == "__main__":
    generator = BrandBibleGenerator()
    filename = generator.generate_brand_bible()
    if filename:
        print(f"✅ Generated: {filename}")
