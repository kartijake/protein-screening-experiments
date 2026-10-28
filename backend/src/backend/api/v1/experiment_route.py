from fastapi import APIRouter, status, UploadFile, File, HTTPException, Form, Query
from backend.schemas.experiment import Experiment, ExperimentCreate,PaginatedExperiments
from backend.services import experiment_service
from backend.services.fasta_parser import parse_fasta

router = APIRouter(
    prefix="/experiments",
    tags=["Experiments"],
)


@router.post(
    "",
    response_model=Experiment,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(data: ExperimentCreate):
    return experiment_service.create_experiment(data)


@router.get(
    "",
    response_model=PaginatedExperiments,
)
def list_experiments(
    limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0)
):
    return experiment_service.list_experiments(limit=limit, offset=offset)


# file size parameters
MAX_FILE_SIZE = 32 * 1024


@router.post("/uplaod")
async def uplaod_fasta(name: str = Form(...), file: UploadFile = File(...)):
    try:
        content = await file.read(MAX_FILE_SIZE + 1)
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail="File too large"
            )
        try:
            fasta_text = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid text encoding",
            )

        sequences = parse_fasta(fasta_text)
        data = ExperimentCreate(name=name, sequences=sequences)
        return experiment_service.create_experiment(data)

    finally:
        await file.close()
