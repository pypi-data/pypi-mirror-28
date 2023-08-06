from distutils.core import setup
setup(
  name = 'xy_wordcloud',
  packages = ['xy_wordcloud'],
  version = '3.0.0',
  description = 'Generate wordcloud',
  long_description='Generate text wordcloud',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'wordcloud', 'python3','python','text wordcloud'],
  license='MIT',
  install_requires=[
        'wordcloud',
        'jieba',
        'imageio'
    ],
)
