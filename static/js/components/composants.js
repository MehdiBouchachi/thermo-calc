/**
 * thermocalc/static/js/components/composants.js
 * Component management functions for adding walls, floors, roofs, and windows
 */

/**
 * Add a wall component to the building via AJAX.
 * Shows loader, sends data to API, and reloads page on success.
 *
 * @param {number} batId - Building ID
 */
async function ajouterMur(batId) {
  const type = document.getElementById("mur-type");
  const lon = document.getElementById("mur-longueur");
  const hau = document.getElementById("mur-hauteur");
  const eta = document.getElementById("mur-etat");

  if (!lon.value || !hau.value) {
    alert("Veuillez remplir longueur et hauteur.");
    return;
  }

  showLoader();
  try {
    const res = await fetch("/api/ajouter-mur", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_batiment: batId,
        id_type_mur: type.value,
        longueur: lon.value,
        hauteur: hau.value,
        etat: eta.value,
      }),
    });
    const data = await res.json();
    if (data.success) {
      location.reload();
    } else {
      alert("Erreur: " + data.message);
    }
  } catch (e) {
    alert("Erreur de connexion");
  } finally {
    hideLoader();
  }
}

/**
 * Add a floor component to the building via AJAX.
 *
 * @param {number} batId - Building ID
 */
async function ajouterPlancher(batId) {
  const type = document.getElementById("plancher-type");
  const surf = document.getElementById("plancher-surface");
  const eta = document.getElementById("plancher-etat");

  if (!surf.value) {
    alert("Veuillez entrer une surface.");
    return;
  }

  showLoader();
  try {
    const res = await fetch("/api/ajouter-plancher", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_batiment: batId,
        id_type_plancher: type.value,
        surface: surf.value,
        etat: eta.value,
      }),
    });
    const data = await res.json();
    if (data.success) {
      location.reload();
    } else {
      alert("Erreur: " + data.message);
    }
  } catch (e) {
    alert("Erreur de connexion");
  } finally {
    hideLoader();
  }
}

/**
 * Add a roof component to the building via AJAX.
 *
 * @param {number} batId - Building ID
 */
async function ajouterToiture(batId) {
  const type = document.getElementById("toiture-type");
  const surf = document.getElementById("toiture-surface");
  const eta = document.getElementById("toiture-etat");

  if (!surf.value) {
    alert("Veuillez entrer une surface.");
    return;
  }

  showLoader();
  try {
    const res = await fetch("/api/ajouter-toiture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_batiment: batId,
        id_type_toiture: type.value,
        surface: surf.value,
        etat: eta.value,
      }),
    });
    const data = await res.json();
    if (data.success) {
      location.reload();
    } else {
      alert("Erreur: " + data.message);
    }
  } catch (e) {
    alert("Erreur de connexion");
  } finally {
    hideLoader();
  }
}

/**
 * Add a window/opening component to the building via AJAX.
 *
 * @param {number} batId - Building ID
 */
async function ajouterOuvrant(batId) {
  const type = document.getElementById("ouvrant-type");
  const surf = document.getElementById("ouvrant-surface");
  const eta = document.getElementById("ouvrant-etat");

  if (!surf.value) {
    alert("Veuillez entrer une surface.");
    return;
  }

  showLoader();
  try {
    const res = await fetch("/api/ajouter-ouvrant", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id_batiment: batId,
        id_type_ouvrant: type.value,
        surface: surf.value,
        etat: eta.value,
      }),
    });
    const data = await res.json();
    if (data.success) {
      location.reload();
    } else {
      alert("Erreur: " + data.message);
    }
  } catch (e) {
    alert("Erreur de connexion");
  } finally {
    hideLoader();
  }
}
