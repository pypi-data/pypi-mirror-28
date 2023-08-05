from distutils.core import setup
setup(
  name = 'xy_pinyin',
  packages = ['xy_pinyin'],
  version = '2.0.0',
  description = 'hanzi to pinyin',
  long_description='get the hanzi to pinyin',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'pinyin', 'python3','python','duoyin'],
  license='MIT',
  install_requires=[
        'pypinyin',
    ],
)
