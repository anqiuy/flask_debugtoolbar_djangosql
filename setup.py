# setup.py

from setuptools import setup, find_packages

setup(
    name="Flask-DebugToolbar-DjangoSQL",
    version="0.1.0",
    description="A Flask Debug Toolbar panel for Django SQL queries.",
    long_description=open('README.md').read(),
    long_description_content_type='text',
    author="Joey",
    author_email="qiuyu.an@hotmail.com",
    url="https://github.com/yourusername/flask-debugtoolbar-djangosql",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-DebugToolbar',
        'Django',
        # Add any other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
