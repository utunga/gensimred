"""
Tools to interact with reddit corpus at http://162.243.228.43/

"""

from setuptools import setup

setup(
    name='genred',
    version='0.0.1',
    url='https://github.com/utunga/gensimred',
    license='GPLv3',
    author='Miles Thompson',
    author_email='utunga@gmail.com',
    description='Reddit + Gensim + Word2Vec',
    long_description=__doc__,
    install_requires=[
        'grequests',
        'requests',
        'nltk',
        'gensim'
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)