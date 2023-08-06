from distutils.core import setup 

classifiers = [
    'Programming Language :: Python :: 3',
]
paramters = {
    'name': 'minquan_funniest',
    'packages': ['funniest'],
    'version': '0.03',
    'author': 'minchiuan.gao',
    'author_email': 'minchiuan.gao@gmail.com',
    'url': 'https://some.com',
    'description': 'test for packaging',
}


setup(**paramters)
