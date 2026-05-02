"""Model for Plancher (floor) component."""


class Plancher:
    """Represents a floor component. Implements Calculer-Déperdition-Plancher."""

    def __init__(self, id, id_batiment, numero_plancher, surface_plancher,
                 etat_plancher, id_type_plancher, k_plancher,
                 nom_type, deperdition_plancher=None):
        self.id = id
        self.id_batiment = id_batiment
        self.numero_plancher = numero_plancher
        self.surface_plancher = float(surface_plancher)
        self.etat_plancher = etat_plancher
        self.id_type_plancher = id_type_plancher
        self.k_plancher = float(k_plancher)
        self.nom_type = nom_type
        self.deperdition_plancher = deperdition_plancher

    def calculer_deperdition(self) -> float:
        """Déperdition Plancher = k_plancher * surface_plancher"""
        return round(self.k_plancher * self.surface_plancher, 3)

    @classmethod
    def from_db_row(cls, row: dict) -> 'Plancher':
        """Builds a Plancher instance from a raw DB dictionary row."""
        return cls(
            id=row['id'], id_batiment=row['id_batiment'],
            numero_plancher=row['numero_plancher'],
            surface_plancher=row['surface_plancher'],
            etat_plancher=row['etat_plancher'],
            id_type_plancher=row['id_type_plancher'],
            k_plancher=row['k_plancher'], nom_type=row['nom_type'],
            deperdition_plancher=row.get('deperdition_plancher')
        )
