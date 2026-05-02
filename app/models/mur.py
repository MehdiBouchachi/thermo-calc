"""Model for Mur (wall) component."""


class Mur:
    """Represents a wall component. Implements Calculer-Déperdition-Mur from class diagram."""

    def __init__(self, id, id_batiment, numero_mur, longueur_mur,
                 hauteur_mur, etat_mur, id_type_mur, k_mur,
                 nom_type, deperdition_mur=None):
        self.id = id
        self.id_batiment = id_batiment
        self.numero_mur = numero_mur
        self.longueur_mur = float(longueur_mur)
        self.hauteur_mur = float(hauteur_mur)
        self.etat_mur = etat_mur
        self.id_type_mur = id_type_mur
        self.k_mur = float(k_mur)
        self.nom_type = nom_type
        self.deperdition_mur = deperdition_mur

    def calculer_deperdition(self) -> float:
        """Déperdition Mur = k_mur * longueur_mur * hauteur_mur"""
        return round(self.k_mur * self.longueur_mur * self.hauteur_mur, 3)

    @classmethod
    def from_db_row(cls, row: dict) -> 'Mur':
        """Builds a Mur instance from a raw DB dictionary row."""
        return cls(
            id=row['id'], id_batiment=row['id_batiment'],
            numero_mur=row['numero_mur'], longueur_mur=row['longueur_mur'],
            hauteur_mur=row['hauteur_mur'], etat_mur=row['etat_mur'],
            id_type_mur=row['id_type_mur'], k_mur=row['k_mur'],
            nom_type=row['nom_type'], deperdition_mur=row.get('deperdition_mur')
        )
