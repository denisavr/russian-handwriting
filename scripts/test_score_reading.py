import unittest
from score_reading import content,compare


class ReadingScore(unittest.TestCase):
    def fixture(self,text,confidence='high',unreadable=False):
        return ({'cases':[{'id':'x','type':'text','reference':'міръ','literal_verified':True}]},
                {'fields':[{'id':'x','text':text,'confidence':confidence,'unreadable':unreadable}]})

    def test_uncertainty_markup_not_letter_errors(self):
        r=compare(*self.fixture('[міръ?]','low'))
        self.assertEqual(r['summary']['edits'],0)
        self.assertEqual(r['summary']['uncertain_correct'],1)

    def test_content_and_literal_are_separate(self):
        r=compare(*self.fixture('мир'))
        self.assertEqual(r['summary']['content_cer'],0)
        self.assertGreater(r['summary']['literal_cer'],0)

    def test_abstention_not_rewarded(self):
        r=compare(*self.fixture('','low',True))
        self.assertEqual(r['summary']['content_cer'],1)
        self.assertEqual(r['summary']['whole_field_abstention_character_share'],1)

    def test_confident_error(self):
        r=compare(*self.fixture('кот'))
        self.assertEqual(r['summary']['confident_errors'],1)

    def test_no_reference_disclosure_by_default(self):
        r=compare(*self.fixture('міръ'))
        self.assertNotIn('reference',r['per_field'][0])
        self.assertNotIn('prediction',r['per_field'][0])

    def test_alternatives_not_matched_to_answer(self):
        self.assertGreater(compare(*self.fixture('міръ/кот'))['summary']['edits'],0)

    def test_hard_sign_inside_word_preserved(self):
        self.assertEqual(content('подъездъ',True),'подъезд')

    def test_invalid_or_duplicate_prediction_rejected(self):
        k,r=self.fixture('x');r['fields']*=2
        with self.assertRaises(ValueError):compare(k,r)


if __name__=='__main__':unittest.main()
