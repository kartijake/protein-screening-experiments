# Sample test inputs

Fixtures are grouped first by input method and then by expected outcome. Add new
cases to the matching `valid` or `invalid` directory and name each file after
the single criterion it exercises.

```text
sample/
  fasta/
    valid/
    invalid/
  manual/
    valid/
    invalid/
```

## Manual text inputs

Each text file contains a `Name:` value for the experiment-name field and a
`Sequences:` section for the manual-input field. Copy only the content after
each label into its corresponding field. The sequence section may use newlines,
commas, or both as delimiters.

### Valid

| File | Expected result |
| --- | --- |
| `manual/valid/uppercase_newline.txt` | Accepted: uppercase sequences separated by newlines |
| `manual/valid/lowercase_newline.txt` | Accepted: lowercase sequences separated by newlines and normalized to uppercase |
| `manual/valid/comma_separated.txt` | Accepted: uppercase sequences separated by commas |
| `manual/valid/sequence_length_100.txt` | Accepted: all 20 sequences are exactly 100 residues |

### Invalid

| File | Expected result |
| --- | --- |
| `manual/invalid/blank_name.txt` | Rejected: the `Name:` value is blank |
| `manual/invalid/sequence_count_19.txt` | Rejected: exactly 20 sequences are required |
| `manual/invalid/invalid_character.txt` | Rejected: a sequence contains `-` |
| `manual/invalid/sequence_length_11.txt` | Rejected: one sequence is shorter than 12 residues |
| `manual/invalid/sequence_length_101.txt` | Rejected: one sequence is longer than 100 residues |
| `manual/invalid/common_prefix_4.txt` | Rejected: shared prefix is shorter than 5 residues |
| `manual/invalid/variable_region_10.txt` | Rejected: variable region is longer than 9 residues |

## FASTA uploads

Use a non-empty experiment name when uploading these files so the fixture
criterion, rather than name validation, determines the result.

### Valid

| File | Expected result |
| --- | --- |
| `fasta/valid/minimum_boundaries.fasta` | Accepted: 20 sequences, 12 residues each, 5-residue shared prefix/suffix, and 2-residue variable region |
| `fasta/valid/multiline_lowercase.fasta` | Accepted: lowercase multiline sequences are normalized to uppercase |
| `fasta/valid/sequence_length_100.fasta` | Accepted: all 20 sequences are exactly 100 residues |

### Invalid

| File | Expected result |
| --- | --- |
| `fasta/invalid/sequence_count_19.fasta` | Rejected: exactly 20 sequences are required |
| `fasta/invalid/missing_initial_header.fasta` | Rejected: sequence data appears before a `>` header |
| `fasta/invalid/empty_sequence.fasta` | Rejected: one header has no sequence |
| `fasta/invalid/invalid_character_hyphen.fasta` | Rejected: `-` is not an accepted sequence character |
| `fasta/invalid/sequence_length_11.fasta` | Rejected: one sequence is shorter than 12 residues |
| `fasta/invalid/sequence_length_101.fasta` | Rejected: one sequence is longer than 100 residues |
| `fasta/invalid/common_prefix_4.fasta` | Rejected: shared prefix is shorter than 5 residues |
| `fasta/invalid/common_suffix_4.fasta` | Rejected: shared suffix is shorter than 5 residues |
| `fasta/invalid/variable_region_1.fasta` | Rejected: variable region is shorter than 2 residues |
| `fasta/invalid/variable_region_10.fasta` | Rejected: variable region is longer than 9 residues |
| `fasta/invalid/file_size_32769_bytes.fasta` | Rejected: file exceeds the 32 KiB limit by one byte |
| `fasta/invalid/invalid_utf8.fasta` | Rejected: file contains bytes that cannot be decoded as UTF-8 |
