from setuptools import setup, find_packages

setup(
    name = 'pycrybittrex',
    version = '0.4.0',  # Ideally should be same as your GitHub release tag varsion
    packages = find_packages(),
    description = 'bittrex python client',
    author = 'namiazad',
    author_email = 'nami.nasserazad@gmail.com',
    install_requires=['requests', 'urllib3'],
    url = 'https://github.com/namiazad/pycrybittrex',
    download_url = 'https://github.com/namiazad/pycrybittrex/archive/0.4.0.tar.gz',
    keywords = ['python', 'bittrex'],
    classifiers = [],
)
