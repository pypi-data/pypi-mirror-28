from setuptools import setup

setup(
    name='Cryptoprice',
    version='0.1',
    py_modules=['cryptoprice'],
    description='A CLI to monitor the crypto market and your portfolio.',
    url='https://github.com/vi-v/cryptoprice',
    author='Vishnu Vijayan',
    author_email='slpxatwon@gmail.com',
    license='MIT',
    keywords='crypto portfolio cli cryptocurrency market',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'Click',
        'requests',
        'terminaltables',
        'tinydb',
        'prompt_toolkit',
    ],
    entry_points='''
        [console_scripts]
        cryptoprice=cryptoprice:cli
    '''
)
