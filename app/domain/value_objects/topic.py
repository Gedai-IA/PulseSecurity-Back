from enum import Enum
from typing import Literal


class Topic(str, Enum):
    """Value Object para tópico."""
    AMEACAS_E_RISCOS = "Ameaças e Riscos"
    RIVALIDADE_ESPORTIVA = "Rivalidade Esportiva"
    SEGURANCA_POLICIAL = "Segurança (Policial)"
    APOIO_E_UNIAO = "Apoio e União"
    ORGANIZACAO_E_EVENTOS = "Organização e Eventos"
    POLITICA_E_GESTAO = "Política e Gestão"
    GERAL = "Geral"


TopicType = Literal[
    "Ameaças e Riscos",
    "Rivalidade Esportiva",
    "Segurança (Policial)",
    "Apoio e União",
    "Organização e Eventos",
    "Política e Gestão",
    "Geral"
]

