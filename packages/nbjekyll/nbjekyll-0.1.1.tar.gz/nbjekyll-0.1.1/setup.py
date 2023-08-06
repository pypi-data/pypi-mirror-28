import os

from setuptools import setup, find_packages

name = 'nbjekyll'

pkg_root = os.path.join(os.path.dirname(__file__), name)
here = os.path.dirname(__file__)

setup_args = dict(name = name,
                  version = '0.1.1',
                  description = 'Package used for easy conversion from Jupyter notebook to Jekyll posts',
                  url = 'https://github.com/trallard/nbconvert-jekyllconvert.git',
                  donwload_url ='https://github.com/trallard/nbjekyll/archive/v0.1.1.tar.gz',
                  author = 'Tania Allard',
                  author_email = 't.allard@sheffield.ac.uk',
                  description_file = 'README.md',
                  license = 'MIT',
                  include_package_data = True,
                  packages = find_packages(),
                  zip_safe = False,
                  install_requires = ['pygit2', 'nbval', 'nbconvert >= 5.0','pytz'],
                  keywords = ['jekyll', 'nbconvert', 'jupyternotebooks'],
                  classifiers = ["Programming Language :: Python :: 3","Development Status :: 4 - Beta",
                  "Intended Audience :: Education", "License :: OSI Approved :: MIT License" ] )

if __name__ == '__main__':
    setup(**setup_args)
