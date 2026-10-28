import pytest

from backend.services.sequence_validator import (
    SequenceValidator,
    SequenceValidationError,
)
import math

@pytest.fixture
def validator():
    return SequenceValidator()


def make_sequences(
    prefix="AAAAA",
    suffix="GGGGG",
    variable_a="CD",
    variable_b="EF",
):
    """Generate 20 sequences with two variable regions."""
    return [
        prefix + (variable_a if i % 2 == 0 else variable_b) + suffix for i in range(20)
    ]


# All valid examples
@pytest.mark.parametrize("variable_length", [2, 5, 9])
def test_valid_variable_lengths(validator, variable_length):
    sequences = make_sequences(
        variable_a="C" * variable_length,
        variable_b="D" * variable_length,
    )

    assert validator.validate(sequences) is None


def test_valid_100_amino_acid_sequences(validator):
    sequences = make_sequences(
        prefix="A" * 86,
        suffix="G" * 5,
        variable_a="C" * 9,
        variable_b="D" * 9,
    )

    assert all(len(seq) == 100 for seq in sequences)
    assert validator.validate(sequences) is None


def test_valid_different_sequence_lengths(validator):
    sequences = make_sequences(
        variable_a="CD",
        variable_b="EFGHI",
    )

    assert validator.validate(sequences) is None


# Sequence count validation
@pytest.mark.parametrize("count", [0, 1, 19, 21])
def test_invalid_sequence_count(validator, count):
    sequences = make_sequences()[:count]

    if count == 21:
        sequences.append("AAAAACDGGGGG")

    with pytest.raises(
        SequenceValidationError,
        match="exactly 20 sequences",
    ):
        validator.validate(sequences)


# Individual sequence validation
@pytest.mark.parametrize(
    "invalid_sequence",
    [
        "",
        "AAAAA123GGGGG",
        "AAAAA-CDGGGGG",
        "AAAAA CDGGGGG",
        "aaaaacdggggg",
        None,
        123,
    ],
)
def test_invalid_sequence_content(validator, invalid_sequence):
    sequences = make_sequences()
    sequences[0] = invalid_sequence

    with pytest.raises(SequenceValidationError):
        validator.validate(sequences)

@pytest.mark.parametrize(
    "invalid_value",
    [
        # Boolean values
        True,
        False,

        # Boolean-like strings
        "True",
        "False",
        "true",
        "false",
        "TRUE",
        "FALSE",

        # Numbers
        0,
        1,
        -1,
        100,
        3.14,
        -3.14,

        # Special floating-point values
        float("inf"),
        float("-inf"),
        float("nan"),
        math.inf,
        -math.inf,
        math.nan,

        # Special floating-point strings
        "inf",
        "-inf",
        "+inf",
        "Infinity",
        "-Infinity",
        "NaN",
        "nan",

        # Empty and whitespace strings
        "",
        " ",
        "   ",
        "\n",
        "\t",

        # Other Python types
        None,
        [],
        {},
        (),
        set(),
        b"AAAAACDGGGGG",

        # Special characters
        "AAAAA@CDGGGGG",
        "AAAAA#CDGGGGG",
        "AAAAA!CDGGGGG",
        "AAAAA-CDGGGGG",
        "AAAAA_CDGGGGG",
        "AAAAA CDGGGGG",
        "AAAAA123GGGGG",

        # Non-ASCII letters
        "AAAAAéCDGGGGG",
        "AAAAAαCDGGGGG",

        # Lowercase amino acids
        "aaaaacdggggg",
        "AAAAAcdGGGGG",
    ],
)
def test_invalid_sequence_types_and_values(
    validator, invalid_value
):
    sequences = make_sequences()
    sequences[0] = invalid_value

    with pytest.raises(SequenceValidationError):
        validator.validate(sequences)

@pytest.mark.parametrize(
    "invalid_sequence",
    [
        "AAAAA-INGGGGG",
        "AAAAA123GGGGG",
        "AAAAAÉFGGGGG",
        "AAAAA😀FGGGGG",
    ],
)
def test_invalid_amino_acid_codes(
    validator, invalid_sequence
):
    sequences = make_sequences()
    sequences[0] = invalid_sequence

    with pytest.raises(SequenceValidationError):
        validator.validate(sequences)

def test_sequence_too_short(validator):
    sequences = make_sequences()
    sequences[0] = "ACDEFGHIKLM"  # 11 amino acids

    with pytest.raises(
        SequenceValidationError,
        match="between 12 and 100",
    ):
        validator.validate(sequences)


def test_sequence_too_long(validator):
    sequences = make_sequences()
    sequences[0] = "A" * 101

    with pytest.raises(
        SequenceValidationError,
        match="between 12 and 100",
    ):
        validator.validate(sequences)


# Common prefix validation
def test_prefix_less_than_five(validator):
    sequences = make_sequences(
        prefix="AAAA",
        variable_a="CDE",
        variable_b="FGH",
        suffix="GGGGG",
    )

    with pytest.raises(
        SequenceValidationError,
        match="at least 5.*beginning",
    ):
        validator.validate(sequences)


def test_prefix_exactly_five(validator):
    sequences = make_sequences(prefix="AAAAA")

    assert validator.validate(sequences) is None


# Common suffix validation
def test_suffix_less_than_five(validator):
    sequences = make_sequences(
        prefix="AAAAA",
        variable_a="CDE",
        variable_b="FGH",
        suffix="GGGG",
    )

    with pytest.raises(
        SequenceValidationError,
        match="at least 5.*end",
    ):
        validator.validate(sequences)


def test_suffix_exactly_five(validator):
    sequences = make_sequences(suffix="GGGGG")

    assert validator.validate(sequences) is None


# -----------------------------
# Variable region validation
# -----------------------------


def test_variable_region_too_short(validator):
    sequences = make_sequences(
        prefix="AAAAAA",
        variable_a="C",
        variable_b="D",
    )

    with pytest.raises(
        SequenceValidationError,
        match="between the longest common prefix and suffix",
    ):
        validator.validate(sequences)


def test_variable_region_too_long(validator):
    sequences = make_sequences(
        variable_a="C" * 10,
        variable_b="D" * 10,
    )

    with pytest.raises(
        SequenceValidationError,
        match="between the longest common prefix and suffix",
    ):
        validator.validate(sequences)


# -----------------------------
# Helper method tests
# -----------------------------


def test_common_prefix_length():
    sequences = make_sequences(prefix="AAAAAAA")

    result = SequenceValidator._common_prefix_length(sequences)

    assert result == 7


def test_common_suffix_length():
    sequences = make_sequences(suffix="GGGGGG")

    result = SequenceValidator._common_suffix_length(
        sequences,
        prefix_length=5,
    )

    assert result == 6


def test_identical_sequences_rejected(validator):
    sequences = ["AAAAACDGGGGG"] * 20

    with pytest.raises(SequenceValidationError):
        validator.validate(sequences)
