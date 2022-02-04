import requests


def get_map(ln, ll, spn=None, z=None, size=None, scale=None, pt=None):
    arguments = {'spn': spn, 'z': z, 'size': size, 'scale': scale, 'pt': pt}
    map_request = f"http://static-maps.yandex.ru/1.x/?l={ln}&ll={ll}"
    for key in arguments.keys():
        if arguments[key]:
            map_request += f'&{key}={arguments[key]}'
    response = requests.get(map_request)
    map_file = "map.png"
    if response.content:
        with open(map_file, "wb") as file:
            file.write(response.content)