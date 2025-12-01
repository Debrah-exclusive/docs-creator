async function submitForm(id, url, mapFn) {
    const form = document.getElementById(id);
    const btn = form.querySelector('button');
    const resultEl = form.querySelector('.result');

    // Reset state
    btn.disabled = true;
    btn.classList.add('loading');
    resultEl.className = 'result';
    resultEl.style.display = 'none';

    try {
        const formData = new FormData(form);
        const payload = mapFn(formData);

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to generate document');
        }

        // Handle binary download
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'document.pdf';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?([^"]+)"?/);
            if (match && match[1]) filename = match[1];
        }

        // Success UI
        resultEl.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span>Document generated!</span>
            </div>
            <div style="margin-top: 0.5rem;">
                <a href="${downloadUrl}" download="${filename}">
                    Download Again
                </a>
            </div>
        `;
        resultEl.classList.add('success');

        // Auto trigger download
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();

    } catch (error) {
        console.error(error);
        resultEl.textContent = error.message;
        resultEl.classList.add('error');
    } finally {
        btn.disabled = false;
        btn.classList.remove('loading');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Set default dates to today
    const today = new Date().toISOString().slice(0, 10);
    document.querySelectorAll('input[type="date"]').forEach(el => {
        if (!el.value) el.value = today;

        // Helper to open picker on click
        const openPicker = () => {
            if (el.showPicker) {
                try { el.showPicker(); } catch (e) { }
            }
        };
        el.addEventListener('click', openPicker);
    });
});
