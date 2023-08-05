from .parser import ArticleArgsParser
import sys, os
from .utils import ask, str_compat, translation, parse_toml
import datetime
from .exceptions import InterfaceNotImplete

class ActionInterface(object):

    def __init__(self, args):
        self.args = args

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def run(self):
        raise InterfaceNotImplete()


class Article(ActionInterface):
    '''
    Article 类
    '''
    def run(self):
        '''根据 self.args 命令开始运行特定操作'''
        if self.args['action'] == 'create':
            data = self.get_article_attrs()
            self.create(data)


    def create(self, data):
        file_name = '{}.md'.format(data['file_name'],**data)
        path = os.path.join(self.args['config_dir'], self.args['Article']['floder'], file_name)
        content = self._content(data)
        self._create_file(path, content)

    def _create_file(self, path, content):
        '''
        创建文件
        Args:
            path : string, 文件的全路径， 包含文件名
            content: 要写入的内容
        '''
        # 递归创建目录
        full_path = self.handle_duplicate_name(*os.path.split(path))

        with open(full_path, 'w+') as fp:
            fp.write(content)

    # def full_path(self):
    #     pass

    def handle_duplicate_name(self, path, filename, start_index = 0):
        '''检测目录下是否有重名文件
        如果有的话， 在当前文件名后面递增数字
        '''
        if not os.path.exists(path):
            os.makedirs(path)

        full_path = ''
        if os.path.exists(os.path.join(path, filename)):
            new_name = filename.split('.')
            start_index += 1
            if len(new_name) == 2:
                new_name.insert(1, str(start_index))
            else:
                new_name[1] = str(start_index)
            full_path = self.handle_duplicate_name(path, '.'.join(new_name), start_index)
        else:
            full_path = os.path.join(path, filename)

        return full_path

    def _content(self, data):
        '''
        根据data ， 组装文章元数据
        '''
        content = list()
        content.append('Title: ' + data['title'])
        content.append('Date: ' + data['date'])
        content.append('Modified: ' + data['modified'])
        content.append('Slug: ' + data['slug'])
        if data.get('tags', None):
            content.append('Tags: ' + data['tags'])
        content.append('Author: ' + data['author'])
        content.append(len(data['slug']) * 5 * '-')
        content.append('\n')

        content = '\n'.join(content)
        return content


    def get_article_attrs(self):
        '''
        与用户交互， 获取文章的属性
        '''

        data = dict()
        data['title'] = ask('What will be the title of this article?', answer=str_compat, default='')
        data['tags']  = ask('Tags，use , split:', answer=str_compat, default='')
        data['slug']  = ask('Slug:', answer=str_compat,
                            default=translation(data['title']))

        data['author'] = ask('Author:', answer=str_compat,
                            default=self.args['Article']['author'])

        date_format = self.args.get('date_format','%Y-%m-%d %H:%M:%S')
        data['date']  = ask('Date:', answer=str_compat,
                            default = datetime.datetime.now().strftime( date_format ))
        data['modified'] = ask('Modified Date:',answer=str_compat,
                            default = datetime.datetime.now().strftime( date_format ))

        default_file_name = datetime.datetime.now().strftime(
                                self.args['filename_format']).format(**data)

        data['file_name'] = ask("Default file name:", answer=str_compat,
                            default = default_file_name)

        confirm = ask('Confirm creation?', bool, True)

        if confirm:
            return data
