# Проверка качества

В 0.1.0 измерений точности не было. Первый малый парный прогон описан в [отчёте](results/2026-10-29/README.md); улучшение не показано. `scenarios.json` проверяет ожидаемое поведение; это не отчёт о пройденных испытаниях.

## Проверка распознавания

1. Подобрать законно доступные изображения с надёжными расшифровками для 1850–1917 и 1918–1950. Указать источники и спорные участки; последние исключить из однозначного эталона. Сохранять документы одного писаря в одной группе при разделении справочного и проверочного наборов.
2. Спрятать ответы проверочного набора от читающего агента. На одинаковых изображениях, с одинаковой моделью, настройками и доступными инструментами сравнить чтение без навыка и с ним. Не использовать известные агенту семейные исправления как слепую проверку.
3. Сохранить обе исходные расшифровки до показа ответов. Посчитать ошибки по символам (CER: расстояние Левенштейна / число символов эталона), отдельно по полным именам, отчествам, фамилиям, датам и возрастам. До проверки зафиксировать правила пробелов и орфографии; сохранять также буквальные результаты.
4. Отдельно оценить долю оставленных неразборчивыми участков и уверенных ошибочных чтений: отказ от чтения не считать правильным распознаванием. Повторить на других писарях перед обобщением результата.

Указать число изображений, писарей, распределение дат и типы документов. Маленький набор показывает результат только на нём. Не объявлять улучшение по структурной проверке SKILL.md, отдельному удачному примеру или числу добавленных инструкций.

Приватные изображения и ответы хранятся в существующем деле вне этого checkout; публикация требует отдельного разрешения. Обезличивание текста само по себе не разрешает публикацию скана.

## Scoring contract (development version)

Freeze literal outputs before revealing keys. Use NFC Unicode and LF line endings;
otherwise preserve case, punctuation, line breaks, spaces and pre-reform spelling.
No transliteration, lowercasing or silent modernization. Aggregate CER is total
Levenshtein edits divided by total reference characters, not the mean of case CERs.
`[неразб.]` remains in the literal prediction and costs edits; it is not a free pass.

After outputs are frozen, an evaluator aligns entity fields and annotates the number
of reference characters covered by explicit abstentions. Do not estimate that number
from the length of the printed `[неразб.]` marker. If an uncertain character has no
reliable key, exclude that span from both scored texts and record the exclusion in
the run report. Do not include unsupported reference characters in the denominator.

Run `python3 scripts/score_eval.py /path/to/frozen-scored-run.json`.
The scorer accepts `{ "cases": [...] }`; each case contains:

```json
{
  "id": "document-region",
  "reference": "20",
  "prediction": "30",
  "illegible_reference_characters": 0,
  "entities": [
    {"type": "age", "reference": "20", "prediction": "30", "confident": true}
  ]
}
```

Entity types: `given_name`, `patronymic`, `surname`, `date`, `age`.
Confidence is an explicit run annotation, not inferred from plausible wording.
Entity exact accuracy includes abstentions as errors. Confident error rate is wrong
confident entity predictions / all confident entity predictions; a zero denominator
is `null`, not zero. Report counts alongside rates. This metric does not cover every
confident wrong letter in prose; a human-reviewed span audit is needed for that claim.

For every paired run record model identifier (or disclose unavailable), settings,
tool access, prompts, time, source IDs, document/hand groups, skill commit, available
reference material, raw output paths/checksums, exclusions and evaluator identity.
Run both conditions in fresh contexts with identical tools and images; only the
skill condition receives the skill and its permitted references. Do not expose keys
or the other condition's output. A public literary quotation may have appeared in
pretraining; report that contamination risk even with correct experimental splitting.

Unit tests verify metric arithmetic and integrity checks only. The first paired comparison is reported in [the frozen run](results/2026-10-29/README.md);
it does not demonstrate an improvement.

Completed run keys may be published with their results, after retirement from blind use. Future readers must receive neither those keys nor same-document/hand references.

## Private target-corpus comparison

Keep private images, keys, writer profiles, crops and raw answers outside the public checkout. Use fresh readers with identical images, requests, model selection and available tools. Freeze candidate, keys and document-level splits before reading. Same-hand independence must be established or explicitly left unknown. Give the baseline the same optional local engine; the skill condition changes instructions, not tool access.

`python3 scripts/score_reading.py KEYS_JSON RUN_JSON --output LOCAL_SCORE_JSON` compares separately held human keys with exact saved responses. `--details` includes private text and is for local use only. Missing readings count as deletions. Confidence and unreadable metadata are separate from recognized text. Main content CER normalizes NFC, whitespace, historical і/ѣ/ѳ and ё, and terminal word hard signs. Literal CER uses only explicitly adjudicated literal keys. Whole-field abstention share does not measure internal unmarked gaps. Report given names, patronymics, surnames, dates and ages separately, including confident errors.

Repetitions characterize variation on the same documents; they do not increase the independent corpus size. A consumed holdout becomes regression material for later candidates. Preserve failures and disclose any post-result key adjudication equally for both conditions. An aggregate result cannot establish a generally reliable transcription system. See `results/2026-10-30-target-local-htr/summary.json` for the current limited target experiment.
