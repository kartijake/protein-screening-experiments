from fastapi import HTTPException, status
from backend.schemas.experiment import AminoAcidSequence

ALLOWED_CODES = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def parse_fasta(content: str) -> list[AminoAcidSequence]:
    sequences = []
    current_sequence = None

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith(">"):
            header = line[1:]

            if not 1 <= len(header) <= 100:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Invalid FASTA header length",
                )

            if current_sequence is not None:
                sequences.append(current_sequence)

            current_sequence = ""

        else:
            if current_sequence is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Invalid FASTA structure",
                )

            sequence = line.upper()

            if not set(sequence).issubset(ALLOWED_CODES):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Invalid amino acid characters",
                )

            current_sequence += sequence

            if len(current_sequence) > 100:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Sequence exceeds 100 amino acids",
                )

    if current_sequence is not None:
        sequences.append(current_sequence)

    if len(sequences) != 20:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Exactly 20 sequences required",
        )

    if any(not sequence for sequence in sequences):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Empty sequences are not allowed",
        )
    for index, sequence in enumerate(sequences, start=1):
        if len(sequence) < 12:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    f"Sequence {index} must contain at least "
                    "12 amino acids"
                ),
            )


    return sequences
