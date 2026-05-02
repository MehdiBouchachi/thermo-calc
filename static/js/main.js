/**
 * thermocalc/static/js/main.js
 * Main ThermoCalc JavaScript - Tabs, loader, and flash message management
 */

/**
 * Switch between tab content panels.
 * Removes active class from all tabs and contents, then activates the selected one.
 *
 * @param {string} name - Tab identifier
 * @param {Event} event - Click event object (optional)
 */
function showTab(name, event) {
  document
    .querySelectorAll(".tab-content")
    .forEach((t) => t.classList.remove("active"));
  document
    .querySelectorAll(".tab")
    .forEach((t) => t.classList.remove("active"));
  document.getElementById("tab-" + name).classList.add("active");
  if (event && event.target) {
    event.target.classList.add("active");
  }
}

/**
 * Toggle a form's visibility.
 * Adds/removes the hidden class from the specified element.
 *
 * @param {string} id - Element ID to toggle
 */
function toggleForm(id) {
  const form = document.getElementById(id);
  if (form) form.classList.toggle("hidden");
}

/**
 * Show the loading overlay spinner.
 * Creates the overlay if it doesn't exist.
 */
function showLoader() {
  let overlay = document.getElementById("loading-overlay");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "loading-overlay";
    overlay.className = "loading-overlay";
    overlay.innerHTML = `
            <div class="loading-box">
                <div class="loading-spinner"></div>
                <div style="font-size:14px; color: var(--text2);">Calcul en cours...</div>
            </div>`;
    document.body.appendChild(overlay);
  }
  overlay.classList.add("active");
}

/**
 * Hide the loading overlay spinner.
 */
function hideLoader() {
  const overlay = document.getElementById("loading-overlay");
  if (overlay) overlay.classList.remove("active");
}

/**
 * Initialize on DOM ready: setup preview listeners and flash auto-dismiss.
 */
document.addEventListener("DOMContentLoaded", () => {
  // Flash messages auto-dismiss after 4 seconds
  setTimeout(() => {
    document.querySelectorAll(".flash").forEach((el) => {
      el.style.transition = "opacity 0.5s";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    });
  }, 4000);
});
