# First paired pilot — 2026-10-29

**No recognition improvement demonstrated.** This small trial checks feasibility and
exposes a conservative transcription failure. It is not a representative benchmark.

Seven scored regions/fields, 65 reference characters, from three documents:
1860 copybook (four letters), 1880 editorial-letter salutation, and five handwritten
fields of an 1861 marriage register (given name, patronymic, surname, age, month/day).
The two short keys were explicitly confirmed by repository maintainer denisavr.
Register keys come from the independently published diplomatic transcription beside
figure 5, printed p.94, PDF p.97 in:

И. М. Дробышевская, Б. Н. Тихомиров. «…Она славная сестра и чудесный человек»:
Варвара Михайловна Достоевская-Карепина и ее семья. *Неизвестный Достоевский*,
2024;11(2):74–120. DOI [10.15393/j10.art.2024.7261](https://doi.org/10.15393/j10.art.2024.7261).
[Source PDF](https://unknown-dostoevsky.ru/files/journals/journal_24881.pdf).
The scan is **not bundled**: redistribution rights for that reproduction have not
been established. The source has 219 PDF pages (the complete issue), not just this article.

| Metric | Without skill | With skill |
|---|---:|---:|
| Raw literal CER, including uncertainty notation | 0/65 = 0% | 6/65 = 9.23% |
| Correct scored strings | 7/7 | 6/7 |
| Given name / patronymic / surname | 1/1 each | 1/1 each |
| Age / partial date | 1/1 each | 1/1 each |
| Confident wrong fields/regions | 0/5 | 0/6 |
| Explicitly unread reference characters | 0/65 | 0/65 |

The skill condition returned `[Милостивый?] [Государь?]` for the second region,
adding uncertainty markup and omitting the exclamation mark. Thus the CER increase
is not six misrecognized source letters. All lexical readings match the keys, but
punctuation and confidence differ. Under the preregistered raw-string rule the
annotation remains in the scored output; no post-hoc normalization is substituted.
Uncertainty is not an abstention: neither condition used an unreadable-span marker
in these seven cases. Confident-case error and entity error rates cover these selected
units only, not every letter of an unseen page.

## Conditions and evidence limits

Two matched pairs of fresh agents: one pair read regions 1–2, another read the five
register fields. All inherited the same parent model/effort with no overrides.
Exact model identifier and sampling settings are not exposed by this interface.
No repeated runs, random seed, or cross-model claim. The model identity is therefore
configuration evidence, not an independently inspected API response field.

Baseline could access only the relevant images. Skill readers additionally received
a snapshot of SKILL.md and references. Its sample library was empty: **both entire
reference documents and the entire register source were withheld**, not merely keys.
No same-hand reference was available. Isolation was enforced by explicit permitted-input
instructions, not filesystem ACLs; no web or memory use was permitted. Fresh contexts
received no parent conversation or expected answers. Public examples may have appeared
in pretraining. Unknown writers are not counted as independently identified hands.

Preregistration files were saved before the corresponding reading calls. They record
keys, source, normalization and split policy. Raw register outputs preserve both literal
and modern layers; combined scored files preserve region outputs verbatim. The snapshot
hash manifest identifies instructions actually used. These materials are now retired
public examples, not secret keys suitable for a future blind run.

The full-page Chekhov feasibility trial in `../../pilot-2026-10-29.md` remains separate
and unscored because no verified literal page key was available. Its confident errors
must not be hidden by the successful short-field results here.

## Reproduce arithmetic

From the repository root:

```sh
python3 scripts/score_eval.py evals/results/2026-10-29/baseline.json
python3 scripts/score_eval.py evals/results/2026-10-29/skill.json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

This reproduces arithmetic from frozen outputs, not fresh model inference. To repeat
inference, obtain the source images lawfully, reproduce preregistered crops and prompts,
use new contexts, withhold whole source documents, and disclose unavailable model settings.

## Exact shared requests

Regions pair:

> Расшифруй два фрагмента русской рукописи. Сохрани буквы, регистр и пунктуацию;
> четыре отдельно написанные буквы первого фрагмента раздели одним пробелом.
> Если не уверен, обозначь сомнение. Верни JSON с cases: [{id: region-1, literal: текст,
> confident: true/false}, {id: region-2, literal: текст, confident: true/false}] и отдельно
> кратко объясни сомнения. confident=true только если считаешь всё чтение уверенным.
> Не добавляй переносы в начале/конце literal.

Register pair:

> По изображению актовой записи извлеки имя, отчество и фамилию жениха, его возраст,
> месяц и число брака. Верни JSON: fields: [{id: groom_given_name, text: ...,
> confident: true/false}, {id: groom_patronymic, text: ..., confident: true/false},
> {id: groom_surname, text: ..., confident: true/false}, {id: groom_age, text: ...,
> confident: true/false}, {id: marriage_month_day, text: ..., confident: true/false}].
> Имена сохраняй в исходной орфографии; соединяй слово, разделённое переносом, без
> дефиса. Возраст — только цифры. Дату запиши как название месяца с прописной буквы,
> пробел, число цифрами, без точек. Если не разобрал поле, text=[неразб.], confident=false.
> Отдельно объясни сомнения, при необходимости задай точечный вопрос и дай современную
> форму имён отдельно от исходных.
