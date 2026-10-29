"""Exercise integrity checks against temporary records, never against source assets."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from validate_samples import validate


class SampleValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'samples/records').mkdir(parents=True)
        (self.root / 'page.jpg').write_bytes(b'test fixture, not an image')
        self.record = dict(schema_version=1, id='example', kind='manuscript',
            document_id='doc', writer_id=None, date={'from': 1880, 'to': 1880},
            document_type='letter', source={'url':'https://example.org', 'title':'letter',
            'page':'1', 'holding_institution':'example'},
            image={'path':'page.jpg', 'sha256':hashlib.sha256(b'test fixture, not an image').hexdigest(),
                   'width':100, 'height':100}, region={'units':'pixels', 'xywh':[0,0,100,100]},
            transcription={'literal':'Пример', 'provenance':'human'},
            review={'status':'verified', 'reviewer':'example', 'method':'human', 'date':'2026-10-29'},
            uncertainties=[], rights={'status':'public-domain', 'basis_url':'https://example.org',
            'attribution':'example', 'modifications':'none'}, split='reference')

    def check_record(self):
        (self.root / 'samples/records/example.json').write_text(json.dumps(self.record))
        return validate(self.root)

    def test_complete(self):
        records, errors = self.check_record()
        self.assertEqual(len(records), 1)
        self.assertEqual(errors, [])

    def test_integrity(self):
        self.record['image']['sha256'] = 'wrong'
        self.assertIn('checksum', self.check_record()[1][0])

    def test_coordinates(self):
        self.record['region']['xywh'] = [90, 0, 30, 10]
        self.assertIn('outside', self.check_record()[1][0])

    def test_eval_answer_rejected(self):
        self.record['split'] = 'evaluation'
        self.assertIn('never evaluation', self.check_record()[1][0])

    def test_unknown_rights(self):
        self.record['rights']['status'] = 'unknown'
        self.assertIn('rights require', self.check_record()[1][0])

    def test_path_escape(self):
        self.record['image']['path'] = '../outside.jpg'
        self.assertIn('outside', self.check_record()[1][0])


if __name__ == '__main__':
    unittest.main()
