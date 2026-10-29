# Third-party notices

## Packaging reference

[ex-USSR Kinship Research](https://github.com/DenisSergeevitch/ex-ussr-kinship-research), Copyright (c) 2026 Denis Shiryaev, uses the MIT License. Its repository layout and presentation were examined as a reference. No source code, reference text, cover artwork or research records were copied into this initial draft. This project is not affiliated with or endorsed by that author.

If substantive material is reused later, preserve its applicable copyright and permission notice alongside the reused material.

## External sources

Links in `references/sources.md` do not sublicense the linked materials. No third-party scans, handwriting datasets, model weights or historical manuals are bundled in version 0.1.0. Availability on a public website does not establish permission to redistribute it.

For each future bundled item record the original URL, author/holding institution, date, identifier/page, applicable license or public-domain basis, required attribution and modifications. Keep restricted items outside the repository and link to their lawful source.

The root MIT License applies to the project's original instructions, documentation and code, not automatically to outside images, datasets or models.

## Development library added after 0.1.0

- `samples/pages/copybook-1860-p03.jpg` , `copybook-1860-p06.jpg` and `copybook-1860-p11.jpg`:
  *Прописи для скорописного почерка*, unknown author, second corrected edition,
  published by Лермонтов и К°, Saint Petersburg, 1860. National Library of Russia,
  НЭБ identifier `000200_000018_RU_NLR_BIBL_A_010983729`.
  [Commons source and rights](https://commons.wikimedia.org/wiki/File:Прописи_для_скорописного_почерка,_1860.pdf),
  revision 1247287690, checked 2026-10-29, marks PD-RusEmpire and US expired copyright.
  Downloaded 1920px JPEG derivatives of PDF pages 3, 6 and 11; no image modifications.
  Page 3 is a contextual pen-stroke exercise, not a transcribed sample.
- `samples/pages/strekoza-1880-letter.jpg`: letter from the editorial office of
  *Стрекоза* to Anton Chekhov, 20 January 1880. Commons attributes the author to
  И. Василевский; the hand has not been independently attributed by this project.
  [Commons source and rights](https://commons.wikimedia.org/wiki/File:Letter_to_Chekhov_from_Strekoza_1880.jpg),
  revision 1034486044, checked 2026-10-29, marks public domain, PD-RusEmpire and
  US expired copyright. Commons uploader Ctac, 2019; original reproduction linked
  there to apchekhov.ru. Original 730×887 JPEG retained unchanged.

These historical images are distributed on the cited public-domain bases, separately
from the MIT-licensed project code and documentation. All three recorded regions were visually verified by repository maintainer denisavr
on 2026-10-29; that review covers only their literal text, not entire source pages. Rights metadata describes the sources' stated bases, not a universal
legal determination for every jurisdiction.

The current review status of the prose region on PDF page 11 is recorded separately in its sample JSON.

## Optional local historical-line recognizer

The optional helper loads external model weights from `achimrabus/crnn-ctc-russian`,
revision `ebb5fc91eb44f40f049bafd74bc95f7c0e2b1ee8`, curated by Achim Rabus.
Model card: https://huggingface.co/achimrabus/crnn-ctc-russian
The model card identifies the weights as Apache-2.0. Weights, training data and
Python runtime dependencies are not bundled. The inference helper implements the
CNN/BiLSTM/CTC architecture described by Puigcerver (2017):
https://www.jpuigcerver.net/pubs/jpuigcerver_icdar2017.pdf

Model probabilities are not calibrated probabilities of a correct archival reading.
Validation numbers from its model card are not measurements on the user's corpus.
