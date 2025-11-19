# DiscreetKit Document Generator

DiscreetKit is a lightweight, template-driven tool for generating professional PDF documents. It's designed to be easily customized for any company's branding, colors, and legal boilerplate with minimal code changes.

## Features

- **Template-Driven:** Document structures are defined in a simple JSON file.
- **Easy Branding:** Customize logos, fonts, colors, and company details in a single configuration file.
- **Organized Output:** Automatically sorts generated documents into category-based folders.
- **Consistent Branding:** Ensures all documents have a uniform header and footer.
- **CLI-Powered:** Generate documents and provide placeholder values directly from the command line.
- **Extensible:** Easily add new document types and generators.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6+
- pip (Python package installer)


## Quick Start

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/discreetkit-docs.git
    cd discreetkit-docs
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your environment:**
    - Copy the example settings file:
      ```bash
      cp config/settings.example.py config/settings.py
      ```
    - Edit `config/settings.py` with your business, director, and branding details. This file is ignored by git and should be customized for each deployment.

4. **Generate a document:**
    ```bash
    # Generate a board resolution (prompts for missing info)
    python generate_documents.py board_resolution --recipient "Branch Manager" --branch "Fidelity Bank"

    # Generate a contributor charter with all details provided
    python generate_documents.py contributor_charter --contributor_name "Jane Doe" --circle_name "Engineering"

    # Generate all available documents interactively
    python generate_documents.py all
    ```
    Generated documents will be saved in the `output/` directory, organized by category.

## CLI Usage

The script `generate_documents.py` is the main entry point for generating documents.

### Basic Command Structure

```bash
python generate_documents.py [document_type] [options]
```

- `[document_type]`: The name of the document to generate (e.g., `board_resolution`, `nda`). Use `all` to generate all documents.
- `[options]`: Optional flags to provide placeholder values.

### Providing Placeholder Data

You can pass data to the document templates using command-line arguments. The argument name should match the placeholder in the template.

**For example:**

If your template has a placeholder `{{contributor_name}}`, you can provide the value like this:

```bash
python generate_documents.py contributor_charter --contributor_name "John Smith"
```

If you omit a required placeholder, the tool will prompt you to enter the value interactively.

### Special Placeholders

- `{{DATE}}`: Automatically filled with the current date. You can override it with the `--date` flag.
  ```bash
  python generate_documents.py board_resolution --date "19 November 2025"
  ```
- All company-specific details (`{{COMPANY_NAME}}`, `{{DIRECTOR_NAME}}`, etc.) are automatically sourced from the configuration file.

## Customization

All branding and company-specific details are managed in the `config/settings.py` file. No code changes are needed for customization.

1.  **Company Identity:**
    - Open `config/settings.py` and edit the following variables:
      - `COMPANY_NAME`
      - `COMPANY_TAGLINE`
      - `COMPANY_ADDRESS`
      - `COMPANY_EMAIL`, `COMPANY_PHONE`
      - `COMPANY_TWITTER`, `COMPANY_LINKEDIN`

2.  **Logo:**
    - Replace `assets/logo.png` with your company's logo. A transparent PNG is recommended.

3.  **Colors:**
    - In `config/settings.py`, modify the hex codes in the `COLORS` dictionary to match your brand's color palette.

4.  **Fonts (Optional):**
    - Place your `.ttf` font files in the `assets/` directory.
    - Update the font paths in `config/settings.py`. If omitted, the default Helvetica font will be used.

5.  **Signatories:**
    - Change `DEFAULT_DIRECTOR` and `DEFAULT_DIRECTOR_TITLE` for document signature blocks.

6.  **Document Text:**
    - Edit the text, paragraphs, and structure of any document in `templates/document_templates.json`.

## Adding a New Document

1.  **Define the Template:**
    - Add a new entry to `templates/document_templates.json`. Follow the existing structure, including a title, body, and any custom placeholders.

2.  **Create a Generator:**
    - Create a new Python file in the `generators/` directory (e.g., `generators/my_new_doc.py`).
    - Implement a class that inherits from `DocumentTemplate` and defines a method to generate the document. Use an existing generator as a reference.

3.  **Register the Generator:**
    - In `generate_documents.py`, import your new generator and add it to the `self.generators` dictionary in the `DocumentGenerator` class.

## Repository Structure
```
├── assets/                  # Fonts & logo
├── config/                  # Configuration file (settings.py)
├── generators/              # Python generator classes for each document
├── output/                  # Generated PDFs (auto-created)
├── templates/               # JSON file with document templates
├── document_template.py     # Core PDF rendering and styling logic
├── generate_documents.py    # CLI entry point for the tool
└── README.md                # This file
```

## Troubleshooting

-   **Blank PDF:** Ensure that `assets/logo.png` exists or that the code doesn't require it. Font loading failures will silently fall back to Helvetica.
-   **Incorrect Company Info:** Double-check that you have correctly updated the values in `config/settings.py`. Placeholders are case-sensitive.
-   **Placeholder Not Replaced:** Make sure the placeholder in the template `{{placeholder}}` matches the argument you are passing via the CLI (`--placeholder`).