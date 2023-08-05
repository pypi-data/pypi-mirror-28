from distutils.core import setup

setup(
  name = 'djang-polls',
  packages = ['django-polls'], # 必须与 name 的值相同
  version = '0.2',
  description = 'A poll program',
  author = 'Joshua Chen',
  author_email = 'iesugrace@gmail.com',
  url = 'https://github.com/iesugrace/django-polls', # 这里使用github地址
  download_url = 'https://github.com/iesugrace/django-polls/archive/0.1.tar.gz',
  keywords = ['polls', 'testing', 'example'], # 各种标签性文字
  classifiers = [],
)
