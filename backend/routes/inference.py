"""Inference API router."""

from fastapi import APIRouter, Depends

from backend.core.security import get_current_user
from backend.models.user import UserModel
from backend.schemas.inference import PredictRequest, PredictResponse

router = APIRouter(prefix="/api/v1/predict", tags=["Inference"])


@router.post("", response_model=PredictResponse)
@router.post("/", response_model=PredictResponse)
def predict(
    request: PredictRequest,
    current_user: UserModel = Depends(get_current_user),
):
    """Perform model inference on input data."""
    return PredictResponse(
        prediction={
            "result": "success",
            "model_id": request.model_id,
            "processed_input": request.input_data,
        },
        confidence=0.95,
        model_version="v1.0.0",
    )
