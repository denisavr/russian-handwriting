# Russian Handwriting

Languages: [English](README.md) / [Русский](README.ru.md)

A skill for reading and transcribing Russian handwriting across historical periods, for Codex and other AI agents.

The first development and evaluation stage covers **1850–1950**: parish registers, revision lists, civil records, letters and administrative documents. Coverage will expand with dated examples and evaluations; universal scope does not imply validated accuracy for every period.

**Version 0.2.0 — working reading skill with a small reviewed reference library. A first paired pilot did not demonstrate recognition improvement.** This is not a trained handwriting model or a completed reference atlas.

## What it does

- Compares letterforms and joins in the same writer's hand.
- Keeps literal transcription separate from modern spelling and interpretation.
- Shows meaningful uncertainties instead of silently completing names from context.
- Requests a contextual image reading from the user when an important ambiguity remains.
- Preserves corrections and withdrawn readings without promoting guesses to facts.

## Install and use

Clone the repository into your agent's skills directory:

```sh
git clone https://github.com/denisavr/russian-handwriting.git ~/.codex/skills/russian-handwriting
```

For other Agent Skills runtimes, place this folder in the runtime's supported skills directory. Installation does not retrain the model.

Ask: “Use $russian-handwriting to read this record. Compare the uncertain patronymic with the same writer's letters on adjacent lines.” Image viewing must be available. The skill does not download models or send images to external recognition services.

## Repository layout

```text
SKILL.md                      Core reading workflow, written in Russian
references/reading-method.md  Comparison and transcription conventions
references/sources.md         Source shortlist and access limitations
references/changelog.md       Version history
evals/README.md               Blind evaluation procedure and current status
evals/scenarios.json          Behavioral checks, not measured recognition results
samples/                     Reviewed images, regions and source records
scripts/                     Standard-library validation and scoring tools
THIRD_PARTY_NOTICES.md        Attribution and separate rights for source materials
LICENSE                      MIT for original project materials
```

## Contributing

Contribute dated, attributable examples with reliable transcriptions and explicit redistribution rights. Keep private case images, family histories and active evaluation answer keys outside reading agents' accessible inputs. Published completed runs are retired from blind reuse. Disputed readings are not reference answers.

## License

[MIT](LICENSE) © 2026 denisavr. External images, datasets, publications and models retain their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).

Packaging was informed by [ex-USSR Kinship Research](https://github.com/DenisSergeevitch/ex-ussr-kinship-research). This is a separate project, not an endorsed extension.

## Development library

See [sample inventory and evidence limits](samples/README.md), [record format](references/sample-format.md) and [scoring procedure](evals/README.md). The library contains three maintainer-reviewed records, including five lines of copybook prose. Run `python3 scripts/validate_samples.py` for structural inventory. The [first paired pilot](evals/results/2026-10-29/README.md) covers only seven strings/fields and shows no improvement.

## Try the bundled example

Attach `samples/pages/strekoza-1880-letter.jpg` and ask the skill to transcribe only the salutation in the middle of the page. The maintainer-reviewed reading is **«Милостивый Государь!»**. The record preserves its source page, region, rights and review status; the rest of the letter has not been verified here.

Python 3.9+ runs the optional validation/scoring helpers without third-party packages. Image viewing belongs to the host agent. Reload the agent's skill list or start a fresh session after installation if needed.
