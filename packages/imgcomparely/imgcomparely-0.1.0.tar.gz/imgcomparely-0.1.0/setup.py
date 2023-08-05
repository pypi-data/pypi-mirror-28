import setuptools

from distutils.core import setup
setup(
  name = 'imgcomparely',
  packages = ['imgcompare'],
  version = '0.1.0',
  description = 'compares two images get difference percentage',
  author = 'lynn0401',
  author_email = '15601602423@163.com',
  url = 'https://github.com/Lynn0401/imgcompare',
  download_url = 'https://github.com/Lynn0401/imgcompare/0.1.0',
  keywords = ['image', 'compare'],
  classifiers = [],
  license='MIT',
  install_requires=['pillow']
)
