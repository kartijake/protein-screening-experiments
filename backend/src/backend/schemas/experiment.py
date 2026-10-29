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




EXAMPLE_SEQUENCES = [
    "MKTAYIAVRNDQGSKLEA",
    "MKTAYIAFPTLWGSKLEA",
    "MKTAYIACIMHYGSKLEA",
    "MKTAYIADNRQEPGSKLEA",
    "MKTAYIATWFGVLGSKLEA",
    "MKTAYIAYHCKIMGSKLEA",
    "MKTAYIASAPLTNGSKLEA",
    "MKTAYIAQVGDRFEGSKLEA",
    "MKTAYIAWMYNPITGSKLEA",
    "MKTAYIALKHCSAVGSKLEA",
    "MKTAYIAEDRTQGNGSKLEA",
    "MKTAYIAGHSTAVCGSKLEA",
    "MKTAYIAFVIYPWMLGSKLEA",
    "MKTAYIANQTSRHKDGSKLEA",
    "MKTAYIAAGCLEVPTGSKLEA",
    "MKTAYIAMWYFQNRIGSKLEA",
    "MKTAYIADEKRHSTNQGSKLEA",
    "MKTAYIAVLIMFWYPGGSKLEA",
    "MKTAYIACASTNQGHRGSKLEA",
    "MKTAYIAPWIFYEDKVGSKLEA",
]

class ExperimentCreate(BaseModel):
    name: str

    sequences: list[AminoAcidSequence] = Field(
        min_length=20,
        max_length=20,
        examples=[EXAMPLE_SEQUENCES]
    )

    @field_validator("sequences", mode="before")
    @classmethod
    def normalize_sequences(cls, value):
        if not isinstance(value, list):
            return value

        return [
            sequence.upper() if isinstance(sequence, str) else sequence
            for sequence in value
        ]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        name = value.strip()

        if not name:
            raise ValueError("Experiment name is required")

        if len(name) > 100:
            raise ValueError("Experiment name must be 100 characters or fewer")

        return name


class Experiment(BaseModel):
    id: UUID
    name: str
    sequences: list[AminoAcidSequence] 
    created_at: datetime


class ExperimentSummary(BaseModel):
    id: UUID
    name: str
    created_at: datetime


class PaginatedExperiments(BaseModel):
    items: list[ExperimentSummary]
    total: int
    limit: int
    offset: int
