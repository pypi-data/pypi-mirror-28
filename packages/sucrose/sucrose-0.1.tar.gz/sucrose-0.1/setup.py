from setuptools import setup, find_packages

setup(
    name='sucrose',
    version='0.1',
    description='mircroservice library using flask and rabbitmq',
    url='http://github.com/diaphel/sucrose',
    author='Diaphel Thompson',
    author_email='diaphel@icloud.com',
    license='Diaphel',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'Flask',
        'requests',
    ],
    extras_require={
        'dev': [
            'mock==2.0.0',
            'pytest==2.9.0',
            'flake8==3.0.4',
            'pyflakes==1.2.3',
        ],
        'docs': [
            "Sphinx==1.3",
        ],
    },
    zip_safe=False)