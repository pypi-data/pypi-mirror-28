from distutils.core import setup, Extension

throestl_hash_module = Extension('throestl_hash', sources = ['throestlmodule.c', 'throestl.c'])

setup (name = 'throestl_hash',
    version = '1.1.0',
    description = 'Throestl hash algorithm.',
    maintainer = 'Allar',
    maintainer_email = 'allar@gamemak.in',
    url = 'https://github.com/dallar-project/throestl-hash-python',
    keywords = ['dallar', 'dal', 'throestl'],
    ext_modules = [throestl_hash_module])
