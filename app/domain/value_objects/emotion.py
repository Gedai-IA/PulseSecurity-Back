from enum import Enum
from typing import Literal


class Emotion(str, Enum):
    """Value Object para emoção."""
    ALEGRIA = "Alegria"
    RAIVA = "Raiva"
    FRUSTRAÇÃO = "Frustração"
    ANSIEDADE = "Ansiedade"
    GERAL = "Geral"


EmotionType = Literal["Alegria", "Raiva", "Frustração", "Ansiedade", "Geral"]

