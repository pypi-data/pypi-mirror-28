from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='funny_greeting',
      version='0.2',
      description='Greeting in Israeli',
      url='http://github.com/xuanminhacsi/funny_greeting',
      author='Minh Vu',
      author_email='xuanminh12995@gmail.com',
      license='MIT',
      packages=['funny_greeting'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])