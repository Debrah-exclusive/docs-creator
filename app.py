import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from generate_documents import DocumentSuite

app = Flask(__name__)
suite = DocumentSuite()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>DiscreetKit Document Portal</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; color: #1A1F2B; }
    h1 { font-size: 20px; margin-bottom: 16px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; }
    .card { border: 1px solid #E5E7EB; border-radius: 8px; padding: 16px; }
    .card h2 { font-size: 18px; margin: 0 0 12px 0; }
    label { display: block; font-size: 12px; margin: 10px 0 6px; color: #4B5563; }
    input { width: 100%; padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 14px; }
    button { margin-top: 12px; padding: 10px 14px; background: #047857; color: white; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; }
    button:disabled { background: #9CA3AF; cursor: not-allowed; }
    .result { margin-top: 12px; font-size: 13px; }
    .link { color: #0EA5E9; text-decoration: none; }
  </style>
  <script>
    async function submitForm(id, url, mapFn) {
      const form = document.getElementById(id);
      const btn = form.querySelector('button');
      const resEl = form.querySelector('.result');
      btn.disabled = true;
      resEl.textContent = 'Generating...';
      try {
        const payload = mapFn(new FormData(form));
        const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        const j = await r.json();
        if (!j.ok) throw new Error(j.error || 'Failed');
        resEl.innerHTML = `Generated: <a class="link" href="${j.download_url}" target="_blank">${j.relative_path}</a>`;
      } catch (e) {
        resEl.textContent = 'Error: ' + e.message;
      } finally {
        btn.disabled = false;
      }
    }
    document.addEventListener('DOMContentLoaded', () => {
      const today = new Date().toISOString().slice(0,10);
      document.querySelectorAll('input[name="date"]').forEach(el => {
        if (!el.value) el.value = today;
        const openPicker = () => { if (el.showPicker) try { el.showPicker(); } catch(e) {} };
        el.addEventListener('focus', openPicker);
        el.addEventListener('click', openPicker);
      });
    });
  </script>
</head>
<body>
  <h1>Generate Tailored Documents</h1>
  <div class="grid">
    <div class="card">
      <h2>Partnership Proposal</h2>
      <form id="pp-form" onsubmit="event.preventDefault(); submitForm('pp-form','/api/generate/partnership_proposal', fd => ({ pharmacy_name: fd.get('pharmacy_name')||'', partner_address: fd.get('partner_address')||'', date: fd.get('date')||'' }))">
        <label>Pharmacy Name</label>
        <input name="pharmacy_name" placeholder="e.g. AlphaCare Pharmacy" />
        <label>Partner Address</label>
        <input name="partner_address" placeholder="e.g. Accra, Ghana" />
        <label>Date</label>
        <input type="date" name="date" />
        <button type="submit">Generate Proposal</button>
        <div class="result"></div>
      </form>
    </div>
    <div class="card">
      <h2>Pharmacy LOI</h2>
      <form id="loi-form" onsubmit="event.preventDefault(); submitForm('loi-form','/api/generate/pharmacy_loi', fd => ({ pharmacy_name: fd.get('pharmacy_name')||'', date: fd.get('date')||'' }))">
        <label>Pharmacy Name</label>
        <input name="pharmacy_name" placeholder="e.g. AlphaCare Pharmacy" />
        <label>Date</label>
        <input type="date" name="date" />
        <button type="submit">Generate LOI</button>
        <div class="result"></div>
      </form>
    </div>
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const today = new Date().toISOString().slice(0,10);
      document.querySelectorAll('input[name="date"]').forEach(el => {
        if (!el.value) el.value = today;
      });
    });
  </script>
</body>
</html>
"""

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

def relpath_from_output(full_path):
    rp = os.path.relpath(full_path, OUTPUT_DIR)
    return rp.replace('\\', '/')

@app.get('/')
def index():
    return render_template_string(INDEX_HTML)

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
    rp = relpath_from_output(path)
    return jsonify({ 'ok': True, 'path': path, 'relative_path': rp, 'download_url': f'/files/{rp}' })

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
    rp = relpath_from_output(path)
    return jsonify({ 'ok': True, 'path': path, 'relative_path': rp, 'download_url': f'/files/{rp}' })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
