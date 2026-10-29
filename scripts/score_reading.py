#!/usr/bin/env python3
"""Compare private reading fields with separately held human keys.

Unlike the archived raw-output scorer, this separates uncertainty syntax from
recognized content. Output is aggregate-only unless --details is requested.
No corpus or answer key is bundled with this tool.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import unicodedata
from score_eval import distance


def content(text, modern=False):
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'\[(?:неразб\.?|нрзб\.?|illegible|…|\.{3})\]', '', text, flags=re.I)
    text = re.sub(r'\[([^\[\]]+)\?\]', r'\1', text)
    if modern:
        text = text.translate(str.maketrans({'і':'и','І':'И','ѣ':'е','Ѣ':'Е','ѳ':'ф','Ѳ':'Ф','ё':'е','Ё':'Е'}))
        text = re.sub(r'[ъЪ](?=\W|$)', '', text)
    return ' '.join(text.split())


def compare(keys, run, details=False):
    refs = keys['cases']
    predictions = run['fields']
    if not refs:
        raise ValueError('empty reference set')
    expected = {r['id'] for r in refs}
    if len(expected) != len(refs):
        raise ValueError('duplicate reference ID')
    by_id = {}
    for p in predictions:
        if p['id'] not in expected or p['id'] in by_id:
            raise ValueError('unknown or duplicate prediction ID')
        if not isinstance(p['text'], str) or p['confidence'] not in ('high','low') or type(p['unreadable']) is not bool:
            raise ValueError('invalid prediction structure')
        if p['unreadable'] and p['text']:
            raise ValueError('whole-field abstention must have empty text; annotate partial spans separately')
        by_id[p['id']] = p
    exclusions=[dict(id=r['id'],reason=r.get('exclusion_reason','not adjudicated')) for r in refs if not r.get('scored',True)]
    refs=[r for r in refs if r.get('scored',True)]
    if not refs:
        raise ValueError('no adjudicated reference fields')
    summary = dict(fields=len(refs), correct=0, reference_characters=0, edits=0,
                   literal_reference_characters=0, literal_edits=0, confident=0,
                   confident_errors=0, uncertain_correct=0, abstained_fields=0,
                   abstained_reference_characters=0)
    categories = defaultdict(lambda:dict(total=0,correct=0,confident=0,confident_errors=0))
    rows=[]
    for ref in refs:
        p = by_id.get(ref['id'],dict(id=ref['id'],text='',confidence='low',unreadable=True))
        if not isinstance(ref['reference'], str) or not ref['reference']:
            raise ValueError('reference text required')
        a,b = content(ref['reference'],True),content(p['text'],True)
        la,lb = content(ref['reference']),content(p['text'])
        if not a:
            raise ValueError('reference is empty after normalization')
        edits = distance(a,b)
        correct = a == b
        high = p['confidence'] == 'high'
        summary['correct'] += correct
        summary['reference_characters'] += len(a)
        summary['edits'] += edits
        # Only explicitly diplomatic keys count toward a literal score.
        if ref.get('literal_verified',False):
            summary['literal_reference_characters'] += len(la)
            summary['literal_edits'] += distance(la,lb)
        summary['confident'] += high
        summary['confident_errors'] += high and not correct
        summary['uncertain_correct'] += not high and correct
        abstained = not b
        summary['abstained_fields'] += abstained
        summary['abstained_reference_characters'] += len(a) if abstained else 0
        cat=categories[ref['type']]
        cat['total'] += 1
        cat['correct'] += correct
        cat['confident'] += high
        cat['confident_errors'] += high and not correct
        row=dict(id=ref['id'],type=ref['type'],correct=correct,edits=edits,
                 reference_characters=len(a),confidence=p['confidence'],abstained=abstained)
        if details:row.update(reference=ref['reference'],prediction=p['text'],grounds=p.get('grounds',''))
        rows.append(row)
    summary['content_cer']=summary['edits']/summary['reference_characters']
    summary['literal_cer']=(summary['literal_edits']/summary['literal_reference_characters']
                            if summary['literal_reference_characters'] else None)
    summary['field_accuracy']=summary['correct']/summary['fields']
    summary['confident_error_rate']=(summary['confident_errors']/summary['confident'] if summary['confident'] else None)
    summary['whole_field_abstention_character_share']=summary['abstained_reference_characters']/summary['reference_characters']
    for cat in categories.values():
        cat['accuracy']=cat['correct']/cat['total']
    return dict(summary=summary,categories=dict(categories),per_field=rows,excluded_fields=exclusions,
                limits='Abstention share measures whole-field empty readings, not unannotated internal gaps. Literal CER uses only explicitly marked literal keys. Modern content normalization does not prove spelling accuracy.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('keys',type=Path)
    parser.add_argument('run',type=Path)
    parser.add_argument('--details',action='store_true',help='Include private reference/prediction text; keep output local.')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=compare(json.loads(args.keys.read_text(encoding='utf-8')),json.loads(args.run.read_text(encoding='utf-8')),args.details)
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.write_text(text,encoding='utf-8')
        print(json.dumps(result['summary'],ensure_ascii=False,indent=2))
    else:print(text,end='')


if __name__=='__main__':main()
