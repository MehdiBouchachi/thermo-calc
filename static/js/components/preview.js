/**
 * thermocalc/static/js/components/preview.js
 * Real-time preview calculators for component heat loss values
 */

/**
 * Setup real-time preview for wall heat loss.
 * Calculates and displays deperdition (W/K) as user enters wall type, length, and height.
 * Formula: k * length * height
 */
function setupMurPreview() {
  const typeEl = document.getElementById("mur-type");
  const longEl = document.getElementById("mur-longueur");
  const hautEl = document.getElementById("mur-hauteur");
  const prevEl = document.getElementById("mur-preview");
  if (!typeEl || !prevEl) return;

  function update() {
    const k = parseFloat(typeEl.selectedOptions[0]?.dataset.k || 0);
    const l = parseFloat(longEl?.value || 0);
    const h = parseFloat(hautEl?.value || 0);
    if (k && l && h) {
      prevEl.textContent = (k * l * h).toFixed(3) + " W/K";
    } else {
      prevEl.textContent = "—";
    }
  }
  typeEl.addEventListener("change", update);
  longEl && longEl.addEventListener("input", update);
  hautEl && hautEl.addEventListener("input", update);
}

/**
 * Setup real-time preview for floor heat loss.
 * Calculates and displays deperdition (W/K) as user enters floor type and surface.
 * Formula: k * surface
 */
function setupPlancherPreview() {
  const typeEl = document.getElementById("plancher-type");
  const surfEl = document.getElementById("plancher-surface");
  const prevEl = document.getElementById("plancher-preview");
  if (!typeEl || !prevEl) return;

  function update() {
    const k = parseFloat(typeEl.selectedOptions[0]?.dataset.k || 0);
    const s = parseFloat(surfEl?.value || 0);
    prevEl.textContent = k && s ? (k * s).toFixed(3) + " W/K" : "—";
  }
  typeEl.addEventListener("change", update);
  surfEl && surfEl.addEventListener("input", update);
}

/**
 * Initialize preview listeners on DOM ready.
 */
document.addEventListener("DOMContentLoaded", () => {
  setupMurPreview();
  setupPlancherPreview();
});
