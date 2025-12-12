"""
Rotas para o módulo de Object Detector
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional
import os
from pathlib import Path

from app.application.services.object_detector_service import get_detector_service, ObjectDetectorService
from app.api.v1.schemas.object_detector_schemas import (
    DetectionResponse,
    DetectionPrediction,
    ErrorResponse
)

router = APIRouter()


@router.post("/object-detector/predict", response_model=DetectionResponse)
async def predict_objects(
    image: UploadFile = File(..., description="Imagem para detecção de objetos"),
    confidence: float = Form(0.25, ge=0.1, le=1.0, description="Threshold de confiança (0.1 a 1.0)"),
    detector_service: ObjectDetectorService = Depends(get_detector_service)
):
    """
    Processa uma imagem e detecta objetos usando YOLO
    
    - **image**: Arquivo de imagem (JPG, PNG, BMP, etc.)
    - **confidence**: Threshold de confiança mínimo (padrão: 0.25)
    
    Retorna as detecções encontradas com bounding boxes e confiança.
    """
    # Valida o tipo de arquivo
    if not image.content_type or not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="Arquivo deve ser uma imagem válida"
        )
    
    try:
        # Processa a imagem
        result = detector_service.predict_from_upload(image, confidence=confidence)
        
        # Converte para o formato de resposta
        predictions = [
            DetectionPrediction(
                model=pred.get("model"),
                class_name=pred.get("class_name", "Unknown"),
                conf=pred.get("conf", 0.0),
                xyxy=pred.get("xyxy", []),
                class_id=pred.get("class_id")
            )
            for pred in result.get("predictions", [])
        ]
        
        # Prepara a URL da imagem anotada (se disponível)
        annotated_image_url = None
        if result.get("annotated_path"):
            annotated_path = result["annotated_path"]
            # Gera URL relativa para download
            annotated_image_url = f"/api/v1/object-detector/image/{Path(annotated_path).name}"
        
        return DetectionResponse(
            image_path=result.get("image_path"),
            annotated_path=result.get("annotated_path"),
            annotated_image_url=annotated_image_url,
            predictions=predictions,
            timestamp=result.get("timestamp"),
            model_info=result.get("model_info")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar imagem: {str(e)}"
        )


@router.get("/object-detector/image/{image_name}")
async def get_annotated_image(
    image_name: str,
    detector_service: ObjectDetectorService = Depends(get_detector_service)
):
    """
    Retorna a imagem anotada com as detecções
    
    - **image_name**: Nome do arquivo da imagem anotada
    """
    try:
        # Tenta encontrar a imagem no diretório temporário
        image_path = detector_service.get_annotated_image_path(image_name)
        
        if image_path is None or not image_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Imagem anotada não encontrada: {image_name}"
            )
        
        return FileResponse(
            path=str(image_path),
            media_type="image/jpeg",
            filename=image_name
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao recuperar imagem: {str(e)}"
        )


@router.get("/object-detector/status/{task_id}")
async def get_detection_status(task_id: str):
    """
    Obtém o status de uma detecção assíncrona (para implementação futura)
    
    - **task_id**: ID da tarefa de detecção
    """
    # TODO: Implementar processamento assíncrono com Celery ou similar
    return {
        "task_id": task_id,
        "status": "not_implemented",
        "message": "Processamento assíncrono ainda não implementado"
    }


@router.get("/object-detector/results/{task_id}")
async def get_detection_results(task_id: str):
    """
    Obtém os resultados de uma detecção assíncrona (para implementação futura)
    
    - **task_id**: ID da tarefa de detecção
    """
    # TODO: Implementar processamento assíncrono com Celery ou similar
    raise HTTPException(
        status_code=501,
        detail="Processamento assíncrono ainda não implementado"
    )

