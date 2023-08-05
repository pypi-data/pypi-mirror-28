from setuptools import setup, find_packages
pkg = "jikan"
ver = '0.2.15'
setup(
    name             = pkg,
    version          = ver,
    description      = "Kanji learning anki deck generator",
    author           = "jikan@cock.li",
    license          = "LGPLv3",
    url              = "https://hydra.bacontoast.org/f/jikan/",
    packages         = find_packages(),
    install_requires = ['lxml>=3',
                        'cached_property',
                        'generic_escape',
                        'etreetools>=0.1.0',
                        'learnusumjap>=0.1.14',
                        'pyjmdict>=0.4.4',
                        'jikan_sqlalchemy_utils>=0.0.5',
                        'tqdm>=4'],
    package_data     = {pkg: [
        'data/substitutions/*.svg',
        'data/mnemonics.txt',
        'data/Heisigs_RTK_6th.json']},
    classifiers      = ["Programming Language :: Python :: 3 :: Only"])
