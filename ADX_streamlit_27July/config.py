login_id = "BK555"
password = "India@5455"
TOTP = 'NJHEOB3LOBCCOOBU'

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    access_token = None

