"""Model for Ouvrant (window/opening) component."""


class Ouvrant:
    """Represents a window/door opening. Implements Calculer-Déperdition-Ouvrant."""

    def __init__(self, id, id_batiment, numero_ouvrant, surface_ouvrant,
                 etat_ouvrant, id_type_ouvrant, k_ouvrant,
                 nom_type, deperdition_ouvrant=None):
        self.id = id
        self.id_batiment = id_batiment
        self.numero_ouvrant = numero_ouvrant
        self.surface_ouvrant = float(surface_ouvrant)
        self.etat_ouvrant = etat_ouvrant
        self.id_type_ouvrant = id_type_ouvrant
        self.k_ouvrant = float(k_ouvrant)
        self.nom_type = nom_type
        self.deperdition_ouvrant = deperdition_ouvrant

    def calculer_deperdition(self) -> float:
        """Déperdition Ouvrant = k_ouvrant * surface_ouvrant"""
        return round(self.k_ouvrant * self.surface_ouvrant, 3)

    @classmethod
    def from_db_row(cls, row: dict) -> 'Ouvrant':
        """Builds an Ouvrant instance from a raw DB dictionary row."""
        return cls(
            id=row['id'], id_batiment=row['id_batiment'],
            numero_ouvrant=row['numero_ouvrant'],
            surface_ouvrant=row['surface_ouvrant'],
            etat_ouvrant=row['etat_ouvrant'],
            id_type_ouvrant=row['id_type_ouvrant'],
            k_ouvrant=row['k_ouvrant'], nom_type=row['nom_type'],
            deperdition_ouvrant=row.get('deperdition_ouvrant')
        )
