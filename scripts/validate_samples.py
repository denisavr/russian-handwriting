#!/usr/bin/env python3
"""Validate bundled records and report coverage; Python standard library only."""
import argparse
import collections
import hashlib
import datetime
import json
from pathlib import Path


def validate(root):
    errors, records = [], []
    required = {'schema_version', 'id', 'kind', 'document_id', 'writer_id', 'date',
                'document_type', 'source', 'image', 'region', 'transcription',
                'review', 'uncertainties', 'rights', 'split'}
    ids = set()
    for path in sorted((root / 'samples/records').glob('*.json')):
        try:
            r = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(r, dict):
                raise ValueError('record must be an object')
            missing = required - r.keys()
            if missing:
                raise ValueError(f'missing fields: {sorted(missing)}')
            if r['schema_version'] != 1 or r['id'] in ids:
                raise ValueError('unsupported schema or duplicate ID')
            ids.add(r['id'])
            if r['id'] != path.stem:
                raise ValueError('ID must equal filename stem')
            if r['kind'] not in ('copybook', 'manuscript'):
                raise ValueError('invalid kind')
            if r['split'] != 'reference':
                raise ValueError('bundled sample records must be reference, never evaluation answers')
            if not r['document_id'] or r['writer_id'] == '':
                raise ValueError('document ID required; unknown writer must be null')
            d = r['date']
            if not (type(d['from']) is int and type(d['to']) is int and d['from'] <= d['to']):
                raise ValueError('invalid date interval')
            for key in ('url', 'title', 'page', 'holding_institution'):
                if not r['source'].get(key):
                    raise ValueError(f'missing source.{key}')
            im = r['image']
            image = (root / im['path']).resolve()
            if not image.is_relative_to(root.resolve()) or not image.is_file():
                raise ValueError('image missing or outside repository')
            if hashlib.sha256(image.read_bytes()).hexdigest() != im['sha256']:
                raise ValueError('image checksum mismatch')
            w, h = im['width'], im['height']
            if type(w) is not int or type(h) is not int or min(w, h) <= 0:
                raise ValueError('image dimensions must be positive integers')
            x, y, rw, rh = r['region']['xywh']
            if any(type(n) is not int for n in (x, y, rw, rh)):
                raise ValueError('coordinates must be integers')
            if r['region']['units'] != 'pixels' or min(x, y) < 0 or min(rw, rh) <= 0 or x+rw > w or y+rh > h:
                raise ValueError('region outside source page')
            if r['review']['status'] not in ('provisional', 'verified'):
                raise ValueError('invalid review status')
            for key in ('reviewer', 'method', 'date'):
                if not r['review'].get(key):
                    raise ValueError(f'missing review.{key}')
            datetime.date.fromisoformat(r['review']['date'])
            if not isinstance(r['uncertainties'], list):
                raise ValueError('uncertainties must be an array')
            if not r['transcription']['literal'] or not r['transcription']['provenance']:
                raise ValueError('literal transcription and provenance required')
            for key in ('status', 'basis_url', 'attribution', 'modifications'):
                if not r['rights'].get(key):
                    raise ValueError(f'missing rights.{key}')
            if r['rights']['status'] not in ('public-domain', 'CC0-1.0', 'CC-BY-4.0', 'CC-BY-SA-4.0'):
                raise ValueError('rights require manual review before bundling')
            records.append(r)
        except (ValueError, KeyError, TypeError, OSError, AttributeError) as e:
            errors.append(f'{path.relative_to(root)}: {e}')
    return records, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    records, errors = validate(args.root)
    print(json.dumps({'records': len(records), 'by_kind': dict(collections.Counter(r['kind'] for r in records)),
                      'by_review_status': dict(collections.Counter(r['review']['status'] for r in records)),
                      'documents': len({r['document_id'] for r in records}),
                      'known_writers': len({r['writer_id'] for r in records if r['writer_id']}),
                      'unknown_writer_records': sum(r['writer_id'] is None for r in records),
                      'errors': errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
