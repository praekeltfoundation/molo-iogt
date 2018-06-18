import codecs
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), 'rb', 'utf-8') as f:
        return f.read()


install_requires = [
    'molo.core==4.4.15',
    'molo.surveys==2.3.0',
    'molo.profiles==3.2.1',
    'molo.commenting==2.1.3',
    'molo.polls==3.2.0',
    "molo.usermetadata==1.2.0",
    'elasticsearch==1.7.0',
    'django-modelcluster>=2.0,<3.0',
    'djangorestframework>=3.1.3,<3.7',
    'celery<4.0',
    'gunicorn',
    'psycopg2',
    'django-extensions>=1,<2',
    'django_compressor==2.0',
    'six>=1.9',
    'html5lib==0.9999999',
    'django-mptt==0.8.5',
    'django-google-analytics-app==4.3.0',
    'Unidecode==0.04.16',
    'django-storages',
    'boto',
    'pyrabbit',
]

setup(name='iogt',
      version=read('VERSION'),
      description='iogt',
      long_description=read('README.rst'),
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Praekelt.org',
      author_email='dev@praekelt.org',
      url='https://github.com/praekelt/molo-iogt',
      license='BSD',
      keywords='praekelt, mobi, web, django',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require = {
        'test': [
            'pytest==3.0.0',
            'pytest-django==3.1.1',
            'responses',
        ],
        'cover': [
            'pytest-cov',
        ],
        'lint': [
            'flake8==3.4.1',
        ],
      },
      entry_points={})
