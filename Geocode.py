import requests


def geocode(geocode, apikey='40d1649f-0493-4b70-98ba-98533de7710b', format='json'):
    geocoder_request = f"http://static-maps.yandex.ru/1.x/?apikey={apikey}&geocode={geocode}&format={format}"
    response = requests.get(geocoder_request)
    return response
