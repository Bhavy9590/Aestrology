import json
from django.test import TestCase
from kundli.engine import _sign,_nak,_navamsa

class EngineTests(TestCase):
    def test_signs(self):
        self.assertEqual(_sign(0)[1],'મેષ'); self.assertEqual(_sign(359.9)[1],'મીન')
    def test_nakshatra(self):
        self.assertEqual(_nak(0)[1],'અશ્વિની'); self.assertEqual(_nak(0)[2],1)
    def test_navamsa(self):
        self.assertIn(_navamsa(0)[0],['મેષ','વૃષભ','મિથુન'])

    def test_kundli_api(self):
        payload={
            'name':'Test User',
            'dob':'1990-01-01',
            'tob':'18:30:00',
            'place':'Ahmedabad',
            'latitude':23.0225,
            'longitude':72.5714,
            'timezone':'Asia/Kolkata'
        }
        response=self.client.post('/api/kundli/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        body=response.json()
        self.assertTrue(body['ok'])
        self.assertEqual(body['name'], 'Test User')
        self.assertIn(body['kundli']['lagna'], ['મેષ','વૃષભ','મિથુન','કર્ક','સિંહ','કન્યા','તુલા','વૃશ્ચિક','ધન','મકર','કુંભ','મીન'])
