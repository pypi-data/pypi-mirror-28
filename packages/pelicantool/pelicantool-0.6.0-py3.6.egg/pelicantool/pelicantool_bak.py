import toml
import argparse
import sys
import os
import datetime
import random
import hashlib
import urllib.parse
import requests

__version__ = '0.6.0'

try:
    from utils import ask, str_compat
except ModuleNotFoundError:
    from pelicantool.utils import ask, str_compat

try:
    sys.path.append(os.getcwd())
    import pelicanconf
except ModuleNotFoundError:
    sys.path.append(os.path.join(os.getcwd(), 'tests'))
    import pelicanconf

class Article(object):
    def __init__(self):
        self._title = ''
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self._date = datetime.datetime.now()
        self._modified = self._date
        self._tags = ' '
        self._author = pelicanconf.AUTHOR
        self._format = '.md'
        self._filename = None

    def translation(self, query, from_='zh', to='en'):
        '''
        请求百度翻译 api 获取翻译结果
        '''
        appid = '20161217000034172'
        secretKey = '07Qh2zEwKIx3kGwer1Uz'
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

    def create(self, expath=None):
        '''
        create article
        args:
            expath: 文件存储目录， 若为None，则根据 pelicanconf.py 中的 PATH 来自动判断
        '''
        print("start creating...")
        if self.title:
            content = '\n'.join(self.content)
            if self._create_file(self.filename, content, expath):
                print("{fullname} craete ....... [successful!]\n".format(
                    fullname=self.filename))
                print('\n'.join(self.content))
            else:
                print("failed!")

    @property
    def filename(self):
        '''
        将要生成的文件名
        '''
        if self._filename is None:
            # self._filename = '{time}-{title}{format}'.format(
            #     time=datetime.datetime.now().strftime('%Y-%m-%d'),
            #     title=self.title,
            #     format=self.format)
            self._filename = '{time}-{title}{format}'.format(
                time=self.date.strftime('%Y-%m-%d'),
                title=self.title,
                format=self.format)

        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def _create_file(self, fullname, content, expath=None):
        # 目录不存在,则创建
        # 如果 expath 不为 None,则在 content 目录中创建子目录
        if expath is not None:
            path = os.path.join(pelicanconf.PELICANTOOL_PATH, expath)
        else:
            path = pelicanconf.PELICANTOOL_PATH
        if os.path.isdir(path) is False:
            print("目录不存在,创建中...........创建完成")
            os.makedirs(os.path.join(path))

        fullname = os.path.join(path, fullname)

        with open(fullname, 'w') as fp:
            fp.write(content)

        return True

    @property
    def content(self):
        '''
        create content
        '''
        content = list()
        content.append('Title: ' + self.title)
        content.append('Date: ' + self.date.strftime(self.date_format))
        content.append('Modified: ' + self.modified.strftime(self.date_format))
        content.append('Slug: ' + self.slug)
        if self.tags:
            content.append('Tags: ' + self.tags)
        content.append('Author: ' + self.author)
        content.append('---\n')
        content.append('\n')

        return content

    @property
    def categories(self):
        '''
        分类
        '''
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        format_ = ('.md', '.rst')
        if value in format_:
            self._format = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        '''
        string => datetime
        '''
        self._date = datetime.datetime.now().strptime(value, self.date_format)
        # self._date = value

    @property
    def modified(self):
        return self._modified

    @modified.setter
    def modified(self, value):
        self._modified = datetime.datetime.now().strptime(value, self.date_format)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def slug(self):
        self._slug = self.translation(self.title)
        if isinstance(self._slug, str):
            self._slug = self._slug.replace(' ', '_')
            self._slug = self._slug.replace(',', '')
            return self._slug
        return None

    @slug.setter
    def slug(self, value):
        self._slug = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    def __str__(self):
        data = {'title': self.title,
                'date': self.date,
                'modified': self.modified,
                'tags': self.tags,
                'slug': self.slug,
                'author': self.author,
                'format': self.format}
        return str(data)


import sys

def main():
    args = get_args(sys.argv[1:])

    print(args)

def get_args(args):
    '''获取参数， 先读取命令行的 -c 命令， 当为None 时读取当前运行目录的 pelicantool.toml，
    当读取不到时， 只返回命令行参数，
    当读取到时，再将配置文件中的配置合并到命令行参数中'''

    cmd_args = vars(parse_args(args))

    if cmd_args['c'] is None:
        cmd_args['c'] = './'

    file_path = os.path.join(cmd_args['c'], 'pelicantool.toml')
    file_args = parse_toml(file_path)

    print(file_args)

def parse_toml(file_path):
    '''读取文件并解析 toml 配置'''
    args = {}
    if os.path.exists(file_path):
        args.update(toml.load(file_path))

    print(args)
    return args

# class Parse(object):
#     '''配置解析类'''
#     def __init__(self):
#         pass
#
#     def parse_toml(self, file_path):
#         if os.path.exists(file_path):
#             pass

def parse_args(args = None):
    '''解析命令行参数
    '''
    if args is None:
        args = []

    class Namespcae(dict):
        pass

    namespace = Namespcae()
    parser = argparse.ArgumentParser(
        prog='pelicantool',
        description='A auto tool for Pelican',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument('-c', nargs=None)
    parser.add_argument('action', nargs='?')

    return parser.parse_args(args)

def make_article(**kw):
    '''
    向用户询问命令行参数
    '''
    data = {}
    data.title = ask('What will be the title of this article?', answer=str_compat)
    # data.author = ask()
    pass

def create_article(path, filename, title, author, **kw):
    '''
    创建文章
    Args:
        path: 要保存的文章目录
        filename: 要保存的文章文件名
        title: 文章标题
        author: 作者名称
        **kw: 其他一些属性
    '''
    pass


def main_bak():
    parser = argparse.ArgumentParser(
        prog='pelicantool',
        description='A auto tool for Pelican',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--version',
                        action='version', version='%(prog)s 2.0')
    args = parser.parse_args()

    print('''Welcome to pelicantool v{v}.

This script helps you create new articles.

Please answer the following questions so this script can generate the

information needed by article.

    '''.format(v=__version__))
    article = Article()
    article.title = ask('What will be the title of this article?',
                        answer=str_compat)
    article.tags = ask('Tags，use , split:',
                       answer=str_compat, default=article.tags)
    article.slug = ask('Slug:', answer=str_compat, default=article.slug)
    article.author = ask('Author:', answer=str_compat, default=article.author)
    article.date = ask('Date:', answer=str_compat, default=article.date.strftime(article.date_format))
    article.modified = ask('Modified Date:', answer=str_compat, default=article.date.strftime(article.date_format))

    confirm = ask('Confirm creation?', bool, True)

    if confirm:
        article.create(expath=article.filename.split('.')[0])


if __name__ == '__main__':
    main()
