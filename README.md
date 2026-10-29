# Russian Handwriting

Languages: [English](README.md) / [Русский](README.ru.md)

A skill for reading and transcribing Russian handwriting across historical periods, for Codex and other AI agents.

The first development and evaluation stage covers **1850–1950**: parish registers, revision lists, civil records, letters and administrative documents. Coverage will expand with dated examples and evaluations; universal scope does not imply validated accuracy for every period.

**Version 0.1.0 — initial workflow draft. Recognition improvement has not been measured.** This is not a trained handwriting model or a completed reference atlas.

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
THIRD_PARTY_NOTICES.md        Attribution and separate rights for source materials
LICENSE                      MIT for original project materials
```

## Contributing

Contribute dated, attributable examples with reliable transcriptions and explicit redistribution rights. Keep private case images, family histories and evaluation answer keys outside this checkout. Disputed readings are not reference answers.

## License

[MIT](LICENSE) © 2026 denisavr. External images, datasets, publications and models retain their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).

Packaging was informed by [ex-USSR Kinship Research](https://github.com/DenisSergeevitch/ex-ussr-kinship-research). This is a separate project, not an endorsed extension.
