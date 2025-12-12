"""
Service para integração com o módulo ObjectDetector
"""
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile
import shutil
from datetime import datetime

# Adiciona o caminho do ObjectDetector ao sys.path
# Tenta múltiplos caminhos possíveis
possible_paths = [
    Path(__file__).resolve().parent.parent.parent.parent.parent / "ObjectDetector",
    Path(__file__).resolve().parent.parent.parent.parent / "ObjectDetector",
    Path.cwd() / "ObjectDetector",
    Path.cwd().parent / "ObjectDetector",
]

OBJECT_DETECTOR_PATH = None
for path in possible_paths:
    if path.exists() and (path / "app" / "yolo" / "image_detector.py").exists():
        OBJECT_DETECTOR_PATH = path
        break

if OBJECT_DETECTOR_PATH is None:
    # Se não encontrar, usa o primeiro caminho como padrão
    OBJECT_DETECTOR_PATH = possible_paths[0]

if str(OBJECT_DETECTOR_PATH) not in sys.path:
    sys.path.insert(0, str(OBJECT_DETECTOR_PATH))

try:
    from app.yolo.image_detector import YoloDetector
except ImportError:
    # Fallback: tenta importar diretamente
    try:
        sys.path.insert(0, str(OBJECT_DETECTOR_PATH / "app"))
        from yolo.image_detector import YoloDetector
    except ImportError:
        YoloDetector = None


class ObjectDetectorService:
    """Service para processamento de detecção de objetos"""
    
    def __init__(self, models_dir: Optional[Path] = None, conf_threshold: float = 0.25):
        """
        Inicializa o service de detecção
        
        Args:
            models_dir: Diretório contendo os modelos YOLO (.pt files)
            conf_threshold: Threshold de confiança mínimo (0.0 a 1.0)
        """
        if YoloDetector is None:
            raise ImportError(
                "Não foi possível importar YoloDetector. "
                "Certifique-se de que o módulo ObjectDetector está disponível."
            )
        
        # Define o diretório de modelos
        if models_dir is None:
            models_dir = OBJECT_DETECTOR_PATH / "models"
        
        self.models_dir = Path(models_dir)
        if not self.models_dir.exists():
            raise FileNotFoundError(f"Diretório de modelos não encontrado: {models_dir}")
        
        self.conf_threshold = conf_threshold
        self.detector: Optional[YoloDetector] = None
        self._temp_dir = None
    
    def _get_detector(self) -> YoloDetector:
        """Lazy loading do detector"""
        if self.detector is None:
            self.detector = YoloDetector(
                models_dir=self.models_dir,
                conf_threshold=self.conf_threshold
            )
        return self.detector
    
    def predict(self, image_path: str, confidence: Optional[float] = None) -> Dict[str, Any]:
        """
        Processa uma imagem e retorna as detecções
        
        Args:
            image_path: Caminho para a imagem a ser processada
            confidence: Threshold de confiança (sobrescreve o padrão se fornecido)
            
        Returns:
            Dicionário com os resultados da detecção
        """
        if confidence is not None:
            # Atualiza o threshold se fornecido
            if self.detector is None or self.conf_threshold != confidence:
                self.conf_threshold = confidence
                self.detector = None  # Força recriação com novo threshold
        
        detector = self._get_detector()
        
        # Cria diretório temporário para imagens anotadas
        if self._temp_dir is None or not self._temp_dir.exists():
            self._temp_dir = Path(tempfile.mkdtemp(prefix="object_detector_"))
        
        # Processa a imagem (YoloDetector aceita Path para save_annotated_dir)
        result = detector.infer(
            image_path=image_path,
            save_annotated_dir=str(self._temp_dir)
        )
        
        # Adiciona informações adicionais
        result["timestamp"] = datetime.now().isoformat()
        result["model_info"] = {
            "models_dir": str(self.models_dir),
            "confidence_threshold": self.conf_threshold
        }
        
        return result
    
    def predict_from_upload(self, uploaded_file, confidence: Optional[float] = None) -> Dict[str, Any]:
        """
        Processa um arquivo enviado via upload
        
        Args:
            uploaded_file: Arquivo FastAPI UploadFile
            confidence: Threshold de confiança
            
        Returns:
            Dicionário com os resultados da detecção
        """
        # Salva o arquivo temporariamente
        if self._temp_dir is None or not self._temp_dir.exists():
            self._temp_dir = Path(tempfile.mkdtemp(prefix="object_detector_"))
        
        temp_image_path = self._temp_dir / uploaded_file.filename
        
        with open(temp_image_path, "wb") as f:
            shutil.copyfileobj(uploaded_file.file, f)
        
        try:
            # Processa a imagem
            result = self.predict(str(temp_image_path), confidence=confidence)
            
            # Atualiza os caminhos para serem relativos ou URLs
            result["original_filename"] = uploaded_file.filename
            
            return result
        finally:
            # Limpa o arquivo temporário original (a imagem anotada é mantida)
            if temp_image_path.exists():
                pass  # Mantém o arquivo para possível download posterior
    
    def get_annotated_image_path(self, annotated_path: str) -> Optional[Path]:
        """
        Retorna o caminho completo da imagem anotada
        
        Args:
            annotated_path: Caminho relativo ou absoluto da imagem anotada
            
        Returns:
            Path completo se existir, None caso contrário
        """
        path = Path(annotated_path)
        if path.is_absolute() and path.exists():
            return path
        
        # Tenta no diretório temporário
        if self._temp_dir and self._temp_dir.exists():
            temp_path = self._temp_dir / Path(annotated_path).name
            if temp_path.exists():
                return temp_path
        
        return None
    
    def cleanup_temp_files(self):
        """Limpa arquivos temporários"""
        if self._temp_dir and self._temp_dir.exists():
            try:
                shutil.rmtree(self._temp_dir)
                self._temp_dir = None
            except Exception as e:
                print(f"Erro ao limpar arquivos temporários: {e}")


# Instância singleton (pode ser inicializada via dependency injection)
_detector_service: Optional[ObjectDetectorService] = None


def get_detector_service() -> ObjectDetectorService:
    """Factory function para obter instância do service"""
    global _detector_service
    if _detector_service is None:
        try:
            _detector_service = ObjectDetectorService()
        except Exception as e:
            print(f"Erro ao inicializar ObjectDetectorService: {e}")
            raise
    return _detector_service

