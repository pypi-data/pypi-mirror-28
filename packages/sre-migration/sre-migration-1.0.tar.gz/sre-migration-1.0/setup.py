from setuptools import setup

setup(
    name = 'sre-migration',
    version = '1.0',
    author = 'NEC',
    author_email = 'aortizdev@gmail.com',
    url = 'http://mex.nec.com',
    packages = ['migration'],
    entry_points = {
        'console_scripts': [
            'sre-migration = migration.__main__:main'
        ]
    }
)
