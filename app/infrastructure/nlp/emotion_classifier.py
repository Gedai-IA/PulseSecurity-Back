from typing import Dict, List
from app.domain.value_objects.emotion import Emotion


class EmotionClassifier:
    """Classificador de emoções baseado em keywords."""
    
    EMOTION_KEYWORDS: Dict[Emotion, List[str]] = {
        Emotion.ALEGRIA: [
            'gostei', 'legal', 'tmj', 'parabéns', 'kkkkk', 'unidos', 'sempre',
            'dominamos', 'vai corinthians', '🦅', '👊🏼', '⚫⚪', 'respeito',
            'obrigado', 'show', 'top', 'massa', 'boa', 'isso', 'vamoo',
            'lindo', 'família', 'melhor', 'meu amor', 'é nós', 'parabens',
            'orgulho', 'gigante', 'raça', 'campeão', 'vencer',
        ],
        Emotion.RAIVA: [
            'correram', 'vergonha', 'ridículo', 'lixo', 'pior', 'odeio',
            'tomaram', 'lamentável', 'piada', 'fdp', 'time pequeno', 'some',
            'fraco', 'covardes', 'merda', 'vtnc', 'humilhação', 'acabou',
            'fora', 'pipoqueiro', 'incompetente', 'desgraça', 'violência',
            'briga', 'morte', 'ferido', 'tumulto', 'confusão', 'bomba',
            'polícia', 'invasão', 'guerra',
        ],
        Emotion.FRUSTRAÇÃO: [
            'decepção', 'absurdo', 'paciência', 'desisto', 'difícil',
            'complicado', 'não aguento mais', 'de novo', 'sempre a mesma coisa',
            'que raiva',
        ],
        Emotion.ANSIEDADE: [
            'esperando', 'ansioso', 'cadê', 'demora', 'logo', 'será que',
            'medo', 'temer', 'cuidado',
        ],
    }
    
    def classify(self, text: str) -> Emotion:
        """Classifica a emoção de um texto."""
        if not text:
            return Emotion.GERAL
        
        lower_text = text.lower()
        
        # Verifica em ordem de prioridade
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in lower_text:
                    return emotion
        
        return Emotion.GERAL
    
    def classify_batch(self, texts: List[str]) -> List[Emotion]:
        """Classifica múltiplos textos."""
        return [self.classify(text) for text in texts]

