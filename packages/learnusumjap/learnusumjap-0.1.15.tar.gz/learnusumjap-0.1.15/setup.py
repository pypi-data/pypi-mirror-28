from setuptools import setup, find_packages
pkg = "learnusumjap"
ver = '0.1.15'
setup(
    name             = pkg,
    version          = ver,
    description      = "Japanese language utilities",
    author           = "jikan@cock.li",
    author_email     = "jikan@cock.li",
    license          = "LGPLv3",
    url              = "https://hydra.bacontoast.org/f/learnusumjap/",
    packages         = find_packages(),
    install_requires = ['pyjmdict>=0.4.2',
                        'jikan_sqlalchemy_utils>=0.0.4',
                        'romkan>=0.2.1'],
    classifiers      = ["Programming Language :: Python :: 3 :: Only"])
