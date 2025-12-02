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

suite = DocumentSuite(output_dir=OUTPUT_DIR)

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
    return render_template('index.html')

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
    if not path:
        return jsonify({ 'ok': False, 'error': 'generation_failed' }), 400
    
    filename = os.path.basename(path)
    return send_file(path, as_attachment=True, download_name=filename)

@app.post('/api/generate/pharmacy_loi')
def api_generate_loi():
    data = request.get_json(silent=True) or {}
    custom = {}
    custom['[Date]'] = ensure_date(data.get('date'))
    # Map to placeholders expected by templates
    pharmacy_name = (data.get('pharmacy_name') or '').strip()
    custom['[Pharmacy Name]'] = pharmacy_name
    # Keep original key for filename logic
    custom['pharmacy_name'] = pharmacy_name
    path = suite.generate_document('pharmacy_loi', custom)
    if not path:
        return jsonify({ 'ok': False, 'error': 'generation_failed' }), 400
    
    filename = os.path.basename(path)
    return send_file(path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
