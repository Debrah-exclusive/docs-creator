import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from generate_documents import DocumentSuite

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = '/tmp' if os.environ.get('VERCEL') else os.path.join(BASE_DIR, 'output')

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
        dt = datetime.strptime(v, '%Y-%m-%d')
        return dt.strftime('%d %B %Y')
    except Exception:
        return v

@app.get('/debug')
def debug_import():
    try:
        from generate_documents import DocumentSuite
        return "Import Successful! App should work."
    except Exception:
        import traceback
        return f"<pre>{traceback.format_exc()}</pre>", 500

@app.get('/')
def index():
    try:
        return render_template('index.html')
    except Exception:
        import traceback
        return f"<h1>Error starting app</h1><pre>{traceback.format_exc()}</pre>", 500

@app.get('/favicon.ico')
def favicon():
    assets_dir = os.path.join(BASE_DIR, 'assets')
    icon_path = os.path.join(assets_dir, 'favicon.ico')
    if os.path.exists(icon_path):
        return send_from_directory(assets_dir, 'favicon.ico', as_attachment=False)
    return ('', 204)

@app.get('/favicon.png')
def favicon_png():
    assets_dir = os.path.join(BASE_DIR, 'assets')
    icon_path = os.path.join(assets_dir, 'favicon.png')
    if os.path.exists(icon_path):
        return send_from_directory(assets_dir, 'favicon.png', as_attachment=False)
    return ('', 204)

@app.get('/files/<path:subpath>')
def serve_file(subpath):
    return send_from_directory(OUTPUT_DIR, subpath, as_attachment=False)

@app.post('/api/generate/<document_type>')
def generate_document(document_type):
    try:
        data = request.get_json(silent=True) or {}
        s = get_suite()

        if 'date' in data:
            data['[Date]'] = ensure_date(data['date'])
        if 'pharmacy_name' in data:
            data['[Pharmacy Name]'] = data['pharmacy_name']
        if 'partner_address' in data:
            data['[Partner Address]'] = data['partner_address']

        path = s.generate_document(document_type, data)
        if not path:
            return jsonify({'ok': False, 'error': 'Generation failed'}), 500

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
