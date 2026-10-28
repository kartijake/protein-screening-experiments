
from dataclasses import dataclass


class SequenceValidationError(ValueError):
    """Raised when an experiment fails sequence design rules."""

class SequenceValidator:
    ALLOWED_CODES = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    REQUIRED_COUNT = 20
    MIN_SEQUENCE_LENGTH = 12
    MAX_SEQUENCE_LENGTH = 100

    MIN_COMMON_LENGTH = 5
    MIN_VARIABLE_LENGTH = 2
    MAX_VARIABLE_LENGTH = 9

    def validate(
        self,
        sequences: list[str],
    ) -> None:
        # 1. Validate number of sequences
        if len(sequences) != self.REQUIRED_COUNT:
            raise SequenceValidationError(
                f"An experiment requires exactly "
                f"{self.REQUIRED_COUNT} sequences"
            )

        # 2. Validate individual sequences
        for index, sequence in enumerate(sequences, start=1):
            if not isinstance(sequence, str) or not sequence.isalpha():
                raise SequenceValidationError(
                    f"Sequence {index} must be a string"
                )

            if not (
                self.MIN_SEQUENCE_LENGTH
                <= len(sequence)
                <= self.MAX_SEQUENCE_LENGTH
            ):
                raise SequenceValidationError(
                    f"Sequence {index} must contain between "
                    f"{self.MIN_SEQUENCE_LENGTH} and "
                    f"{self.MAX_SEQUENCE_LENGTH} amino acids. "
                    f"Received {len(sequence)}."
                )

            if any(
                code not in self.ALLOWED_CODES
                for code in sequence
            ):
                raise SequenceValidationError(
                    f"Sequence {index} contains invalid amino acid codes"
                )

        # 3. Find longest common prefix
        prefix_length = self._common_prefix_length(sequences)

        if prefix_length < self.MIN_COMMON_LENGTH:
            raise SequenceValidationError(
                "Sequences must share at least 5 "
                "amino acids at the beginning"
            )

        # 4. Find longest common suffix without prefix overlap
        suffix_length = self._common_suffix_length(
            sequences,
            prefix_length,
        )

        if suffix_length < self.MIN_COMMON_LENGTH:
            raise SequenceValidationError(
                "Sequences must share at least 5 "
                "amino acids at the end"
            )

        # 5. Calculate variable region lengths
        variable_lengths = [
            len(sequence) - prefix_length - suffix_length
            for sequence in sequences
        ]

        # 6. Validate variable regions
        for index, length in enumerate(variable_lengths, start=1):
            if not (
                self.MIN_VARIABLE_LENGTH
                <= length
                <= self.MAX_VARIABLE_LENGTH
            ):
                raise SequenceValidationError(
                    f"Sequence {index} has {length} amino acids "
                    "between the longest common prefix and suffix. "
                    f"Expected between {self.MIN_VARIABLE_LENGTH} "
                    f"and {self.MAX_VARIABLE_LENGTH}."
                )



    @staticmethod
    def _common_prefix_length(sequences: list[str]) -> int:
        """Find the longest prefix shared by all sequences."""
        shortest_length = min(len(seq) for seq in sequences)

        for index in range(shortest_length):
            character = sequences[0][index]

            if any(
                seq[index] != character
                for seq in sequences[1:]
            ):
                return index

        return shortest_length

    @staticmethod
    def _common_suffix_length(
        sequences: list[str],
        prefix_length: int,
    ) -> int:
        """Find the longest shared suffix without prefix overlap."""
        shortest_length = min(len(seq) for seq in sequences)
        remaining_length = shortest_length - prefix_length

        for offset in range(1, remaining_length + 1):
            character = sequences[0][-offset]

            if any(
                seq[-offset] != character
                for seq in sequences[1:]
            ):
                return offset - 1

        return remaining_length
