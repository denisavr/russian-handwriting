#!/usr/bin/env python3
"""Score a completed reading run after its outputs have been frozen.

Input JSON: {cases:[{id, reference, prediction, entities:[{type,reference,
prediction,confident}], illegible_reference_characters}]}.
Entity alignment and abstention span lengths are annotated by the evaluator.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import unicodedata


def canonical(text):
    # Preserve spelling, punctuation, case and all internal whitespace.
    return unicodedata.normalize('NFC', text.replace('\r\n', '\n').replace('\r', '\n'))


def distance(a, b):
    row = list(range(len(b) + 1))
    for i, ac in enumerate(a, 1):
        new = [i]
        for j, bc in enumerate(b, 1):
            new.append(min(new[-1] + 1, row[j] + 1, row[j-1] + (ac != bc)))
        row = new
    return row[-1]


def score(cases):
    if not cases:
        raise ValueError('empty evaluation')
    ids = set()
    edits = characters = illegible = 0
    confident_cases = confident_case_errors = 0
    entities = defaultdict(lambda: {'total':0, 'correct':0, 'confident':0, 'confident_errors':0})
    per_case = []
    for case in cases:
        if case['id'] in ids:
            raise ValueError('duplicate case ID')
        ids.add(case['id'])
        ref, pred = canonical(case['reference']), canonical(case['prediction'])
        if not ref:
            raise ValueError('empty reference')
        confidence = case.get('confident')
        if confidence is not None and type(confidence) is not bool:
            raise ValueError('case confidence must be a boolean or absent')
        confident_cases += confidence is True
        confident_case_errors += confidence is True and ref != pred
        unknown = case['illegible_reference_characters']
        if type(unknown) is not int or not 0 <= unknown <= len(ref):
            raise ValueError('invalid evaluator-annotated illegible span length')
        error = distance(ref, pred)
        edits += error
        characters += len(ref)
        illegible += unknown
        per_case.append({'id':case['id'], 'edits':error, 'reference_characters':len(ref), 'cer':error/len(ref)})
        for entity in case['entities']:
            kind = entity['type']
            if kind not in ('given_name','patronymic','surname','date','age'):
                raise ValueError('unknown entity type')
            if type(entity['confident']) is not bool or not entity['reference']:
                raise ValueError('entity needs reference and explicit boolean confidence')
            item = entities[kind]
            correct = canonical(entity['reference']) == canonical(entity['prediction'])
            item['total'] += 1
            item['correct'] += correct
            item['confident'] += entity['confident']
            item['confident_errors'] += entity['confident'] and not correct
    for item in entities.values():
        item['exact_accuracy'] = item['correct']/item['total']
        item['confident_error_rate'] = item['confident_errors']/item['confident'] if item['confident'] else None
    return {'cases':len(cases),'reference_characters':characters, 'edits':edits,
            'cer':edits/characters, 'confident_cases':confident_cases,
            'confident_case_errors':confident_case_errors,
            'confident_case_error_rate':confident_case_errors/confident_cases if confident_cases else None,
            'illegible_reference_characters':illegible,
            'illegible_share':illegible/characters, 'entities':dict(entities), 'per_case':per_case}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    args = parser.parse_args()
    print(json.dumps(score(json.loads(args.run.read_text(encoding='utf-8'))['cases']), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
