"""Model Registry API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.security import get_current_user
from backend.db.database import get_db
from backend.models.model_registry import ModelRegistryModel
from backend.models.user import UserModel
from backend.schemas.model import ModelRegisterRequest, ModelRegistryResponse

router = APIRouter(prefix="/api/v1/models", tags=["Model Registry"])


@router.post("/register", response_model=ModelRegistryResponse, status_code=status.HTTP_201_CREATED)
def register_model(
    model_in: ModelRegisterRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Register a new machine learning model record using append-only pattern."""
    model_record = ModelRegistryModel(
        model_name=model_in.model_name,
        version=model_in.version,
        minio_weight_path=model_in.minio_weight_path,
        metrics=model_in.metrics,
        created_by=current_user.id,
    )
    db.add(model_record)
    db.commit()
    db.refresh(model_record)
    return model_record


@router.get("", response_model=List[ModelRegistryResponse])
@router.get("/", response_model=List[ModelRegistryResponse])
def get_models(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve list of all registered models."""
    models = db.query(ModelRegistryModel).all()
    return models
