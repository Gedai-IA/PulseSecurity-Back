from typing import Dict, List
from app.domain.value_objects.topic import Topic


class TopicClassifier:
    """Classificador de tópicos baseado em keywords."""
    
    TOPIC_KEYWORDS: Dict[Topic, List[str]] = {
        Topic.AMEACAS_E_RISCOS: [
            'guerra', 'ataque', 'bater', 'briga', 'luta', 'vingança',
            'morte', 'ferido', 'tumulto', 'confusão', 'invasão',
            'emboscada', 'vai morrer', 'matar', 'mct', 'bct', 'gdf', 'pista',
        ],
        Topic.RIVALIDADE_ESPORTIVA: [
            'correram', 'mancha', 'porko', 'palmeiras', 'sem mundial',
            'freguês', 'trikas', 'bambis',
        ],
        Topic.SEGURANCA_POLICIAL: [
            'polícia', 'segurança', 'violência', 'roubo', 'bomba',
            'choque', 'pm', 'viatura',
        ],
        Topic.APOIO_E_UNIAO: [
            'unidos', 'sempre', 'irmão', 'tmj', 'apoio', 'torcida',
            'respeito', 'corinthians', 'gaviões', 'fiel', 'orgulho',
        ],
        Topic.ORGANIZACAO_E_EVENTOS: [
            'jogo', 'grupo', 'evento', 'final', 'campeonato', 'paulista',
            'estádio', 'caravana', 'ingresso', 'bandeira',
        ],
        Topic.POLITICA_E_GESTAO: [
            'política', 'corrupção', 'vergonha', 'governo', 'pagar',
            'diretoria', 'augusto melo', 'presidente', 'fora', 'eleição',
        ],
    }
    
    def classify(self, text: str) -> Topic:
        """Classifica o tópico de um texto."""
        if not text:
            return Topic.GERAL
        
        lower_text = text.lower()
        
        # Verifica em ordem de prioridade (mais específico primeiro)
        priority_order = [
            Topic.AMEACAS_E_RISCOS,
            Topic.SEGURANCA_POLICIAL,
            Topic.RIVALIDADE_ESPORTIVA,
            Topic.POLITICA_E_GESTAO,
            Topic.ORGANIZACAO_E_EVENTOS,
            Topic.APOIO_E_UNIAO,
        ]
        
        for topic in priority_order:
            for keyword in self.TOPIC_KEYWORDS.get(topic, []):
                if keyword in lower_text:
                    return topic
        
        return Topic.GERAL
    
    def classify_batch(self, texts: List[str]) -> List[Topic]:
        """Classifica múltiplos textos."""
        return [self.classify(text) for text in texts]

