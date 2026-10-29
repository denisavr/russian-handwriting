# Reference library

Records in `records/` use [sample format v1](../references/sample-format.md).
Full page images in `pages/` preserve context; each record identifies a pixel region on
that exact page. A record's checksum identifies the downloaded derivative, not the
institution's master scan. Copybooks model prescribed writing, not natural handwriting.

`provisional` means a proposed reading that must not serve as a verified answer.
`verified` requires a recorded check against an independently published transcription
or an explicitly identified human review. Two model passes are not human verification.
Unknown writers stay `null`; document IDs still keep their examples together.

Use `python3 scripts/validate_samples.py` from the repository root for inventory and
structural checks. These checks cannot establish reading accuracy or legal status.
No private documents belong here. Evaluation answers are held outside this library.

## Current coverage (2026-10-29)

Three records from two documents: two 1860 copybook regions (four repeated `я`
forms and five lines of prose) and one 1880 editorial-letter salutation. All three regions, including the full five-line passage, were **visually verified
by denisavr** on 2026-10-29. No writer identity has been independently
attributed. Review does not verify the rest of either page. Four full-page images
are retained, including one untranscribed pen-stroke exercise. No reference coverage
of 1918–1950, registers, revision lists, natural multi-line prose, names or ages has
been established. The separate register evaluation is not a reference-library entry.
This is a starting library, not a representative corpus.
