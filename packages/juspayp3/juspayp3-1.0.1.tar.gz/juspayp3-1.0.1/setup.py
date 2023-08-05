from setuptools import setup, find_packages

setup(name='juspayp3',
      version='1.0.1',
      description='Python 3 version of expresscheckout-python-client - JusPay Express Checkout API',
      url='https://github.com/dhavalsavalia/juspay-expresscheckout-python3-client',
      author='Dhaval Savalia',
      author_email='dhaval.savalia6@gmail.com',
      license='MIT',
      packages=find_packages(),
      keywords='juspay expresscheckout payments',
      install_requires = ['requests'],
      )