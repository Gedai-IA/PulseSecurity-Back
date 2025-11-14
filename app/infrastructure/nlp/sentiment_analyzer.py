from typing import Dict, List
import spacy

from app.domain.value_objects.sentiment import Sentiment


class SentimentAnalyzer:
    """Analisador de sentimento baseado em keywords (compatível com front-end)."""
    
    # Keywords do front-end
    POSITIVE_KEYWORDS = [
        'gostei', 'legal', 'tmj', 'parabéns', 'kkkkk', 'unidos', 'sempre',
        'dominamos', 'vai corinthians', '🦅', '👊🏼', '⚫⚪', 'respeito',
        'obrigado', 'show', 'top', 'massa', 'boa', 'isso', 'vamoo',
        'lindo', 'família', 'melhor', 'meu amor', 'é nós', 'parabens',
        'orgulho', 'gigante', 'raça', 'campeão', 'vencer', 'ganhamos',
    ]
    
    NEGATIVE_KEYWORDS = [
        'correram', 'vergonha', 'ridículo', 'lixo', 'pior', 'odeio',
        'tomaram', 'lamentável', 'piada', 'fdp', 'time pequeno', 'some',
        'fraco', 'covardes', 'merda', 'vtnc', 'humilhação', 'acabou',
        'fora', 'pipoqueiro', 'incompetente', 'desgraça', 'violência',
        'briga', 'morte', 'ferido', 'tumulto', 'confusão', 'invasão',
        'guerra', 'perdemos', 'lixos',
    ]
    
    def __init__(self):
        self.nlp = None  # Pode ser inicializado com spaCy se necessário
    
    def analyze(self, text: str) -> Sentiment:
        """Analisa o sentimento de um texto."""
        if not text:
            return Sentiment.NEUTRO
        
        lower_text = text.lower()
        
        # Verifica keywords negativas primeiro
        for keyword in self.NEGATIVE_KEYWORDS:
            if keyword in lower_text:
                return Sentiment.NEGATIVO
        
        # Verifica keywords positivas
        for keyword in self.POSITIVE_KEYWORDS:
            if keyword in lower_text:
                return Sentiment.POSITIVO
        
        return Sentiment.NEUTRO
    
    def analyze_batch(self, texts: List[str]) -> List[Sentiment]:
        """Analisa múltiplos textos."""
        return [self.analyze(text) for text in texts]

