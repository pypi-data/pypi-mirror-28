from setuptools import setup

setup(
    name="masonite-cli",
    version='0.25',
    py_modules=['craft'],
    packages=['snippets', 'snippets.auth', 'snippets.auth.controllers', 'snippets.auth.templates.auth'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        craft=craft:group
        craft-vendor=craft:cli
    ''',
)
