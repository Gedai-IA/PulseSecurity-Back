from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DetectionPrediction(BaseModel):
    """Predição individual de detecção"""
    model: Optional[str] = None
    class_name: str
    conf: float
    xyxy: List[float]  # [x1, y1, x2, y2]
    class_id: Optional[int] = None


class DetectionResponse(BaseModel):
    """Resposta de detecção de objetos"""
    image_path: Optional[str] = None
    annotated_path: Optional[str] = None
    annotated_image_url: Optional[str] = None
    predictions: List[DetectionPrediction]
    processing_time: Optional[float] = None
    timestamp: Optional[datetime] = None
    model_info: Optional[dict] = None


class DetectionStatusResponse(BaseModel):
    """Status de uma detecção assíncrona"""
    task_id: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    progress: Optional[float] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Resposta de erro"""
    detail: str
    error_code: Optional[str] = None

