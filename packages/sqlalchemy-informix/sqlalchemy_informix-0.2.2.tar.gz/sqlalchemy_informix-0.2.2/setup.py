import os
import re

from setuptools import setup

v = open(os.path.join(os.path.dirname(__file__), 'sqlalchemy_informix', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()


setup(name='sqlalchemy_informix',
      version=VERSION,
      description="",
      long_description="",
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: Implementation :: CPython',
      'Topic :: Database :: Front-Ends',
      ],
      keywords='SQLAlchemy Informix',
      author='Florian Apolloner',
      author_email='florian@apolloner.eu',
      license='MIT',
      packages=['sqlalchemy_informix'],
      include_package_data=True,
      zip_safe=False,
      entry_points={
         'sqlalchemy.dialects': [
              'informix = sqlalchemy_informix.ibmdb:InformixDialect',
              ]
        }
)
