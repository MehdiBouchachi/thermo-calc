"""Model for SourceEnergie (energy source)."""


class SourceEnergie:
    """Represents an energy source."""

    def __init__(self, id, nom_source, etat_source=None, caracteristiques=None):
        self.id = id
        self.nom_source = nom_source
        self.etat_source = etat_source
        self.caracteristiques = caracteristiques

    @classmethod
    def from_db_row(cls, row: dict) -> 'SourceEnergie':
        """Builds a SourceEnergie from a DB row."""
        return cls(id=row['id'], nom_source=row['nom_source'],
                   etat_source=row.get('etat_source'),
                   caracteristiques=row.get('caracteristiques'))
