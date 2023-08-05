# paytrek

## Installation

    $ pip install paytrek

## Usage

    >>> from paytrek import Paytrek
    >>> client = Paytrek('username', 'password', 'sandbox')
    >>> sale_params = {
            "amount": 1.9,
            "billing_address": "123 Market St. San Francisco",
            "billing_city": "San Francisco",
            "billing_country": "US",
            "billing_state": "CA",
            "billing_zipcode": "34410",
            "currency": "/api/v1/currency/USD/",
            "customer_email": "johndoe@gmail.com",
            "customer_first_name": "John",
            "customer_ip_address": "212.57.9.204",
            "customer_last_name": "Doe",
            "fraud_check_enabled": False,
            "installment": 1,
            "items": [
              {
                "name": "Ramada Hotel",
                "photo": "http://d1ldkdiqjyt22f.cloudfront.net/hotelimages/UKSFLE/1937525_140x110.jpg",
                "quantity": 1,
                "unit_price": 1.9
               }
            ],
            "order_id": "1467034250",
            "pre_auth": False,
            "sale_data": {},
            "secure_option": "No"
          }

    >>> sale_response = client.sale(sale_params)
    >>> sale_token = sale_response['token']
    >>> charge_params = {
           "number":"4263982640269299",
           "expiration":"02/2018",
           "cvc":"000",
           "card_holder_name":"John Doe",
           "sale":"/api/v1/sale/{}/".format(sale_token)
        }
    >>> charge_response = client.charge(charge_params)
    
    >>> client.refund(sale_token=sale_token, amount=1)

## License

This library is available to anybody free of charge, under the terms of MIT License:

Copyright (c) 2018 Erkan Ay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.