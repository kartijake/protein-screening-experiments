
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, StrictStr, field_validator


AminoAcidSequence = Annotated[
    StrictStr,
    Field(
        min_length=12,
        max_length=100,
        pattern=r"^[A-Z]+$",
    ),
]


class ExperimentCreate(BaseModel):
    name: str

    sequences: list[AminoAcidSequence] = Field(
        min_length=20,
        max_length=20,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        name = value.strip()

        if not name:
            raise ValueError("Experiment name is required")

        return name


class Experiment(BaseModel):
    id: UUID
    name: str
    sequences: list[str]
    created_at: datetime
