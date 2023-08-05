from setuptools import setup

setup(name='autovalidate',
      version='0.1.0',
      author='Dan Tao',
      author_email='daniel.tao@gmail.com',
      packages=['autovalidate',
                'autovalidate.reporters',
                'autovalidate.validators'],
      install_requires=['pyyaml>=3.0'],
      scripts=['bin/autovalidate'])
