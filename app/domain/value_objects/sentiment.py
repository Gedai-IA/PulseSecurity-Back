from enum import Enum
from typing import Literal


class Sentiment(str, Enum):
    """Value Object para sentimento."""
    POSITIVO = "Positivo"
    NEGATIVO = "Negativo"
    NEUTRO = "Neutro"


SentimentType = Literal["Positivo", "Negativo", "Neutro"]

