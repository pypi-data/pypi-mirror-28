from distutils.core import setup

classifiers = [
    'Programming Language :: Python :: 3',
]

requirements = [
    'tqdm',
    'fasttext',
    'pandas',
    'numpy',
    'jieba',
]

paramters = {
    'name': 'word_expanding',
    'packages': ['word_expanding'],
    'version': '0.01',
    'author': 'minchiuan.gao',
    'author_email': 'minchiuan.gao@gmail.com',
    'url': 'https://github.com/fortymiles',
    'description': 'test for packaging',
    'install_requires': requirements
}


setup(**paramters)