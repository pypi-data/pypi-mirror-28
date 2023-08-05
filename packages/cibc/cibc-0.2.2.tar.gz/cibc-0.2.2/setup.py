from setuptools import setup

setup(name='cibc',
      version='0.2.2',
      description='Client library to support the Canadian Imperial Bank of Canadas API',
      url='https://louismillette.com',
      author='Louis Millette',
      author_email='louismillette1@gmail.com',
      license='MIT',
      packages=['cibc'],
        install_requires=[
          'requests',
      ],
      include_package_data=True,
      zip_safe=False)