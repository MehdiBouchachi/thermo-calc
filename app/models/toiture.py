"""Model for Toiture (roof) component."""


class Toiture:
    """Represents a roof component. Implements Calculer-Déperdition-Toiture."""

    def __init__(self, id, id_batiment, numero_toiture, surface_toit,
                 etat_toiture, id_type_toiture, k_toiture,
                 nom_type, deperdition_toiture=None):
        self.id = id
        self.id_batiment = id_batiment
        self.numero_toiture = numero_toiture
        self.surface_toit = float(surface_toit)
        self.etat_toiture = etat_toiture
        self.id_type_toiture = id_type_toiture
        self.k_toiture = float(k_toiture)
        self.nom_type = nom_type
        self.deperdition_toiture = deperdition_toiture

    def calculer_deperdition(self) -> float:
        """Déperdition Toiture = k_toiture * surface_toit"""
        return round(self.k_toiture * self.surface_toit, 3)

    @classmethod
    def from_db_row(cls, row: dict) -> 'Toiture':
        """Builds a Toiture instance from a raw DB dictionary row."""
        return cls(
            id=row['id'], id_batiment=row['id_batiment'],
            numero_toiture=row['numero_toiture'], surface_toit=row['surface_toit'],
            etat_toiture=row['etat_toiture'], id_type_toiture=row['id_type_toiture'],
            k_toiture=row['k_toiture'], nom_type=row['nom_type'],
            deperdition_toiture=row.get('deperdition_toiture')
        )
