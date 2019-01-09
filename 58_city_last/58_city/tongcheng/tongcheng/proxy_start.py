import requests

def get_proxy():
    PROXY_POOL_URL = "http://0.0.0.0:5555/random"

    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except ConnectionError:
        return None


if __name__ == '__main__':
    get_proxy()
