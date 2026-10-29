# Sample format v1

One UTF-8 JSON record per sample in `samples/records/<id>.json`.
No maximum transcription length. Keep line breaks and visible historical characters.
Coordinates identify the original page derivative, before any crop or enlargement.

| Field | Meaning |
|---|---|
| `schema_version` | Integer `1` |
| `id` | Stable unique filename stem |
| `kind` | `copybook` or `manuscript` |
| `document_id` | Stable source document grouping; all its regions stay in one split |
| `writer_id` | Stable identified hand, or `null`; never infer a writer from author alone |
| `date` | `{from: year, to: year, basis: explanation}` |
| `document_type` | Concrete type of source |
| `source` | `url`, `title`, `holding_institution`, `page`; archive identifier where available |
| `image` | Repository-relative full-page `path`, `sha256`, `width`, `height` |
| `region` | `units: pixels`, `xywh: [x,y,width,height]`, top-left origin |
| `transcription` | `literal`, optional `modern`, and `provenance` of the reading |
| `review` | `status: provisional/verified`, `reviewer`, ISO `date`, `method` |
| `uncertainties` | Array of unresolved spans, alternatives and visual grounds; empty if none |
| `rights` | `status`, `basis_url`, `attribution`, `modifications` |
| `split` | `reference` for this public library |

A verified reading needs independent published transcription or named human review.
A model's visual transcription may be useful as a provisional worked example but is
not an independent answer key. If a source transcription normalizes spelling, record
that difference and check literal details against the image.

Store private writer profiles beside the user's own case files, outside this checkout.
A profile can link hand-specific examples, locations, uncertain forms and user corrections;
do not publish it automatically. Reuse an existing case log rather than creating a competing one.

Evaluation material must be grouped by both document and known writer; overlapping
groups are joined before assigning splits. Unknown hands from one collection must not
be claimed writer-independent. Keep answer keys outside the reading agents' accessible
workspace and do not expose reference records from evaluation documents.
