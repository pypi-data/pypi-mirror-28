from setuptools import setup
from codecs import open

# http://setuptools.readthedocs.io/en/latest/setuptools.html

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(name='checklinks',
      version='0.3',
      description='Fetch, find and report broken links on all pages of a website.',
      url='https://gitlab.com/alexbenfica/check-links/',
      author='Alex Benfica',
      author_email='alexbenfica@gmail.com',
      keywords="broken links check checker invalid urls url",
      long_description=readme,
      license='MIT',
      packages=['checklinks'],
      package_dir={'checklinks': 'app'},
      install_requires=[
            'requests',
            'markdown',
            'bs4',
            'colorama'
            ],
      zip_safe=False,
      )
