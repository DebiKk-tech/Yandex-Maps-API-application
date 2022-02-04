import requests


def geocode(geocode):
    geocode = '+'.join(geocode.split())
    print(geocode)
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={geocode}&format=json"
    response = requests.get(geocoder_request)
    return response