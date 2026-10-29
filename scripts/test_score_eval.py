import unittest
from score_eval import canonical, distance, score


class Metrics(unittest.TestCase):
    def test_edit_operations(self):
        self.assertEqual(distance('кот', 'кит'), 1)
        self.assertEqual(distance('кот', 'коты'), 1)
        self.assertEqual(distance('кот', 'кт'), 1)
        self.assertEqual(distance('', 'кот'), 3)

    def test_literal_policy(self):
        self.assertNotEqual(canonical('міръ'), canonical('мир'))
        self.assertEqual(canonical('а\r\nб'), 'а\nб')
        self.assertEqual(canonical('и\u0306'), 'й')

    def test_weighted_cer_and_entities(self):
        cases = [dict(id='a', reference='Иван', prediction='Иван', illegible_reference_characters=0,
                      entities=[dict(type='given_name',reference='Иван',prediction='Иван',confident=True)]),
                 dict(id='b', reference='20', prediction='30', illegible_reference_characters=1,
                      entities=[dict(type='age',reference='20',prediction='30',confident=True)])]
        result=score(cases)
        self.assertEqual(result['cer'], 1/6)
        self.assertEqual(result['illegible_share'], 1/6)
        self.assertEqual(result['entities']['age']['confident_error_rate'], 1)

    def test_empty_and_duplicate_rejected(self):
        with self.assertRaises(ValueError): score([])
        c=dict(id='x', reference='x', prediction='', illegible_reference_characters=1, entities=[])
        with self.assertRaises(ValueError): score([c,c])


if __name__ == '__main__': unittest.main()
