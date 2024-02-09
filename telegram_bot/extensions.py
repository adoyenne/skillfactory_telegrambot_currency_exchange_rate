import requests

class APIException(Exception):
    pass

#my API=5a481dd660b64a9a90e65e141c4f6063

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        # Определяем URL API для получения курса валют
        print(base,quote)
        url = f'https://openexchangerates.org/api/latest.json?app_id=5a481dd660b64a9a90e65e141c4f6063&base={base}&symbols={quote}'
        try:
            # Отправляем запрос к API
            data = requests.get(url).json()

            # Проверяем наличие курса валюты в ответе API
            if 'rates' not in data or quote not in data['rates']:
                raise APIException("Курс валюты не найден в ответе API")

            # Извлекаем курс валюты из ответа API
            exchange_rate = data['rates'][quote]

            # Рассчитываем конвертированную сумму
            converted_amount = amount * exchange_rate

            return converted_amount

        except Exception as e:
            # Если произошла ошибка при запросе к API, выводим исключение
            raise APIException("Ошибка при запросе к API")