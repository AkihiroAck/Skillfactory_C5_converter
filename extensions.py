import json
import requests
import config


def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


class APIException(Exception):
    def __init__(self, message='ConvertException'):
        super().__init__(message)


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        try:
            if base != quote:
                price = json.loads(requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}').content)[quote]
                return str(price * amount) + ' ' + quote
            else:
                raise APIException('Нельзя переводить на ту же валюту')
        except APIException as e:
            return e
        except Exception as e:
            return e

    @staticmethod
    def is_currency(message):
        if len(message.text.split()) != 3:
            raise APIException('Ошибка количества параметра. Нужно писать как на примере\nПример: рубль доллар 100.0\n\n/help - Список команд')
        
        elif message.text.split()[0].title() not in config.currency.keys():
            raise APIException(f'{message.text.split()[0].title()} не в списке (/values - что бы узнать доступные валюты)')
        
        elif message.text.split()[1].title() not in config.currency.keys():
            raise APIException(f'{message.text.split()[1].title()} не в списке (/values - что бы узнать доступные валюты)')
        
        elif not is_number(message.text.split()[2]):
            raise APIException(f'Это не цифра: "{message.text.split()[2]}"')
