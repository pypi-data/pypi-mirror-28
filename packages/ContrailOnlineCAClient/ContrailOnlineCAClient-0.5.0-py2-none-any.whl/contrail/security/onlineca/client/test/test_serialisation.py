'''
Created on 16 Jan 2018

@author: philipkershaw
'''
import unittest
import os

import requests
from OpenSSL import crypto

from contrail.security.onlineca.client import OnlineCaClient


class SerialisationTestCase(unittest.TestCase):
    '''Troubleshoot serialisation issues with Python 2 vs. 3'''
    THIS_DIR = os.path.dirname(__file__)
    KEYPAIR_STORE_FILEPATH = os.path.join(THIS_DIR, 'serialisation-test.key')
    CERTREQ_STORE_FILEPATH = os.path.join(THIS_DIR, 'serialisation-test.csr')
    REF_PY3_CERT_REQ = {b'certificate_request': b'-----BEGIN CERTIFICATE REQUEST-----\nMIICRTCCAS0CAQAwADCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAN+Q\nxKSRmapD1uxBO/JPIGaXAz19NBj0ncbsgSvKqSNFV9hhnps2PMdBkKHirPM6DflN\ngSSa4iR0inS2djMqlHMQoFRKtxuQzcxNVlO0joovDhGRSW3Kq/ZDaOvwcNG5apzS\njf6OhgT0zn22w9WyrkgetIG+f6cBxO5oUb6E+tFn5h2gPmHJdR4Ce7fuHFW+Zp7x\n/y1eQk1w/sLWIbSizI2GdC49f6cDdPD8VYh8A4xhORSaNQmkfkzI9nVYLQw3Qy3H\nbFCLTA74fnnHL1U2wEUWKXTqgUAlSXw2xw5vLQnd3/IHtwTZS4jLxC5d38R1DHhT\nYUH9n6Ym7zcgJgKM2h8CAwEAAaAAMA0GCSqGSIb3DQEBCwUAA4IBAQAi+af/sJmn\npDRXf0Amvwr3Q2hvX5aLFfcuDdcPV7y0IPlmPK+9WT1eVOU7ejLNHFzEuPpmEQB0\nATdHseJY8AikJ4KOPld6gjedmVpFL8J0udcMSp/1wxXGnWvB3rsMF4+DlSW+HU7d\nF4T+9719V/KleYMrBD7Nzjzna2NcDM/vrZVmV3oQdhGoeS6/J25xn2nHZV8QKm8Y\nvBz77HlzEI3uvSUzluFXiMznMe06kTaoZPdWvl5O70JRIposYy2njZKK0hXyrvfg\nrgluelDq+ZhCgKIunlSPXwAvo3dmMUzkL+7o3vND28C9JDOGeY6xmxpbOarPMhvw\nRB3aP2goH2tM\n-----END CERTIFICATE REQUEST-----\n'}

    def setUp(self):
        if not os.path.exists(self.__class__.KEYPAIR_STORE_FILEPATH):
            self.key_pair = OnlineCaClient.create_key_pair()
            s_key_pair = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                                self.key_pair)
            with open(
                self.__class__.KEYPAIR_STORE_FILEPATH, 'wb') as key_pair_pfile:
                key_pair_pfile.write(s_key_pair)

            self.cert_req = OnlineCaClient.create_cert_req(self.key_pair)

            with open(
                self.__class__.CERTREQ_STORE_FILEPATH, 'wb') as cert_req_pfile:
                cert_req_pfile.write(self.cert_req)
        else:
            with open(
                self.__class__.KEYPAIR_STORE_FILEPATH, 'rb') as key_pair_pfile:
                s_key_pair = key_pair_pfile.read()

            self.key_pair = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                                   s_key_pair)

            with open(
                self.__class__.CERTREQ_STORE_FILEPATH, 'rb') as cert_req_pfile:
                self.cert_req = cert_req_pfile.read()

    def test01(self):
        cert_req = OnlineCaClient.create_cert_req(self.key_pair)
        self.assertEqual(cert_req, self.cert_req,
                         'Request are not equal')

    def test02_call_slcs(self):
        session = requests.Session()

        username = 'pjkersha'
        password = 'uYkkGOU$PY'
        session.auth = requests.auth.HTTPBasicAuth(username, password)

        req = {OnlineCaClient.CERT_REQ_POST_PARAM_KEYNAME: self.cert_req}
        res = session.post('https://slcs.jasmin.ac.uk/certificate/', data=req)
        self.assert_(res.ok)
        print(res.content)


if __name__ == "__main__":
    unittest.main()