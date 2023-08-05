from setuptools import setup

setup(
    name="masonite-cli",
    version='0.23',
    py_modules=['craft', 'snippets'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        craft=craft:group
        craft-vendor=craft:cli
    ''',
)
