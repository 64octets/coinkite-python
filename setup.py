from setuptools import setup, find_packages

setup(
  name = 'coinkite-python',
  version = '1.0',
  description = 'CoinKite Python Binding',
  author = 'Peter D. Gray',
  author_email = 'peter@coinkite.com',
  license='',
  url = 'https://github.com/coinkite/coinkite-python',
  keywords = ['coinkite', 'bitcoin'],
  packages = find_packages(),
  include_package_data = True,
  install_requires = ['simplejson>=3.2.0', 'python-dateutil==1.5'],
  classifiers = [],
)
