import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Paytrek(object):
    BASE_URLS = {
        'sandbox': 'https://sandbox.paytrek.com',
        'worldwide_live': 'https://secure.paytrek.com',
        'turkey_live': 'https://secure.paytrek.com.tr'
    }

    def __init__(self, username, password, environment='sandbox'):
        self.basic_auth = (username, password)
        self.base_url = self.BASE_URLS.get(environment)
        self.endpoints = {
            'sale': ''.join([self.base_url, '/api/v1/sale/']),
            'charge': ''.join([self.base_url, '/api/v1/charge/']),
            'capture': ''.join([self.base_url, '/api/v1/capture/']),
            'refund': ''.join([self.base_url, '/api/v1/refund/']),
            'fraudcheck': ''.join([self.base_url, '/api/v1/fraudcheck/']),
            'charge_with_token': ''.join([self.base_url, '/api/v1/charge_with_token/']),
            'tokenization': ''.join([self.base_url, '/payment/tokenization/']),
            'options': ''.join([self.base_url, '/payment/options/']),
            'vault': ''.join([self.base_url, '/payment/vault/']),
        }
        self.headers = {'Content-type': 'application/json'}

    def _request(self, url, query={}):
        """
        Returns json response according to defined endpoint

        :param url:
        :param query:
        :return:
        """
        response = requests.post(url=url, auth=self.basic_auth, json=query,
                                 headers=self.headers, verify=False)
        if not response.ok:
            raise Exception(response.text)
        return response.json()

    def sale(self, payload=None, sale_token=None):
        """
        Returns json response within sale result
        to create sale resource payload is required
        to get created sale resource sale_token is required

        :param payload: https://sandbox.paytrek.com/docs/integration/saleresource.html#list-of-parameters
        :param sale_token:
        :return:
        """
        if payload:
            response = requests.post(url=self.endpoints.get('sale'),
                                     json=payload, headers=self.headers,
                                     auth=self.basic_auth, verify=False)
        elif sale_token:
            url = ''.join([self.endpoints.get('sale'), sale_token])
            response = requests.get(url=url, headers=self.headers,
                                    auth=self.basic_auth, verify=False)
        if not response.ok:
            raise Exception(response.text)
        return response.json()

    def charge(self, payload):
        """
        Returns json response within charge result

        :param payload: https://sandbox.paytrek.com/docs/integration/chargeresource.html#list-of-parameters
        :return:
        """
        return self._request(self.endpoints.get('charge'), query=payload)

    def charge_with_token(self, sale_token, payment_token, dcc_currency=None, secure_charge=False):
        """
        Returns json response within succeeded or failed result

        :param sale_token:
        :param payment_token:
        :param secure_charge: redirects to 3D secure
        :param dcc_currency: the DCC currency symbol that you have obtained
        :return:
        """
        payload = {
            'sale': '/api/v1/sale/{}/'.format(sale_token),
            'payment_token': payment_token,
            'dcc_currency': dcc_currency,
            'secure_charge': secure_charge
        }
        return self._request(self.endpoints.get('charge_with_token'), query=payload)

    def fraudcheck(self, sale_token, payment_token):
        """
        Returns json response within sale risk result

        :param sale_token:
        :param payment_token:
        :return:
        """
        payload = {
            'sale': '/api/v1/sale/{}/'.format(sale_token),
            'payment_token': payment_token,
        }
        return self._request(self.endpoints.get('fraudcheck'), query=payload)

    def capture(self, sale_token, comments=None):
        """
        Returns json response within succeeded or fail result

        :param comments: comments for accepting the fraud review decision
        :param sale_token:
        :return:
        """
        params = {'comments': comments}
        url = ''.join([self.endpoints.get('capture'), sale_token, '/'])
        return self._request(url, query=params)

    def refund(self, sale_token, amount=None, comments=None):
        """
        Returns json response within refund or fail result

        :param sale_token:
        :param amount: amount to refund
        :param comments: comments for reject decision
        :return:
        """
        params = {
            'amount': amount,
            'comments': comments
        }
        url = ''.join([self.endpoints.get('refund'), sale_token, '/'])
        return self._request(url, query=params)

    def tokenization(self, payload):
        """
        Returns json response representing payment token and strict card information
        such as bin number, bin country, card currency and card issuer.

        :param payload: https://sandbox.paytrek.com/docs/integration/tokenization.html#list-of-parameters
        :return:
        """
        return self._request(self.endpoints.get('tokenization'), query=payload)

    def vault(self, payload):
        """
        Returns json response representing payment token and strict card information
        such as bin number, bin country, card currency and card issuer.

        :param payload: https://sandbox.paytrek.com/docs/integration/vault.html#list-of-parameters
        :return:
        """
        return self._request(self.endpoints.get('vault'), query=payload)

    def options(self, payload):
        """
        Returns json response representing payment token and strict card information
        such as bin number, bin country, card currency and card issuer.

        :param payload: https://sandbox.paytrek.com/docs/integration/vault.html#list-of-parameters
        :return:
        """
        return self._request(self.endpoints.get('options'), query=payload)
