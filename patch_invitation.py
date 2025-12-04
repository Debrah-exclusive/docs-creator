import json
import os

file_path = r'c:\Users\derri\Desktop\docs-creator\templates\document_templates.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'invitation_to_the_circle' in data:
    sig = data['invitation_to_the_circle']['signature']
    # Check if placeholder already exists
    if not any('[SIGNATURE:signature.svg]' in line for line in sig):
        # Insert before the first underscore line or Naeem's line
        inserted = False
        for i, line in enumerate(sig):
            if '______________________________' in line:
                sig.insert(i, '[SIGNATURE:signature.svg]')
                inserted = True
                break
        
        if not inserted:
             sig.append('[SIGNATURE:signature.svg]')

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Successfully patched invitation signature")
