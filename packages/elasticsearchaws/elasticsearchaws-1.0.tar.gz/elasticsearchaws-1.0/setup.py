from setuptools import setup

setup(name='elasticsearchaws',
      version='1.0',
      description='Elasticsearch connection class for AWS',
      url='http://github.com/humeniukd/elasticsearch-aws',
      author='Dmytro Humeniuk',
      author_email='dmitry.gumenyuk@gmail.com',
      license='MIT',
      packages=['elasticsearchaws'],
      install_requires=['boto', 'elasticsearch'],
      zip_safe=False)
