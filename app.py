import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from generate_documents import DocumentSuite

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use /tmp for Vercel or if explicitly requested, otherwise default local output
if os.environ.get('VERCEL'):
    OUTPUT_DIR = '/tmp'
else:
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Lazy initialization
suite = None
def get_suite():
    global suite
    if suite is None:
        suite = DocumentSuite(output_dir=OUTPUT_DIR)
    return suite

def ensure_date(val):
    v = (val or '').strip()
    if not v:
        return datetime.now().strftime('%d %B %Y')
    try:
        # Handle ISO date from <input type="date"> (YYYY-MM-DD)
        dt = datetime.strptime(v, '%Y-%m-%d')
        return dt.strftime('%d %B %Y')
    except Exception:
        # Assume already in desired format; return as-is
        return v

@app.get('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        import traceback
        return f"<h1>Error starting app</h1><pre>{traceback.format_exc()}</pre>", 500

@app.get('/files/<path:subpath>')
def serve_file(subpath):
    return send_from_directory(OUTPUT_DIR, subpath, as_attachment=False)

@app.post('/api/generate/partnership_proposal')
def api_generate_pp():
    data = request.get_json(silent=True) or {}
    custom = {}
    custom['[Date]'] = ensure_date(data.get('date'))
    # Map to placeholders expected by templates
    pharmacy_name = (data.get('pharmacy_name') or '').strip()
    partner_address = (data.get('partner_address') or '').strip()
    custom['[Pharmacy Name]'] = pharmacy_name
    custom['[Partner Address]'] = partner_address
    # Keep original keys for filename logic used by generators
    custom['pharmacy_name'] = pharmacy_name
    custom['partner_address'] = partner_address
    path = suite.generate_document('partnership_proposal', custom)
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from generate_documents import DocumentSuite

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use /tmp for Vercel or if explicitly requested, otherwise default local output
if os.environ.get('VERCEL'):
    OUTPUT_DIR = '/tmp'
else:
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Lazy initialization
suite = None
def get_suite():
    global suite
    if suite is None:
        suite = DocumentSuite(output_dir=OUTPUT_DIR)
    return suite

def ensure_date(val):
    v = (val or '').strip()
    if not v:
        return datetime.now().strftime('%d %B %Y')
    try:
        # Handle ISO date from <input type="date"> (YYYY-MM-DD)
        dt = datetime.strptime(v, '%Y-%m-%d')
        return dt.strftime('%d %B %Y')
    except Exception:
        # Assume already in desired format; return as-is
        return v

@app.get('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        import traceback
        return f"<h1>Error starting app</h1><pre>{traceback.format_exc()}</pre>", 500

@app.get('/files/<path:subpath>')
def serve_file(subpath):
    return send_from_directory(OUTPUT_DIR, subpath, as_attachment=False)

@app.post('/api/generate/<document_type>')
def generate_document(document_type):
    try:
        data = request.get_json(silent=True) or {}
        # Use lazy suite
        s = get_suite()
        
        # The generators expect specific keys. 
        # Our frontend sends keys matching the generator's expectations (mostly).
        # Let's pass the data dict as custom_data.
        
        # Generate
        # The ensure_date logic needs to be applied to the 'date' field if present
        if 'date' in data:
            data['[Date]'] = ensure_date(data['date'])
        
        # Map pharmacy_name and partner_address to their placeholder versions if present
        if 'pharmacy_name' in data:
            data['[Pharmacy Name]'] = data['pharmacy_name']
        if 'partner_address' in data:
            data['[Partner Address]'] = data['partner_address']

        path = s.generate_document(document_type, data)
        
        if not path:
            return jsonify({'ok': False, 'error': 'Generation failed'}), 500

        # Serve the file directly
        return send_file(
            path,
            as_attachment=True,
            download_name=os.path.basename(path)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}), 500
if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
