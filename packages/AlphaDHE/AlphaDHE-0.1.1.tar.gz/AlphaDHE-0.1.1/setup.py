from distutils.core import setup
setup(
  name = 'AlphaDHE',
  packages = ['AlphaDHE'],
  version = '0.1.1',
  description = 'DiffieHellman Ephemeral for A-Z ciphers',
  author = 'Karl Zander',
  author_email = 'pvial@kryptomagik.com',
  url = 'https://github.com/pvial00/MASH',
  keywords = ['cryptography', 'encryption', 'security'],
  classifiers = [],
  install_requires = [
      'MASHHASH',
      'pycrypto',
      ],
)
