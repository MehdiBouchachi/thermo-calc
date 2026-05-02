#!/usr/bin/env python
"""Add dummy buildings to test the application"""

import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'life3002%%IdHeM',
    'database': 'thermique_db',
}

try:
    print("Connecting to MySQL server...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Insert 3 dummy buildings
    buildings = [
        {
            'code': 'BAT-001',
            'address': '12 rue de la Paix, Alger',
            'type': 'Bureau',
            'surface': 450,
            'volume': 1350,
            'construction_year': 2015,
            'levels': 3,
            'occupants': 45,
            'zone_id': 2,
            'geo': '36.7538, 3.0588'
        },
        {
            'code': 'BAT-002',
            'address': '25 avenue Didouche Mourad, Alger',
            'type': 'Logement collectif',
            'surface': 800,
            'volume': 2400,
            'construction_year': 2010,
            'levels': 5,
            'occupants': 120,
            'zone_id': 2,
            'geo': '36.7556, 3.0650'
        },
        {
            'code': 'BAT-003',
            'address': '5 boulevard Zirout Youcef, Alger',
            'type': 'Hôpital',
            'surface': 2500,
            'volume': 12500,
            'construction_year': 2005,
            'levels': 6,
            'occupants': 400,
            'zone_id': 2,
            'geo': '36.7620, 3.0720'
        }
    ]
    
    batiment_ids = []
    
    for building in buildings:
        cursor.execute("""
            INSERT INTO batiment 
            (code_batiment, adresse_batiment, type_batiment, surface, volume, 
             annee_construction, nombre_niveaux, nombre_occupants, id_zone_climatique, coordonnees_geo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            building['code'],
            building['address'],
            building['type'],
            building['surface'],
            building['volume'],
            building['construction_year'],
            building['levels'],
            building['occupants'],
            building['zone_id'],
            building['geo']
        ))
        batiment_ids.append(cursor.lastrowid)
        print(f"✓ Created building: {building['code']} (ID: {cursor.lastrowid})")
    
    # Add energy sources for each building
    sources = [2, 5, 6]  # Electricity, Gas, Solar
    for batiment_id in batiment_ids:
        for source_id in sources:
            cursor.execute(
                "INSERT INTO batiment_source (id_batiment, id_source) VALUES (%s, %s)",
                (batiment_id, source_id)
            )
    
    # Add sample walls for building 1
    if batiment_ids:
        cursor.execute("SELECT k_mur FROM type_mur WHERE id=3 LIMIT 1")
        k_mur = cursor.fetchone()['k_mur']
        
        # 4 walls with different dimensions
        walls = [
            (1, 10, 3, 0.45 * 10 * 3, 'Bon état'),
            (2, 8, 3, 0.45 * 8 * 3, 'Bon état'),
            (3, 10, 3, 0.45 * 10 * 3, 'Bon état'),
            (4, 8, 3, 0.45 * 8 * 3, 'Bon état'),
        ]
        for wall_num, length, height, dep, condition in walls:
            cursor.execute("""
                INSERT INTO mur (id_batiment, numero_mur, longueur_mur, hauteur_mur, 
                               etat_mur, id_type_mur, deperdition_mur)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (batiment_ids[0], wall_num, length, height, condition, 3, dep))
        print(f"✓ Added 4 walls to BAT-001")
        
        # Add floor
        cursor.execute("SELECT k_plancher FROM type_plancher WHERE id=2 LIMIT 1")
        k_plancher = cursor.fetchone()['k_plancher']
        dep_plancher = k_plancher * 450
        cursor.execute("""
            INSERT INTO plancher (id_batiment, numero_plancher, etat_plancher, 
                                surface_plancher, id_type_plancher, deperdition_plancher)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (batiment_ids[0], 1, 'Bon état', 450, 2, dep_plancher))
        print(f"✓ Added floor to BAT-001")
        
        # Add roof
        cursor.execute("SELECT k_toiture FROM type_toiture WHERE id=1 LIMIT 1")
        k_toiture = cursor.fetchone()['k_toiture']
        dep_toiture = k_toiture * 450
        cursor.execute("""
            INSERT INTO toiture (id_batiment, numero_toiture, etat_toiture, 
                                surface_toit, id_type_toiture, deperdition_toiture)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (batiment_ids[0], 1, 'Bon état', 450, 1, dep_toiture))
        print(f"✓ Added roof to BAT-001")
        
        # Add windows
        cursor.execute("SELECT k_ouvrant FROM type_ouvrant WHERE id=1 LIMIT 1")
        k_ouvrant = float(cursor.fetchone()['k_ouvrant'])
        for i in range(8):
            dep_ouvrant = k_ouvrant * 2.5
            cursor.execute("""
                INSERT INTO ouvrant (id_batiment, numero_ouvrant, surface_ouvrant, 
                                    etat_ouvrant, id_type_ouvrant, deperdition_ouvrant)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (batiment_ids[0], i+1, 2.5, 'Bon état', 1, dep_ouvrant))
        print(f"✓ Added 8 windows to BAT-001")
        
        # Calculate total heat loss for building 1
        k_mur = float(k_mur)
        k_plancher = float(k_plancher)
        k_toiture = float(k_toiture)
        total_dep = (4 * k_mur * 10 * 3 + float(dep_plancher) + float(dep_toiture) + 8 * k_ouvrant * 2.5)
        surface = 450
        consumption = (total_dep * 2400) / (surface * 1000)
        
        if consumption <= 70:
            classe = 'A'
        elif consumption <= 110:
            classe = 'B'
        elif consumption <= 180:
            classe = 'C'
        elif consumption <= 250:
            classe = 'D'
        elif consumption <= 330:
            classe = 'E'
        elif consumption <= 420:
            classe = 'F'
        else:
            classe = 'G'
        
        cursor.execute("""
            INSERT INTO resultat_calcul (id_batiment, deperdition_totale, consommation_kwh, classe_energetique)
            VALUES (%s, %s, %s, %s)
        """, (batiment_ids[0], round(total_dep, 3), round(consumption, 3), classe))
        print(f"✓ Calculated results for BAT-001: Class {classe}, Consumption {round(consumption, 2)} kWh/m²/an")
    
    conn.commit()
    print('\n✅ Successfully added 3 dummy buildings with components!')
    cursor.close()
    conn.close()
except Error as e:
    print(f'❌ Error: {e}')
    exit(1)
except Exception as e:
    print(f'❌ Unexpected error: {e}')
    exit(1)
