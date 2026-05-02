"""Classifier service for energy class determination."""


def classify(consommation: float) -> str:
    """Returns energy class A–G from a kWh/m²/an consumption value."""
    if consommation <= 70:
        return 'A'
    if consommation <= 110:
        return 'B'
    if consommation <= 180:
        return 'C'
    if consommation <= 250:
        return 'D'
    if consommation <= 330:
        return 'E'
    if consommation <= 420:
        return 'F'
    return 'G'
