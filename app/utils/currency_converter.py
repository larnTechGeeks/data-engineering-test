import requests

class CurrencyClient:
    def __init__(self, 
                base_url, 
                api_id,
                api_key,
                to_currencies, 
                from_currency = "USD",
            ) -> None:
        self.__options = {
            'auth': {
                'user':api_id,
                'password': api_key
            },
            'baseUrl': base_url,
            'query_string': {}
        }
        self.__convert_from_uri = "convert_from"
        self.__from_currency = from_currency
        self.__to_currencies = to_currencies

    def __make_request(self, ops):
        self.__options.update(ops)
        url = self.__options["url"]
        username = self.__options['auth']['user']
        password = self.__options['auth']['password']
        query_string = self.__options['query_string']

        response = requests.get(url, auth=(username, password), params=query_string)

        if response.status_code == 200:
            data = response.json()
            return {'success': True, 'data': data}
        else:
            try:
                error_data = response.json()
            except ValueError:
                error_data = {'message': 'Unknown error occurred'}
            return {'success': False, 'data': error_data}

    def convert_from(self, options = {}):
        options_ = {
            'url': self.__options['baseUrl'] + self.__convert_from_uri,
            'query_string': {
                'from': self.__from_currency,
                'to': ','.join(self.__to_currencies),
            }
        }

        options_.update(options)
        return self.__make_request(options_)
