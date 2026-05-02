/**
 * ThermoCalc - Calcul de Déperditions Thermiques
 * JavaScript principal
 */

// ============================================================
// TABS
// ============================================================
function showTab(name) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    event.target.classList.add('active');
}

// ============================================================
// TOGGLE FORM
// ============================================================
function toggleForm(id) {
    const form = document.getElementById(id);
    if (form) form.classList.toggle('hidden');
}

// ============================================================
// APERÇU DÉPERDITION EN TEMPS RÉEL
// ============================================================
function setupMurPreview() {
    const typeEl = document.getElementById('mur-type');
    const longEl = document.getElementById('mur-longueur');
    const hautEl = document.getElementById('mur-hauteur');
    const prevEl = document.getElementById('mur-preview');
    if (!typeEl || !prevEl) return;

    function update() {
        const k = parseFloat(typeEl.selectedOptions[0]?.dataset.k || 0);
        const l = parseFloat(longEl?.value || 0);
        const h = parseFloat(hautEl?.value || 0);
        if (k && l && h) {
            prevEl.textContent = (k * l * h).toFixed(3) + ' W/K';
        } else {
            prevEl.textContent = '—';
        }
    }
    typeEl.addEventListener('change', update);
    longEl && longEl.addEventListener('input', update);
    hautEl && hautEl.addEventListener('input', update);
}

function setupPlancherPreview() {
    const typeEl = document.getElementById('plancher-type');
    const surfEl = document.getElementById('plancher-surface');
    const prevEl = document.getElementById('plancher-preview');
    if (!typeEl || !prevEl) return;

    function update() {
        const k = parseFloat(typeEl.selectedOptions[0]?.dataset.k || 0);
        const s = parseFloat(surfEl?.value || 0);
        prevEl.textContent = (k && s) ? (k * s).toFixed(3) + ' W/K' : '—';
    }
    typeEl.addEventListener('change', update);
    surfEl && surfEl.addEventListener('input', update);
}

document.addEventListener('DOMContentLoaded', () => {
    setupMurPreview();
    setupPlancherPreview();
    // Flash auto-dismiss
    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(el => {
            el.style.transition = 'opacity 0.5s';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 500);
        });
    }, 4000);
});

// ============================================================
// LOADER
// ============================================================
function showLoader() {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-box">
                <div class="loading-spinner"></div>
                <div style="font-size:14px; color: var(--text2);">Calcul en cours...</div>
            </div>`;
        document.body.appendChild(overlay);
    }
    overlay.classList.add('active');
}

function hideLoader() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.classList.remove('active');
}

// ============================================================
// AJOUTER MUR
// ============================================================
async function ajouterMur(batId) {
    const type = document.getElementById('mur-type');
    const lon = document.getElementById('mur-longueur');
    const hau = document.getElementById('mur-hauteur');
    const eta = document.getElementById('mur-etat');

    if (!lon.value || !hau.value) { alert('Veuillez remplir longueur et hauteur.'); return; }

    showLoader();
    try {
        const res = await fetch('/api/ajouter-mur', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_batiment: batId,
                id_type_mur: type.value,
                longueur: lon.value,
                hauteur: hau.value,
                etat: eta.value
            })
        });
        const data = await res.json();
        if (data.success) {
            location.reload();
        } else {
            alert('Erreur: ' + data.message);
        }
    } catch(e) {
        alert('Erreur de connexion');
    } finally {
        hideLoader();
    }
}

// ============================================================
// AJOUTER PLANCHER
// ============================================================
async function ajouterPlancher(batId) {
    const type = document.getElementById('plancher-type');
    const surf = document.getElementById('plancher-surface');
    const eta = document.getElementById('plancher-etat');

    if (!surf.value) { alert('Veuillez entrer une surface.'); return; }

    showLoader();
    try {
        const res = await fetch('/api/ajouter-plancher', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_batiment: batId,
                id_type_plancher: type.value,
                surface: surf.value,
                etat: eta.value
            })
        });
        const data = await res.json();
        if (data.success) { location.reload(); }
        else { alert('Erreur: ' + data.message); }
    } catch(e) { alert('Erreur de connexion'); }
    finally { hideLoader(); }
}

// ============================================================
// AJOUTER TOITURE
// ============================================================
async function ajouterToiture(batId) {
    const type = document.getElementById('toiture-type');
    const surf = document.getElementById('toiture-surface');
    const eta = document.getElementById('toiture-etat');

    if (!surf.value) { alert('Veuillez entrer une surface.'); return; }

    showLoader();
    try {
        const res = await fetch('/api/ajouter-toiture', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_batiment: batId,
                id_type_toiture: type.value,
                surface: surf.value,
                etat: eta.value
            })
        });
        const data = await res.json();
        if (data.success) { location.reload(); }
        else { alert('Erreur: ' + data.message); }
    } catch(e) { alert('Erreur de connexion'); }
    finally { hideLoader(); }
}

// ============================================================
// AJOUTER OUVRANT
// ============================================================
async function ajouterOuvrant(batId) {
    const type = document.getElementById('ouvrant-type');
    const surf = document.getElementById('ouvrant-surface');
    const eta = document.getElementById('ouvrant-etat');

    if (!surf.value) { alert('Veuillez entrer une surface.'); return; }

    showLoader();
    try {
        const res = await fetch('/api/ajouter-ouvrant', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_batiment: batId,
                id_type_ouvrant: type.value,
                surface: surf.value,
                etat: eta.value
            })
        });
        const data = await res.json();
        if (data.success) { location.reload(); }
        else { alert('Erreur: ' + data.message); }
    } catch(e) { alert('Erreur de connexion'); }
    finally { hideLoader(); }
}

// ============================================================
// LANCER LE CALCUL GLOBAL
// ============================================================
async function lancerCalcul(batId, surface) {
    showLoader();
    try {
        const res = await fetch('/api/calculer/' + batId, { method: 'POST' });
        const data = await res.json();
        hideLoader();

        if (data.success) {
            // Mise à jour des valeurs affichées
            const setVal = (id, val) => {
                const el = document.getElementById(id);
                if (el) el.textContent = val;
            };
            setVal('r-murs', data.dep_murs);
            setVal('r-planchers', data.dep_planchers);
            setVal('r-toitures', data.dep_toitures);
            setVal('r-ouvrants', data.dep_ouvrants);
            setVal('r-total', data.dep_totale);
            setVal('r-conso', data.consommation);

            // Mise à jour classe
            const classeDiv = document.querySelector('.grande-classe');
            if (classeDiv) {
                classeDiv.textContent = data.classe;
                classeDiv.className = 'grande-classe classe-' + data.classe;
            }

            // Mise à jour DPE scale
            document.querySelectorAll('.dpe-row').forEach(row => {
                row.classList.remove('dpe-active');
            });
            const letters = ['A','B','C','D','E','F','G'];
            const rows = document.querySelectorAll('.dpe-row');
            const idx = letters.indexOf(data.classe);
            if (idx >= 0 && rows[idx]) rows[idx].classList.add('dpe-active');

            // Panel visible
            const panel = document.getElementById('resultat-panel');
            if (panel) {
                panel.classList.add('updated');
                const placeholder = panel.querySelector('.resultat-placeholder');
                if (placeholder) { placeholder.style.display = 'none'; }
            }

            // Animation flash
            document.querySelector('.btn-calcul')?.classList.add('btn-success');
            setTimeout(() => document.querySelector('.btn-calcul')?.classList.remove('btn-success'), 1500);

            // Reload pour synchro complète
            setTimeout(() => location.reload(), 800);

        } else {
            alert('Erreur lors du calcul: ' + data.message);
        }
    } catch(e) {
        hideLoader();
        alert('Erreur de connexion au serveur.');
    }
}
