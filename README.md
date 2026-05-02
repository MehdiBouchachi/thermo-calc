# ThermoCalc — Guide d'Installation
## Calcul de Déperditions Thermiques d'un Bâtiment
**Département d'Informatique — TP 2026 SIA M1-IL**

---

## 1. Logiciels et Versions Requis

| Outil       | Version recommandée | Rôle                        |
|-------------|---------------------|-----------------------------|
| Python      | 3.9 ou supérieur    | Serveur web / logique métier |
| MySQL       | 8.0 ou supérieur    | Base de données              |
| pip         | dernière version    | Gestionnaire de paquets Python |
| Navigateur  | Chrome / Firefox    | Interface utilisateur        |

---

## 2. Bibliothèques Python à installer

```bash
pip install -r requirements.txt
```

Contenu de `requirements.txt` :
- `flask==3.0.3` — Framework web Python
- `mysql-connector-python==9.0.0` — Connecteur MySQL pour Python

---

## 3. Procédure d'Installation et Lancement

### Étape 1 — Créer la base de données MySQL

Ouvrez votre client MySQL (MySQL Workbench, phpMyAdmin, ou ligne de commande) et exécutez :

```sql
SOURCE database.sql;
```

Ou via la ligne de commande :
```bash
mysql -u root -p < database.sql
```

Cela va créer automatiquement :
- La base `thermique_db`
- Toutes les tables (batiment, mur, plancher, toiture, ouvrant, etc.)
- Les données de référence (types de murs, planchers, toitures, ouvrants)

### Étape 2 — Configurer la connexion à la base de données

Ouvrez le fichier `app.py` et modifiez la section suivante selon votre configuration MySQL :

```python
DB_CONFIG = {
    'host': 'localhost',        # ← Hôte MySQL (ex: 127.0.0.1)
    'user': 'root',             # ← Utilisateur MySQL
    'password': '',             # ← Mot de passe MySQL
    'database': 'thermique_db', # ← Nom de la base (ne pas modifier)
    'charset': 'utf8mb4'
}
```

### Étape 3 — Lancer l'application

```bash
# Se placer dans le dossier du projet
cd thermique/

# Installer les dépendances (si pas encore fait)
pip install -r requirements.txt

# Lancer le serveur Flask
python app.py
```

L'application démarre sur : **http://localhost:5000**

---

## 4. Utilisation de l'Application

### Accueil
- Liste tous les bâtiments enregistrés avec leur classe énergétique
- Bouton "+ Nouveau Bâtiment" pour commencer une analyse

### Créer un Bâtiment
1. Cliquer sur **+ Nouveau Bâtiment**
2. Renseigner : code, type, adresse, surface, zone climatique
3. Sélectionner les sources d'énergie
4. Valider → redirection vers la fiche du bâtiment

### Saisir les Composants
Sur la fiche du bâtiment, 4 onglets sont disponibles :
- **Murs** : longueur × hauteur × type de mur → déperdition calculée automatiquement
- **Planchers** : surface × type de plancher
- **Toitures** : surface × type de toiture
- **Ouvrants** : surface × type d'ouvrant (fenêtres, portes…)

Chaque ajout calcule instantanément la déperdition en **W/K**.

### Calculer la Déperdition Totale
Cliquer sur **⚡ Calculer Déperditions** :
- Somme de toutes les déperditions (murs + planchers + toitures + ouvrants)
- Conversion en **kWh/m²/an**
- Attribution de la **Classe Énergétique** (A à G) selon le DPE
- Affichage de l'étiquette énergie colorée

### Statistiques
Page récapitulant la répartition des bâtiments par classe énergétique.

---

## 5. Formules Utilisées

### Déperdition par composant :
```
Déperdition = K × Surface  (en W/K)
```

### Surface mur :
```
Surface_mur = Longueur × Hauteur  (en m²)
```

### Déperdition totale bâtiment :
```
Dep_totale = Σ(Dep_murs) + Σ(Dep_planchers) + Σ(Dep_toitures) + Σ(Dep_ouvrants)
```

### Consommation énergétique :
```
Consommation (kWh/m²/an) = (Dep_totale × 2400) / (Surface_bâtiment × 1000)
```

### Classification DPE :
| Classe | Consommation (kWh/m²/an)  |
|--------|---------------------------|
| A      | ≤ 70                      |
| B      | 71 – 110                  |
| C      | 111 – 180                 |
| D      | 181 – 250                 |
| E      | 251 – 330                 |
| F      | 331 – 420                 |
| G      | > 420                     |

---

## 6. Structure du Projet

```
thermique/
├── app.py                  ← Application Flask principale
├── requirements.txt        ← Dépendances Python
├── database.sql            ← Script SQL (CREATE + INSERT)
├── README.md               ← Ce fichier
├── static/
│   ├── css/
│   │   └── style.css       ← Feuille de styles
│   └── js/
│       └── main.js         ← JavaScript (AJAX, interactions)
└── templates/
    ├── base.html           ← Template de base (navbar, footer)
    ├── index.html          ← Page d'accueil / liste bâtiments
    ├── nouveau_batiment.html ← Formulaire de création
    ├── detail_batiment.html  ← Fiche + calcul déperditions
    └── statistiques.html   ← Vue statistiques globales
```

---

## 7. Déploiement sur une Autre Machine

1. Copier le dossier `thermique/` sur la machine cible
2. Installer Python 3.9+ et MySQL 8.0+
3. Importer `database.sql` dans MySQL
4. Modifier `DB_CONFIG` dans `app.py` avec les bons paramètres
5. Installer les dépendances : `pip install -r requirements.txt`
6. Lancer : `python app.py`
7. Accéder via navigateur : `http://localhost:5000`

---

*TP 2026 — Département d'Informatique — SIA M1-IL*
