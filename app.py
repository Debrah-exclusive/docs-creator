import os # Trigger deployment
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from generate_documents import DocumentSuite

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

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
        print('[INDEX] template paths:', getattr(app.jinja_loader, 'searchpath', None))
        tpl_path = os.path.join(BASE_DIR, 'templates', 'index.html')
        if os.path.exists(tpl_path):
            try:
                print('[INDEX] index.html size:', os.path.getsize(tpl_path))
            except Exception:
                pass
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

        print('[API] generate', document_type, data)

        if 'date' in data:
            data['[Date]'] = ensure_date(data['date'])
            data['{{DATE}}'] = ensure_date(data['date'])
        if 'pharmacy_name' in data:
            data['[Pharmacy Name]'] = data['pharmacy_name']
        if 'partner_address' in data:
            data['[Partner Address]'] = data['partner_address']
        if 'contributor_name' in data:
            data['[Contributor Name]'] = data['contributor_name']
        if 'circle_name' in data:
            data['[Circle Name]'] = data['circle_name']

        path = s.generate_document(document_type, data)
        print('[API] result path:', path)
        if not path and document_type == 'invitation_to_the_circle':
            print('[API] ERROR: Invitation generation returned None. Checking data:', data)
            # No manual retry needed if generator is fixed.
            # If we really wanted to retry with clean data, we could, but let's trust the generator first.
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

@app.post('/api/generate_invite')
def generate_invite():
    try:
        data = request.get_json(silent=True) or {}
        s = get_suite()
        print('[API] generate_invite', data)
        # Map placeholders
        payload = {
            '[Contributor Name]': data.get('contributor_name') or data.get('[Contributor Name]', ''),
            '[Circle Name]': data.get('circle_name') or data.get('[Circle Name]', ''),
            '[Date]': ensure_date(data.get('date') or data.get('[Date]', '')),
            '{{DATE}}': ensure_date(data.get('date') or data.get('{{DATE}}', '')),
            'date': ensure_date(data.get('date') or data.get('[Date]', ''))
        }
        from generate_documents import InvitationToCircleGenerator
        gen = InvitationToCircleGenerator(OUTPUT_DIR)
        path = gen.generate_invitation(payload)
        print('[API] invite path:', path)
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
    app.run(host='0.0.0.0', port=port, debug=False)
