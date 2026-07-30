"""Dataset storage API router."""

from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from backend.core.security import get_current_user
from backend.db.database import get_db
from backend.models.dataset import DatasetModel
from backend.models.user import UserModel
from backend.schemas.dataset import DatasetResponse
from backend.services.minio_service import MinIOService

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets"])


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload dataset file to MinIO and store metadata record in PostgreSQL."""
    contents = await file.read()
    file_size = len(contents)
    filename = file.filename

    bucket_name = "raw-datasets"
    object_path = f"datasets/{current_user.id}/{filename}"

    minio_service = MinIOService()
    minio_service.ensure_bucket(bucket_name)
    minio_service.upload_bytes(
        object_name=object_path,
        data=contents,
        bucket_name=bucket_name,
        content_type=file.content_type or "application/octet-stream",
    )

    dataset_record = DatasetModel(
        filename=filename,
        minio_path=object_path,
        file_size=file_size,
        uploaded_by=current_user.id,
    )
    db.add(dataset_record)
    db.commit()
    db.refresh(dataset_record)

    return dataset_record


@router.get("", response_model=List[DatasetResponse])
@router.get("/", response_model=List[DatasetResponse])
def get_datasets(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve list of datasets."""
    datasets = db.query(DatasetModel).all()
    return datasets
