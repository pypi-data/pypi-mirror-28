from distutils.core import setup
setup(
  name = 'AlphaDHE',
  packages = ['AlphaDHE'],
  version = '0.1.7',
  description = 'DiffieHellman Ephemeral for A-Z ciphers',
  author = 'Karl Zander',
  author_email = 'pvial@kryptomagik.com',
  url = 'https://github.com/pvial00/AlphaDHE',
  keywords = ['cryptography', 'encryption', 'security'],
  classifiers = [],
  install_requires = [
      'MASHHASH',
      'pycrypto',
      ],
)
