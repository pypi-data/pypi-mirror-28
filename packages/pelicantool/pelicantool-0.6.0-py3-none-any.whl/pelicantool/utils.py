import six
import urllib, random, hashlib
import requests
import os
import toml

if six.PY3:
    str_compat = str
else:
    str_compat = unicode


def _input_compat(prompt):
    if six.PY3:
        r = input(prompt)
    else:
        r = raw_input(prompt)
    return r


def ask(question, answer=str_compat, default=None, l=None):
    if answer == str_compat:
        r = ''
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question, default))

            r = r.strip()

            if len(r) <= 0:
                if default is not None:
                    r = default
                    break
                else:
                    print('You must enter something')
            else:
                if l and len(r) != l:
                    print('You must enter a {0} letters long string'.format(l))
                else:
                    break

        return r

    elif answer == bool:
        r = None
        while True:
            if default is True:
                r = _input_compat('> {0} (Y/n) '.format(question))
            elif default is False:
                r = _input_compat('> {0} (y/N) '.format(question))
            else:
                r = _input_compat('> {0} (y/n) '.format(question))

            r = r.strip().lower()

            if r in ('y', 'yes'):
                r = True
                break
            elif r in ('n', 'no'):
                r = False
                break
            elif not r:
                r = default
                break
            else:
                print("You must answer 'yes' or 'no'")
        return r
    elif answer == int:
        r = None
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question))

            r = r.strip()

            if not r:
                r = default
                break

            try:
                r = int(r)
                break
            except:
                print('You must enter an integer')
        return r
    else:
        raise NotImplemented(
            'Argument `answer` must be str_compat, bool, or integer')


def translation(query, appid='20161217000034172', appkey = '07Qh2zEwKIx3kGwer1Uz', from_='zh', to='en'):
    '''
    请求百度翻译 api 获取翻译结果
    '''
    # appid = '20161217000034172'
    # secretKey = '07Qh2zEwKIx3kGwer1Uz'
    appid = appid
    secretKey = appkey
    salt = random.randint(32768, 65536)
    sign = appid + query + str(salt) + secretKey
    m1 = hashlib.md5(sign.encode('utf8'))
    sign = m1.hexdigest()
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
    url = url + urllib.parse.urlencode(
        {'q': query, 'from': from_, 'to': to, 'appid': appid,
         'salt': salt, 'sign': sign})

    r = requests.get(url)
    r.encoding = 'utf-8'
    result = r.json()
    if 'error_code' in result:
        return None

    if 'trans_result' in result:
        return result['trans_result'][0].get('dst', None)

    return None

def parse_toml(path = None):
    '''从 filepath 中解析 toml 配置文件
    '''
    config = {}
    if os.path.exists(path):
        config.update(toml.load(path))

    return config
