from setuptools import setup

static_js_files = [
    'dataclean/static/main.js',
    'dataclean/static/jquery.tablesorter.min.js',
    'dataclean/static/iosbadge.js',
    'dataclean/static/main.css',
]

setup(
    name='sherlockml-dataclean',
    version='0.1.3',
    url='https://sherlockml.com',
    author='ASI Data Science',
    author_email='engineering@asidatascience.com',
    data_files=[
        ('share/jupyter/nbextensions/sherlockml-dataclean', static_js_files)
    ],
    packages=['dataclean'],
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'ipywidgets'
    ]
)
