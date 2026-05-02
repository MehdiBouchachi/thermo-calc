/**
 * thermocalc/static/js/calcul.js
 * Thermal calculation and result display management
 */

/**
 * Launch thermal calculation for a building.
 * Sends POST request to calculate total heat loss and energy consumption.
 * Updates result panel with calculation outcomes and DPE scale.
 *
 * @param {number} batId - Building ID
 * @param {number} surface - Building surface area in m²
 */
async function lancerCalcul(batId, surface) {
  showLoader();
  try {
    const res = await fetch("/api/calculer/" + batId, { method: "POST" });
    const data = await res.json();
    hideLoader();

    if (data.success) {
      // Update component deperdition values
      const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      };
      setVal("r-murs", data.dep_murs);
      setVal("r-planchers", data.dep_planchers);
      setVal("r-toitures", data.dep_toitures);
      setVal("r-ouvrants", data.dep_ouvrants);
      setVal("r-total", data.dep_totale);
      setVal("r-conso", data.consommation);

      // Update energy class badge
      const classeDiv = document.querySelector(".grande-classe");
      if (classeDiv) {
        classeDiv.textContent = data.classe;
        classeDiv.className = "grande-classe classe-" + data.classe;
      }

      // Update DPE scale with active indicator
      document.querySelectorAll(".dpe-row").forEach((row) => {
        row.classList.remove("dpe-active");
      });
      const letters = ["A", "B", "C", "D", "E", "F", "G"];
      const rows = document.querySelectorAll(".dpe-row");
      const idx = letters.indexOf(data.classe);
      if (idx >= 0 && rows[idx]) rows[idx].classList.add("dpe-active");

      // Make result panel visible and persistent
      const panel = document.getElementById("resultat-panel");
      if (panel) {
        panel.classList.add("updated");
        panel.classList.add("visible");
        const placeholder = panel.querySelector(".resultat-placeholder");
        if (placeholder) {
          placeholder.style.display = "none";
        }
      }

      // Visual feedback: flash success on button
      document.querySelector(".btn-calcul")?.classList.add("btn-success");
      setTimeout(
        () =>
          document
            .querySelector(".btn-calcul")
            ?.classList.remove("btn-success"),
        1500,
      );
    } else {
      alert("Erreur lors du calcul: " + data.message);
    }
  } catch (e) {
    hideLoader();
    alert("Erreur de connexion au serveur.");
  }
}
