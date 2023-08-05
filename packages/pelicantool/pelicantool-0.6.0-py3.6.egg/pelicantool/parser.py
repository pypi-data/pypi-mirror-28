import os, sys
import argparse
import toml
from .utils import ask, str_compat
from .exceptions import ParserNotFound
from . import __version__

class ArgsParser(object):
    def __init__(self, args):
        self.args = args

    def parse_args(self):
        parser = argparse.ArgumentParser(
            prog='pelicantool',
            description='A auto tool for Pelican',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        parser.add_argument('-v', '--version', action='version', version = '%(prog)s {}'.format(__version__))
        parser.add_argument('-c', '--config_dir', default = './')
        parser.add_argument('action', nargs='?')
        parser.add_argument('target', nargs='?', help='操作的目标')

        return parser.parse_args(self.args)


class Parser(object):
    def __init__(self, parser):
        self.parser = parser

    @property
    def args(self):
        return self.parser.parse_args()

    def parse_toml(self, path = None):
        '''从 filepath 中解析 toml 配置文件
        '''
        if path is None or not os.path.exists(path):
            path = './config/pelicantool.toml'

        config = {}
        config.update(toml.load(path))

        return config

    def get_attrs(self):
        '''
        解析命令行参数， 并且读取覆盖文本配置
        '''
        path = os.path.join(self.args.config_dir, 'pelicantool.toml')
        attrs = vars(self.args)
        attrs.update(self.parse_toml(path))

        return attrs


class ArticleArgsParser(Parser):
    '''
    文章命令解析
    '''
    def instance(self):
        '''
        返回动作实例
        '''
        from .article import Article
        return Article(self.get_attrs())

class ParserFactory(object):
    '''parser factory'''

    @classmethod
    def factory(self, args):
        parser = ArgsParser(args)
        args = parser.parse_args()

        if args.target == 'article':
            return ArticleArgsParser(parser)
        else:
            raise ParserNotFound()
