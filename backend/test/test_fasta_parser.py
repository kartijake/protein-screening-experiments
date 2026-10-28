
import pytest
from fastapi import HTTPException, status
from backend.services.fasta_parser import parse_fasta


@pytest.fixture
def valid_fasta():
    """Generate a valid FASTA document containing 20 sequences."""
    return "\n".join(
        f">SEQUENCE_{i}\nAAAAACDGGGGG"
        for i in range(1, 21)
    )


# Successful parsing
def test_valid_fasta(valid_fasta):
    result = parse_fasta(valid_fasta)

    assert len(result) == 20
    assert all(seq == "AAAAACDGGGGG" for seq in result)


def test_lowercase_sequences():
    content = "\n".join(
        f">SEQUENCE_{i}\naaaaacdggggg"
        for i in range(1, 21)
    )

    result = parse_fasta(content)

    assert all(seq == "AAAAACDGGGGG" for seq in result)


def test_multiline_sequences():
    content = "\n".join(
        f">SEQUENCE_{i}\nAAAAA\nCD\nGGGGG"
        for i in range(1, 21)
    )

    result = parse_fasta(content)

    assert len(result) == 20
    assert all(seq == "AAAAACDGGGGG" for seq in result)


def test_blank_lines(valid_fasta):
    content = valid_fasta.replace("\n", "\n\n")

    result = parse_fasta(content)

    assert len(result) == 20


def test_windows_line_endings(valid_fasta):
    content = valid_fasta.replace("\n", "\r\n")

    result = parse_fasta(content)

    assert len(result) == 20


def test_maximum_header_length():
    content = "\n".join(
        f">{'H' * 100}\nAAAAACDGGGGG"
        for _ in range(20)
    )

    result = parse_fasta(content)

    assert len(result) == 20


def test_maximum_sequence_length():
    content = "\n".join(
        f">SEQUENCE_{i}\n{'A' * 100}"
        for i in range(1, 21)
    )

    result = parse_fasta(content)

    assert len(result) == 20
    assert all(len(seq) == 100 for seq in result)


# Invalid sequence count
@pytest.mark.parametrize("count", [0, 1, 19, 21])
def test_invalid_sequence_count(count):
    content = "\n".join(
        f">SEQUENCE_{i}\nAAAAACDGGGGG"
        for i in range(1, count + 1)
    )

    with pytest.raises(
        HTTPException,
        match="Exactly 20 sequences required",
    ) as exc:
        parse_fasta(content)

    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# Invalid FASTA headers
@pytest.mark.parametrize(
    "header",
    [
        "",
        "H" * 101,
    ],
)
def test_invalid_header_length(header):
    content = "\n".join(
        f">{header}\nAAAAACDGGGGG"
        for _ in range(20)
    )

    with pytest.raises(
        HTTPException,
        match="Invalid FASTA header length",
    ) as exc:
        parse_fasta(content)

    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_legacy_semicolon_header_rejected():
    content = ";LCBO - Prolactin precursor - Bovine\nMDSKGSSQ"

    with pytest.raises(
        HTTPException,
        match="Invalid FASTA structure",
    ):
        parse_fasta(content)

def test_missing_initial_header():
    content = "AAAAACDGGGGG\n>SEQUENCE_1\nAAAAACDGGGGG"

    with pytest.raises(
        HTTPException,
        match="Invalid FASTA structure",
    ):
        parse_fasta(content)


# Invalid amino acid characters
@pytest.mark.parametrize(
    "invalid_sequence",
    [
        "AAAAA123GGGGG",
        "AAAAA-CDGGGGG",
        "AAAAA_CDGGGGG",
        "AAAAA@CDGGGGG",
        "AAAAA😀DGGGGG",
        "AAAAAÉDGGGGG",
        "AAAAA CDGGGGG",
        "AAAAA\tCDGGGGG",
    ],
)
def test_invalid_amino_acid_characters(invalid_sequence):
    content = "\n".join(
        f">SEQUENCE_{i}\n{invalid_sequence}"
        for i in range(1, 21)
    )

    with pytest.raises(
        HTTPException,
        match="Invalid amino acid characters",
    ) as exc:
        parse_fasta(content)

    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# Sequence length validation
def test_sequence_exceeds_100():
    content = "\n".join(
        f">SEQUENCE_{i}\n{'A' * 101}"
        for i in range(1, 21)
    )

    with pytest.raises(
        HTTPException,
        match="Sequence exceeds 100 amino acids",
    ) as exc:
        parse_fasta(content)

    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_multiline_sequence_exceeds_100():
    content = "\n".join(
        f">SEQUENCE_{i}\n{'A' * 60}\n{'C' * 41}"
        for i in range(1, 21)
    )

    with pytest.raises(
        HTTPException,
        match="Sequence exceeds 100 amino acids",
    ):
        parse_fasta(content)


# Empty sequences
def test_empty_sequence():
    content = "\n".join(
        f">SEQUENCE_{i}\n"
        for i in range(1, 21)
    )

    with pytest.raises(
        HTTPException,
        match="Empty sequences are not allowed",
    ) as exc:
        parse_fasta(content)

    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
