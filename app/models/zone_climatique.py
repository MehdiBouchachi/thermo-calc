"""Model for ZoneClimatique (climate zone)."""


class ZoneClimatique:
    """Represents a climate zone."""

    def __init__(self, id, nom_zone, description=None):
        self.id = id
        self.nom_zone = nom_zone
        self.description = description

    @classmethod
    def from_db_row(cls, row: dict) -> 'ZoneClimatique':
        """Builds a ZoneClimatique from a DB row."""
        return cls(id=row['id'], nom_zone=row['nom_zone'],
                   description=row.get('description'))
