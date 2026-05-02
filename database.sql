-- ============================================================
-- Base de données : Calcul de Déperditions Thermiques
-- Département d'informatique - TP 2026 SIA M1-IL
-- ============================================================

CREATE DATABASE IF NOT EXISTS thermique_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE thermique_db;

-- ============================================================
-- Table : Zone Climatique
-- ============================================================
CREATE TABLE IF NOT EXISTS zone_climatique (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_zone VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

INSERT INTO zone_climatique (nom_zone, description) VALUES
('Zone H1 - Climat très froid', 'Nord de la France, altitude élevée'),
('Zone H2 - Climat froid', 'Centre de la France'),
('Zone H3 - Climat tempéré', 'Sud de la France, bord de mer'),
('Zone Semi-aride', 'Régions à faible pluviométrie'),
('Zone Aride', 'Régions désertiques');

-- ============================================================
-- Table : Type de Mur
-- ============================================================
CREATE TABLE IF NOT EXISTS type_mur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_type VARCHAR(150) NOT NULL,
    k_mur DECIMAL(5,3) NOT NULL COMMENT 'Coefficient de transmission surfacique W/m²K'
);

INSERT INTO type_mur (nom_type, k_mur) VALUES
('Mur sans isolation (simple paroi béton 20cm)', 3.200),
('Mur double paroi sans isolation', 2.100),
('Mur double paroi avec isolation laine de verre', 0.450),
('Mur double paroi avec isolation polyuréthane', 0.300),
('Mur en brique pleine 22cm', 1.800),
('Mur en brique creuse 20cm', 1.200),
('Mur en parpaing 20cm', 2.500),
('Mur ossature bois avec isolation', 0.280),
('Mur en pierre de taille 60cm', 1.500),
('Mur BBC (Bâtiment Basse Consommation)', 0.200);

-- ============================================================
-- Table : Type de Plancher
-- ============================================================
CREATE TABLE IF NOT EXISTS type_plancher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_type VARCHAR(150) NOT NULL,
    k_plancher DECIMAL(5,3) NOT NULL COMMENT 'Coefficient de transmission surfacique W/m²K'
);

INSERT INTO type_plancher (nom_type, k_plancher) VALUES
('Plancher béton armé sans isolation', 3.500),
('Plancher béton avec isolant sous chape', 0.600),
('Plancher bois sur vide sanitaire sans isolation', 2.100),
('Plancher bois avec isolation laine de roche', 0.400),
('Plancher parquet contrecollé sur béton', 1.800),
('Plancher chauffant avec isolation', 0.350),
('Dallage béton sur terre-plein', 2.800),
('Plancher hourdis béton sans isolation', 2.900),
('Plancher hourdis béton avec isolation', 0.550),
('Plancher en terre cuite', 2.200);

-- ============================================================
-- Table : Type de Toiture
-- ============================================================
CREATE TABLE IF NOT EXISTS type_toiture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_type VARCHAR(150) NOT NULL,
    k_toiture DECIMAL(5,3) NOT NULL COMMENT 'Coefficient de transmission surfacique W/m²K'
);

INSERT INTO type_toiture (nom_type, k_toiture) VALUES
('Toiture plate sans isolation', 3.300),
('Toiture plate avec isolation polyuréthane', 0.280),
('Toiture inclinée tuiles sans isolation combles', 2.800),
('Toiture inclinée avec isolation combles perdus', 0.250),
('Toiture inclinée avec isolation combles aménagés', 0.350),
('Toiture terrasse végétalisée', 0.400),
('Toiture bac acier sans isolation', 4.500),
('Toiture bac acier avec isolation', 0.450),
('Chaume traditionnel', 1.200),
('Toiture BBC haute performance', 0.180);

-- ============================================================
-- Table : Type d'Ouvrant
-- ============================================================
CREATE TABLE IF NOT EXISTS type_ouvrant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_type VARCHAR(150) NOT NULL,
    k_ouvrant DECIMAL(5,3) NOT NULL COMMENT 'Coefficient de transmission surfacique W/m²K'
);

INSERT INTO type_ouvrant (nom_type, k_ouvrant) VALUES
('Fenêtre simple vitrage aluminium', 5.800),
('Fenêtre double vitrage standard PVC', 2.900),
('Fenêtre double vitrage à faible émissivité', 1.800),
('Fenêtre triple vitrage haute performance', 0.800),
('Porte pleine bois massive', 3.200),
('Porte vitrée simple', 4.500),
('Porte-fenêtre double vitrage', 2.600),
('Velux / Fenêtre de toit double vitrage', 2.200),
('Baie vitrée double vitrage coulissante', 3.100),
('Porte métallique isolée', 1.500);

-- ============================================================
-- Table : Source d'énergie
-- ============================================================
CREATE TABLE IF NOT EXISTS source_energie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_source VARCHAR(100) NOT NULL,
    etat_source VARCHAR(50),
    caracteristiques TEXT
);

INSERT INTO source_energie (nom_source, etat_source, caracteristiques) VALUES
('Gaz naturel', 'Disponible', 'Énergie fossile, rendement ~90%'),
('Électricité réseau', 'Disponible', 'Mix énergétique national'),
('Fioul domestique', 'Disponible', 'Énergie fossile liquide'),
('Pompe à chaleur air/air', 'Disponible', 'COP moyen 3.5'),
('Pompe à chaleur géothermique', 'Disponible', 'COP moyen 4.5'),
('Énergie solaire thermique', 'Disponible', 'Renouvelable'),
('Biomasse / Bois', 'Disponible', 'Renouvelable, CO2 neutre'),
('Réseau de chaleur urbain', 'Disponible', 'Efficacité variable selon réseau');

-- ============================================================
-- Table : Bâtiment
-- ============================================================
CREATE TABLE IF NOT EXISTS batiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code_batiment VARCHAR(50) UNIQUE NOT NULL,
    adresse_batiment VARCHAR(255) NOT NULL,
    coordonnees_geo VARCHAR(100),
    type_batiment VARCHAR(100) NOT NULL,
    surface DECIMAL(10,2) NOT NULL COMMENT 'Surface totale en m²',
    volume DECIMAL(10,2) COMMENT 'Volume en m³',
    annee_construction INT,
    nombre_niveaux INT DEFAULT 1,
    nombre_occupants INT DEFAULT 0,
    id_zone_climatique INT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_zone_climatique) REFERENCES zone_climatique(id)
);

-- ============================================================
-- Table : Mur
-- ============================================================
CREATE TABLE IF NOT EXISTS mur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment INT NOT NULL,
    numero_mur INT NOT NULL,
    longueur_mur DECIMAL(8,2) NOT NULL,
    hauteur_mur DECIMAL(8,2) NOT NULL,
    etat_mur VARCHAR(50) DEFAULT 'Bon état',
    id_type_mur INT NOT NULL,
    deperdition_mur DECIMAL(10,3),
    FOREIGN KEY (id_batiment) REFERENCES batiment(id) ON DELETE CASCADE,
    FOREIGN KEY (id_type_mur) REFERENCES type_mur(id)
);

-- ============================================================
-- Table : Plancher
-- ============================================================
CREATE TABLE IF NOT EXISTS plancher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment INT NOT NULL,
    numero_plancher INT NOT NULL,
    etat_plancher VARCHAR(50) DEFAULT 'Bon état',
    surface_plancher DECIMAL(10,2) NOT NULL,
    id_type_plancher INT NOT NULL,
    deperdition_plancher DECIMAL(10,3),
    FOREIGN KEY (id_batiment) REFERENCES batiment(id) ON DELETE CASCADE,
    FOREIGN KEY (id_type_plancher) REFERENCES type_plancher(id)
);

-- ============================================================
-- Table : Toiture
-- ============================================================
CREATE TABLE IF NOT EXISTS toiture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment INT NOT NULL,
    numero_toiture INT NOT NULL,
    type_toiture_label VARCHAR(100),
    etat_toiture VARCHAR(50) DEFAULT 'Bon état',
    surface_toit DECIMAL(10,2) NOT NULL,
    id_type_toiture INT NOT NULL,
    deperdition_toiture DECIMAL(10,3),
    FOREIGN KEY (id_batiment) REFERENCES batiment(id) ON DELETE CASCADE,
    FOREIGN KEY (id_type_toiture) REFERENCES type_toiture(id)
);

-- ============================================================
-- Table : Ouvrant
-- ============================================================
CREATE TABLE IF NOT EXISTS ouvrant (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment INT NOT NULL,
    numero_ouvrant INT NOT NULL,
    surface_ouvrant DECIMAL(8,2) NOT NULL,
    etat_ouvrant VARCHAR(50) DEFAULT 'Bon état',
    id_type_ouvrant INT NOT NULL,
    deperdition_ouvrant DECIMAL(10,3),
    FOREIGN KEY (id_batiment) REFERENCES batiment(id) ON DELETE CASCADE,
    FOREIGN KEY (id_type_ouvrant) REFERENCES type_ouvrant(id)
);

-- ============================================================
-- Table : Résultat de calcul
-- ============================================================
CREATE TABLE IF NOT EXISTS resultat_calcul (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_batiment INT NOT NULL UNIQUE,
    deperdition_totale DECIMAL(12,3) NOT NULL COMMENT 'en W/K',
    consommation_kwh DECIMAL(12,3) NOT NULL COMMENT 'en kWh/m²/an',
    classe_energetique CHAR(1) NOT NULL,
    date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_batiment) REFERENCES batiment(id) ON DELETE CASCADE
);

-- ============================================================
-- Table : Association Bâtiment - Source d'énergie
-- ============================================================
CREATE TABLE IF NOT EXISTS batiment_source (
    id_batiment INT NOT NULL,
    id_source INT NOT NULL,
    PRIMARY KEY (id_batiment, id_source),
    FOREIGN KEY (id_batiment) REFERENCES batiment(id) ON DELETE CASCADE,
    FOREIGN KEY (id_source) REFERENCES source_energie(id)
);
