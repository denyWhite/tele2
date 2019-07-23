import requests
import re


def check_status_code(response, expected_code):
    result_code = response.status_code
    if result_code != expected_code:
        url = response.url
        method = response.request.method
        print('{method} to {url} resulted in {result_code} status code instead of {expected_code}'.format(**locals()))
    return 0


def get_balance(number, password):
    s = requests.Session()
    response = s.get('https://login.tele2.ru/ssotele2/wap/auth/')
    check_status_code(response, 200)
    match = re.search(r'value="(.*?)" name="_csrf"', response.content.decode("utf-8"))
    csrf_token = match.group(1)
    if csrf_token is None:
        print('CSRF token not found')
    data = dict(pNumber=number, password=password, _csrf=csrf_token, authBy='BY_PASS', rememberMe='true')
    response = s.post(
        'https://login.tele2.ru:443/ssotele2/wap/auth/submitLoginAndPassword',
        data=data)
    check_status_code(response, 200)
    response = s.get('https://my.tele2.ru/api/subscribers/{}/balance'.format(number))
    check_status_code(response, 200)
    amount = response.json().get('data', {}).get('value', None)
    if amount is None:
        print('Unable to get balance amount from JSON')
    return int(amount)


print(get_balance("79000000000", "######"))